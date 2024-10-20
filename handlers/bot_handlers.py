import asyncio
import vk_api
from config import VK_TOKEN
from database.database import create_tables, add_post_to_db, post_exists_in_db
from filters.filters import bot

vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
last_sent_posts = set()


def get_vk_posts(group_id, count=5):
    """Получает посты из VK группы"""
    posts = vk.wall.get(owner_id=group_id, count=count)
    return posts['items']


async def send_vk_posts(channel_username, group_id):
    """Автоматически отправляет последние посты из VK группы в Telegram канал"""
    try:
        posts = get_vk_posts(group_id)
        channel_name = '@inputstudios'

        telegram_group_link = "https://t.me/inputstudios"

        if posts:
            for post in posts:
                post_id = post['id']
                post_text = post.get('text', 'Без текста')

                attachments = post.get('attachments', [])
                image_url = None

                for attachment in attachments:
                    if attachment['type'] == 'photo':
                        photo_sizes = attachment['photo']['sizes']
                        image_url = max(photo_sizes, key=lambda x: x['height'])['url']
                        break

                subscribe_link = f"\n\n[Подписаться на {channel_name}]({telegram_group_link})✏️"

                full_message = post_text + subscribe_link

                if not post_exists_in_db(post_id) and (post_text.strip() or image_url):
                    if image_url:
                        await bot.send_photo(channel_username, photo=image_url, caption=full_message, parse_mode='Markdown')
                    else:
                        await bot.send_message(channel_username, full_message, parse_mode='Markdown')

                    add_post_to_db(post_id)
        else:
            await bot.send_message(channel_username, "Нет новых постов.")
    except Exception as e:
        await bot.send_message(channel_username, f"Произошла ошибка при получении данных из VK: {e}")


async def periodic_post_fetching(channel_username, group_id):
    """Периодически получает и отправляет посты из VK группы в Telegram канал"""
    while True:
        await send_vk_posts(channel_username, group_id)
        await asyncio.sleep(60)


async def on_startup(dispatcher):
    """Функция, вызываемая при старте бота"""
    create_tables()
    channel_username = '@inputstudios'
    group_id = -222118996
    asyncio.create_task(periodic_post_fetching(channel_username, group_id))
