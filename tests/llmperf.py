from g4f.Provider import Blackbox
from g4f import ChatCompletion
from datetime import datetime

for model in Blackbox.userSelectedModel:
    print('\n\ttesting model - %s' % model)
    print('generating response...')
    time_a = datetime.now()
    response = ChatCompletion.create(
        model = model,
        provider=Blackbox,
        messages=[{"role": "user", "content": "Можешь мне рассказать как работают ИИ? Старайся рассказать в очень краткой форме, желательно меньше 100 символов. Также пиши только на русском."}],
    )
    time_b = datetime.now()

    print(response)
    print('done in {} seconds!'.format((time_b - time_a).total_seconds()))