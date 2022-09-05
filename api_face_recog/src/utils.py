import base64

def base64_decode(data):
    format, imgstr = data.split(';base64,')
    return imgstr.decode('base64')


def base64_encode(data):
    if data:
        return 'data:image/png;base64,' + data

