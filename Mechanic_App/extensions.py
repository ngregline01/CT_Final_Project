#extensions.py
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

#the extension you use should be here
ma = Marshmallow()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()