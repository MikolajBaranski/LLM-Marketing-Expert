# Prompt A1 - Expert describing the asset and its purpose
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
```
[
    {
        "ad_description":$description,
        "ad_purpose":$purpose
    }
]
```

In this format, $description is a placeholder for the description of the
advert, $purpose can only be either "brand-building" or "conversion".
</response-template>.
"""

# Prompt A2 - Expert describing most visually salient elements of ad
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
```
[
    {
         "saliency_description":$description
    }
]
```
In this format, $description is a placeholder for the description of the
visually salient elements in the advertisement.
"""


# Prompt B - Analysis of perceptual/cognitive load of asset
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
```
[
{
    "cognitive_description":$description
}
]
```
In this format, $description is a placeholder for assessment of the cognitive
load induced by the advertisement in viewers.
"""

# Prompt C - Summarization and text collection
PROMPT_C = """
<role>
You are a professional writer.
</role>
<input-overview>
You are provided with text descriptions that are outputs from two different
multi-modal LLMs.
</input-overview>
<task>
You have a single task:
Summarise the text provided from the two different outputs and ensure that the
JSON format of the final output matches the requirements provided below.
</task>
<response-template>
Provide the final output in the following JSON format
```
[
    {
        "ad_description":$ad_description,
        "ad_purpose":$ad_purpose,
        "saliency_description":$saliency_description,
        "cognitive_description":$cognitive_description
    }
]
```
In this format, $ad_description, $ad_purpose, $saliency_description and
$cognitive_description are placeholders for the summarised versions of the text
provided as input.
Here is the text:
"""