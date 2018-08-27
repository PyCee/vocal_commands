#!/usr/bin/env python3

import speech_recognition as sr

ONLINE = True
#ONLINE = False

keywords_callbacks = []
offline_keywords = []

def audio_callback(recognizer, audio):
    global keyword_callbacks
    try:
        if ONLINE:
            possibilities = recognizer.recognize_google(audio, show_all=True)
            for possibility in possibilities['alternative']:
                sentence = possibility['transcript']
                for keyword_combo in keyword_callbacks:
                    if keyword_combo[0] in sentence:
                        keyword_combo[1]()
                        return
        else:
            print("Recognizing...")
            sentence = recognizer.recognize_sphinx(audio, keyword_entries=offline_keywords)
            print("Recognized: " + str(sentence))
            for keyword_combo in keyword_callbacks:
                if keyword_combo[0] in sentence:
                    keyword_combo[1]()
                    return
    except sr.UnknownValueError:
        print("I couldn't understand that")
        
class Speech_Handler:
    def __init__(self):
        self.r = sr.Recognizer()
        '''
        self.r.pause_threshold = 0.5
        # seconds of non-speaking audio before a phrase is considered complete
        self.r.phrase_threshold = 0.5
        # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
        self.r.non_speaking_duration = 0.4
        # seconds of non-speaking audio to keep on both sides of the recording
        '''
        self.m = sr.Microphone()
        self.stop_listening = None
    def is_active(self):
        return self.stop_listening != None
    def start(self, key_callbacks):
        global keyword_callbacks
        global offline_keywords
        keyword_callbacks = key_callbacks
        offline_keywords = [(key[0], key[2]) for key in keyword_callbacks]
        with self.m as source:
            self.r.adjust_for_ambient_noise(source, duration=3.0)
            print("Start speaking")
        self.stop_listening = self.r.listen_in_background(self.m, audio_callback)
    def stop(self):
        if self.is_active():
            self.stop_listening(wait_for_stop=False)
            self.stop_listening = None
