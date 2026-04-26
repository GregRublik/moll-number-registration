Создайте файл ``.env`` заполните по подобию `.env.example`
- где `RECAPTCHA_CALLBACK_URL` это ваш `url/callback` (url сервера, где запущено это приложение)

Также необходимо создать файл `rucaptcha.txt` и положить в него `jwt` со страницы: https://rucaptcha.com/setting/pingback 
И установить на этой же странице `url` вашего приложения куда будет приходить ваш callback

В корневой папке проекта выполните `uv sync` (если его нет на пк то установите https://docs.astral.sh/uv/getting-started/installation/ )

Активируйте виртуальное окружение (если оно не активировалось после uv sync): 
- windows: `.\venv\Scripts\activate`
- mac\linux: `source venv/bin/activate`

Запустите скрипт: `python src/main.py`


После запуска вам будет доступно api на {host}:{port} где можно выполнить метод: /get_number/{inn}


