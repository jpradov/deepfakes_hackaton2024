from openai import OpenAI
import os
import json
import argparse

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)



# Function to query the OpenAI API using gpt-3.5-turbo
def query_openai(conspiracy_theory):
    try:
        # Prompts for generating the news article components
        system_prompt = "Only produce one prompt, which should be short and keyword based, with 8 words max."
        user_prompt = f"Write a single text prompt for a text-to-image model fine-tuned on realistic photos that can be used as hard evidence in a news article about the {conspiracy_theory} conspiracy theory."
        diffusion_prompt_chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2048,  # You can adjust this depending on your needs
            temperature=0.7
        )

        return {"diffusion_prompt" : diffusion_prompt_chat_completion.choices[0].message.content}
    except Exception as e:
        return str(e)

def main(conspiracy_theory, output_file):
    # Set your OpenAI API key
    
    # Query OpenAI API to generate the article body
    result = query_openai(conspiracy_theory)
    

    # Save the result as a JSON file
    with open(output_file, "w") as json_file:
        json.dump(result, json_file, indent=4)
    
    print(f"Generated article saved to {output_file}")

if __name__ == "__main__":
    # Argument parsing for command line usage
    parser = argparse.ArgumentParser(description="Generate a news article based on a conspiracy theory.")
    parser.add_argument("--conspiracy_theory", required=True, help="Conspiracy theory to generate an article for")
    parser.add_argument("--output_file", default="diffusion_prompt_output_file.json", help="Output file to save the generated article (default: output_file.json)")

    args = parser.parse_args()

    # Call the main function
    main(args.conspiracy_theory, args.output_file)
