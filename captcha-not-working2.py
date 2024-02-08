from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis.models import VisualFeatures
from dotenv import load_dotenv
import os
import re  


from google.cloud import vision


def get_captcha_code_azure(imageUrl):
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    apiKey = os.getenv("AZURE_VISION_KEY")

    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(apiKey))


    result = client.analyze(
        image_url=imageUrl,
        visual_features=[VisualFeatures.READ],
    )

    word = ""
    if result.read is not None:
        print("Read result:")
        print(result.read)
        for line in result.read.blocks[0].lines:
            cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', line.text)
            word += cleaned_text
    return word

def get_captcha_code_google(imageUrl):
    
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = imageUrl
    response = client.text_detection(image=image)
    texts = response.text_annotations


    text = texts[0].description



    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    return text
