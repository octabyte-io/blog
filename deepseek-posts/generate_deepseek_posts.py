import requests
import yaml
import time
import os

# Your DeepSeek API key
API_KEY = "sk-c5798a7c18fa4bd6a7ec3e9a4fc4d5a1"
API_URL = "https://api.deepseek.com/v1/chat/completions"

# Define the prompt template
prompt_template = """
I have a website Octabyte (octabyte.io) where I'm providing fully managed services for open source softwares, I have 350+ softwares. Customer pick a software and choose a subscription plan then I deploy that software on VM and handover to customer. All technical things are managed by OctaByte. Here are some key benefits of using OctaByte. 

Time Savings: 
Skip the steep learning curve of deploying and maintaining open-source software. Let our experts handle the heavy lifting.

Cost-Effective Solution: 
Avoid hiring specialized IT staff or investing in expensive infrastructure. OctaByte provides an all-in-one solution at an affordable price.

Automatic Backups & Restores: 
Your data is safe with us. We provide regular automated backups and easy restoration options for peace of mind.

Seamless SSL Management: 
Enjoy secure connections with automatically managed SSL certificates, ensuring your software is always up-to-date with the latest security standards.

Support: 
Our dedicated support team is always available to address your concerns and provide expert guidance.

what I want you to write a blog post title "Deploy {software_name} in Minutes with OctaByte.io" The post should explain what {software_name} is, why it is useful and what benefits to deploy {software_name} in OctaByte. Write this post in markdown format, write title, short description, seo keywords
"""

# Load the YAML file
def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)
    
def generate_posts(file_path):
    data = load_yaml(file_path)
    for catalog in data.get("catalog_list", []):
        category_id = catalog['id']
        category_name = catalog['name']

        print(f"Category: {category_name}")

        if category_id == "databases":
            continue

        for service in catalog.get("services", []):
            software_id = service['id']
            software_name = service['title']
            software_category = service['category'].split()[0]

            post_dir = f"posts/{category_id}/{software_category}"

            os.makedirs(post_dir, exist_ok=True)

            print(f"Generating post for {software_name} ...")

            try:

                prompt = prompt_template.format(software_name=software_name)

                payload = {
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
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
                filename = f"{post_dir}/{software_id}.md"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(blog_content)

                print(f"Generated: {filename}")

                # Sleep to avoid rate limits
                time.sleep(2)

            except Exception as e:
                print(f"Error generating post for {software_name}: {e}")

        print(f"Category {category_name} completed")
        exit(1)

file_path = "services.yaml"
generate_posts(file_path)

