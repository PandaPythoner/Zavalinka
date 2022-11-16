from random import randint
import os

os.makedirs('zavalinka/media/profile_images/', exist_ok=True)
secret_key = ""

for i in range(50):
    secret_key += chr(ord('a') + randint(0, 25))

with open('zavalinka/zavalinka/hidden_settings.py', 'w') as f:
    f.write(f"SECRET_KEY = '{secret_key}'\nDEBUG = True")


