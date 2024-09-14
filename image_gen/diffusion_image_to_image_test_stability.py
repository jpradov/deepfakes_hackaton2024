import torch
from diffusers import DiffusionPipeline
from PIL import Image

def generate_image_from_image(prompt, input_image_path, output_path, strength=0.75):
    # Use the smaller stable-diffusion-2-base model
    #model_id = "stabilityai/stable-diffusion-2-base"
    #model_id = "stabilityai/stable-diffusion-3-medium"
    #model_id = "stabilityai/stable-diffusion-xl-base-1.0"
    #model_id = "CompVis/stable-diffusion-v1-4"
    model_id = "stabilityai/stable-diffusion-xl-base-1.0"


    # Load the pipeline with low-memory optimizations
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")

    # Use the DPMSolverMultistepScheduler for faster inference
    #pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

    # Enable memory efficient attention
    #pipe.enable_attention_slicing()

    # Move the pipeline to GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = pipe.to(device)
    #pipe.enable_model_cpu_offload()

    # Load and preprocess the input image
    #init_image = Image.open(input_image_path).convert("RGB")
    #init_image = init_image.resize((768, 768))

    # Generate the image
    #image = pipe(prompt=prompt,
    # #image=init_image,
    #strength=strength,
    # guidance_scale=7.5).images[0]
    image = pipe(prompt=prompt).images[0] 

    # Save the image
    image.save(output_path)
    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    #prompt = input("Enter your image prompt: ")
    #input_image_path = input("Enter the path to your input image: ")
    output_path = "hackathon_images_ai/generated_image_stability_prompt2.png"
    #prompt = "Mr. Bean with a hat"
    #prompt = "Evidence of alien technology in Ancient Egypt"
    prompt ="""
    A museum exhibit showcasing an ancient archeological sample of alien technology discovered in Egypt. The exhibit includes a mysterious artifact, made of sleek, metallic materials not found on Earth, with glowing symbols resembling hieroglyphics. The artifact is partially embedded in ancient sandstone, surrounded by other Egyptian relics such as statues, scrolls, and pottery. The alien technology has a futuristic, extraterrestrial design, contrasting with the traditional ancient Egyptian aesthetic. Museum lighting highlights the artifact, casting long shadows and creating an aura of mystery and discovery.
    """
    input_image_path = "hackathon_images_base/mr_bean.jpg"
    generate_image_from_image(prompt, input_image_path, output_path)