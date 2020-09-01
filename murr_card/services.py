import base64

from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string


def generate_user_cover(cover):
    if cover:
        img_type, img_str = cover.split('base64,')
        image_extension = img_type.split('/')[-1].split(';')[0]
        img_base64 = base64.b64decode(img_str)
        cover = ContentFile(img_base64)
        cover.name = '.'.join([get_random_string(length=6), image_extension])
        return cover