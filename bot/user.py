from bot.db import select_actions
from bot.db import dml_actions


class User:
    def __init__(self, user_id, tg_id):
        self.user_id = None
        self.tg_id = None
        self.message_format = None
        self.exclude_banks = None
        self.exclude_methods = None
        self.uncertainty = None

        self.refresh_args(user_id, tg_id)

    def check(self):
        if self.tg_id is None \
                or self.message_format is None \
                or self.uncertainty is None:
            return False
        return True

    def refresh_args(self, user_id, tg_id):
        user_info = select_actions.get_user_info(user_id, tg_id)

        if user_info is not None:
            tmp_exclude_banks = user_info["exclude_banks"]
            if tmp_exclude_banks is None:
                tmp_exclude_banks = []
            else:
                tmp_exclude_banks = tmp_exclude_banks.split(",")

            tmp_exclude_methods = user_info["exclude_methods"]
            if tmp_exclude_methods is None:
                tmp_exclude_methods = []
            else:
                tmp_exclude_methods = tmp_exclude_methods.split(",")

            self.user_id = user_info["user_id"]
            self.tg_id = user_info["tg_id"]
            self.message_format = user_info["message_format"]
            self.exclude_banks = tmp_exclude_banks
            self.exclude_methods = tmp_exclude_methods
            self.uncertainty = user_info["uncertainty"]

    def refresh(self):
        self.refresh_args(self.user_id, self.tg_id)

    def update_user_info(self, tg_id=None, message_format=None, exclude_banks=None, exclude_methods=None,
                         uncertainty=None):
        dml_actions.update_user_info(self.user_id, tg_id=tg_id, message_format=message_format,
                                     exclude_banks=exclude_banks, exclude_methods=exclude_methods,
                                     uncertainty=uncertainty)
        self.refresh()
