import google.generativeai as genai
import os
import PIL.Image

def get_captcha_code(imagePath):
    
    img = PIL.Image.open(imagePath)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel('models/gemini-pro-vision')

    response = model.generate_content(["Print out all letters or numbers visible in the right order on this image. Do not print out anything else. Just the letters and numbers. Don't include whitespaces. The Output alway consists out of 6 characters. There cannot be other characters than letters and numbers.",img])

    text = ""

    try :
        text = extract_string(response.candidates[0].content.parts[0])
    except Exception as e:
        print(e)
        text = "Error"

    os.remove(imagePath)
    print(text)
    return text


def extract_string(output):
    # Find the start and end indices of the double quotes
    output = str(output)
    start = output.find('"') + 1
    end = output.rfind('"')

    # Extract the string inside the double quotes and remove all spaces
    return output[start:end].replace(' ', '')