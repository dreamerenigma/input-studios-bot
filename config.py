from decouple import config

ADMIN_ID = config("ADMIN_ID")
BOT_TOKEN = config("BOT_TOKEN")
VK_TOKEN = config("VK_TOKEN")
HOST = config("HOST")
PORT = int(config("PORT"))
BASE_URL = config("BASE_URL")
WEBHOOK_PATH = f'/{BOT_TOKEN}'
ENVIRONMENT = config("ENVIRONMENT", "development")
USE_WEBHOOK = config("USE_WEBHOOK", cast=bool, default=False)

if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN is not set in the environment variables.")
if VK_TOKEN is None:
    raise ValueError("VK_TOKEN is not set in the environment variables.")
