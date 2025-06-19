import random
import string

def random_email():
    return "user_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8)) + "@mail.ru"

def random_name():
    return "User" + "".join(random.choices(string.ascii_letters, k=5))
