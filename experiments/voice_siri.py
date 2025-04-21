import json

import pyttsx3
import requests
import speech_recognition as sr
import whisper

from test_model import (
    available_function_calls,
)


def speak(text):
    # Text-to-speech engine
    engine = pyttsx3.init()

    engine.say(text)
    engine.runAndWait()


# Speech recognizer


def listen_to_user():
    # Initialize Whisper model (this can be moved outside if you want to reuse the model)
    model = whisper.load_model(
        "base"
    )  # You can choose "tiny", "base", "small", "medium", or "large"

    with sr.Microphone() as source:
        print("🎙️ Speak now...")
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(
            source,
            timeout=20,
            phrase_time_limit=30,
        )

    try:
        print("🧠 Transcribing with Whisper...")
        # Save audio to temporary file (Whisper needs a file input)
        with open("temp_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())

        # Transcribe using Whisper
        result = model.transcribe("temp_audio.wav")
        query = result["text"]

        print(f"🗣️ You said: {query}")
        return query
    except Exception as e:
        print(f"Speech recognition error: {e}")
        speak("Sorry, I didn't catch that.")
        return None


def call_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "hf.co/valex95/llama3.1_ollama:Q4_K_M",
            "prompt": prompt,
            "stream": False,
        },
    )
    print(response.json())
    return response.json()["response"]


def execute_tools(response_text):
    try:
        tool_calls = json.loads(response_text)
        results = []
        for call in tool_calls:
            name = call["name"]
            args = call.get("arguments", {})
            func = available_function_calls.get(name)
            if func:
                result = func(**args)
                results.append(f"{name} -> {result}")
            else:
                results.append(f"Unknown function: {name}")
        return results
    except Exception as e:
        return [f"Error parsing function calls: {e}"]


# Main flow
def main():
    query = listen_to_user()
    print(query)
    if not query:
        return

    tool_prompt = f"""
You are a local assistant that calls functions. Only return a JSON array like this:
[
  {{
    "name": "function_name",
    "arguments": {{
      "param1": "value1"
    }}
  }}
]

Available functions: {list(available_function_calls.keys())}
User: {query}
"""

    print("🤖 Sending to Ollama...")
    response = call_llm(tool_prompt)
    print("\n💬 LLM response:\n", response)

    results = execute_tools(response)
    for res in results:
        print("🛠️", res)
        speak(res)


if __name__ == "__main__":
    main()
