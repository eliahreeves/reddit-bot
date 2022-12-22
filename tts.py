import pyttsx3
import constants as c
import random
random.seed = 70
if c.RANDOMIZE_VOICE:
    voice_id = random.randint(0,1)
else:
    voice_id = c.VOICE

def TextToSpeach(string, path):
    engine = pyttsx3.init() # object creation

    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', c.RATE)     # setting up new voice rate


    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    engine.setProperty('volume', c.VOLUME)    # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    
    engine.setProperty('voice', voices[voice_id].id)   #changing index, changes voices. 1 for female


    """Saving Voice to a file"""
    # On linux make sure that 'espeak' and 'ffmpeg' are installed
    engine.save_to_file(string, path)
    engine.runAndWait()

if c.RANDOMIZE_VOICE:
    voice_id = random.randint(0,1)
else:
    voice_id = c.VOICE

print(voice_id)