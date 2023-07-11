from random import choice
from string import ascii_letters, digits
from django.conf import settings
from .models import QRCode

SIZE = getattr(settings, "MAXIMUM_URL_CHARS", 7)

AVAIABLE_CHARS = ascii_letters + digits

def create_random_string(chars=AVAIABLE_CHARS):
    return "".join([choice(chars) for _ in range(SIZE)])


def create_shortened_url():
    random_code = create_random_string()

    if QRCode.objects.filter(short_url=random_code).exists():
        # Run the function again
        return create_shortened_url()

    return random_code