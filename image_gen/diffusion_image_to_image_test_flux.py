import torch
#from diffusers import StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler
from PIL import Image
from diffusers import FluxPipeline, DPMSolverMultistepScheduler

def generate_image_from_image(prompt, input_image_path, output_path, strength=0.75):
    # Use the smaller stable-diffusion-2-base model
    #model_id = "stabilityai/stable-diffusion-2-base"
    #model_id = "stabilityai/stable-diffusion-3-medium"

    #model_id = "stabilityai/stable-diffusion-xl-base-1.0"

    #model_id = "black-forest-labs/FLUX.1-dev"
    model_id = "VideoAditor/Flux-Lora-Realism"

    pipe = FluxPipeline.from_pretrained(model_id, torch_dtype=torch.bfloat16)

    # Enable memory efficient attention
    pipe.enable_attention_slicing()

    # Move the pipeline to GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = pipe.to(device)
    #pipe = pipe.enable_model_cpu_offload()

    # Load and preprocess the input image
    #init_image = Image.open(input_image_path).convert("RGB")
    #init_image = init_image.resize((768, 768))

    # Generate the image
    image = pipe(prompt=prompt,
        height=1024,
        width=1024,
        guidance_scale=3.5,
        num_inference_steps=50,
        max_sequence_length=512,).images[0]

    # Save the image
    image.save(output_path)
    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    #prompt = input("Enter your image prompt: ")
    #input_image_path = input("Enter the path to your input image: ")
    output_path = "hackathon_images_ai/generated_image_flux_output2_realism.png"
    #prompt = "Evidence of alien technology in Ancient Egypt"
    #prompt = "An ancient archeological artifact displayed in a museum exhibit. The artifact is a weathered stone tablet inscribed with faded hieroglyphics, partially cracked from centuries of exposure. It's displayed on a pedestal under soft, warm lighting, with a glass case surrounding it. Behind the artifact is a descriptive plaque detailing its origin, from a lost civilization. The background includes other artifacts, like bronze tools, pottery shards, and a tall statue with intricate carvings. The museum room has a calm, scholarly atmosphere, with dark wooden floors and high ceilings adorned with spotlights."
    prompt ="""
    A museum exhibit showcasing an ancient archeological sample of alien technology discovered in Egypt. The exhibit includes a mysterious artifact, made of sleek, metallic materials not found on Earth, with glowing symbols resembling hieroglyphics. The artifact is partially embedded in ancient sandstone, surrounded by other Egyptian relics such as statues, scrolls, and pottery. The alien technology has a futuristic, extraterrestrial design, contrasting with the traditional ancient Egyptian aesthetic. Museum lighting highlights the artifact, casting long shadows and creating an aura of mystery and discovery.
    """
    input_image_path = "hackathon_images_base/mr_bean.jpg"
    generate_image_from_image(prompt, input_image_path, output_path)