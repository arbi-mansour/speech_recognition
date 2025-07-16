import streamlit as st
import nltk
import speech_recognition as sr

# Setup
nltk.download('punkt')

# Load chatbot knowledge base
def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        corpus = file.read()
    return corpus

# Simple chatbot response generator
def generate_response(user_input, corpus):
    sentences = nltk.sent_tokenize(corpus)
    for sentence in sentences:
        if user_input.lower() in sentence.lower():
            return sentence
    return "I'm not sure I understand. Please try rephrasing."

# Speech-to-text transcription
def transcribe_speech(language='en-US'):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak clearly.")
        audio = recognizer.listen(source)
    try:
        st.success("Processing speech input...")
        return recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        return "Sorry, I could not understand your speech."
    except sr.RequestError as e:
        return f"Speech Recognition error: {e}"

# Load knowledge base
corpus = load_corpus('chatbot_knowledge.txt')

# Streamlit App
st.title("🎙️ Speech-Enabled Chatbot")

input_mode = st.radio("Select Input Mode:", ['Text Input', 'Speech Input'])

if input_mode == 'Text Input':
    user_input = st.text_input("Type your message here:")
    if st.button("Send"):
        if user_input.strip():
            response = generate_response(user_input, corpus)
            st.text_area("Chatbot Response:", value=response, height=100)
        else:
            st.warning("Please type a message.")

elif input_mode == 'Speech Input':
    if st.button("Start Speech Input"):
        transcribed_text = transcribe_speech()
        st.text_input("Transcribed Text:", value=transcribed_text)
        response = generate_response(transcribed_text, corpus)
        st.text_area("Chatbot Response:", value=response, height=100)
