from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

imageUrl = input("Enter the image url: ")

result = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type":"text",
                "text":"Print out all letters or numbers visible in the right order on this image. Do not print out anything else. Just the letters and numbers."
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
    

print(captcha_code)