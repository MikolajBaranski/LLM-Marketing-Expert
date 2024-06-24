from utils.base_prompts import (
    PROMPT_A1,
    PROMPT_A2,
    PROMPT_B
)
from utils.config import (
    IMAGE_RAW_PATH,
    IMAGE_HEATMAP_PATH,
    MODEL_ID
)

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
            model_id: str = MODEL_ID,
            prompt_A1: str = PROMPT_A1,
            prompt_A2: str = PROMPT_A2,
            prompt_B: str = PROMPT_B,
        ):
        self.image_raw = Image.open(image_raw_path)
        self.image_heat = Image.open(image_heatmap_path)
        self.pipe = pipeline("image-to-text", model=model_id)
        self.prompt_A1 = prompt_A1
        self.prompt_A2 = prompt_A2
        self.prompt_B = prompt_B
    
    def format_prompt(self, prompt):
        complete_prompt = fr'USER: <image>\n {prompt} \nASSISTANT:\n'
        return complete_prompt
    
    def clean_output(self, prompt_output):
        return json.loads(prompt_output[0]["generated_text"].split("ASSISTANT:\\n\n", 1)[-1].replace(r'\_', '_'))
    
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

    def run_marketing_prompt(self, image, prompt):
        prompt = self.format_prompt(prompt)
        prompt_output = self.pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 400})
        json_output = self.clean_output(prompt_output)
        return json_output
    
    def full_agent_pipe(self, image_raw, image_heat):
        # Run the agents in order
        json_output_A1 = self.run_marketing_prompt(image_raw, self.prompt_A1)
        json_output_A2 = self.run_marketing_prompt(image_heat, self.prompt_A2)
        json_output_B = self.run_marketing_prompt(image_raw, self.prompt_B)

        # Combine outputs together
        json_combined = self.combine_outputs(json_output_A1, json_output_A2, json_output_B)
        return json_combined