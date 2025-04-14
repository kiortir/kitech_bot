import asyncio
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, URLInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from client import TheCatApiKeyAuth, CatApiClient
from storage import FsUserStorage
from config import Config


config = Config()  # type: ignore
storage = FsUserStorage(path=config.storage_file_path)

client_auth = TheCatApiKeyAuth(
    api_key=config.the_cat_api_key.get_secret_value()
)


@asynccontextmanager
async def get_cat_api_client():
    global client_auth
    client = CatApiClient(auth=client_auth)
    yield client
    await client.aclose()


dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    response = """
    Привет! Для того, чтобы получить фото китеков - используй /cats.\nПотом можно приделать кнопки и фильтры про породам, но уже спать пора)
    """
    await message.answer(response)


@dp.message(F.text, Command(commands="cats"))
async def echo_handler(message: Message) -> None:
    global storage
    if not message.from_user or not storage.is_authorized(
        message.from_user.id
    ):
        await message.answer("Вы не Соня(")

    await message.answer("Так, ща")

    async with get_cat_api_client() as client:
        images = await client.get_images()

    media_group_builder = MediaGroupBuilder()
    for image in images:
        file = URLInputFile(image.url)
        media_group_builder.add_photo(media=file)

    media_group = media_group_builder.build()
    await message.answer_media_group(media=media_group)


async def main() -> None:
    global config, dp
    bot = Bot(
        token=config.bot_api_key.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
