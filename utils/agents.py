from utils.base_prompts import (
    PROMPT_A1,
    PROMPT_A2,
    PROMPT_B,
    PROMPT_C
)
from utils.config import (
    IMAGE_RAW_PATH,
    IMAGE_HEATMAP_PATH,
    MODEL_ID
)

import requests
from PIL import Image
import json
from transformers import pipeline



class MarketingAgent:
    """
    Main class that contains the four different prompt pipelines
    """

    def __init__(
            self, 
            image_raw_path: str = IMAGE_RAW_PATH,
            image_heatmap_path: str = IMAGE_HEATMAP_PATH,
            model_id: str = MODEL_ID
        ):
        self.image_raw = Image.open(image_raw_path)
        self.image_heat = Image.open(image_heatmap_path)
        self.pipe = pipeline("image-to-text", model=model_id)
    
    def format_prompt(self, prompt):
        complete_prompt = fr'USER: <image>\n {prompt} \nASSISTANT:'
        return complete_prompt
    
    def clean_output(self, prompt_output):
        return json.loads(prompt_output[0]["generated_text"].split("ASSISTANT:\n", 1)[-1].replace(r'\_', '_'))
    
    def combine_outputs(
            self,
            json_output_A1,
            json_output_A2,
            json_output_B
        ):
        # Extract elements from each JSON output
        ad_description = json_output_A1[0]["ad_description"]
        ad_purpose = json_output_A1[0]["ad_purpose"]
        ad_saliency_description = json_output_A2[0]["saliency_description"]
        ad_cognitive_description = json_output_B[0]["cognitive_description"]

        # Combine into a new JSON object
        json_combined = {
            "ad_description": ad_description,
            "ad_purpose": ad_purpose,
            "ad_saliency_description": ad_saliency_description,
            "ad_cognitive_description": ad_cognitive_description
        }
        return json_combined

    def run_marketing_prompt(self, image, prompt, json_combined={}, multimodal=True):
        if multimodal:
            prompt = self.format_prompt(prompt)
            prompt_output = self.pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})
        else:
            prompt = f'{prompt} {json_combined}'
            prompt = self.format_prompt(prompt)
            prompt_output = self.pipe(prompt=prompt, generate_kwargs={"max_new_tokens": 200})
        json_output = self.clean_output(prompt_output)
        return json_output