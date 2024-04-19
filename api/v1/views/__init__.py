#!/usr/bin/python3
"""Init"""
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import to avoid circular import errors
from api.v1.views.index import *
from .states import *
from .cities import *
from .amenities import *
from .users import *
from .places import *
from .reviews import *