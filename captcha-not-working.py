from openai import OpenAI

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
    print(result)
    captcha_code = result.choices[0].message.content
    return captcha_code
