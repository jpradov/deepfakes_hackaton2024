import argparse
import subprocess

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run a script with a conspiracy theory argument.")
    parser.add_argument('-c', '--conspiracy_theory', type=str, required=True, help='Text of the conspiracy theory')
    args = parser.parse_args()

    # Get the conspiracy theory text from the argument
    conspiracy_theory = args.conspiracy_theory

    # Print the received conspiracy theory for demonstration
    print(f"Received conspiracy theory: {conspiracy_theory}")

    # Run the other script and pass the conspiracy theory as an argument
    generate_diffusion_prompts = subprocess.run(['python', f'generate_diffusion_prompt.py', '--conspiracy_theory', conspiracy_theory], capture_output=False, text=False)

    # Check the result of the subprocess
    if generate_diffusion_prompts.returncode == 0:
        print("generate_prompts.py completed successfully.")

        generate_article_text = subprocess.run(['python', f'generate_prompts.py', '--conspiracy_theory', conspiracy_theory, '--diffusion_prompt', 'diffusion_prompt_output_file.json'], capture_output=False, text=False)
        generate_image = subprocess.run(['python', f'prompt_to_image.py', '--diffusion_prompt', 'diffusion_prompt_output_file.json'], capture_output=False, text=False)

        if generate_article_text.returncode == 0 and generate_image.returncode == 0:
                serve_website = subprocess.run(['python', f'app_text.py'], capture_output=False, text=False)

                if serve_website.returncode == 0:
                     print("Done.")

        else:
            print("generate_prompt.py failed.")

    else:
        print("generate_diffusion_prompt.py failed.")

    # Trigger the next part of your code
    print("Now executing the next part of the code.")

if __name__ == "__main__":
    main()
