
from stadium.sammy import SammyOferApi
from bots.telegramBot import TelegramBot
from config.config import bot_token, user_id
from deep_translator import GoogleTranslator

class GamesAlert(object):
    def __init__(self, telegram_bot, user_id):
        self.telegram_bot = telegram_bot
        self.user_id = user_id

    def run(self):
        api = SammyOferApi()

        # Get all games and print them
        all_games = api.get_all_games()
        print("All Games:")
        for game in all_games:
            print(game)

        # Get today's game
        today_game = api.get_today_game()

        if today_game is not None:
            # If there is a game today, send a message
            message = self.format_game_message(today_game)
            self.telegram_bot.send_message(self.user_id, message)

        else:
            print("No game today")
            exit(0)
            
    def translate_to_hebrew(self, text):
        translation = GoogleTranslator(source='en', target='iw').translate(text)
        return translation

    def format_game_message(self, game):
        team1 = self.translate_to_hebrew(game['team1'])
        team2 = self.translate_to_hebrew(game['team2'])
        time = self.translate_to_hebrew(game['date'].strftime("%d.%m.%Y %H:%M"))
        formatted_message = f"שלום חברים! ⚽🔥\n היום {time} יתרחש המשחק: \n\n {team1} VS {team2}"
        return formatted_message

if __name__ == "__main__":
    # Create an instance of the TelegramBot class
    telegram_bot = TelegramBot(bot_token)

    # Create an instance of the GamesAlert class and run the script
    games_alert = GamesAlert(telegram_bot, user_id)
    games_alert.run()
