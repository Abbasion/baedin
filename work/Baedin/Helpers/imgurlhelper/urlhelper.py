import base64
import datetime
import math

from django.forms import model_to_dict
from rest_framework import request

from Baedin import settings
from Baedin.settings import IMG_URL






def img_url(name):
            return  str(IMG_URL)+r"\myGift/uploads\\"+name


def img_url_profile(name):
    return str(IMG_URL) + r"\myGift/uploads\\" + name