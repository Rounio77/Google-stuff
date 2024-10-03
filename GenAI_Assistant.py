import customtkinter as ctk
import speech_recognition as sr
import pyttsx3 as tts
import threading
import google.generativeai as genai
from GOOGLE_CLOUD_API_KEY import API_KEY

recognize = sr.Recognizer()
speaker = tts.init()
wake_word = 'hey bob'

# set up GenAI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.0-pro-latest')

chat = model.start_chat()
generate_config = {
    'temperature': 0.7,
    'top_p': 1,
    'top_k': 1,
    'max_output_tokens': 2048
}

# Initialize Customtkinter GUI
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')


# Create virtual Assistant
class VirtualAssistant(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title('BOB')
        self.geometry('400x200')

        # Assistant Label
        self.state_label = ctk.CTkLabel(self, text='Waiting for Wake Word', font=("Arial", 20))
        self.state_label.pack(pady=20)

        # Indicator
        self.indicator = ctk.CTkLabel(self, text="🔴", font=("Arial", 20))
        self.indicator.pack(pady=10)

        # Start listening button
        self.listen_button = ctk.CTkButton(self, text='Start Listening', command=self.start_listening)
        self.listen_button.pack(pady=10)

    def start_listening(self):
        threading.Thread(target=self.listen_for_wake_word).start()

    def listen_for_wake_word(self):
        # continuously listen for wake word
        with sr.Microphone() as audio_source:
            while True:
                self.state_label.configure(text='Waiting for wake word...')
                self.indicator.configure(text="🔴")

                audio = recognize.listen(audio_source)
                try:
                    text = recognize.recognize_google(audio).lower()
                    print(f'Recognized {text}')

                    if wake_word in text:
                        self.state_label.configure(text='Wake Word detected, Listening for commands...')
                        self.indicator.configure(text="🟢")
                        self.assistant_command()
                    else:
                        print('Wake word not found')\

                except sr.UnknownValueError:
                    print('Google Speech Recognition could not understand audio.')
                except sr.RequestError as e:
                    print(f'Could not request result: {e}')

    def assistant_command(self):
        user_input = self.get_audio_input()

        if user_input:
            chat.send_message(user_input)
            response = chat.last.text
            print(f'AI Response: {response}')
            speaker.say(response)
            speaker.runAndWait()
            speaker.stop()

    def get_audio_input(self):
        with sr.Microphone() as audio_source:
            self.state_label.configure(text='Listening for commands...')
            self.indicator.configure(text="🟢")

            audio = recognize.listen(audio_source)
            try:
                text = recognize.recognize_google(audio).lower()
                print(f'User said: {text}')
                return text
            except sr.UnknownValueError:
                print('Google Speech Recognition could not understand audio.')
                return None
            except sr.RequestError as e:
                print(f'Could not request result: {e}')
                return None


if __name__ == '__main__':
    app = VirtualAssistant()
    app.mainloop()

