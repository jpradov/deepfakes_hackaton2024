import requests
import time
API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
start_time = time.time()

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content
image_bytes = query({
	"inputs": "Photo-realistic aliens in ancient egypt",
})


import io
from PIL import Image
image = Image.open(io.BytesIO(image_bytes))

image.save('media/hackaton_images_base/fake_image.png')  # You can specify any file format like .jpg, .png, etc.

end_time = time.time()
time_cost = end_time - start_time
print(f"Time taken to save the image: {time_cost:.6f} seconds")