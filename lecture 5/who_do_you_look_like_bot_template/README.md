# Who Do You Look Like Telegram Bot

## Настраиваем окружение, в котором будет запускать бота

Запускать бота будет на Unix-like системах (MacOS, Linux). Если у вас Windows, то используйте WSL и следуйте Linux инструкциям. Следующие команды выполняем из командой строки.

### Устанавливаем miniconda3

**Linux**
```bash
$ mkdir -p ~/miniconda3
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
$ bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
$ rm -rf ~/miniconda3/miniconda.sh
$ ~/miniconda3/bin/conda init bash
$ ~/miniconda3/bin/conda init zsh
```

**MacOS**
```bash
$ mkdir -p ~/miniconda3
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda3/miniconda.sh
$ bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
$ rm -rf ~/miniconda3/miniconda.sh
$ ~/miniconda3/bin/conda init bash
$ ~/miniconda3/bin/conda init zsh
```

### Создаем окружение

Запускать бота будем на Python 3.10. Для этого создаем отдельное conda-окружение (env).

```bash
$ env_name=who_do_you_look_like
$ python_version=3.10
$ conda create -y --name ${env_name} python="${python_version}"
```

После этого переходим в созданное изолированное окружение.

```bash
$ conda activate who_do_you_look_like
```

### Настраиваем зависимости

Теперь нужно установить необходимые для нашего бота зависимости (пакеты). Они уже есть в файле `requirements.txt` в корне проекта с ботом. Клонируем репозиторий курса, если еще этого не сделали, и переходим в проект с ботом.

```bash
$(who_do_you_look_like) git clone git@github.com:zhenyanikishkina/who_do_you_look_like.git
$(who_do_you_look_like) cd lecture 5/who_do_you_look_like_bot_template
```

Устанавливаем необходимые зависимости (еще раз убедитесь, что находитесь в созданном ранее окружении).

```bash
$(who_do_you_look_like) pip install -r requirements.txt
```

Готово! Теперь из этого окружения можно запускать бота.

## Структура проекта

Наш проект выглядит следующим образом.

```
who_do_you_look_like/
|   utils/
|   |   database.py
|   |   face_embeddings.py
|   |   search.py
|   bot.py
|   build.py
|   config.py
|   download_dataset.py
|   README.md
|   requirements.txt
```

- `utils/database.py` реализует интерфейсы взаимодействия с [lmdb](https://lmdb.readthedocs.io/en/latest/) базой данных, которая нам будет нужна для хранения картинок и имен для каждой из знаменитостей.
- `utils/face_embeddings.py` реализует функции для получения вектора изображения на основе переданной фотографии лица.
- `utils/search.py` реализует функцию поиска ближайших векторов в faiss индексе.
- `bot.py` реализует основную логику работы нашего бота.
- `build.py` реализует построение faiss индексов и lmdb баз данных отдельно для мужчин и отдельно для женщин.
- `config.py` хранит конфигурацию нашего бота. Сюда же нужно будет вставить token, который вы получили у [BotFather](https://core.telegram.org/bots/tutorial).
- `download_dataset.py` загружает датасет imdb с Kaggle.
- `README.md` cейчас вы здесь.
- `requirements.txt` хранит все необходимые пакеты для работы бота. Его мы уже успели использовать выше для настройки окружения.

## Пишем код

Здесь задача понятна: смотрим на код и заполняем пропущенные части (см. `# YOUR_CODE_HERE`). Как только заработает этот предложенный бот, начинаем брейнштормить новые идеи и добавлять новую функциональность нашему боту. Не бойтесь менять структуру и код проекта. Чем больше поменяете, тем лучше!

## Запускаем бота

Сначала скачиваем датасет с кагла.

```bash
$(who_do_you_look_like) python download_dataset.py
```

После запуска этой команды у вас должна появиться новая директория в проекте с датасетом.

```
who_do_you_look_like/
|   data/
|   |   imdb_crop
|   utils/
|   |   database.py
|   |   face_embeddings.py
|   |   search.py
|   bot.py
|   build.py
|   config.py
|   download_dataset.py
|   README.md
|   requirements.txt
```

Далее строим lmdb базы данных для мужчин и женщин, а также faiss индексы для них же.

```bash
$(who_do_you_look_like) python build.py
```

После этого у вас должны появиться еще несколько новых директорий и бинарных файлов.

```
who_do_you_look_like/
|   data/
|   |   imdb_crop/
|   |   celeb_db_female/
|   |   celeb_db_male/
|   |   faiss_index_female.bin
|   |   faiss_index_male.bin
|   utils/
|   |   database.py
|   |   face_embeddings.py
|   |   search.py
|   bot.py
|   build.py
|   config.py
|   download_dataset.py
|   README.md
|   requirements.txt
```

Все готово, можем запускать бота.

```bash
$(who_do_you_look_like) python bot.py
```

Теперь переходим в телеграмм и дебажим бота.

## [Deploy](https://practicum.yandex.ru/blog/chto-takoe-deploy/#chto-takoe)

Как только вы закончите бота, его нужно будет "развернуть". Для нашего просто проекта это, грубо говоря, означает, сделать так, чтобы при выключении вашего ноутбука, ваш ТГ бот не умирал. Для этого заходите на виртуальную машину по ssh, закидываете на нее ваши исходники и запускаете там следующую команду.

```bash
$(who_do_you_look_like) nohup python bot.py&
```

На виртуальной машине нужно не забыть проделать ту же настройку окружения. Команад [nohup](https://losst.pro/kak-zapustit-protsess-v-fone-linux) запускает ваш процесс (в данном случае интерпретатор питона, который запускает вашего бота) в фоне. Это означет, что при убийсте терминала, из котрого этот процесс был запущен, сам процесс убит не будет. На практике, бот будет работать все время, даже после разрыва вашего ssh подключения.