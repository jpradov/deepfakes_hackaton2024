"""
# Your Hugging Face API Key
api_key = "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"

# The model you want to use for text-to-image generation

# model_id = "CompVis/stable-diffusion-v1-4"

# model_id = "black-forest-labs/FLUX.1-schnell"
model_id = "black-forest-labs/FLUX.1-schnell"
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
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)

"""
import json
import replicate
import requests

# Read the nested JSON file
with open('diffusion_prompt_output_file.json', 'r') as file:
    data = json.load(file)

prompt = data['diffusion_prompt']

input = {
    "prompt": f"{prompt}",
    "guidance": 3.5
}

output = replicate.run(
    "black-forest-labs/flux-dev",
    input=input
)

# output is of this form: ['https://replicate.delivery/yhqm/9qdyBrs7jQruFB4zQ7SDuyT5gH3wQa8R8gxUoBGQu8mefycTA/out-0.webp']
# we need to download the image from the url and save it to a file

# Download the image from the url and save it to a file
response = requests.get(output[0])

# save the image to a file
save_path = '"media/conspiracy_image.png"'
with open(save_path, "wb") as f:
    f.write(response.content)
