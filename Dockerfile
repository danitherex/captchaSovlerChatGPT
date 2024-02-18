# Use the selenium/standalone-chrome image as the base image
FROM python:3.11.7

# Set the working directory
WORKDIR /usr/src/app


RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# Copy the requirements.txt file to the working directory
COPY requirements.txt .


# Install the Python packages defined in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Selenium script to the working directory
#COPY captcha.py .
COPY prepocessing.py .
COPY termin_buchung.py .
COPY uploadImage.py . 
COPY captcha_gemini.py .


# Add the environment variables
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
#ENV AZURE_VISION_ENDPOINT=${AZURE_VISION_ENDPOINT}
#ENV AZURE_VISION_KEY=${AZURE_VISION_KEY}
ENV SPORT_EMAIL=${SPORT_EMAIL}
ENV SPORT_PASSWORD=${SPORT_PASSWORD}
ENV SPORT_URL=${SPORT_URL}
ENV CAPTCHA=${CAPTCHA}
ENV WEEKDAYS=${WEEKDAYS}
ENV AZURE_CONNECTION_STRING=${AZURE_CONNECTION_STRING}
ENV AZURE_BLOB_CONTAINER_NAME=${AZURE_BLOB_CONTAINER_NAME}


# Set the entrypoint to run the Selenium script
ENTRYPOINT ["python", "termin_buchung.py"]
