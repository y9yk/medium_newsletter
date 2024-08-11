import os
import gspread
import pandas as pd

from config import settings
from modules.utils import logger


class SeedDataManager(object):
    def __init__(self):
        system_google_service_account_filename = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        if system_google_service_account_filename:
            filename = system_google_service_account_filename
        else:
            filename = f"{settings.GOOGLE_SERVICE_ACCOUNT_FILEPATH}/{settings.GOOGLE_SERVICE_ACCOUNT_FILENAME}"

        with open(filename, "r") as f:
            ret = f.read()
            print(ret)

        import json

        ret = json.loads(ret)
        print(ret)

        #
        self.client = gspread.service_account(filename=filename)

    def get_seed_urls(self):
        worksheet = self.client.open(settings.SEED_FILENAME)
        return worksheet.sheet1.get_all_values()

    def get_reading_list(self):
        worksheet = self.client.open(settings.READING_LIST_FILENAME)
        return [v[0] for v in worksheet.sheet1.get_all_values() if len(v) > 0]

    def get_title_list(self):
        worksheet = self.client.open(settings.TITLE_LIST_FILENAME)
        return [v[0] for v in worksheet.sheet1.get_all_values() if len(v) > 0]

    def record_reading_list(self, feeds):
        worksheet = self.client.open(settings.READING_LIST_FILENAME)

        # merge
        previous_reading_list = worksheet.sheet1.get_all_values()
        df = pd.concat(
            [
                pd.DataFrame(previous_reading_list, dtype=str),
                pd.DataFrame(feeds, dtype=str),
            ]
        )
        df = df.dropna()
        # logger.debug(df.values.tolist())

        # update
        worksheet.sheet1.update(df.values.tolist())

    def record_title_list(self, title):
        worksheet = self.client.open(settings.TITLE_LIST_FILENAME)

        # merge
        previous_title_list = worksheet.sheet1.get_all_values()
        df = pd.concat(
            [
                pd.DataFrame(previous_title_list, dtype=str),
                pd.DataFrame(title, dtype=str),
            ]
        )
        df = df.dropna()
        # logger.debug(df.values.tolist())

        # update
        worksheet.sheet1.update(df.values.tolist())


seed_data_manager = SeedDataManager()


def get_seed_data_manager() -> SeedDataManager:
    return seed_data_manager
