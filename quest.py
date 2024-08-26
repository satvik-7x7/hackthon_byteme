import json
import google.generativeai as genai
import time

# Set your Gemini API key
GOOGLE_API_KEY = 'AIzaSyAakOajBZLCheFPLaEVZQA8q3HW1nSFVJY'

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

def generate_questions(links, num_questions=10):
    # Prepare the prompt for the LLM
    prompt = f"Given the following list of URLs from a website:\n\n"
    for link in links:
        prompt += f"- {link}\n"
    prompt += f"\nGenerate {num_questions} unique, concise questions (each under 80 characters) that could be answered by the content of these webpages. The questions should cover a range of topics suggested by the URLs."

    try:
        # Generate content using Gemini
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        # Extract questions from the response
        questions_text = response.text.strip()
        questions = [q.strip() for q in questions_text.split('\n') if q.strip()]

        return questions[:num_questions]  # Ensure we only return the requested number of questions

    except genai.types.generation_types.BlockedPromptException as e:
        print(f"The prompt was blocked: {e}")
        return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Read the JSON file
try:
    with open('links.json', 'r') as file:
        content = file.read()
        print("File contents:", repr(content))  # This will show any hidden characters
        if not content.strip():
            print("The file is empty.")
        else:
            try:
                data = json.loads(content)
                print("Successfully parsed JSON.")
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
                print(f"Error at position {e.pos}: {content[e.pos-10:e.pos+10]}")
except FileNotFoundError:
    print("The file 'links.json' was not found.")
except Exception as e:
    print(f"An unexpected error occurred while reading the file: {e}")

# Generate questions
questions = generate_questions(data['links'])

# Create output dictionary
output = {
    "questions": questions
}

# Write output to JSON file
with open('questions.json', 'w') as file:
    json.dump(output, file, indent=4)

print("Questions have been generated and saved to 'questions.json'")