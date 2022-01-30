Инструкция запуска бота.

1. Файл .env.dist переименовать в файл .env и ввести свои данные
2. Заполнение БД вписывать в файл ./utils/db_api/add_to_database.py
3. Создание/изменение БД:
    1) .\utils\db_api\database.py раскомментите строки создания БД
    2) .\utils\db_api\add_to_database.py запустить файл для создания
    3) Закомментить код обратно в подпункте 1)
4. Теперь можно запустить бота =) (запустить файл app.py)

Как добавлять картинки? В файле .\utils\db_api\add_to_database.py есть столбец category_code она также используется для
указания пути к картинке. В столбце photo закидывается только наименование картинки с её расширением. В файле
./handlers/users/menu_handlers.py на строке 67 формируется путь к картинке. Если путь к картинке
./media/test1/test2/test3.jpg, то в файле .\utils\db_api\add_to_database.py столбец category_code="test1/test2", а
столбец photo=test3.jpg

С файлами которыми работаете:

1. ./utils/db_api/add_to_database.py
2. ./utils/db_api/database.py
3. .env

Как будет выполнено задание надо скинуть файл ./utils/db_api/add_to_database.py на GitHub или в ВК