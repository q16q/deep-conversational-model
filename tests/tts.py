# config
SHOW_MODELS = False
MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"
DEFAULT_MODEL = "tts_models/multilingual/multi-dataset/bark"
REFERENCE_WAV="../refs/samplervc.wav"

TEST_TEXT = """Представьте, вы 24/7 выслушиваете хуйню, нытье, вообще что угодно от миллиона людей"""

from pprint import pprint
from datetime import datetime

print('initializing torch and coqui... ', end = '')
initbegin = datetime.now()
import torch
from TTS.api import TTS
initend = datetime.now()
print('done in {} seconds!'.format((initend - initbegin).total_seconds()))

device = "cuda" if torch.cuda.is_available() else "cpu"

print('using device:', device)



if SHOW_MODELS:
    models = TTS().list_models().list_models()

    print('\nmultilingual models:')
    pprint(list(filter(lambda x: '/multilingual/' in x, models)))
    print('\nru models:')
    pprint(list(filter(lambda x: '/ru/' in x, models)))
    print('\nen models:')
    pprint(list(filter(lambda x: '/en/' in x, models)))

model = MODEL or DEFAULT_MODEL

print('loading model... ', end = '')
lmodelbegin = datetime.now()
tts = TTS(model).to(device)
lmodelend = datetime.now()
print('done in {} seconds'.format((lmodelend - lmodelbegin).total_seconds()))

text = TEST_TEXT or "Привет, мир!"
print('generating ({} chars)... '.format(len(text)), end = '')
ttsbegin = datetime.now()
wav = tts.tts_to_file(text, speaker_wav = REFERENCE_WAV, file_path = "outputs/tts.wav", language = "ru")
ttsend = datetime.now()
print('done in {} seconds'.format((ttsend - ttsbegin).total_seconds()))