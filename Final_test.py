# ================= IMPORTS =================
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import requests
import webbrowser
import os
import pywhatkit as kit
import pyautogui
import random
import time

# ================= VOICE ENGINE =================
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 160)

author = "Human"
assistant_name = "Lichi"
# ================= CONTACTS =================
contacts = {
    "mom": "+91903280xxxx",
    "dad": "+91630230xxxx",
    "friend": "+91960327xxxx"
}

# ================= SPEAK FUNCTION =================
def speak(text):
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.3)

# ================= MS OFFICE =================
def open_word():
    os.startfile("winword")
    speak("Opening Microsoft Word")

def open_excel():
    os.startfile("excel")
    speak("Opening Microsoft Excel")

def open_powerpoint():
    os.startfile("powerpnt")
    speak("Opening Microsoft PowerPoint")

# ================= NAVIGATION =================
def go_back():
    speak("Going back")
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')

def browser_back():
    speak("Going to previous page")
    pyautogui.hotkey('alt', 'left')

# ================= EMAIL OPEN =================
def open_email():
    speak("Opening email")
    webbrowser.open("https://mail.google.com")

# ================= OPEN WHATSAPP =================
def open_whatsapp():
    speak("Opening WhatsApp")
    webbrowser.open("https://web.whatsapp.com")

# ================= WHATSAPP =================

def send_whatsapp():
    speak("Whom should I send the message to?")
    name = takeCommand().lower()

    # Smart matching
    number = None
    for contact in contacts:
        if contact in name:
            number = contacts[contact]
            name = contact
            break

    if not number:
        speak("Contact not found")
        return

    speak("What message should I send?")
    message = takeCommand()

    speak(f"Sending message to {name}")

    try:
        kit.sendwhatmsg_instantly(number, message, wait_time=10)
        speak("Message sent successfully")
    except:
        speak("Failed to send message")

# ================= OLLAMA EMAIL =================
def generate_email_body(topic):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": f"Write a professional email about {topic}",
                "stream": False
            }
        )
        return response.json().get("response", "Error generating email")
    except:
        return "Email generation failed"

# ================= EMAIL SEND =================
def sendEmail(to, content):
    url = "https://api.emailjs.com/api/v1.0/email/send"

    payload = {
        "service_id": "service_xutn3nr",
        "template_id": "template_o06bx1i",
        "user_id": "wDVZo_L_LVi7LZn8K",
        "template_params": {
            "to_email": to,
            "message": content
        }
    }

    try:
        requests.post(url, json=payload)
        speak("Email sent successfully")
    except:
        speak("Failed to send email")

# ================= WISH =================
def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    speak(f"{greeting} {author}. I am {assistant_name}. How may I help you?")

# ================= TAKE COMMAND =================
def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.2
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("User Said:", query)
        return query.lower()
    except:
        speak("Please say that again")
        return ""

# ================= SCREENSHOT =================
def takeScreenshot():
    folder = os.path.join(os.path.expanduser("~"), "Pictures", "LichiScreenshots")
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, f"screenshot_{int(time.time())}.png")
    pyautogui.screenshot().save(path)

    speak("Screenshot taken")

# ================= MUSIC =================
def play_music(song_name=None):
    song_dir = os.path.join(os.path.expanduser("~"), "Music")

    songs = [s for s in os.listdir(song_dir)
             if s.endswith((".mp3", ".wav"))]

    if song_name:
        songs = [s for s in songs if song_name in s.lower()]

    if songs:
        os.startfile(os.path.join(song_dir, random.choice(songs)))
        speak("Playing music")
    else:
        speak("No song found")

# ================= MAIN =================
if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand()

        if not query:
            continue

        # -------- MS OFFICE --------
        elif "open word" in query:
            open_word()

        elif "open excel" in query:
            open_excel()

        elif "open powerpoint" in query:
            open_powerpoint()

        # -------- NAVIGATION --------
        elif "go back" in query:
            go_back()

        elif "previous page" in query:
            browser_back()

        # -------- EMAIL --------
        elif "open email" in query:
            open_email()
        
        # -------- WHATSAPP OPEN --------
        elif "open whatsapp" in query:
            open_whatsapp()

        elif "send email" in query:
            speak("What is the email about?")
            topic = takeCommand()

            speak("Generating email")
            body = generate_email_body(topic)

            print(body)

            to = input("Enter email address: ")
            sendEmail(to, body)

        # -------- WHATSAPP --------
        elif "send whatsapp" in query:
            send_whatsapp()

        # -------- GOOGLE SEARCH (IMPROVED) --------
        elif "search" in query:
            search_query = query.replace("search", "").strip()

            if search_query == "":
                speak("What should I search?")
                search_query = takeCommand()

            speak(f"Searching for {search_query}")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        # -------- YOUTUBE --------
        elif "open youtube" in query:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")

        elif "play youtube" in query:
            speak("What should I play?")
            video = takeCommand()
            kit.playonyt(video)

        # -------- WIKIPEDIA --------
        elif "wikipedia" in query:
            topic = query.replace("wikipedia", "")
            result = wikipedia.summary(topic, sentences=2)
            speak(result)

        # -------- SCREENSHOT --------
        elif "screenshot" in query:
            takeScreenshot()

        # -------- MUSIC --------
        elif "play music" in query:
            song = query.replace("play music", "")
            play_music(song)

        # -------- EXIT --------
        elif "exit" in query:
            speak("Goodbye")
            break

        else:
            speak("Command not recognized")