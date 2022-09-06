import base64
import base64
from django.core.files.base import ContentFile


def base64_file(data, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))


def base64_decode(data):
    format, imgstr = data.split(';base64,')
    return imgstr.decode('base64')


def base64_encode(data):
    if data:
        return 'data:image/png;base64,' + data

