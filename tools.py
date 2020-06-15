import room
import playa
import random
import threading
import time
import colors

original_deck = playa.original_deck
power_deck = playa.power_deck
power_dictionary = playa.power_dictionary


def display_cards(player: playa.playa):
    print(f"\n-- Remember your cards : ")
    print(f"{colors.purple}-- 1 : {show_card(player.cards[0])},  2 : {show_card(player.cards[1])}{colors.ENDC}", end='')

    time.sleep(4)
    for i in range(50):
        print('\b', end='')

    print(f"{colors.purple}-- That's all the time you get, kid.{colors.ENDC}")


def shuffle(deck: list):
    new_deck = deck.copy()
    random.shuffle(new_deck)
    return new_deck


def pop_cards(deck: list, count: int):
    cards = []
    for i in range(count):
        cards.append(deck.pop(0))

    return cards, deck


def list_indices(deck: list):
    indices = []

    for card in deck:
        indices.append(original_deck.index(card))

    return indices


def init_game():
    current_deck = shuffle(original_deck)
    # current_deck = shuffle(power_deck)

    my_room = room.room()
    my_room.publisher(current_status=0, players=[''], player_status='', stack_status=[''],
                      deck_status=list_indices(current_deck))

    time.sleep(1)
    refresh = threading.Thread(target=my_room.refresher)
    refresh.start()
    print("- room initialising -\n")
    return join_room(my_room=my_room, through_init=True)


def join_room(my_room=None, through_init=False):
    start = time.time()
    player = input("Enter your name : ")

    if not through_init:
        my_room = room.room(join=True)

        refresh = threading.Thread(target=my_room.refresher)
        refresh.start()

    player_cards, new_deck = pop_cards(deck=my_room.deck, count=5)
    my_player = playa.playa(name=player.lower(), cards=player_cards)

    print("\n- adding you to the ROOM -")
    my_room.add_player(player=my_player, deck=new_deck)

    print(f"JOINED ROOM in : {time.time() - start}s")

    time.sleep(1)
    display_cards(player=my_player)
    return my_room, my_player


def show_card(card):
    if card == '-':
        return '-'
    else:
        return original_deck[int(card)]


def get_other_player(my_room: room.room, name: str):
    return my_room.all_players[name]


def compute_score(my_room: room.room):
    scores_dictionary = {}

    for player in my_room.all_players.values():
        player, score = player_score(player=player)
        scores_dictionary[player] = score
    return scores_dictionary


def player_score(player: playa.playa, indexes: list = None):
    player_sum = 0

    cards = []
    if indexes is not None:
        for index in room.remove_blanks(indexes):
            cards.append(original_deck[int(player.cards[int(index)])])
    else:
        cards = player.cards

    for card in cards:
        card = show_card(card)
        print(card)
        if card == 'HK' or card == 'DK':
            continue
        elif card[-1] in power_dictionary:
            player_sum += power_dictionary[card[-1]]
        else:
            player_sum += int(card[1:])

    return player, player_sum


def execute_burn(my_room: room.room, my_player: playa.playa, indexes: list):
    stack = []

    for index in indexes:
        card = my_player.cards[int(index)]
        stack.append(card)
        my_player.cards_index.remove(int(index))

    for index in range(len(my_player.cards)):
        if index not in my_player.cards_index:
            my_player.cards[int(index)] = '_'

    my_room.stack.extend(sorted(stack, reverse=True))
    print(f"\nAnd that's a {colors.red}BURN !{colors.ENDC}")

    stage_changes(my_room=my_room, player=my_player, what="burn1", whose=my_player.name)


def lol_burn(my_room: room.room, my_player: playa.playa):
    my_player.cards.append(my_room.deck.pop(0))

    if max(my_player.cards_index) > 5:
        my_player.cards_index.append(max(my_player.cards_index) + 1)
    else:
        my_player.cards_index.append(5)

    print(f"\nMISMATCHED !\nInstead of your cards, {colors.red}YOU JUST GOT BURNED.{colors.ENDC} Here's an extra card for your troubles.")
    stage_changes(my_room=my_room, player=my_player, what="burn0", whose=my_player.name)


def stage_changes(my_room: room.room, player: playa.playa, what: str, whose: str, which: str = None):
    other_player = None

    player.CHANGED = True
    player.WHAT = what
    player.WHOSE = whose

    if player.name != whose:
        other_player = get_other_player(my_room=my_room, name=whose)
        other_player.CHANGED = True
        other_player.WHAT = what
        other_player.WHOSE = whose

    if which is not None and ',' in which:
        player.WHICH = which.split(',')[0]
        other_player.WHICH = which.split(',')[1]

    elif which is not None:
        if other_player is not None:
            other_player.WHICH = which
        else:
            player.WHICH = which


def power_function(my_room: room.room):
    new_player_list = my_room.players[-1:] + my_room.players[:-1]
    my_room.players = new_player_list


def invoke_cameo(my_room: room.room, my_player: playa.playa):
    my_room.cameo_invoked = my_player.name
    player, score = player_score(player=my_player)

    my_player.CHANGED = True
    my_player.WHAT = "Cameo"
    my_player.WHICH = score


def execute_cameo(my_room: room.room):
    scores_dictionary = compute_score(my_room=my_room)

    min_score = 100
    winner = None

    for player, score in scores_dictionary.items():
        player.WHICH = score

        if score < min_score:
            min_score = score
            winner = player

    my_room.winner = winner
    my_room.print_result()
    my_room.kill_me()
