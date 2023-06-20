from bot.db import select_actions
from bot.db import dml_actions


class User:
    def __init__(self, user_id, tg_id):
        self.user_id = None
        self.tg_id = None
        self.message_format = None
        self.include_banks = None

        self.refresh_args(user_id, tg_id)

    def check(self):
        if self.tg_id is None \
                or self.message_format is None:
            return False
        return True

    def refresh_args(self, user_id, tg_id):
        user_info = select_actions.get_user_info(user_id, tg_id)

        if user_info is not None:
            tmp_include_banks = user_info["include_banks"]
            if tmp_include_banks is None or tmp_include_banks == "":
                tmp_include_banks = []
            else:
                tmp_include_banks = tmp_include_banks.split(",")

            self.user_id = user_info["user_id"]
            self.tg_id = user_info["tg_id"]
            self.message_format = user_info["message_format"]
            self.include_banks = tmp_include_banks

    def refresh(self):
        self.refresh_args(self.user_id, self.tg_id)

    def update_user_info(self, tg_id=None, message_format=None, include_banks=None):
        dml_actions.update_user_info(self.user_id, tg_id=tg_id, message_format=message_format,
                                     include_banks=include_banks)
        self.refresh()
