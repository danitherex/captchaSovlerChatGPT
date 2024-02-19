import requests

def send_discord_webhook_notification(messageToSend,DISCORD_WEBHOOK,mention=False):
    message = ""
    if(mention):
        message = f"<@{mention}>\n"
    message += messageToSend
    
    # Prepare the payload
    data = {"content": message, "username": "Hochschulsport Buchungs Bot"}
    
    # Send the request
    response = requests.post(DISCORD_WEBHOOK, json=data)
    print("Notification sent, status code:", response.status_code)