# LH Lock Telegram Bot

This project shall control the garage door of LautisHannover. It combines different APIS 
into a shared "core" library. This is used by:API

- A Telegram-BOT, found in the src-bot directory
- A FastAPI backend for the lautis-portal website.

## setup and install packages
- install the package via pyproject toml from the different subdirectories:
```
pip install -e ./src-core
pip install -e ./src-bot
pip install -e ./src-portal
```
- update the config.cfg file in the directory accordingly:
    - add API-Keys for NUKI and TELEGRAM
    - add your telegram chat id to the [auth] section.
    - (adjust logging levels for different python modules)


## running the bot
- when the config.cfg file in the current working directory is configured and src-bot is installed,
a new command should be available to start the bot with
```
python -m lh_bot
```
or
```
lockbot
```
You can use the "-h" flag to show the help page.

## testing the portal backend
``` 
fastapi dev .\src-portal\lh_portal\main.py
```
or 
```
lhportal dev
```
This starts a development server and hosts the documentation.


### development
- install the package with optional dependencies
```
pip install -e .[dev]
```
- you can download some testdata from the API. This will be saved in "tests/data".
```
lhtool testdata
```
- you can run pytest from the main directory. This will run the tests defined within the tests subdirectory.
```
pytest
```


## License

This project is licensed under the MIT License. Feel free to use and modify it for your purposes.

## Contributions

Contributions are welcome! If you'd like to improve the bot or add features, feel free to submit a pull request.

