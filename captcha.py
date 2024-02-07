from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis.models import VisualFeatures
from dotenv import load_dotenv
import os
import re  


def get_captcha_code(imageUrl):
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    apiKey = os.getenv("AZURE_VISION_KEY")

    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(apiKey))


    result = client.analyze(
        image_url=imageUrl,
        visual_features=[VisualFeatures.READ],
    )

    word = ""
    if result.read is not None:
        for line in result.read.blocks[0].lines:
            cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', line.text)
            word += cleaned_text
    return word
        