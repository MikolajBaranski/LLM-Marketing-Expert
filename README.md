# LLM-Marketing-Expert
**Author: Mikolaj Baranski**

The following repository holds code to run a open-source multimodal LLM as a marketing expert.

### Purpose of code:

This repository holds the code for a GenAI workflow involving multiple processes using a multi-modal LLM `llava-1.5-7b-hf` for the purpose of making expert analysis of marketing assets and their attention heatmaps.

The end-user would interact with the API by giving it an image of a marketing asset and its associated heatmap (created by a NeuroAI system). The expected output (show below), provides the following insights in the form of a JSON:

- **ad_description**
    - Concise description of the advertisement
- **ad_purpose**
    - Identifies the purpose of advert (brand building or conversion)
- **ad_saliency_description**
    - Description of the most visually salient elements based on the heatmap
- **ad_cognitive_description**
    - Assessment of the perceptual/cognitive load of the asset

### Overview of repository:

- The core file of this repository is the `api.py`, which controls the API which is used to prompt the LLM.
    - The file depends on various supporting elements in the `utils` folder.
    - The `base_prompts.py` file holds the internal prompts guiding the functioning of the LLM (see below).
    - The `config.py` file holds all key variables used throughout the code.
    - The `experts.py` file defines exactly how the LLM experts use the prompts and the user-input of photos to generate the desired output.
- The example images used to verify the performance of the model are stored in the `assets` folder. 
- The code can be tested locally to verify the performance of the model by using the `test/test_agent.ipynb` file. For a test of the whole API that can be run locally see the `test/test_api.ipynb`.
- The API can be deployed using a Docker container by running the `Dockerfile` file. 

### Internal prompts to the LLM:

The prompts shown below are used to guide the LLM towards the desired output. They are stored in the `utils/base_prompts.py` file.

**Prompt A1** - Provide image and ask model to describe key elements of advert (product,
brand, CTA, etc.) and also identify purpose of advert (brand building or conversion).
```
PROMPT_A1 = """
<role>
You are a Senior Insights Manager with decades of experience, and a background
in marketing.
</role>
<input-overview>
You are provided with an image of a digital advertisement.
</input-overview>
<task>
You have two tasks:
1) Provide a detailed description of the advert. In other words, identify and
describe the key elements such as the product being advertised, the brand name,
and the call-to-action (CTA), where available.
2) Additionally, assess and determine the primary purpose of the advertisement,
i.e. whether it is aimed at brand building or aimed at driving conversion.
</task>
<response-template>
Provide the output in the following JSON format

[
    {
        "ad_description":$description,
        "ad_purpose":$purpose
    }
]

In this format, $description is a placeholder for the description of the
advert, $purpose can only be either "brand-building" or "conversion".
</response-template>.
"""
```

**Prompt A2** - Provide corresponding attention heatmap and ask model to describe the
most visually salient elements based on the heatmap.

```
PROMPT_A2 = """
<input-overview>
You are now provided with the attention heatmap of the same image. The
attention heatmap illustrates the distribution of attention as predicted by an
AI model that was trained on eye-tracking data. Red colour indicates high
attention, green implies moderate level and transparent colours mean low
attention. Please do not confuse the heatmap colours, i.e. the red, yellow,
green blobs etc. with the actual colours of the video frames.
</input-overview>
<task>
You have a single task:
Based on the provided heatmap, identify the most visually salient elements,
i.e. the elements that catch the most attention. Please pay special attention
to the product being advertised, the brand or logo, and call-to-action (CTA),
where available.
</task>
<response-template>
Provide the output in the following JSON format

[
    {
         "saliency_description":$description
    }
]

In this format, $description is a placeholder for the description of the
visually salient elements in the advertisement.
"""
```

**Prompt B** - Provide image and ask model to assess perceptual/cognitive load of the
asset.

```
PROMPT_B = """
<role>
You are an expert in applied neuroscience and behavioural psychology.
</role>
<input-overview>
You are provided with an image of a digital advertisement.
</input-overview>
<task>
You have a single task:
Assess the perceptual or cognitive load of the image. This is a measure of the
effort required for mental processing based on the visual complexity, such as
diversity of colours, presence of patterns and the inclusion of text. In other
words, assess how accessible the image will be to a viewer in terms of the
brain processing capacity required to interpret and understand the
advertisement.
</task>
<response-template>
Provide the output in the following JSON format

[
    {
    "cognitive_description":$description
    }
]

In this format, $description is a placeholder for assessment of the cognitive
load induced by the advertisement in viewers.
"""
```

### Example output:

The example output was generated on this advertisment and its associated attention heatmap.
*The advertisement and heatmap were provided by Neurons Inc.*

<img src="assets/image1.png" width="300">
<img src="assets/image1_heatmap.jpeg" width="300">

```
{'ad_description': 'A woman wearing a colorful jacket and a knitted hat is posing for a photo. She is wearing a pink hat and a pink jacket. The background is a brightly colored gradient. The advertisement is for Snowstyle, a clothing brand. The call-to-action is to visit the Snowstyle website.', 'ad_purpose': 'conversion', 'ad_saliency_description': "The woman in the advertisement is wearing a colorful jacket, which is visually salient and likely to catch the viewer's attention.", 'ad_cognitive_description': 'The advertisement is visually complex, with a diverse color palette and a mix of patterns. The inclusion of text adds to the perceptual load, as the viewer must process the message and the visual elements simultaneously. This may make the advertisement less accessible to some viewers, particularly those with lower cognitive capacity or visual impairments.'}
```
