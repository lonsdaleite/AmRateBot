import re
from aiogram import executor
import bot.common
from add_rates import add_all_rates
from bot import update_rates, user_state
from bot.db import sql_init
from bot.handlers.base import handle_start, handle_welcome, handle_action_user_accept, handle_cancel, main_command_dict
from bot.handlers.convert import handle_convert, callback_update_convert, \
    callback_update_from_currency, callback_update_to_currency, callback_update_from_union_type, \
    callback_update_to_union_type, handle_convert_all
from bot.handlers.settings import handle_settings, handle_set_message_format, handle_action_set_message_format, \
    settings_dict, handle_set_uncertainty, handle_action_set_uncertainty


def register_handlers_main():
    add_all_rates(bot.common.all_rates)
    bot.common.dp.register_message_handler(handle_start, commands=['start', 'help'], state='*')
    bot.common.dp.register_message_handler(handle_cancel,
                                           text=['/cancel', 'Отмена', 'Главное меню'],
                                           state='*')
    bot.common.dp.register_message_handler(handle_action_user_accept, state=user_state.InitialState.waiting_for_accept)
    bot.common.dp.register_message_handler(handle_set_message_format, text=['/message_format',
                                                                            settings_dict['message_format']],
                                           state=[user_state.InitialState.waiting_for_settings])
    bot.common.dp.register_message_handler(handle_action_set_message_format,
                                           state=[user_state.InitialState.waiting_for_set_message_format])
    bot.common.dp.register_message_handler(handle_set_uncertainty, text=['/uncertainty',
                                                                         settings_dict['uncertainty']],
                                           state=[user_state.InitialState.waiting_for_settings])
    bot.common.dp.register_message_handler(handle_action_set_uncertainty,
                                           state=[user_state.InitialState.waiting_for_set_uncertainty])

    bot.common.dp.register_message_handler(handle_settings, text=['/settings', main_command_dict['settings']])
    bot.common.dp.register_message_handler(handle_convert_all, text=['/convert_all'])  # Hidden method
    bot.common.dp.register_message_handler(handle_convert, text=['/convert', main_command_dict['convert']])
    bot.common.dp.register_message_handler(handle_welcome)

    bot.common.dp.register_callback_query_handler(callback_update_convert, regexp=re.compile(r"update.*"))
    bot.common.dp.register_callback_query_handler(callback_update_from_currency,
                                                  regexp=re.compile(r"from_currency.*"))
    bot.common.dp.register_callback_query_handler(callback_update_to_currency,
                                                  regexp=re.compile(r"to_currency.*"))
    bot.common.dp.register_callback_query_handler(callback_update_from_union_type,
                                                  regexp=re.compile(r"from_union_type.*"))
    bot.common.dp.register_callback_query_handler(callback_update_to_union_type,
                                                  regexp=re.compile(r"to_union_type.*"))


sql_init.run_scripts()

register_handlers_main()
executor.start_polling(bot.common.dp, skip_updates=False, on_startup=update_rates.run)
