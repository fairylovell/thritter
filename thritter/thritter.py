from twikit import Client
from threads_api.src.threads_api import ThreadsAPI
import json

class Thritter:
    def __init__(self):
        self.client = Client()
        self.config = dict()
        self.tracked_twitter_accounts = dict()
        self.latest_tweets = dict()
        self.ids = dict()

    async def load_config(self):
        with open("config.json") as f:
            json_data = json.load(f)

            self.client.login(
                auth_info_1=json_data["twitter_credentials"]["username"],
                auth_info_2=json_data["twitter_credentials"]["email"],
                password=json_data["twitter_credentials"]["password"]
            )

            for threads_account in json_data["bot_settings"]:
                api = ThreadsAPI()
                token_path = "." + threads_account["threads_credentials"]["username"] + ".token"
                result = await api.login(
                    threads_account["threads_credentials"]["username"],
                    threads_account["threads_credentials"]["password"], 
                cached_token_path=token_path)

                if result:
                    print("Login successful")
                else:
                    raise Exception("Login failed")

                self.config[api] = threads_account["tracked_twitter_accounts"]

                for twitter_account in threads_account["tracked_twitter_accounts"]:
                    self.tracked_twitter_accounts.setdefault(twitter_account,[]).append(api)

            for twitter_account in self.tracked_twitter_accounts.keys():
                self.latest_tweets[twitter_account] = None
                self.ids[twitter_account] = self.client.get_user_by_screen_name(twitter_account).id

    async def update(self):
        for tracked_account, apis in self.tracked_twitter_accounts.items():
            tweets = self.client.get_user_tweets(self.ids[tracked_account], 'Tweets')

            if self.latest_tweets[tracked_account] is None or self.latest_tweets[tracked_account].id != tweet[0].id:
                for tweet in tweets:
                    if self.latest_tweets[tracked_account] is None or tweet.id != self.latest_tweets[tracked_account].id:
                        for api in apis:
                            print(tweet.text)

                        continue
                    break

                self.latest_tweets[tracked_account] = tweets[0].id

    async def close_gracefully(self):
        for api in self.config.keys():
            await api.close()

        self.client.close()
