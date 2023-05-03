import speech_recognition as sr
import os
import playsound
import pygame
import requests
import json
import openai
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

#This is for microphone input
def listen():
    with sr.Microphone(device_index = 0) as source:
              inputM=sr.Recognizer()
              inputM.adjust_for_ambient_noise(source)
              print("Speak")
              try:
               audio =inputM.listen(source)
               print("Heard")
               google=inputM.recognize_google(audio)
               print(google)
               return (google)
              except:
               print("Didnt get it")
               return("Exception")    

#Speaker output using snoops voice
def response(text):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/sB2RryECBQpVI5VSPfTN"

    headers = {"Accept": "audio/mpeg","Content-Type": "application/json","xi-api-key": "e5e9659f93ff737ca4e732724fbd48de"}

    data = {"text":text,"voice_settings": {"stability": 0,"similarity_boost": 0}}

    response = requests.post(url, json=data, headers=headers)


    with open('output.mp3', 'wb') as f:
     for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
      if chunk:
       f.write(chunk)

    playsound.playsound("output.mp3")

def main():
       WAKE="hey Snoop"
       while True:
        audio=listen()
        total=0
        #activates snoop when wake call is heard
        if (audio=="hey Snoop"):
         total+=1
         if total>0:
          response("Hey big dawg")
          audio=listen()
          #Weather api
          if "weather" in audio:
           weather_data = requests.get('https://api.openweathermap.org/data/2.5/weather?zip=05405,us&appid=442c5a0f2d168e78d9b6412f248aca19&units=imperial').json()
           ftemp=weather_data['main']['temp']
           response(f"{ftemp} degrees fahrenheit")

          #Using spotify api 
          if "play" in audio: 
          
           manager = spotipy.oauth2.SpotifyOAuth(scope='user-modify-playback-state',
                                                                    username="1212878785",
                                                                    client_id="2d93cd3bcd2a401485ef8133345f59bf",
                                                                    client_secret="d740e820345c4edc81744d036e22fc5f",
                                                                    redirect_uri='http://localhost:8888/callback')
           
           rs = spotipy.Spotify(client_credentials_manager=manager)

           #Breaking user input by name and artists
           song_f=(audio.find('play'))+5
           song_b=audio.find('by')-1
           song_name=audio[song_f:song_b]
           print({song_name})

           artist_f=(audio.find('by'))+3
           artist_name=audio[artist_f:]
           print({artist_name})
           add1="artist:"
           combine=song_name+add1+artist_name

           #Gets URL for song 
           results = rs.search(song_name+' '+artist_name ,1,0,"track")
           print(results)
           items = results['tracks']['items']
           print(items)
           track_uri =items[0]['uri']
           
           #Plays songs
           rs.start_playback(device_id="d230f7a82c5d1e4d61da3b449f218aaff3a1d1ea",uris=[track_uri])
           #Pauses Song
          if 'pause' in audio:
            rs.pause_playback()

         
          #ChatGPT API
          if "what" or "who" or "how" or "where" in audio:
           message=[{"role":"system","content":audio}]
           openai.api_key = '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'
           response1= openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=message)
           reply=response1.choices[0].message
           content=reply.content
           findE=content.find("information") 
           chat=content[:]
           response(chat)
           
         
main()
