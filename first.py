import settings

def first_key():
    from random import randint
    return randint(1000000000,9999999999999) * randint(10,99)
try:
    print(settings.key)
except AttributeError:
    with open('settings.py','a') as file:
        file.write(f"key = {first_key()}")
