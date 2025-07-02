import openai
import speech_recognition as sr

# Load OpenAI API key
openai.api_key = "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"

# Define a class for the interviewee chatbot
class IntervieweeChatbot:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.chat_history = [
            {
                "role": "system",
                "content": (
                    "You are Parth Akre, a highly skilled software engineer applying for a Software Engineer, Back-End Development role. "
                    "You must respond as the interviewee in a mock interview, providing detailed and professional answers to technical, behavioral, and scenario-based questions "
                    "posed by the recruiter. Your responses must be concise, professional, and tailored to the following job description and your resume."
                )
            }
        ]

    def generate_response(self, recruiter_question):
        self.chat_history.append({"role": "user", "content": recruiter_question})

        try:
            # Send request to OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.chat_history,
                temperature=0.7,  # Lower temperature for more focused responses
                max_tokens=150,  # Limit token count for quicker responses
            )

            assistant_message = response['choices'][0]['message']['content']
            # Add response to chat history
            self.chat_history.append({"role": "assistant", "content": assistant_message})

            return assistant_message

        except Exception as e:
            return f"An error occurred: {e}"

    def clear_history(self):
        self.chat_history = [
            {
                "role": "system",
                "content": (
                    "You are Parth Akre, a highly skilled software engineer applying for a Software Engineer, Back-End Development role. "
                    "You must respond as the interviewee in a mock interview, providing detailed and professional answers to technical, behavioral, and scenario-based questions "
                    "posed by the recruiter. Your responses must be concise, professional, and tailored to the following job description and your resume."
                )
            }
        ]

# Function to capture recruiter voice input
def listen_for_recruiter_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for the recruiter's question...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Reduce adjustment time
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Shorter time limits
    try:
        recruiter_input = recognizer.recognize_google(audio)
        print(f"Recruiter: {recruiter_input}")
        return recruiter_input
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the question. Please try again.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

# Main function to simulate the interview
def main():
    print("Welcome to the Backend Development Interview Simulator! Say 'exit' to quit or 'clear' to reset the conversation.")
    
    chatbot = IntervieweeChatbot()

    while True:
        recruiter_question = listen_for_recruiter_input()

        if recruiter_question.lower() == "exit":
            print("Goodbye!")
            break
        elif recruiter_question.lower() == "clear":
            chatbot.clear_history()
            print("Chat history cleared.")
        elif recruiter_question:
            response = chatbot.generate_response(recruiter_question)
            print(f"Parth: {response}")

# Entry point
if __name__ == "__main__":
    main()
