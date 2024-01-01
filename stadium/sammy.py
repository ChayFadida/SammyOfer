from typing import Union
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class SammyOferApi:
    def __init__(self):
        self.base_url = 'https://www.haifa-stadium.com'
        self.games = []
        self.info_per_event = 3
        self.page = requests.get(f"{self.base_url}/schedule_of_matches_in_the_stadium/")
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.divs = self.soup.find_all('div', class_="elementor-text-editor elementor-clearfix")
        self.divs = self.divs[2:]
        self.divs = [item.findNext('p').text for item in self.divs if item.findNext('p') is not None and hasattr(item.findNext('p'), 'text')]
        if len(self.divs) % self.info_per_event != 0:
            raise ValueError(f'events does not divide by {self.info_per_event}!')
        self.current_year = datetime.now().year
        self.scrape()
 
    def _get_actual_date(self, date_time):
        format_strings = ['%d/%m/%Y %H:%M', '%d/%m %H:%M', '%d/%m', '%d/%m/%y %H:%M', '%d/%m/%y %H:%M']
 
        for format_string in format_strings:
            try:
                date = datetime.strptime(date_time, format_string)
                if 'y' not in format_string.lower():
                    date = date.replace(year=self.current_year)
                    if date < datetime.now():
                        date = date.replace(year=self.current_year + 1)
                return date
            except ValueError:
                pass
 
        raise ValueError(f"The provided date '{date_time}' does not match any of the expected formats: {', '.join(format_strings)}")



    def scrape(self):
        split_events = [self.divs[i:i + self.info_per_event] for i in range(0, len(self.divs), self.info_per_event)]
        for event in split_events:
            team1, date_time, team2 = event
            date = self._get_actual_date(date_time)
            self.games.append({
                'team1': team1,
                'team2': team2,
                'date': date
            })
 
    def get_all_games(self):
        return self.games
    
    def print_all_games(self):
        print("Upcoming Games:")
        print("---------------")
        for game in self.games:
            team1 = game['team1']
            team2 = game['team2']
            date = game['date']
            print(f"{team1} vs {team2} on {date}")
        print("---------------")
 
    def get_game_on_date(self, wanted_date: datetime) -> Union[dict, None]:
        for game in self.games:
            if game.get('date').date() == wanted_date.date():
                return game
        return None
 
    def get_today_game(self):
        today = datetime.today()
        return self.get_game_on_date(today)
 

if __name__ == "__main__":
    api = SammyOferApi()
    api.print_all_games()
    game = api.get_today_game()
    if game is None:
        print('no game today!')
        exit(0)
    else:
        print(f'played today: {game}')
