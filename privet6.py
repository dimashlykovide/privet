import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import ChatJoinRequest, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = "8347558460:AAESWUEjlvVbw2d5HysdXCtEw9BDHFqALYM"
POST_LINK = "https://t.me/c/2645114369/73"  # Ссылка на пост с гайдом

# Пути к изображениям
FIRST_IMAGE_PATH = "gleb_photo.jpg"  # Изображение для первого сообщения (знакомство)
SECOND_IMAGE_PATH = "gleb1.jpg"  # Изображение для второго сообщения (проект)

# Проверяем наличие изображений
if os.path.exists(FIRST_IMAGE_PATH):
    logger.info(f"✅ Изображение для первого сообщения найдено: {FIRST_IMAGE_PATH}")
else:
    logger.warning(f"⚠️ Изображение для первого сообщения не найдено: {FIRST_IMAGE_PATH}")

if os.path.exists(SECOND_IMAGE_PATH):
    logger.info(f"✅ Изображение для второго сообщения найдено: {SECOND_IMAGE_PATH}")
else:
    logger.warning(f"⚠️ Изображение для второго сообщения не найдено: {SECOND_IMAGE_PATH}")

# Инициализация бота с правильными параметрами для aiogram 3.x
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

def create_post_button():
    """Создает кнопку для перехода к посту"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="📖 Читать пост + гайд", 
                url=POST_LINK
            )]
        ]
    )
    return keyboard

async def send_first_message_with_photo(user_id: int, user_first_name: str):
    """Отправка первого сообщения с фото (знакомство) - используем имя пользователя"""
    try:
        # Текст первого сообщения с HTML форматированием
        first_message_text = f"""<b>Привет</b>, {user_first_name}. Давай знакомиться

Меня зовут Глеб. Мне всего 18 лет и в свои годы я уже перепробовал разные способы заработка

От работы в найме и написания отзывов за копейки до реально прибыльной ниши

<blockquote>Если бы не РКО, то я бы никогда не выбрался из ямы шабашек и одноразовых темок</blockquote>

Я знаю какого это не иметь денег в кармане, не видеть перспектив и каждый день просыпаться с мыслью что ненавидишь свою жизнь

И именно поэтому я создал канал BLACKHOLE и знаю как тебе помочь

👇👇👇"""
        
        # Отправляем изображение с подписью, если файл существует
        if os.path.exists(FIRST_IMAGE_PATH):
            try:
                photo = FSInputFile(FIRST_IMAGE_PATH)
                await bot.send_photo(
                    chat_id=user_id,
                    photo=photo,
                    caption=first_message_text
                )
                logger.info(f"📸 Первое сообщение с фото и форматированием отправлено для {user_first_name}")
            except Exception as photo_error:
                logger.error(f"❌ Ошибка отправки первого фото: {photo_error}")
                # Если фото не отправилось, отправляем только текст с форматированием
                await bot.send_message(
                    chat_id=user_id,
                    text=first_message_text
                )
                logger.info(f"📝 Первое сообщение с форматированием без фото отправлено для {user_first_name}")
        else:
            # Если файл не найден, отправляем только текст с форматированием
            await bot.send_message(
                chat_id=user_id,
                text=first_message_text
            )
            logger.info(f"📝 Первое сообщение с форматированием без фото отправлено для {user_first_name}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке первого сообщения: {e}")

async def send_second_message_with_photo(user_id: int, user_first_name: str):
    """Функция для отправки второго сообщения с фото через 5 секунд"""
    await asyncio.sleep(5)  # Ждем 5 секунд
    
    try:
        # Текст второго сообщения
        second_message_text = """<b>BLACKHOLE</b> — это проект посвященный онлайн-заработку

Я не сливаю деньги на крипте и прочей ерунде, а строю систему заработка на сотрудничестве с банками

<blockquote>Речь идёт про РКО и другие финансовые продукты</blockquote>

Сейчас советую тебе ознакомиться с этим постом чтобы войти в курс дела

Там же я подготовил для вас бесплатный ГАЙД в который входит:

<blockquote>- Понятие ниши мотивированного трафика
- С чего лучше всего начать
- Как масштабироваться
</blockquote>
И секретный подарок который ждет тебя после прочтения"""
        
        # Отправляем изображение с подписью, если файл существует
        if os.path.exists(SECOND_IMAGE_PATH):
            try:
                photo = FSInputFile(SECOND_IMAGE_PATH)
                await bot.send_photo(
                    chat_id=user_id,
                    photo=photo,
                    caption=second_message_text,
                    reply_markup=create_post_button()
                )
                logger.info(f"📸 Второе сообщение с фото и кнопкой отправлено для {user_first_name}")
            except Exception as photo_error:
                logger.error(f"❌ Ошибка отправки второго фото: {photo_error}")
                # Если фото не отправилось, отправляем текст с кнопкой
                await bot.send_message(
                    chat_id=user_id,
                    text=second_message_text,
                    reply_markup=create_post_button()
                )
                logger.info(f"📝 Второе сообщение с кнопкой без фото отправлено для {user_first_name}")
        else:
            # Если файл не найден, отправляем только текст с кнопкой
            await bot.send_message(
                chat_id=user_id,
                text=second_message_text,
                reply_markup=create_post_button()
            )
            logger.info(f"📝 Второе сообщение с кнопкой без фото отправлено для {user_first_name}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при отправке второго сообщения: {e}")

@dp.chat_join_request()
async def blackhole_welcome(chat_join: ChatJoinRequest):
    """
    Автоматическое принятие заявки и отправка приветствия
    """
    user = chat_join.from_user
    
    # Используем только имя пользователя (first_name)
    user_name = user.first_name or "Пользователь"
    logger.info(f"Пользователь: {user_name} (ID: {user.id})")
    
    try:
        # Автоматически принимаем заявку
        await chat_join.approve()
        logger.info(f"✅ Заявка принята: {user_name}")
        
        # Отправляем первое сообщение с фото и форматированием
        await send_first_message_with_photo(user.id, user_name)
        
        # Запускаем задачу для отправки второго сообщения с фото через 5 секунд
        asyncio.create_task(send_second_message_with_photo(user.id, user_name))
        
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        
        if "bot was blocked" in str(e).lower():
            logger.warning(f"Пользователь {user_name} заблокировал бота")

# Команда для проверки работы бота
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработка команды /start"""
    await message.answer(
        "👋 Я бот канала BLACKHOLE. Если ты подал заявку на вступление, я автоматически её приму и отправлю информацию."
    )

# Запуск бота
async def main():
    logger.info("=" * 50)
    logger.info("🤖 Бот BLACKHOLE запущен!")
    logger.info("=" * 50)
    logger.info(f"🔗 Ссылка на пост с гайдом: {POST_LINK}")
    logger.info(f"🖼  Первое изображение: {FIRST_IMAGE_PATH}")
    logger.info(f"🖼  Второе изображение: {SECOND_IMAGE_PATH}")
    logger.info("👤 Используется имя пользователя (first_name)")
    logger.info("📨 Первое сообщение: Знакомство + фото + форматирование")
    logger.info("📨 Второе сообщение: Описание проекта BLACKHOLE + фото + кнопка")
    logger.info("⏰ Второе сообщение отправляется через 5 секунд")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())