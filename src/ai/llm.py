import logging
logger = logging.getLogger('llm')

logger.info('loading g4f...')
from g4f.Provider import Blackbox
from g4f import ChatCompletion
logger.info('done!')
from datetime import datetime

class LLM:
    def __init__(self, model = 'gemini-2.0-flash', provider = Blackbox, max_messages: int = 100, **kwargs):
        logger.info('using: model={};provider={};max_messages={}'.format(
            model, provider, max_messages
        ))
        
        self.model = model
        self.provider = provider
        self.max_messages = max_messages
        self.current_session = [{
            "role": "system",
            "content": "Ты - полезный помощник, тебя зовут Катя и ты женщина - именно поэтому ты используешь женские местоимения. Старайся отвечать кратко, до 100 символов. Ты общаешься на дискорд сервере, поэтому веди себя как ее участник. Все знаки в своих ответах расписывай словами, также в словах более 3 слогов, ставь ударения с помощью определе."
        }]

        logger.info('initialized!')
    
    def create_new_session(self):
        logger.info('resetting session!')
        self.current_session = [{
            "role": "system",
            "content": "Ты - полезный помощник, тебя зовут Катя и ты женщина - именно поэтому ты используешь женские местоимения. Старайся отвечать кратко, до 100 символов. Ты общаешься на дискорд сервере, поэтому веди себя как ее участник."
        }]
    
    def clean_up_session(self):
        if len( self.current_session ) > self.max_messages:
            logger.info('cleaning session...')
            self.current_session = self.current_session[
                - abs(self.max_messages) :
            ]

    def generate(self, message: str):
        self.current_session.append({
            "role": 'user',
            "content": message
        })
        self.clean_up_session()
        logger.info('responding to message: {}'.format(message))

        time_before = datetime.now()
        response = ChatCompletion.create(
            model = self.model,
            provider = self.provider,
            messages = self.current_session
        )
        time_after = datetime.now()
        self.current_session.append({
            "role": "assistant",
            "content": response
        })

        logger.info('done in {} seconds'.format((time_after - time_before).total_seconds()))
        return response