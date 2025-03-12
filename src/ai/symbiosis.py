from .tts import TTS
from .llm import LLM

class AI:
    def __init__(self, **kwargs):
        tts_kwargs = {k.replace('tts_', ''): v for k,v in kwargs.items() if k.startswith('tts_')}
        llm_kwargs = {k.replace('llm_', ''): v for k,v in kwargs.items() if k.startswith('llm_')}
        self.tts = TTS(**tts_kwargs)
        self.llm = LLM(**llm_kwargs)
    
    def respond(self, message: str, output_fp: str = "output.wav"):
        response = self.llm.generate(message)
        wav = self.tts.generate(response, output_path = output_fp)
        return response, wav