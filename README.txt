Hi, it's our app for playing zavalinka game!


If you want to run it on your own, you should:
    1. Run configure.py (it will create some important folders/files that are in gitignore)
    2. Run 'python manage.py makemigrations zavalinka_game' and 'python manage.py migrate'
    3. Add some words to ZavalinkaWord database table
        (Admin users have button "add words" at home page,
        so they can add upload file with words.
        Also at the root folder of the project (near README),
        there is a file words.txt, which contains some words that you can upload)

Yeah, now you can play!