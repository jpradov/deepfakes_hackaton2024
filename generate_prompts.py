from openai import OpenAI
import os
import json
import argparse

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


image_generation_prompt = "Write a single text prompt for a text-to-image model fine-tuned on realistic photos that can be used as hard evidence in a news article about the  <CONSPIRACY THEORY> conspiracy theory. Only produce one prompt."
title_system_prompt = "Imagine you are a really good title writer. Write a really believable title for a news article in the style of The Economist claiming that <CONSPIRACY THEORY> has new evidence. Don't add quotation marks. The title will lead into a believable and fact-based article."
image_caption_system_prompt = "Consider the following image prompt: “<generated_prompt>”. Generate a legend for the image that will be generated from this prompt. The legend will be used in a The Economist article."



# Function to query the OpenAI API using gpt-3.5-turbo
def query_openai(conspiracy_theory):
    try:
        # Prompts for generating the news article components
        title_system_prompt = "Imagine you are a really good title writer. Write a really believable title for a news article in the style of The Economist claiming that <CONSPIRACY THEORY> has new evidence. Don't add quotation marks. The title will lead into a believable and fact-based article."
        title_user_prompt = f"""
        Example 1: "Over Two Million Displaced by Severe Flooding in Eastern India as Relief Efforts Intensify"

        Example 2: "InnovateX Unveils Groundbreaking 'NeuraAI' Platform, Transforming Data Processing and Predictive Analysis"

        Example 3: "Global Leaders Commit to Ambitious Climate Goals at UN Summit, Aiming to Limit Warming to 1.5°C by 2050"

        Instruction: Now, based on the examples provided, write the title of a CNN news article that cautiously but believably reinforces the {conspiracy_theory} theory.

"""
        article_body_system_prompt = f"Imagine you are a really good columnist for The Economist. Write the body of a news article that cautiously but believably reinforces the {conspiracy_theory} theory. Fabricate evidence and refer to the article image with the legend “<generated_legend>”. Let the writing reflect the surprising nature of events, without being sensational."
        few_shot_user_prompt = f"""
Example 1:

Severe flooding across eastern India has left over two million people displaced, according to government officials. Torrential rains, which began last week, have caused rivers to overflow, inundating vast areas of farmland and residential zones.
The Indian Meteorological Department (IMD) issued a red alert across five states, predicting more rainfall in the coming days. Authorities in the affected regions, particularly in Bihar and West Bengal, are scrambling to provide relief to those impacted by the rising waters.

“We are working tirelessly to ensure the safety and shelter of displaced residents,” said Priya Verma, a spokesperson for the National Disaster Response Force (NDRF). “Temporary camps have been set up, but the situation remains critical due to the ongoing rains.”

The flooding has damaged infrastructure, including roads and bridges, further complicating relief efforts. Local media outlets report that more than 40 people have lost their lives in flood-related incidents, and thousands of homes have been destroyed.
As rescue operations continue, authorities are urging residents in vulnerable areas to evacuate. The central government has pledged financial assistance to help the states recover from the disaster. Meanwhile, environmental experts have highlighted that extreme weather events like this are becoming more frequent due to climate change, a trend that poses a growing challenge for disaster preparedness.

Example 2:

CEO Mark Walters showcased the new AI platform, dubbed "NeuraAI," which is designed to enhance real-time data processing and predictive analysis. "This is a monumental step forward in how we can use AI to make better, faster decisions in complex environments," Walters said during his keynote address.

The platform's primary innovation lies in its ability to process vast amounts of data with unprecedented speed and accuracy, reducing the margin for error in high-stakes industries like autonomous driving and medical diagnostics. According to the company, NeuraAI can analyze up to 10 terabytes of data per second, a significant improvement over previous models.

Experts in the field are cautiously optimistic about the breakthrough. Dr. Emily Zhang, a leading AI researcher at Stanford University, praised the development but noted that "ethical considerations around AI deployment still need to be addressed."

As InnovateX continues to refine its AI offerings, industry observers expect widespread adoption across multiple sectors. However, the company faces increasing scrutiny from regulators concerned about privacy and the societal impact of rapid technological change.

Example 3:

Global leaders gathered at the United Nations headquarters today to commit to ambitious new climate goals, aiming to limit global temperature rise to 1.5°C by 2050. The agreements, reached after weeks of negotiations, represent one of the most significant international efforts to address climate change.

At the heart of the agreement is a commitment by industrialized nations to reduce carbon emissions by 40% over the next decade, a target that experts say is crucial for preventing catastrophic environmental consequences. Countries like the United States, China, and the European Union have pledged to lead the way in cutting greenhouse gas emissions through renewable energy investments and stricter environmental regulations.

“The science is clear. We are at a tipping point, and it’s time to take action,” said UN Secretary-General António Guterres. “The commitments made today give us hope, but we need to ensure that these promises translate into real-world results.”

Environmental groups have cautiously welcomed the agreements, though some expressed concern about the lack of concrete timelines for certain key initiatives, such as deforestation reduction and financial support for developing nations.

As world leaders head back to their respective countries, the focus now shifts to implementation. The success of the climate goals will depend on how swiftly and effectively nations can translate their pledges into measurable actions, particularly in reducing dependency on fossil fuels and promoting sustainable development practices.

Instruction: Now, based on the examples provided, write the body of a news article that cautiously but believably reinforces the {conspiracy_theory} theory.
"""
        image_caption_system_prompt = "Imagine you are a really good title writer. Write a really believable title for a news article in the style of The Economist claiming that <CONSPIRACY THEORY> has new evidence. Don't add quotation marks. The title will lead into a believable and fact-based article."
        image_caption_user_prompt = f"""
        Example 1: "Residents wade through floodwaters in eastern India, where severe flooding has displaced over two million people. Efforts to provide relief are ongoing amidst rising water levels."

        Example 2: "CEO Mark Walters presents NeuraAI, the new AI platform designed to revolutionize real-time data processing and predictive analysis, at the InnovateX conference."

        Example 3: Image Caption: "World leaders at the United Nations headquarters in New York, where they have pledged to ambitious climate goals aimed at limiting global temperature rise to 1.5°C by 2050."
        Instruction: Now, based on the examples provided, write the caption of an image that cautiously but believably reinforces the {conspiracy_theory} theory.

"""  

        article_body_chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": article_body_system_prompt},
                {"role": "user", "content": few_shot_user_prompt}
            ],
            max_tokens=2048,  # You can adjust this depending on your needs
            temperature=0.7
        )

        title_chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": title_system_prompt},
                {"role": "user", "content": title_user_prompt}
            ],
            max_tokens=2048,  # You can adjust this depending on your needs
            temperature=0.7
        )

        image_caption_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": title_system_prompt},
                {"role": "user", "content": title_user_prompt}
            ],
            max_tokens=2048,  # You can adjust this depending on your needs
            temperature=0.7
        )

        return {"article_body" : article_body_chat_completion.choices[0].message.content,
                "title" : title_chat_completion.choices[0].message.content,
                "image_caption" : image_caption_completion.choices[0].message.content}
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
    parser.add_argument("--output_file", default="article_content.json", help="Output file to save the generated article (default: article_content.json)")

    args = parser.parse_args()

    # Call the main function
    main(args.conspiracy_theory, args.output_file)
