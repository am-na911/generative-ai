import streamlit as st
from dotenv import load_dotenv

import os
load_dotenv() # load all the environment variables
import google.generativeai as genai
 
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv('Google_API_KEY'))

# based on youtube id, it will extract transcript
def extract_transcript(url):
   try:
        video_id = url.split('=')[1]

        transcript_text =  YouTubeTranscriptApi.get_transcript(video_id)
        # the output will be in the form of many list

        transcript = ''
        for i in transcript_text:
            transcript += ' ' + i['text'] 

        return transcript
   except Exception as e:
       raise e


prompt = """You are a youtube video summarizer. You will be taking the the transcript 
       text and summarizing the entire video and providing the important summary in points 
       within 300 words. Your choice of words should be easy to understand. Please provide the summary
        of the given text : """

# getting summary based on prompt from google gemini
def generate_gemini_content(transcript, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt+transcript)
    return response.text

st.title('Convert YouTube Video into Notes Within Seconds!')

st.sidebar.image('gemini.png', use_container_width='True')
st.sidebar.title('LLM: Google Gemini pro')
st.sidebar.text('Generative AI has made your life easier like never before❤')
youtube_link = st.text_input('Enter Youtube Video link: ')

if youtube_link:
    splitted_url = youtube_link.split('=')[1]
    video_id = splitted_url.split('&')[0]
    

    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button('Get Detailed Note'):
    transcript_text=extract_transcript(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown('## Detailed Notes:')
        st.write(summary)