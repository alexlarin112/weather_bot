__version__ = '1.0'

import logging
import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator
from middleware.apsched_middleware import SchedulerMiddleWare
from aiogram.fsm.storage.redis import RedisStorage

from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers, apsched_handlers
from keyboards.main_menu import set_main_menu


# Инициализируем логгер
logger = logging.getLogger(__name__)
logger2 = logging.getLogger('peewee')
logger2.setLevel(logging.DEBUG)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        filename="py_log.log",
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем хранилище redis
    storage = RedisStorage.from_url('redis://localhost:6379/0')

    # Инициализируем бот и диспетчер, передаем в диспечер хранилище redis
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)

    jobstores = {
        'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                                 run_times_key='dispatched_trips_running',
                                 db=2,
                                 host='localhost',
                                 port=6379)
    }

    # Инициализируем и регистрируем планировщик
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="utc", jobstores=jobstores))
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.start()
    dp.update.middleware.register(SchedulerMiddleWare(scheduler))

    scheduler.print_jobs()

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(apsched_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

