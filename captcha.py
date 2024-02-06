from openai import OpenAI
import base64
from PIL import Image
from io import BytesIO
import os
import uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def get_captcha_code(imageUrl):

    client = OpenAI()
    result = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type":"text",
                    "text":"Print out all letters or numbers visible in the right order on this image. Do not print out anything else. Just the letters and numbers. Don't include whitespaces"
                    },
                    {"type":"image_url",
                    "image_url": {
                        "url":imageUrl
                    }
                    }
                ],

            }
        ],
        max_tokens=300,
        model="gpt-4-vision-preview",

    )

    captcha_code = result.choices[0].message.content
    return captcha_code


def upload_image(base64_string):
    imageFile = convert_base64_to_image(base64_string)
    
    connection_string = os.getenv('AZURE_CONNECTION_STRING')
    container_name = os.getenv('AZURE_BLOB_CONTAINER_NAME')
    
    try:
        # Create the BlobServiceClient that is used to call the Blob service for the storage account
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Create the BlobClient to interact with the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=imageFile)

        # Upload the file
        with open(imageFile, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            print(f"File {imageFile} uploaded to Azure Blob Storage.")
            
        blob_url = f"{blob_client.url}"
        print(f"Blob URL: {blob_url}")
        return blob_url
        
    except Exception as ex:
        print('Exception:')
        print(ex)
    
def convert_base64_to_image(base64_string):
    base64_image = base64_string.split(',')[1]
    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data))
    random_file_name = f"{uuid.uuid4()}.png"
    image.save(random_file_name)
    return random_file_name