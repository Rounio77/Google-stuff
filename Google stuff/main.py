# Import the Google Generative AI package
import google.generativeai as genai

# Import the API key from a separate file (ensure this file contains the appropriate API key)
from GOOGLE_CLOUD_API_KEY import API_KEY

# Configure the generative AI model with the API key
genai.configure(api_key=API_KEY)

# Initialize the generative model, specifying the model to use
model = genai.GenerativeModel("gemini-1.0-pro-latest")

# Start a new chat session
chats = model.start_chat()

# Define the configuration settings for text generation
generate_config = {
    "temperature": 0.7,          # Controls the creativity of the output (0.7 is a balanced value)
    "top_p": 1,                  # Nucleus sampling parameter (1 means no restriction on top_p)
    "top_k": 1,                  # Top-k sampling parameter (1 means no restriction on top_k)
    "max_output_tokens": 2048    # Maximum number of tokens in the output
}

# Main loop to continuously get user input and generate responses
while True:
    # Prompt the user to input a question or statement
    user_input = input("Ask Gemini: ")
    
    # Send the user's input to the generative model for a response
    chats.send_message(user_input)
    
    # Print the last response from the model
    print(chats.last.text)
