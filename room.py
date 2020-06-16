from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

import colors
import playa
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

original_deck = playa.original_deck


def remove_blanks(data: list):
    for item in data:
        if item == '':
            data.remove('')
    return data


def string_representation(data: list):
    data = remove_blanks(data)
    return ''.join(f'{str(x)}-' for x in data)


def create_driver():
    return webdriver.Chrome(options=options)


def update(status: int):
    if int(status) == 0:
        return 1
    else:
        return 0


def next_turn(players: list):
    return players[1:] + players[:1]


class room:
    def __init__(self, join=False):
        self.reader = create_driver()
        self.writer = create_driver()

        self.connection = False
        self.reader.get("https://rentry.co/cameo-room/raw")
        self.connection = True
        print("\n- connection established -\n")

        text_element = self.reader.find_element_by_xpath('/html/body/pre').text
        self.data = text_element.split("|")

        self.room_status = None
        self.player_status = None
        self.cards_status = None

        self.current_status = 0
        self.players = None

        self.stack = None
        self.deck = None
        self.all_players = {}

        self.changes_dictionary = {}

        self.cameo_invoked = None
        self.winner = None

        if join:
            self.room_status = self.data[0]
            self.player_status = self.data[1]
            self.cards_status = self.data[2]

            self.current_status = self.room_status.split(",")[0]
            self.players = remove_blanks([*self.room_status.split(",")[1].split("-")])

            self.stack = remove_blanks([*self.cards_status.split(",")[0].split("-")])
            self.deck = remove_blanks([*self.cards_status.split(",")[1].split("-")])

            self.all_players = {}
            self.all_players = self.update_all_players()

            self.count = len(self.players)
            self.refresh_flag = True

    def refresher(self):
        while True:
            if self.refresh_flag:
                time.sleep(1)
                try:
                    self.reader.refresh()
                except exceptions.InvalidSessionIdException:
                    exit()

                text_element = None

                while True:
                    try:
                        text_element = self.reader.find_element_by_xpath('html/body/pre').text
                        break
                    except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException):
                        continue
                    except exceptions.InvalidSessionIdException:
                        exit()

                data = text_element.split("|")

                if self.current_status != data[0].split(",")[0]:
                    self.read_changes(data=data)
            else:
                continue

    def publisher(self, current_status: int, players: list, player_status: str, stack_status: list, deck_status: list):
        self.refresh_flag = False
        self.writer.get("https://rentry.co/cameo-room/edit")

        to_send = f'{str(update(current_status))},{string_representation(players)}|{player_status}|' \
                  f'{string_representation(stack_status)},{string_representation(deck_status)}'

        body = self.writer.find_element_by_xpath('//*[@id="text"]/div/div[5]/div[1]/div/div/div/div[5]/pre/span')
        while True:
            try:
                if body.text != '':
                    body.send_keys(Keys.LEFT_CONTROL + 'a')
                    time.sleep(1)
                    body.send_keys(Keys.DELETE)

            except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException):
                break

        new_body = self.writer.find_element_by_xpath('//*[@id="text"]/div/div[5]/div[1]/div/div/div/div[5]/pre/span')
        new_body.send_keys(to_send)

        edit_code = self.writer.find_element_by_xpath('//*[@id="id_edit_code"]')
        edit_code.send_keys("cameo_room")

        while True:
            try:
                save = self.writer.find_element_by_xpath('//*[@id="submitButton"]')
                save.click()
                break
            except (exceptions.NoSuchElementException, exceptions.StaleElementReferenceException):
                time.sleep(1)
                continue

        time.sleep(1)
        self.refresh_flag = True

    def read_changes(self, data: list):
        self.room_status = data[0]
        self.player_status = data[1]
        self.cards_status = data[2]

        self.current_status = self.room_status.split(",")[0]
        self.players = remove_blanks([*self.room_status.split(",")[1].split("-")])
        self.changes_dictionary.clear()

        for index, player in enumerate(self.players):
            if "_" in player:
                name, line = player.split('_')
                if '[' in line and '\033[' not in line:
                    line = line.replace('[', '\033[')

                    self.changes_dictionary[name] = line
                    self.players[index] = name

                elif '[' not in line and len(line) < 4:
                    self.cameo_invoked = name

        self.stack = remove_blanks([*self.cards_status.split(",")[0].split("-")])
        self.deck = remove_blanks([*self.cards_status.split(",")[1].split("-")])

        self.all_players = self.update_all_players(players_dictionary=self.all_players)

    def kill_me(self):
        self.refresh_flag = False
        self.reader.close()
        self.writer.close()

    def add_player(self, player: playa.playa, deck: list):
        self.players.append(f'{player.name}')
        self.player_status += f'{player.name}-{string_representation(player.cards)},'

        self.all_players[player.name] = player
        self.publisher(current_status=self.current_status, players=self.players, player_status=self.player_status, stack_status=self.stack, deck_status=deck)

    def update_all_players(self, players_dictionary=None):
        if players_dictionary is None:
            players_dictionary = {}

        players = self.player_status.split(",")

        for player in remove_blanks(players):
            player_details = player.split("-")
            player_details = remove_blanks(player_details)

            if player_details[0] in players_dictionary:
                new_player = players_dictionary[str(player_details[0])]
                new_player.update_cards(player_details[1:])

            else:
                new_player = playa.playa(name=player_details[0], cards=player_details[1:])

            players_dictionary[str(player_details[0])] = new_player

        return players_dictionary

    def update_individual_player(self, player: list):
        for user in player:
            self.all_players[user.name] = user
        self.update_player_status()

    def update_player_status(self):
        status_string = ''
        for player in self.all_players.values():
            status_string += f'{player.name}-'
            status_string += string_representation(player.cards)
            status_string += ","

        self.player_status = status_string

    def update_room(self):
        self.players = next_turn(self.players)

        for player_name, player_object in self.all_players.items():
            if player_object.CHANGED:
                if player_object.WHAT != 'Cameo':
                    self.players[self.players.index(player_name)] = f"{player_name}_{player_object.show_cards()}"
                else:
                    self.players[self.players.index(player_name)] = f"{player_name}_{player_object.WHICH}"

        self.publisher(current_status=self.current_status, players=self.players, player_status=self.player_status,
                       stack_status=self.stack, deck_status=self.deck)

    def print_result(self):
        to_print = '\n'
        to_print += "--------------------------------------\n"
        to_print += f"|             {colors.BOLD}THE ROOM{colors.ENDC}               |\n"
        to_print += "--------------------------------------\n"
        to_print += f"->           {colors.blue}RESULTS{colors.ENDC}                <-\n"
        to_print += "--------------------------------------\n"

        for player in self.all_players.values():
            if player == self.winner:
                to_print += f"|->  {colors.green}{colors.BOLD}{player.name} :  {player.WHICH}{colors.ENDC}\n"
            else:
                to_print += f"|->  {player.name} :  {player.WHICH}\n"

        print(to_print)

    def __str__(self):
        changed = []

        if len(self.stack) > 0:
            stack_top = original_deck[int(self.stack[-1])]
        else:
            stack_top = '-'

        to_print = '\n'
        to_print += "--------------------------------------\n"
        to_print += f"|             {colors.BOLD}THE ROOM{colors.ENDC}               |\n"
        to_print += "--------------------------------------\n"
        to_print += f"->           {colors.blue}stack :  {colors.UNDERLINE}{stack_top}{colors.ENDC}           <-\n"
        to_print += "--------------------------------------\n"

        for player in self.all_players.values():
            if player.name in self.changes_dictionary:
                changed.append(player.name)

                if player.name == self.players[0]:
                    to_print += f"|->  {player.name} :  {self.changes_dictionary[player.name]}\n"
                else:
                    to_print += f"|    {player.name} :  {self.changes_dictionary[player.name]}\n"
            else:
                if player.name == self.players[0]:
                    to_print += f"|->  {player.name} :  {player.show_cards()}\n"
                else:
                    if player.name == self.cameo_invoked:
                        to_print += f"|    {colors.yellow}{colors.BOLD}{player.name} :  {player.show_cards()}{colors.ENDC}\n"
                    else:
                        to_print += f"|    {player.name} :  {player.show_cards()}\n"

            player.CHANGED = False
            player.WHAT = None
            player.WHOSE = None
            player.WHICH = None

        to_print += "--------------------------------------\n"
        comment = f"{colors.blue}"

        if self.cameo_invoked == self.players[-1]:
            comment += f"{self.cameo_invoked.upper()} HAS JUST INVOKED {colors.BOLD}CAMEO!{colors.ENDC} {colors.red}BRACE FOR WAR !{colors.ENDC}\n"

        if stack_top[1:] in ['7', '8']:
            if self.players[-1] in self.changes_dictionary and '[4m' in self.changes_dictionary[self.players[-1]]:
                comment += f"{self.players[-1].upper()} just saw their own... card."

        #     elif '[91m' in self.changes_dictionary[self.players[-1]]:
        #         if self.changes_dictionary[self.players[-1]].index('[0m') - self.changes_dictionary[self.players[-1]].index('[91m') > :
        #          comment += f"{self.players[-1].upper()} just tried a {colors.red} BURN !{colors.ENDC}"

        elif stack_top[1:] in ['9', '10']:
            for name, cards in self.changes_dictionary.items():
                if '[4m' in cards:
                    comment += f"{self.players[-1].upper()} just saw {name.upper()}'s... card."

        # elif stack_top[-1] == 'J':
        #     for name, cards in self.changes_dictionary.items():
        #         if '[91m' in cards and name != self.players[-1]:
        #             comment += f"{self.players[-1].upper()} just SHUFFLED {name.upper()}'s cards."

        elif stack_top[-1] in ['J','Q']:
            for name, cards in self.changes_dictionary.items():
                if '[91m' in cards and name != self.players[-1]:
                    comment += f"{self.players[-1].upper()} just swapped one of their own cards with a {name.upper()}'s card."

        elif stack_top[-1] == 'K':
            for name, cards in self.changes_dictionary.items():
                if '[91m' in cards and name != self.players[-1]:
                    comment += f"{self.players[-1].upper()} just looked and swapped one of their own cards with a {name.upper()}'s card."
                elif '[4m' in cards and name != self.players[-1]:
                    comment += f"{self.players[-1].upper()} just looked one of {name.upper()}'s card, but did not swap."

        to_print += f"{comment}{colors.ENDC}"
        self.changes_dictionary.clear()
        return to_print
