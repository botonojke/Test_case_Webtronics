from starlette.config import Config


config = Config(".env")
DATABASE_URL = config('EE_DATABASE_URL', cast=str)
WEB_HOST = config('WEB_HOST', cast=str)
WEB_PORT = config('WEB_PORT', cast=str)
