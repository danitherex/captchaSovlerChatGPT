from openai import OpenAI
from uploadImage import upload_image

def get_captcha_code(imageUrl):

    client = OpenAI()
    result = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type":"text",
                    "text":"Print out all letters or numbers visible in the right order on this image. Do not print out anything else. Just the letters and numbers. Don't include whitespaces. The Output alway consists out of 6 characters. There cannot be other characters than letters and numbers."
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
    try:
        captcha_code = result.choices[0].message.content
    except:
        captcha_code = result
    return captcha_code
