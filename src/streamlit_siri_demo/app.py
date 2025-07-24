import streamlit as st
import sounddevice as sd
import numpy as np
import tempfile
import os
import json
import re
from faster_whisper import WhisperModel
from llama_cpp import Llama
import src.functions.functions as fc

def test_function_call(query):
    # Use the EXACT same format as your training
    chat = [
        {"role": "system", "content": (
            "You are a function-calling assistant that replies with JSON.\n"
            f"Available functions:\n{json.dumps(fc.functions, indent=2)}"
        )},
        {"role": "user", "content": query}
    ]
    
    # Apply the same chat template as your training (llama-3 format)
    prompt = ""
    for message in chat:
        if message["role"] == "system":
            prompt += f"<|start_header_id|>system<|end_header_id|>\n\n{message['content']}<|eot_id|>"
        elif message["role"] == "user":
            prompt += f"<|start_header_id|>user<|end_header_id|>\n\n{message['content']}<|eot_id|>"
    prompt += "<|start_header_id|>assistant<|end_header_id|>\n\n"
    
    # Generate response
    response = llm(
        prompt,
        max_tokens=512,
        temperature=0.1,
        stop=["<|eot_id|>", "<|end_of_text|>"],
        echo=False
    )
    
    generated_text = response["choices"][0]["text"].strip()
    print(f"Raw model response: {generated_text}")
    
    results = []
    parsed_responses = extract_json_arrays(generated_text)
    
    for call in parsed_responses:
        name = call.get("name")
        args = call.get("arguments", {})
        func = fc.available_function_calls.get(name)
        
        if func:
            try:
                result = func(**args)
                success_msg = f"✅ {name} ran: {result}"
                print(success_msg)
                results.append(success_msg)
            except Exception as e:
                error_msg = f"❌ Error in {name}: {e}"
                print(error_msg)
                results.append(error_msg)
        else:
            not_found_msg = f"⚠️ Function not found: {name}"
            print(not_found_msg)
            results.append(not_found_msg)
    
    return {
        "raw_response": generated_text,
        "function_results": results,
        "parsed_calls": parsed_responses
    }

def extract_json_arrays(text):
    array_pattern = r"\[\s*{.*?}\s*]"
    matches = re.findall(array_pattern, text, re.DOTALL)
    
    parsed = []
    for match in matches:
        try:
            parsed.extend(json.loads(match))
        except json.JSONDecodeError as e:
            print("Error decoding:", match, e)
    return parsed

# --- LOAD MODELS ---
@st.cache_resource
def load_llm_model():
    llm = Llama.from_pretrained(
        repo_id="CosminMihai02/llama3.1_ollama_v2",
        filename="unsloth.Q4_K_M.gguf",
        n_ctx=4096,  # Context length
        n_threads=4,  # CPU threads
        verbose=False
    )
    return llm

@st.cache_resource
def load_stt_model():
    model = WhisperModel("base", device="cpu", compute_type="int8")
    return model

# Load models
try:
    llm = load_llm_model()
    stt_model = load_stt_model()
    st.success("Models loaded successfully!")
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

# --- CONFIG ---
SAMPLE_RATE = 16000
DURATION = 5

# --- UI ---
st.title("Real-time Speech-to-Function-Calling Demo")
st.write("Click 'Record' and speak your command or write your command in the text box.")

# Text input option
text_input = st.text_input("Or type your command here:", placeholder="e.g., Set volume to 50 and search Python tutorials")

if 'audio' not in st.session_state:
    st.session_state['audio'] = None

if st.button('Record'):
    st.write(f"Recording for {DURATION} seconds...")
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    st.session_state['audio'] = audio
    st.success("Recording complete!")

transcription = ""

if st.session_state['audio'] is not None:
    st.audio(st.session_state['audio'].astype(np.float32).tobytes(), format='audio/wav', sample_rate=SAMPLE_RATE)
    
    # Add clear button
    if st.button('Clear Recording'):
        st.session_state['audio'] = None
        st.rerun()
    
    # Save to temp file for whisper
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        from scipy.io.wavfile import write
        write(f.name, SAMPLE_RATE, st.session_state['audio'])
        temp_wav = f.name
    
    # Transcribe
    segments, info = stt_model.transcribe(temp_wav)
    transcription = " ".join([seg.text for seg in segments])
    st.write("**Transcription:**", transcription)
    
    os.remove(temp_wav)

# Use either transcription or text input (prioritize non-empty content)
query = transcription.strip() if transcription.strip() else text_input.strip()

if query and st.button('Send to Model'):
    # Show which input is being used
    input_source = "🎤 Voice" if transcription.strip() else "✏️ Text"
    st.info(f"Using {input_source} input: {query}")
    
    with st.spinner('Running model...'):
        try:
            result = test_function_call(query)
            st.write("**Model Output:**", result)
        except Exception as e:
            st.error(f"Error: {e}")