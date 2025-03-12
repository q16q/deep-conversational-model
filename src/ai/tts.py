import logging

logger = logging.getLogger('tts')

logger.info('initializing coqui api...')
from TTS.api import TTS as TTS_
logger.info('done!')

logger.info('initializing torch...')
import torch
logger.info('done!')


class TTS:
    def __init__(self, reference_wav_fp: str, **kwargs):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = 'tts_models/multilingual/multi-dataset/xtts_v2'
        self.reference_wav_fp = reference_wav_fp
        self.output_path = "output.wav"
        self.language = "ru"

        for k,v in kwargs.items():
            setattr(self, k, v)

        logger.info('using device {}'.format(self.device))
        logger.info('using model {}'.format(self.model))
        logger.info('using reference {}'.format(self.reference_wav_fp))

        logger.info('loading model...')
        self.tts = TTS_(self.model).to(self.device)
        logger.info('done!')

    def generate(self, text: str, language: str = "", output_path: str = "") -> str:
        language = language or self.language
        output_path = output_path or self.output_path

        logger.info('generating with options: lang={},out={}'.format(language,output_path))
        wav = self.tts.tts_to_file(text, speaker_wav = self.reference_wav_fp,
                              file_path = output_path, language = language)
        
        return wav