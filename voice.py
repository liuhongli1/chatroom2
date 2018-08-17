#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# outhor:刘洪礼 time:2018/7/31

# In[3]:


# pip install msgpack
# pip install SpeechRecognition
speechKey = '4cdf23d37c61485db82298c6b3260993'
import speech_recognition as sr

# Read the audio file
#r = sr.Recognizer()
#with sr.AudioFile('RainSpain.wav') as source:
    #audio = r.record(source)
    
# Alternative code to use mic input (only works in local Jupyter - not in Azure Notebooks)
def my_voice():
	r = sr.Recognizer()
	with sr.Microphone() as source:
	    print("Say something!")
	    audio = r.listen(source)

	# transcribe speech using the Bing Speech API
	try:
	    transcription = r.recognize_bing(audio, key=speechKey,language='zh-CN')
	    print("Here's what I heard:")
	    return 'OK'+' '+transcription 
	    
	except sr.UnknownValueError:
	    return 'U'+' '+"The audio was unclear"
	except sr.RequestError as e:
	    return 'W'+' '+"Something went wrong :-(; {0}".format(e)
my_voice()
