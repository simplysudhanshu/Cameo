import random
import time
import colors

original_deck = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'HJ', 'HQ', 'HK',
                 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'DJ', 'DQ', 'DK',
                 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'CJ', 'CQ', 'CK',
                 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'SJ', 'SQ', 'SK']                         # 12, 25, 38, 51

# power_deck = ['H7', 'H8', 'H9', 'H10', 'HJ', 'HQ', 'HK',
#               'D7', 'D8', 'D9', 'D10', 'DJ', 'DQ', 'DK',
#               'C7', 'C8', 'C9', 'C10', 'CJ', 'CQ', 'CK',
#               'S7', 'S8', 'S9', 'S10', 'SJ', 'SQ', 'SK']

power_deck = ['H10', 'HJ', 'HQ', 'HK', 'D10', 'DJ', 'DQ', 'DK',
              'C10', 'CJ', 'CQ', 'CK', 'S10', 'SJ', 'SQ', 'SK']

power_dictionary = {'J': 11, 'Q': 12, 'K': 13}


class playa:
    def __init__(self, name: str, cards: list):
        self.name = name
        self.cards = cards
        self.cards_index = [self.cards.index(x) for x in self.cards]

        self.CHANGED = False
        self.WHAT = None
        self.WHOSE = None
        self.WHICH = None

    def swap(self, card, index: int):
        original = self.cards[index]
        self.cards[index] = card
        return original

    def look(self, index: int):
        print(f"\n{colors.purple}->{self.name.upper()}'s CARD {index} : {original_deck[int(self.cards[index])]}{colors.ENDC}", end='')
        time.sleep(4)
        for i in range(20):
            print('\b', end='')

        print(f"{colors.purple}That's all the time you get, kid.{colors.ENDC}")

    def shuffle(self):
        random.shuffle(self.cards)

    def update_cards(self, cards: list):
        self.cards = cards
        new_indexes = []

        for index, card in enumerate(cards):
            if card != '_':
                new_indexes.append(index)
        self.cards_index = new_indexes

    def show_cards(self):
        to_print = ''

        if self.CHANGED:
            if 'burn' in self.WHAT or 'shuffle' in self.WHAT:
                if self.WHOSE == self.name:
                    to_print = to_print.join(f'{str(x)} ' for x in self.cards_index)
                    to_print = f'{colors.red}{to_print}{colors.ENDC}'
                else:
                    to_print = to_print.join(f'{str(x)} ' for x in self.cards_index)

            elif 'cameo' in self.WHAT:
                to_print = to_print.join(f'{str(x)} ' for x in self.cards_index)
                to_print = f'{colors.red}{colors.BOLD}{to_print}{colors.ENDC}'

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
