import random,string


ALPHABET = string.ascii_letters + string.digits

def generate_short_code(length = 6):
    return "".join(random.choices(ALPHABET,k=length))


