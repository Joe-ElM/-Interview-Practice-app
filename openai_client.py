import os

# Load API key from local file
with open('D:\\Visual Studio Code\\desktop_openai.txt', 'r') as f:
    os.environ['OPENAI_API_KEY'] = f.read().strip()

# Access the key from environment
api_key = os.getenv("OPENAI_API_KEY")
