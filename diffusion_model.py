import replicate
import requests


prompt = """
A museum exhibit showcasing an ancient archeological sample of alien technology discovered in Egypt. The exhibit includes a mysterious artifact, made of sleek, metallic materials not found on Earth, with glowing symbols resembling hieroglyphics. The artifact is partially embedded in ancient sandstone, surrounded by other Egyptian relics such as statues, scrolls, and pottery. The alien technology has a futuristic, extraterrestrial design, contrasting with the traditional ancient Egyptian aesthetic. Museum lighting highlights the artifact, casting long shadows and creating an aura of mystery and discovery.
"""

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
save_path = 'media/hackaton_images_base/fake_image.png'
with open(save_path, "wb") as f:
    f.write(response.content)