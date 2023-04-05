# tech_support_bot
![logo.gif](https://dvmn.org/media/lessons/Andi-Animation2_iW1QQio.gif) 

This repository has three scripts, ```tg_speaker_bot.py``` support bot for Telegram, ```vk_speaker_bot.py``` support bot for [VK](https://vk.com), both scripts use
natural language recognition cloud service from Google - Dialogflow. ```bot_training.py``` is a script to load training phrases for Dialogflow from a .json file.

![example.gif](https://dvmn.org/media/filer_public/7a/08/7a087983-bddd-40a3-b927-a43fb0d2f906/demo_tg_bot.gif)

## How to install?

1. Copy the contents of the project to your working directory.

    Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

    ```
    pip install -r requirements.txt
    ```

    Recommended to use [virtualenv/venv](https://docs.python.org/3/library/venv.html) for isolate the project

2. Create a project in [Google](https://cloud.google.com/resource-manager/docs/creating-managing-projects)

3. Create a [Dialogflow agent](https://dialogflow.cloud.google.com/#/getStarted)
4. Create a JSON key:

    ```
    gcloud auth application-default login
    ```
    You will need to follow the link in the console, select an account and then copy the key that appears to the console.
5. Add your Google project to the key:
    ```
    gcloud auth application-default set-quota-project <YOUR_PROJECT>
    ```
6. Added to `.env` file:

   `TG_TOKEN` - Telegram token. You will receive it when registering a bot

   `PROJECT_ID` - ID of your Google project

   `VK_TOKEN` - VK bot token. You can get it in your community settings

   `DIALOGFLOW_TOKEN` - your Google project API Key

   `TELEGRAM_LOGGER_TOKEN` - Logger bot telegram token

   `TG_CHAT_ID` - ID of your chat. 
## Launch.

Launch telegram bot:

```
python3 tg_speaker_bot.py
```

Launch VK bot:
```
python3 vk_speaker_bot.py
```

Launch `bot_training.py`:

Put the practice phrases in the `questions.json` file in the root directory of the project and launch in console:
```commandline
python3 bot_training.py
```

Example `questions.json`:
```
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
    "Забыл пароль": {
        "questions": [
            "Не помню пароль",
            "Не могу войти",
            "Проблемы со входом",
            "Забыл пароль",
            "Забыл логин",
            "Восстановить пароль",
            "Как восстановить пароль",
            "Неправильный логин или пароль",
            "Ошибка входа",
            "Не могу войти в аккаунт"
        ],
        "answer": "Если вы не можете войти на сайт, воспользуйтесь кнопкой «Забыли пароль?» под формой входа. Вам на почту прийдёт письмо с дальнейшими инструкциями. Проверьте папку «Спам», иногда письма попадают в неё."
    }
}
```

