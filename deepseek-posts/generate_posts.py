import requests
import time
import os
import json

# Your DeepSeek API key
API_KEY = "sk-c5798a7c18fa4bd6a7ec3e9a4fc4d5a1"
API_URL = "https://api.deepseek.com/v1/chat/completions"

# Define the prompt template
prompt_template = """
I have website OctaByte(octabyte.io) where I provide fully managed services for 
open source software. Customer select software and choose subscription plan 
and then I deploy this software on VM and handover to customer. Every technical 
things are handle by OctaByte like installation, backup, server management etc. 
Now I created a blog for OctaByte so I want to write a blog posts for 
open source softwares. Write a detailed blog post in markdown syntax for 
"{software_name} - {software_title}" Also write title, short description 
and keywords for seo. Ensure the content is engaging if possible also add 
comparison table with other softwares related to "{software_name}"
"""

    
def generate_posts(service):
    try:
        software_id = service['id']
        software_name = service['title']
        software_title = service['extended_title']

        prompt = prompt_template.format(software_name=software_name, software_title=software_title)

        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "system", "content": "You are an expert SEO blog writer."},
                            {"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status() 

        # Extract generated text
        blog_content = response.json()["choices"][0]["message"]["content"]

        # Save to Markdown file
        filename = f"posts/{software_id}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(blog_content)

        print(f"Generated: {filename}")

        # Sleep to avoid rate limits
        time.sleep(2)

    except Exception as e:
        print(f"Error generating post for {software_name}: {e}")


os.makedirs("posts", exist_ok=True)

# Load software details from services.json
with open("services.json", "r") as file:
    services = json.load(file)

# Loop through all software entries and generate blog posts
for software_id, software in services.items():
    print(f"Generating post for {software_id} ...")
    generate_posts(software)

print("Complete!!!")
