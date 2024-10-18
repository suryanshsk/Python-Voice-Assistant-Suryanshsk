import google.generativeai as genai

# Configure the API key
genai.configure(api_key="API Key")  # Replace with your actual API key

# Set up the model configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

# Initialize the model (ensure this method is correct)
model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)  # Verify this method
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    q = """
        I have a list of tools that can perform specific actions. Based on the user query, select the appropriate tool from the list and extract the necessary inputs. Please respond in the following JSON format:

        {{
            "tool": "<tool_name>",
            "inputs": {{
                "input1": "<value1>",
                "input2": "<value2>",
                ...
            }}
        }}

        Here is the list of tools:
        1. "just_print": Requires general response if none of the following tools fits best.
        2. "set_reminder": Requires "time" (strictly in ISO format . that is,'date+T+time', including both date and time) and "message".
        3. "search_wikipedia": Requires "search_query".
        4. "get_weather": Requires "city_name".
        5. "tell_joke": Requires no inputs.
        6. "play_music": Requires "song_name".
        7. "open_website": Requires "website_name".

        If the tool requires no inputs, leave the "inputs" field empty.

        Query: "Heyy.... How is weather in hyderabad"
        """
    print(get_gemini_response(q))
