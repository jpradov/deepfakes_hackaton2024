# # from diffusers import StableDiffusionPipeline
# # import torch
# #
# # # Load the pre-trained Stable Diffusion model from Hugging Face
# # model_id = "CompVis/stable-diffusion-v1-4"  # You can also try newer versions like v1-5 or v2
# # pipe = StableDiffusionPipeline.from_pretrained(model_id)
# #
# # # Move the model to GPU (if available)
# # pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
# #
# # # Define the text prompt
# # prompt = "A beautiful sunset over a futuristic city skyline with flying cars"
# #
# # # Generate the image from the text prompt
# # image = pipe(prompt).images[0]
# #
# # # Save the generated image to a file
# # image.save("generated_image.png")
# #
# # # Optionally, display the image
# # image.show()
# #
# #
#
#
# import requests
# import base64
# from io import BytesIO
# from PIL import Image
#
# # Your Hugging Face API Key
# api_key = "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"
#
# # The model you want to use for text-to-image generation
# # model_id = "CompVis/stable-diffusion-v1-4"
# # model_id = "black-forest-labs/FLUX.1-schnell"
# model_id = "stabilityai/stable-diffusion-2-1"
#
#
# # Define the text prompt
# prompt = "A futuristic cityscape with flying cars and neon lights"
#
# # API URL for text-to-image generation
# api_url = f"https://api-inference.huggingface.co/models/{model_id}"
#
# # Headers including your API key
# headers = {
#     "Authorization": f"Bearer {api_key}"
# }
#
# # Data payload with the prompt
# payload = {
#     "inputs": prompt,
# }
#
# # Send the request to Hugging Face API
# response = requests.post(api_url, headers=headers, json=payload)
#
# # Check if the response is OK
# if response.status_code == 200:
#     # Decode the image from the base64-encoded response
#     image_bytes = base64.b64decode(response.content)
#     image = Image.open(BytesIO(image_bytes))
#
#     # Save or display the generated image
#     image.save("generated_image.png")
#     image.show()
# else:
#     print(f"Request failed with status code: {response.status_code}")
#     print(response.text)


import requests
from io import BytesIO
from PIL import Image

# Your Hugging Face API Key
api_key = "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"

# The model you want to use for text-to-image generation

# model_id = "CompVis/stable-diffusion-v1-4"

# model_id = "black-forest-labs/FLUX.1-schnell"
model_id = "stabilityai/stable-diffusion-2-1"
# model_id = "merve/flux-lego-lora-dreambooth"



# Define the text prompt
import json

# Read the nested JSON file
with open('diffusion_prompt_output_file.json', 'r') as file:
    data = json.load(file)


# prompt = "Alien technology artifacts found in the Old Ancient Egypt by archeologist."
prompt = data['diffusion_prompt']

# API URL for text-to-image generation
api_url = f"https://api-inference.huggingface.co/models/{model_id}"

# Headers including your API key
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Data payload with the prompt
payload = {
    "inputs": prompt,
}

# Send the request to Hugging Face API
response = requests.post(api_url, headers=headers, json=payload)

# Check if the response is OK
if response.status_code == 200:
    # Load the image directly from the raw bytes (no base64 decoding needed)
    image = Image.open(BytesIO(response.content))

    # Save or display the generated image
    image.save("media/conspiracy_image.png")
    image.show()
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
