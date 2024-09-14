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
save_path = 'media/conspiracy_image.png'
with open(save_path, "wb") as f:
    f.write(response.content)
