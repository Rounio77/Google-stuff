import google.generativeai as genai
from GOOGLE_CLOUD_API_KEY import API_KEY

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.0-pro-latest")

chats = model.start_chat()
generate_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048
}

while True:
    user_input = input("Ask Gemini: ")
    chats.send_message(user_input)
    print(chats.last.text)
