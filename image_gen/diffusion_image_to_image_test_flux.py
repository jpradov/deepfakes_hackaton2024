import torch
#from diffusers import StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler
from PIL import Image
from diffusers import FluxPipeline, DPMSolverMultistepScheduler

def generate_image_from_image(prompt, input_image_path, output_path, strength=0.75):
    # Use the smaller stable-diffusion-2-base model
    #model_id = "stabilityai/stable-diffusion-2-base"
    #model_id = "stabilityai/stable-diffusion-3-medium"

    #model_id = "stabilityai/stable-diffusion-xl-base-1.0"

    model_id = "black-forest-labs/FLUX.1-dev"

    pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)

    # Use the DPMSolverMultistepScheduler for faster inference
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

    # Enable memory efficient attention
    pipe.enable_attention_slicing()

    # Move the pipeline to GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = pipe.to(device)
    #pipe = pipe.enable_model_cpu_offload()

    # Load and preprocess the input image
    init_image = Image.open(input_image_path).convert("RGB")
    init_image = init_image.resize((768, 768))

    # Generate the image
    image = pipe(prompt=prompt,
        image=init_image,
        strength=strength,
        height=1024,
        width=1024,
        guidance_scale=7.5,
        num_inference_steps=50,
        max_sequence_length=512,).images[0]

    # Save the image
    image.save(output_path)
    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    #prompt = input("Enter your image prompt: ")
    #input_image_path = input("Enter the path to your input image: ")
    output_path = "hackathon_images_ai/generated_image.png"
    prompt = "Mr. Bean with a hat"
    input_image_path = "hackathon_images_base/mr_bean.jpg"
    generate_image_from_image(prompt, input_image_path, output_path)