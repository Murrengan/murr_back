import base64

from django.core.files.base import ContentFile
from django.db.models import OuterRef
from django.utils.crypto import get_random_string

from murren.models import Murren
from murr_rating.models import Rating


def generate_user_cover(cover):
    if cover:
        img_type, img_str = cover.split('base64,')
        image_extension = img_type.split('/')[-1].split(';')[0]
        img_base64 = base64.b64decode(img_str)
        cover = ContentFile(img_base64)
        cover.name = '.'.join([get_random_string(length=6), image_extension])
        return cover


def get_rating_query() -> tuple:
    """
    Получение queryset's для агрегирующей функции.
    К возвращенным кверисетам будет применина функция Count,
    произведется расчет разницы между лайками и дизлайкими, после чего результат присвоится полю rating объекта.
    """
    rating = Rating.objects.filter(object_id=OuterRef('pk'), object_type='Card').only('pk')
    likes = rating.filter(rating_type='Like')
    dislikes = rating.filter(rating_type='Dislike')
    return likes, dislikes


def rating_handler(murren_id: int, obj_id: int, obj_type: str, rating_type: str) -> None:
    """
    Логика обработки оценки.
    1. Получаем или создаем оценку, если ее нет.
    2. Если оценка есть и ее rating_type равен переданному, то удаляем(отмена оценки).
    В противном случае присваиваем новый вид оценки.
    """
    rating, is_created = Rating.objects.get_or_create(murren_id=murren_id, object_id=obj_id, object_type=obj_type)
    if not is_created and rating.rating_type == rating_type:
        rating.delete()
    else:
        rating.rating_type = rating_type
        rating.save()
