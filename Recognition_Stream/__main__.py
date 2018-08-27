#!/usr/bin/env python3

import sys
import os
import subprocess
import math
import audioop
from collections import deque

from pocketsphinx.pocketsphinx import *
from pocketsphinx import LiveSpeech, get_model_path, get_data_path, DefaultConfig, Decoder
from sphinxbase.sphinxbase import *
import pyaudio

class Speech_Stream:
    def __init__(self):
        
        MODELDIR = get_model_path()
        CURR_DIR = os.path.dirname(os.path.realpath(__file__))
        KEYPHRASE_THRESH_DIR = CURR_DIR + '/keyphrases.thresh'
        
        # Create a decoder with certain model
        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(MODELDIR, 'en-us'))
        config.set_string('-dict', \
                          os.path.join(MODELDIR, 'cmudict-en-us.dict'))
        config.set_string('-kws', KEYPHRASE_THRESH_DIR)
        #config.set_string('-logfn', '/dev/null')
        decoder = Decoder(config)
        
        
        p = pyaudio.PyAudio()
        host_info = p.get_host_api_info_by_index(0)
        device_index = 3
        for i in range(host_info.get('deviceCount')):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            #print('\n\n\n\n'+str(i)+device_info.get('name') + " : " + str(device_info.get('maxInputChannels')))
            if 'USB' in device_info.get('name'):
                device_index = i
                break

        '''
        fire /1e18/
        '''
            
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024,
            input_device_index=device_index)
        
        stream.start_stream()
        in_speech_bf = True
        
        decoder.start_utt()
        print("Starting to listen")
        
        while True:
            buf = stream.read(1024, exception_on_overflow = False)
            decoder.process_raw(buf, False, False)
            if decoder.hyp() != None:
                print("\nDetected: " + decoder.hyp().hypstr + "\n")
                decoder.end_utt()
                #print "Detected Move Forward, restarting search"
                decoder.start_utt()
        print("Am not listening any more")
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        
if __name__ == "__main__":
    sd = Speech_Stream()
