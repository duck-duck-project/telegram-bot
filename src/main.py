import asyncio
import pathlib
from functools import partial

import cloudinary
import httpx
import humanize
import sentry_sdk
import structlog
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from structlog.stdlib import BoundLogger

import handlers
from config import (
    load_config_from_file_path, load_commands_from_file,
    load_role_play_actions_from_file,
)
from logger import setup_logging
from middlewares import (
    HTTPClientFactoryMiddleware,
    APIRepositoriesInitializerMiddleware,
    user_retrieve_middleware,
)
from repositories import (
    UserRepository,
    ContactRepository,
    SecretMediaRepository,
    SecretMessageRepository,
    TeamMemberRepository,
    TeamRepository,
    BalanceRepository,
    FoodMenuRepository,
    ManasIdRepository,
)
from repositories.themes import ThemeRepository
from services import BalanceNotifier, AnonymousMessageSender
from services.role_play_actions import RolePlayActions

logger: BoundLogger = structlog.get_logger('app')


def include_routers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        handlers.probability.router,
        handlers.anti_how_your_bot.router,
        handlers.anti_media.router,
        handlers.balance.router,
        handlers.birthdays.router,
        handlers.work.router,
        handlers.cats.router,
        handlers.casino.router,
        handlers.choice.router,
        handlers.cinematica.router,
        handlers.dogs.router,
        handlers.food_menu.router,
        handlers.server.router,
        handlers.users.router,
        handlers.manas_id.router,
        handlers.obis.router,
        handlers.teams.router,
        handlers.team_members.router,
        handlers.themes.router,
        handlers.transfers.router,
        handlers.role_play.router,
        handlers.secret_messages.router,
        handlers.secret_medias.router,
        handlers.contacts.router,
        handlers.anonymous_messages.router,
        handlers.common.router,
    )


async def main() -> None:
    humanize.i18n.activate('ru_RU')

    config_file_path = pathlib.Path(__file__).parent.parent / 'config.toml'
    config = load_config_from_file_path(config_file_path)

    commands_file_path = pathlib.Path(__file__).parent.parent / 'commands.json'
    commands = load_commands_from_file(commands_file_path)

    role_play_actions_file_path = (
            pathlib.Path(__file__).parent.parent / 'role_play_actions.json'
    )
    role_play_actions = load_role_play_actions_from_file(
        file_path=role_play_actions_file_path,
    )

    setup_logging(config.logging.level)

    cloudinary.config(
        cloud_name=config.cloudinary.cloud_name,
        api_key=config.cloudinary.api_key,
        api_secret=config.cloudinary.api_secret,
    )

    redis = Redis(
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db,
    )
    storage = RedisStorage(redis)

    bot = Bot(token=config.telegram_bot_token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher(storage=storage)

    bot_user = await bot.me()

    await bot.set_my_commands(commands)

    balance_notifier = BalanceNotifier(bot)

    dispatcher['anonymous_message_sender'] = AnonymousMessageSender(bot)
    dispatcher['bot_user'] = bot_user
    dispatcher['closing_http_client_factory'] = partial(
        httpx.AsyncClient,
        base_url=config.server_api_base_url,
        timeout=60,
    )
    dispatcher['chat_id_for_retranslation'] = config.main_chat_id
    dispatcher['timezone'] = config.timezone
    dispatcher['balance_notifier'] = balance_notifier
    dispatcher['role_play_actions'] = RolePlayActions(role_play_actions)

    include_routers(dispatcher)

    dispatcher.update.outer_middleware(HTTPClientFactoryMiddleware(
        dispatcher['closing_http_client_factory'],
    ))
    dispatcher.update.outer_middleware(
        APIRepositoriesInitializerMiddleware(
            contact_repository=ContactRepository,
            secret_media_repository=SecretMediaRepository,
            secret_message_repository=SecretMessageRepository,
            team_member_repository=TeamMemberRepository,
            team_repository=TeamRepository,
            theme_repository=ThemeRepository,
            user_repository=UserRepository,
            balance_repository=BalanceRepository,
            food_menu_repository=FoodMenuRepository,
            manas_id_repository=ManasIdRepository,
        )
    )
    dispatcher.update.outer_middleware(user_retrieve_middleware)

    if config.sentry.is_enabled:
        sentry_sdk.init(
            dsn=config.sentry.dsn,
            traces_sample_rate=config.sentry.traces_sample_rate,
        )
        logger.info('Sentry enabled')

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
