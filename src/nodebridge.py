import logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger('nodebridge')

import asyncio, json
from websockets.asyncio.server import serve
from ai.symbiosis import AI
from datetime import datetime

async def wsreturn(ws, success: bool, **kwargs):
    kwargs.update({ 'success': success })
    logger.info('responding with: {}'.format(kwargs))
    await ws.send(json.dumps(kwargs))

ai = AI(tts_reference_wav_fp = '../refs/samplervc.wav')
async def echo(websocket):
    async for message in websocket:
        logger.info('got request: {}'.format(message))
        try:
            content = json.loads(message)
        except json.JSONDecodeError:
            await wsreturn(websocket, False, reason = "Invalid JSON!")
            continue

        # check message for errors
        if 'type' not in content:
            await wsreturn(websocket, False, reason = "No 'type' in content")
            continue
        
        if content['type'] == 'respond':
            if 'message' not in content:
                await wsreturn(websocket, False, reason = "No 'message' in content")
                continue

            fp = "output.wav"
            if 'fp' in content: fp = content['fp']

            time_a = datetime.now()
            response, wav = ai.respond(content['message'], fp)
            time_b = datetime.now()

            logger.info('symbiosis responded in total of {} seconds'.format((time_b - time_a).total_seconds()))
            await wsreturn(websocket, True, response = response, wav = wav)
            continue

        if content['type'] == 'tts':
            if 'message' not in content:
                await wsreturn(websocket, False, reason = "No 'message' in content")
                continue

            fp = "output.wav"
            if 'fp' in content: fp = content['fp']

            time_a = datetime.now()
            wav = ai.tts.generate(content['message'], output_path = fp)
            time_b = datetime.now()

            await wsreturn(websocket, True, wav = wav)

async def main():
    global ai
    async with serve(echo, "localhost", 8127) as server:
        logger.info('running!')
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())