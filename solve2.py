import datetime
import webbrowser
import pyttsx3
import psutil
import socket
import openai

# === CONFIG ===
openai.api_key = "your-api-key-here"  # Replace with your OpenAI API key

# === TTS Setup ===
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio: str) -> None:
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# === System Info ===
def get_battery_status() -> str:
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        plugged = battery.power_plugged
        status = f"Battery is at {percent} percent."
        status += " Charging." if plugged else " Not charging."
        return status
    return "Unable to get battery information."

def get_cpu_usage() -> str:
    usage = psutil.cpu_percent(interval=1)
    return f"Current CPU usage is {usage} percent."

def get_network_status() -> str:
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return "Network status: Connected to the internet."
    except OSError:
        return "Network status: Not connected to the internet."

# === ChatGPT API Call ===
def ask_chatgpt(question: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available to you
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error talking to ChatGPT: {e}"

# === Greeting and Status ===
def wish() -> None:
    hour = datetime.datetime.now().hour
    current_time = datetime.datetime.now().strftime("%I:%M %p")

    if 0 <= hour < 12:
        speak("Good morning sir")
    elif 12 <= hour < 18:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")

    speak(f"The current time is {current_time}")
    speak(get_battery_status())
    speak(get_cpu_usage())
    speak(get_network_status())
    speak("I am Edith, your AI assistant. How can I help you?")

# === Assistant Class ===
class TextAssistant:
    def __init__(self) -> None:
        pass

    def get_greeting(self) -> str:
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            return "Good morning"
        elif 12 <= hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

    def handle_command(self, command: str) -> None:
        command = command.lower()

        if "google" in command:
            search_query = command.replace("google", "").strip()
            if search_query:
                url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(url)
                print(f"Searching Google for: {search_query}")
            else:
                print("What should I search on Google?")

        elif "chatgpt" in command:
            question = command.replace("chatgpt", "").strip()
            if question:
                response = ask_chatgpt(question)
                speak(response)
            else:
                speak("What do you want to ask ChatGPT?")

        elif "exit" in command or "stop" in command:
            speak("Have a nice day sir. Goodbye!")
            exit()

        else:
            print(f"You typed: {command}")

# === Main Loop ===
def main() -> None:
    assistant = TextAssistant()
    print(assistant.get_greeting())

    while True:
        command = input("Type your command: ")
        assistant.handle_command(command)

if __name__ == "__main__":
    wish()
    main()
