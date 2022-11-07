from aiogram import executor, types, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import bot.common
from bot import bot_reply_markup
from add_rates import add_all_rates
from rate import get_best_convert, format_rates

main_command_dict = dict(#rate='Получить курсы',
                         convert='Получить способы конвертации',
                         help='Помощь с командами')


async def handle_start(message: types.Message, state: FSMContext):
    await state.finish()
    await handle_welcome(message, state)


async def handle_welcome(message: types.Message, state: FSMContext):
    msg = "Привет!\n" \
          + "Я бот, который подскажет лучшие способы обмена валюты в Армении!\n"
    await bot.common.send_message(message.from_user.id, msg, reply_markup=bot_reply_markup.dict_menu(main_command_dict))


async def handle_rate(message: types.Message, state: FSMContext):
    all_rates = add_all_rates()
    for rate in all_rates:
        await bot.common.send_message(message.from_user.id, rate, reply_markup=bot_reply_markup.dict_menu(main_command_dict))


async def handle_convert(message: types.Message, state: FSMContext):
    all_rates = add_all_rates()
    msg = get_best_convert(all_rates, "rur", "cash", "eur", "cash", allow_uncertainty=0.003, print_=False)
    await bot.common.send_message(message.from_user.id, msg,
                                  reply_markup=bot_reply_markup.dict_menu(main_command_dict))
    msg = get_best_convert(all_rates, "rur", "tinkoff", "eur", "cash", allow_uncertainty=0.003, print_=False)
    await bot.common.send_message(message.from_user.id, msg,
                                  reply_markup=bot_reply_markup.dict_menu(main_command_dict))
    msg = get_best_convert(all_rates, "rur", "tinkoff", "eur", "yunibank", allow_uncertainty=0.003, print_=False)
    await bot.common.send_message(message.from_user.id, msg,
                                  reply_markup=bot_reply_markup.dict_menu(main_command_dict))

    msg = get_best_convert(all_rates, "rur", "cash", "usd", "cash", allow_uncertainty=0.003, print_=False)
    await bot.common.send_message(message.from_user.id, msg,
                                  reply_markup=bot_reply_markup.dict_menu(main_command_dict))
    msg = get_best_convert(all_rates, "rur", "tinkoff", "usd", "cash", allow_uncertainty=0.003, print_=False)
    await bot.common.send_message(message.from_user.id, msg,
                                  reply_markup=bot_reply_markup.dict_menu(main_command_dict))
    msg = get_best_convert(all_rates, "rur", "tinkoff", "usd", "yunibank", allow_uncertainty=0.003, print_=False)
    await bot.common.send_message(message.from_user.id, msg,
                                  reply_markup=bot_reply_markup.dict_menu(main_command_dict))

    msg = get_best_convert(all_rates, "rur", "cash", "amd", "cash", allow_uncertainty=0.003, print_=False)
    await bot.common.send_message(message.from_user.id, msg,
                                  reply_markup=bot_reply_markup.dict_menu(main_command_dict))
    msg = get_best_convert(all_rates, "rur", "tinkoff", "amd", "cash", allow_uncertainty=0.003, print_=False)
    await bot.common.send_message(message.from_user.id, msg,
                                  reply_markup=bot_reply_markup.dict_menu(main_command_dict))
    msg = get_best_convert(all_rates, "rur", "tinkoff", "amd", "yunibank", allow_uncertainty=0.003, print_=False)
    await bot.common.send_message(message.from_user.id, msg,
                                  reply_markup=bot_reply_markup.dict_menu(main_command_dict))


def register_handlers_main():
    bot.common.dp.register_message_handler(handle_start, commands=['start', 'help'], state='*')
    # bot.common.dp.register_message_handler(handle_rate, text=['/rate', main_command_dict['rate']])
    bot.common.dp.register_message_handler(handle_convert, text=['/convert', main_command_dict['convert']])
    bot.common.dp.register_message_handler(handle_welcome)


register_handlers_main()
executor.start_polling(bot.common.dp, skip_updates=False)
