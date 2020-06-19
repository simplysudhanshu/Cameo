import time
import colors

original_deck = ['\u2665 A', '\u2665 2', '\u2665 3', '\u2665 4', '\u2665 5', '\u2665 6', '\u2665 7', '\u2665 8', '\u2665 9', '\u2665 10', '\u2665 J', '\u2665 Q', '\u2665 K',
                 '\u2666 A', '\u2666 2', '\u2666 3', '\u2666 4', '\u2666 5', '\u2666 6', '\u2666 7', '\u2666 8', '\u2666 9', '\u2666 10', '\u2666 J', '\u2666 Q', '\u2666 K',
                 '\u2663 A', '\u2663 2', '\u2663 3', '\u2663 4', '\u2663 5', '\u2663 6', '\u2663 7', '\u2663 8', '\u2663 9', '\u2663 10', '\u2663 J', '\u2663 Q', '\u2663 K',
                 '\u2660 A', '\u2660 2', '\u2660 3', '\u2660 4', '\u2660 5', '\u2660 6', '\u2660 7', '\u2660 8', '\u2660 9', '\u2660 10', '\u2660 J', '\u2660 Q', '\u2660 K']
# KINGS: 12, 25, 38, 51

power_deck = ['\u2665 7', '\u2665 8', '\u2665 9', '\u2665 10', '\u2665 J', '\u2665 Q', '\u2665 K',
              '\u2666 7', '\u2666 8', '\u2666 9', '\u2666 10', '\u2666 J', '\u2666 Q', '\u2666 K',
              '\u2663 7', '\u2663 8', '\u2663 9', '\u2663 10', '\u2663 J', '\u2663 Q', '\u2663 K',
              '\u2660 7', '\u2660 8', '\u2660 9', '\u2660 10', '\u2660 J', '\u2660 Q', '\u2660 K']

power_dictionary = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}


class playa:
    def __init__(self, name: str, cards: list):
        self.name = name
        self.cards = cards
        self.cards_index = [self.cards.index(x)+1 for x in self.cards]

        self.CHANGED = False
        self.WHAT = None
        self.WHOSE = None
        self.WHICH = None

    def swap(self, card, index: int):
        original = self.cards[index]
        self.cards[index] = card
        return original

    def look(self, index: int):
        print(f"\n{colors.purple}-> {self.name.upper()}'s CARD {index+1} : {original_deck[int(self.cards[index])]}{colors.ENDC}", end='')
        time.sleep(4)
        for i in range(30):
            print('\b', end='')

        print(f"{colors.purple}That's all the time you get, kid.{colors.ENDC}")

    def update_cards(self, cards: list):
        self.cards = cards
        new_indexes = []

        for index, card in enumerate(cards):
            if card != '_':
                new_indexes.append(index+1)
        self.cards_index = new_indexes

    def results(self):
        return ''.join(f'{original_deck[int(x)]}, ' for x in self.cards)[:-2]

    def show_cards(self):
        to_print = ''

        if self.CHANGED:
            if 'burn' in self.WHAT:
                to_print = to_print.join(f'{str(x)} ' for x in self.cards_index)
                to_print = f'{colors.yellow}{to_print}{colors.ENDC}'

            elif 'Cameo' in self.WHAT:
                to_print = to_print.join(f'{str(x)} ' for x in self.cards_index)
                to_print = f'{colors.yellow}{colors.BOLD}{to_print}{colors.ENDC}'

            else:
                for index in self.cards_index:
                    if self.WHICH is not None and index == int(self.WHICH):

                        if "looked" in self.WHAT and "swapped" in self.WHAT:
                            to_print += f'{colors.UNDERLINE}{colors.red}{str(index)}{colors.ENDC} '

                        elif "swap" in self.WHAT:
                            to_print += f'{colors.red}{str(index)}{colors.ENDC} '

                        elif "looked" in self.WHAT:
                            to_print += f'{colors.UNDERLINE}{str(index)}{colors.ENDC} '
                    else:
                        to_print += f"{index} "

        else:
            to_print = to_print.join(f'{str(x)} ' for x in self.cards_index)
        return to_print
