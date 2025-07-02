
import openai
import os
import speech_recognition as sr
import pyttsx3

# Load OpenAI API key from environment variables
openai.api_key = "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"

# Initialize the TTS engineexit

engine = pyttsx3.init()
engine.setProperty("rate", 160)  # Adjust speed (optional)

# Define a class for the chatbot
class GPTChatbot:
    def __init__(self, model="gpt-4"):
        self.model = model
        self.chat_history = [
            {
                "role": "system",
                "content": (
                    "You are acting as a customer interested in buying a car, and your role is solely to raise objections, express concerns, and ask questions as a customer."
                    "You should never start the conversation directly by asking sales question, first thing is to always ask the user why they are calling and then introduce and greet the User. Do this for all simulations"
                    "In this conversation, you are not a salesperson and should never provide answers, solutions, or information. "
                    "Always introduce yourself as a random customer, and do not attempt to guide or help in any way.\n\n"
                    "Your job is only to test the salesperson's objection handling skills by:\n"
                    "- Raising common objections related to pricing, financing, trade-in values, warranty coverage, features, and maintenance costs.\n"
                    "- Expressing doubts and concerns without offering answers or solutions.\n\n"
                    "Examples of responses include:\n"
                    "- Hi #User's Name# I am not sure why I am recieving this Call.'\n"
                    "- 'I'm not sure the monthly payment fits within my budget.'\n"
                    "- 'I don't know if this car has all the features I want.'\n"
                    "- 'The interest rate seems high. Are there better options?'\n"
                    "- 'I’m not convinced this is the best price I can get elsewhere.'\n"
                    "- 'I’m concerned about the long-term maintenance costs.'\n\n"
                    "Do not offer help or suggestions. Stay in the role of a customer with objections and questions only. If the salesperson asks how they can help, respond with questions or concerns rather than any answers."
                    "Ask follow up questions everytime the user responds appropriately in the context."
                )
            }
        ]
    
    def detect_off_topic_or_inappropriate(self, user_input):
        # List of inappropriate or off-topic keywords (you can expand this list)
        inappropriate_keywords = ["politics", "religion", "insult", "hate", "racist", "offensive", "violence", "disrespect", "abuse"]

        # Check if any inappropriate keyword is in the user input
        for keyword in inappropriate_keywords:
            if keyword in user_input.lower():
                return True
        return False

    def generate_response(self, user_message):
        # Check for off-topic or inappropriate content
        if self.detect_off_topic_or_inappropriate(user_message):
            warning_message = "I'm sorry, but this conversation has gone off-topic or has become inappropriate. Ending the session."
            print(warning_message)
            speak_text(warning_message)
            return "END_CONVERSATION"

        # Append user message to the chat history
        self.chat_history.append({"role": "user", "content": user_message})

        try:
            # Generate a response from the GPT model using ChatCompletion API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.chat_history,
            )

            assistant_message = response['choices'][0]['message']['content']
            
            # Append assistant's response to the chat history
            self.chat_history.append({"role": "assistant", "content": assistant_message})

            return assistant_message

        except Exception as e:
            return f"An error occurred: {e}"

    def clear_history(self):
        # Clear the chat history and reinitialize with system message
        self.chat_history = [
            {
                "role": "system",
                "content": ( 
                 "You are acting as a customer interested in buying a car, and your role is solely to raise objections, express concerns, and ask questions as a customer."
                    "You should never start the conversation directly by asking sales question, first thing is to always ask the user why they are calling and then introduce and greet the User. Do this for all simulations"
                    "In this conversation, you are not a salesperson and should never provide answers, solutions, or information. "
                    "Always introduce yourself as a random customer, and do not attempt to guide or help in any way.\n\n"
                    "Your job is only to test the salesperson's objection handling skills by:\n"
                    "- Raising common objections related to pricing, financing, trade-in values, warranty coverage, features, and maintenance costs.\n"
                    "- Expressing doubts and concerns without offering answers or solutions.\n\n"
                    "Examples of responses include:\n"
                    "- Hi #User's Name# I am not sure why I am recieving this Call.'\n"
                    "- 'I'm not sure the monthly payment fits within my budget.'\n"
                    "- 'I don't know if this car has all the features I want.'\n"
                    "- 'The interest rate seems high. Are there better options?'\n"
                    "- 'I’m not convinced this is the best price I can get elsewhere.'\n"
                    "- 'I’m concerned about the long-term maintenance costs.'\n\n"
                    "Do not offer help or suggestions. Stay in the role of a customer with objections and questions only. If the salesperson asks how they can help, respond with questions or concerns rather than any answers."
                    "Ask follow up questions everytime the user responds appropriately in the context."
                )
            }
        ]

# Function to use text-to-speech for chatbot response
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture user voice input using SpeechRecognition
def listen_for_user_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

# Main function to run the voice-enabled chatbot
def main():
    print("Welcome to the Car Sales Objection Handling Training Chatbot! Type 'exit' to quit or 'clear' to reset the conversation.")
    
    chatbot = GPTChatbot()

    while True:
        user_input = listen_for_user_input()

        if user_input.lower() == "exit":
            print("Goodbye!")
            speak_text("Goodbye!")
            break
        elif user_input.lower() == "clear":
            chatbot.clear_history()
            print("Chat history cleared.")
            speak_text("Chat history cleared.")
        elif user_input:
            response = chatbot.generate_response(user_input)
            if response == "END_CONVERSATION":
                break
            print(f"Chatbot: {response}")
            speak_text(response)

# Entry point
if __name__ == "__main__":
    main()
