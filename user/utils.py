# -*- coding: utf-8 -*-
# @Time    : 2018/3/6 15:39
# @Author  : 陈强
# @FileName: utils.py
# @Software: PyCharm

from PIL import Image,ImageOps
from io import BytesIO
from itsdangerous import URLSafeTimedSerializer as utsr
import base64
from django.core.files.uploadedfile import SimpleUploadedFile

IMAGE_LARGE = 144
IMAGE_MEDIUM = 96
IMAGE_SMALL = 48
NUM_PER_PAGE = 20


def _thumbnail(upload, size, fmt):
    img = ImageOps.fit(upload, size, Image.ANTIALIAS)

    temp = BytesIO()
    img.save(temp, fmt, quality=95)
    temp.seek(0)

    return temp


def create_thumbnail(src, new_name, ext):
    upload = Image.open(BytesIO(src.read()))
    fmt = src.content_type.split('/')[-1]

    large = _thumbnail(upload, (IMAGE_LARGE, IMAGE_LARGE), fmt)
    filename_l = "%s_l.%s" % (new_name, ext)
    large_file = SimpleUploadedFile(filename_l, large.read(), content_type=src.content_type)

    # medium = _thumbnail(upload, (IMAGE_MEDIUM, IMAGE_MEDIUM), fmt)
    # filename_m = "%s_m.%s" % (new_name, ext)
    # medium_file = SimpleUploadedFile(filename_m, medium.read(), content_type=src.content_type)
    #
    # small = _thumbnail(upload, (IMAGE_SMALL, IMAGE_SMALL), fmt)
    # filename_s = "%s_s.%s" % (new_name, ext)
    # small_file = SimpleUploadedFile(filename_s, small.read(), content_type=src.content_type)

    return large_file





class Token():
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodebytes(security_key.encode()).decode()

    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token,
                                salt=self.salt,
                                max_age=expiration)

