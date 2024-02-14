import requests
import os

def get_captcha_code(base64imageString):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PROXY = os.getenv("PROXY")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={GEMINI_API_KEY}"
        
    proxies = {
        "http": f"http://{PROXY}",
        "https": f"http://{PROXY}"
    }
    body = {
      "contents": [{
        "parts": [
          {"text": "Act as if you are a software program which purpose it is to solve text captcha imges. Print out all letters or numbers visible from left to right on this image. Only print the letters and numbers. Don't include whitespaces. The Output should always consists out of 6 uppercase characters without whitespaces. With big probability it will be a mix of letters and numbers and not only one of them."}, 
          {
            "inline_data": {
              "mime_type": "image/jpeg",
              "data": base64imageString
            }
          }
        ]
      }]
    }

    response = requests.post(url, json=body, proxies=proxies)
    
    text = ""
    try:
        text = str(response.json()["candidates"][0]["content"]["parts"][0]["text"]).upper()
        text = text.replace(" ", "")
    except Exception as e:
        print(e)
        text = "Error"
    print(text)
    return text