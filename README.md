# telegram-bot
Bot telegram 

## Converting Anaconda environment to pip requirements

1. Use [conda-minify](https://github.com/jamespreed/conda-minify) to export only the top level requirements without the build string. It **must** be installed and executed within the conda `base` environment.

conda run --name base conda-minify -n mairror-api > environment.yml

2. Use the conversion tool `utils/conversor.py` to convert the requirements to a pip requirements file. It reads the previously generated YAML file and outputs a requirements.txt file in the same folder.

python utils/conversor.py

## Testing

There isn't any framework to do unit test with our code, you can check it in this mail: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Writing-Tests

## References

- https://stackoverflow.com/questions/42796300/get-photo-in-telegram-bot-through-pytelegrambotapi
- https://towardsdatascience.com/bring-your-telegram-chatbot-to-the-next-level-c771ec7d31e4
- [Testing Wiki](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Writing-Tests)
- [Telegram Bot Testing Suite](https://github.com/python-telegram-bot/ptbtest)
- [Telegram Bot Testing Suite RTD](https://ptbtestsuite.readthedocs.io/en/master/?badge=master)
- https://core.telegram.org/bots/api
