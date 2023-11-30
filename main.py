import pyttsx3
import speech_recognition as sr
import wikipedia
import os
import webbrowser

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Could not request results. Check your network connection. Error: {e}")
        return ""

# Activation command
# activation_command = "hey assistant"

def handle_command(command):
    if "stop" in command:
        speak("Goodbye!")
        exit()
    
    elif "who are you" in command:
        speak("I am your virtual assistant.")
    
    elif "what can you do" in command:
        speak("I can help you with various tasks, such as searching the web, setting reminders, and more.")
    
    elif "search wikipedia for" in command:
        search_query = command.replace("search wikipedia for", "").strip()
        try:
            result = wikipedia.summary(search_query, sentences=2)
            speak(f"According to Wikipedia, {result}")
        except wikipedia.exceptions.DisambiguationError as e:
            speak("It seems there are multiple results. Please be more specific.")
        except wikipedia.exceptions.PageError as e:
            speak("I couldn't find any information on that topic.")
    
    elif "open" in command and ("application" in command or "app" in command):
        app_name = command.replace("open", "").replace("application", "").replace("app", "").strip()
        try:
            os.system(f"start {app_name}")
            speak(f"Opening {app_name}")
        except Exception as e:
            speak(f"Sorry, I couldn't open {app_name}.")
    
    elif "take a note" in command or "write this down" in command:
        speak("Sure, what would you like me to note?")
        note_text = listen()
        with open("notes.txt", "a") as notes_file:
            notes_file.write(note_text + "\n")
        speak("Note taken and saved.")
    
    elif "play music" in command and "from my local directory" in command:
        music_dir = "music/"  # Replace with the path to your music directory
        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, songs[0])) 
        else:
            speak("No music files found in your local directory.")
    else:
        speak("I'm sorry, I didn't understand that command.")

while True:
    # command = listen()
    # if activation_command in command:
        # speak("Hello! How can I assist you?")
        # while True:
            command = listen()
            handle_command(command)