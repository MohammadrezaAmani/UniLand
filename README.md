<p align="center">
    <a>
        <img src="./assets/bot_logo.png" alt="UniLand" width="256">
    </a>
    <br>
    <b>Highly Modular and Diverse Telegram Bot</b>
    <br>
    <a href="https://t.me/UniLandbot">
        Bot
    </a>
    •
    <a href="">
        Documentation
    </a>
    •
    <a href="https://t.me/UniLand_AUT">
        Channel
    </a>
    •
    <a href="https://t.me/UniLandSupport">
        Support
    </a>
</p>

<br>

# UniLand Telegram Bot
> *An instance of this bot is active at [UniLand Telegram Bot](https://t.me/UniLandbot "UniLand Bot")*  

A highly modular and diverse Telegram Bot for universities and institutions written in python. This is the effort of a group of eight CS students at [AUT](https://math.aut.ac.ir/index.php?sid=7&slc_lang=en "Amirkabir University of Technology") as the final project for Software Engineering Course *(1380044)*.




## <a name='Contents'></a>Contents
<!-- vscode-markdown-toc -->
* [Contents](#Contents)
* [Requirements](#Requirements)
	* [Python Compatibility](#PythonCompatibility)
	* [Dependencies](#Dependencies)
* [Instructions](#Instructions)
* [Key Features](#KeyFeatures)
* [License](#License)

<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->


## <a name='Requirements'></a>Requirements
### <a name='Python-Compatibility'></a>**Python Compatibility**
This bot is written entirely in python. tested versions are `python 3.8, 3.7` while older versions should not cause any problem, we recommend using the latest version of `python3`.

### <a name='Dependencies'></a>**Dependencies**
This package requires the following packages:
* [pyrogram](https://github.com/pyrogram/pyrogram "Pyrogram Github") - Telegram MTProto API
* [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy "SQLAlchemy Github") - SQL & ORM Toolkit
* [uvloop](https://github.com/MagicStack/uvloop "uvloop Github") - Asynchronus Programming
* [TgCrypto](https://github.com/pyrogram/tgcrypto "TgCrypto Github") - Secure Encryption for Telegram Protocols

## <a name='Instructions'></a>Instructions
To run the bot, you need to have a Telegram API ID and API Hash. You can get them from [my.telegram.org](https://my.telegram.org "Telegram API"). Then, you need to create a `config.py` file in the root directory of the project and fill it with the following information:

```python
     API_ID = # Your API ID
     API_HASH = # Your API Hash
     BOT_TOKEN = # Your Bot Token
     REPL_URL = # Your Replit URL
```
> *We recommend using a [Repl](https://replit.com/ "Replit") to host the bot but if you have your own server, replace `REPL_URL` with its URL.*  

Then, you can run the bot using the following command:

```bash
    python3 -m uniland
```

## <a name='Key-Features'></a>Key Features
Some of the key feature are listed below. For more information, please refer to the Documentation.
* **Modular** - Highly modular and can be easily extended.
* **Easy to Use** - Easy to customize the interface and messages.
* **Diverse** - Can be used for a wide range of purposes.
* **Secure** - Uses the latest encryption protocols matched by Telegram's MTProto.
* **Fast** - Build with the fastest performing asynchronus libraries to achieve high performance.

## <a name='License'></a>License
Distributed under the MIT License. See `LICENSE` for more information.
