import tools
import time
import colors

in_room = False
my_room = None
my_player = None

print(f"\nSome {colors.UNDERLINE}RULES{colors.ENDC} before we get into it :\n--\n")
time.sleep(1.5)
print(f"1.  Don't rush into anything in life. Join the game {colors.BOLD}ONE PLAYER AT A TIME{colors.ENDC}.\n")
time.sleep(1)
print(f"2.  Be patient in life. You will have to {colors.BOLD}WAIT{colors.ENDC} for the room to be initialised and connected. <Waiting for 30s won't hurt.>")
print("    (It depends on your internet connection and fragility of my code, but mostly your internet.) MEH.\n")
time.sleep(1)
print(f"3.  Understand that you won't be the number 1 always. {colors.BOLD}DO NOT{colors.ENDC} initialise room after it has been initialised once.\n")
time.sleep(1)
print(f"4.  It's the spirit of sportsmanship that drives the world. Don't be an asshole. {colors.BOLD}DON'T CHEAT{colors.ENDC}.\n")
time.sleep(1)
print(f"5.  Don't assume, ask. So ask yourself, do {colors.BOLD}I KNOW THE RULES OF CAMEO ?{colors.ENDC}\n")
time.sleep(1)
print(f"6.  You don't get second chances in life. {colors.BOLD}DON'T MESS UP THE OPTIONS AND SPELLINGS{colors.ENDC}. Whole room will have to be re-initialised.\n")
time.sleep(1)
print(f"7.  Lower the expectations, lesser the hurt. This game might have some {colors.BOLD}BUGS{colors.ENDC} and {colors.BOLD}ERRORS{colors.ENDC}, we'll keep making it better.\n")
time.sleep(1)
print(f"8.  You are an Engineer. Act like one. Make sure you meet all the {colors.BOLD}REQUIREMENTS{colors.ENDC} of the game -> Python with 'Selenium' package.\n")
time.sleep(1)
print(f"9.  Keep your feet on the ground, but touch the sky. Be connected to {colors.BOLD}INTERNET{colors.ENDC}.\n")
time.sleep(1.5)
print("--------------------------------------------------------------------------------------------------------------------")
time.sleep(1.5)


def power_play(top_card):
    if tools.show_card(top_card)[2:] in ['7', '8']:
        my_index = int(input("Enter the index of the card you want to SEE : "))
        my_player.look(index=my_index-1)
        tools.stage_changes(my_room=my_room, player=my_player, what="looked", whose=my_player.name, which=str(my_index))

    elif tools.show_card(top_card)[2:] in ['9', '10']:
        other_index = 0

        while True:
            other_name = input("WHOSE card do you wanna SEE : ").lower()
            if other_name != my_room.cameo_invoked:
                other_index = int(input(f"INDEX of {other_name.upper()}'s card which you wanna see : "))
                break
            else:
                print(f"-> {other_name.upper()} has invoked {colors.red}CAMEO{colors.ENDC}. You can't mess with that player.\n")
                continue

        if other_name == my_player.name:
            print(f"-> You can't see your own card with these powers.\n")

            while True:
                other_name = input("WHOSE card do you wanna SEE : ").lower()
                if other_name == my_player.name:
                    print(f"-> You can't see your own card with these powers.\n")
                    continue
                else:
                    break

        other_player = tools.get_other_player(my_room=my_room, name=other_name)
        other_player.look(index=other_index-1)
        tools.stage_changes(my_room=my_room, player=my_player, what="looked", whose=other_name, which=str(other_index))

    # elif tools.show_card(top_card)[-1] == 'J':
    #     while True:
    #         other_name = input("WHOSE cards do you wanna SHUFFLE : ").lower()
    #         if other_name != my_room.cameo_invoked:
    #             break
    #         else:
    #             print(f"-> {other_name.upper()} has invoked {colors.red}CAMEO{colors.ENDC}. You can't mess with that player.\n")
    #             continue
    #
    #     other_player = tools.get_other_player(my_room=my_room, name=other_name)
    #     other_player.shuffle()
    #
    #     my_room.update_individual_player(player=[other_player])
    #     tools.stage_changes(my_room=my_room, player=my_player, what="shuffled", whose=other_name)

    elif tools.show_card(top_card)[-1] in ['J', 'Q']:
        other_index = 0
        while True:
            other_name = input("WHOSE card do you wanna SWAP with one of yours : ").lower()
            if other_name != my_room.cameo_invoked:
                other_index = int(input(f"INDEX of {other_name.upper()}'s card which you wanna swap : "))
                break
            else:
                print(
                    f"-> {other_name.upper()} has invoked {colors.red}CAMEO{colors.ENDC}. You can't mess with that player.\n")
                continue

        my_index = int(input(f"INDEX of YOUR card which you wanna swap : "))

        other_player = tools.get_other_player(my_room=my_room, name=other_name)

        temp_card = other_player.cards[other_index-1]
        other_player.swap(card=my_player.cards[my_index-1], index=other_index-1)
        my_player.swap(card=temp_card, index=my_index-1)

        my_room.update_individual_player(player=[other_player, my_player])
        tools.stage_changes(my_room=my_room, player=my_player, what="swapped", whose=other_name, which=f"{my_index},{other_index}")

    elif tools.show_card(top_card)[-1] == 'K':
        other_index = 0
        while True:
            other_name = input("WHOSE card do you wanna COMPARE & SWAP with one of yours : ").lower()
            if other_name != my_room.cameo_invoked:
                other_index = int(input(f"INDEX of {other_name}'s card which you wanna swap : "))
                break
            else:
                print(
                    f"-> {other_name.upper()} has invoked {colors.red}CAMEO{colors.ENDC}. You can't mess with that player.\n")
                continue

        my_index = int(input(f"INDEX of YOUR card which you wanna swap : "))

        other_player = tools.get_other_player(my_room=my_room, name=other_name)

        print(f"\n{colors.purple}{other_name.upper()} card {other_index} : {tools.show_card(other_player.cards[other_index-1])}{colors.ENDC}")
        print(f"{colors.purple}YOUR card {my_index} : {tools.show_card(my_player.cards[my_index-1])}{colors.ENDC}")
        swap_option = input("Do you want to SWAP them ? (yes/no) -> ").lower()

        if swap_option == 'yes':
            temp_card = other_player.cards[other_index-1]
            other_player.swap(card=my_player.cards[my_index-1], index=other_index-1)
            my_player.swap(card=temp_card, index=my_index-1)

            my_room.update_individual_player(player=[other_player, my_player])
            tools.stage_changes(my_room=my_room, player=my_player, what="looked,swapped", whose=other_name,
                                which=f"{my_index},{other_index}")
        else:
            tools.stage_changes(my_room=my_room, player=my_player, what="looked", whose=other_name,
                                which=f"{my_index},{other_index}")

    my_room.stack.append(top_card)


# ---------------------------------
print(f"{colors.yellow}{colors.BOLD}\n\\ __ - CAMEO - __ /{colors.ENDC}")

while True:
    game_choice = int(input("\n1. Initialise room\n"
                            "2. Join room\n"
                            "3. Exit\n"
                            "-> "))

    if game_choice == 1:
        if not in_room:
            my_room, my_player = tools.init_game()
            in_room = True
            time.sleep(1)
            print("\nPlayer CONNECTED!\tPlease advise the next player to join.")
            time.sleep(2)
            starter = input(f"{colors.green}Please wait until all the players have joined.{colors.ENDC} \n\nENTER 'start' TO BEGIN -> ").lower()
            if starter == "start":
                break
        break

    elif game_choice == 2:
        if not in_room:
            my_room, my_player = tools.join_room()
            in_room = True
            time.sleep(1)
            print("\nPlayer CONNECTED!\tPlease advise the next player to join.")
            time.sleep(2)
            starter = input(f"{colors.green}Please wait until all the players have joined. {colors.ENDC}\n\nENTER 'start' TO BEGIN -> ").lower()
            if starter == "start":
                break
        break

    elif game_choice == 3:
        if in_room:
            my_room.kill_me()
        exit()

print("\n== INSIDE THE ROOM ==\n")
current_player = my_player.name

while True:
    current_bit = my_room.current_status

    if "_" in my_room.players[0]:
        first_player = my_room.players[0].split('_')[0]
    else:
        first_player = my_room.players[0]

    if first_player == my_room.cameo_invoked:
        tools.execute_cameo(my_room=my_room)

    elif first_player == my_player.name:
        current_player = my_room.players[0]
        time.sleep(1.5)
        print(my_room)

        # if power_card is None:

        in_game = int(input("1. New card from deck\n"
                            "2. Burn\n"
                            "3. CAMEO !\n"
                            "-> "))

        if in_game == 1:
            new_card = my_room.deck.pop(0)

            if len(my_room.deck) == 0:
                my_room.deck = tools.shuffle(deck=my_room.stack)
                my_room.stack = []

            print(f"\nnew card : {colors.BOLD}{tools.show_card(new_card)}{colors.ENDC}")

            if tools.show_card(new_card) not in tools.power_deck:
                card_option = int(input("1. Do nothing\n"
                                        "2. Replace with one of yours\n"
                                        "-> "))

            else:
                card_option = int(input(f"{colors.red}POWER CARD !{colors.ENDC}\n"
                                        "1. Do nothing\n"
                                        "2. Replace with one of yours\n"
                                        "3. Avail powers\n"
                                        "-> "))

            if card_option == 1:
                # if tools.show_card(new_card) in tools.power_deck:
                #     print("\n-\\(-.-)/-")
                #     time.sleep(0.5)
                #     print(f"Listen here, you little shit.   THIS IS A POWER CARD. You get powers. {colors.BOLD}USE THE POWERS.{colors.ENDC}\n")
                #     power_play(top_card=new_card)
                # else:
                my_room.stack.append(new_card)

            elif card_option == 2:
                index = int(input("Enter the number of the card you want to SWAP : "))
                player_card = my_player.swap(card=new_card, index=index-1)

                # if tools.show_card(player_card) in tools.power_deck:
                #     my_room.stack.append(player_card)
                #     power_card = player_card
                #     tools.power_function(my_room=my_room)
                #
                # else:
                my_room.update_individual_player(player=[my_player])
                my_room.stack.append(player_card)
                tools.stage_changes(my_room=my_room, player=my_player, what="swapped", whose=my_player.name, which=str(index))

            elif card_option == 3:
                power_play(top_card=new_card)

        elif in_game == 2:
            cards = input("Enter the indexes of cards you want to BURN. <use commas to separate them> :")
            if len(cards) > 0:
                cards = cards.split(",")
            else:
                cards = [cards]

            if tools.show_card(my_room.stack[-1])[2:] in ['J', 'Q', 'K']:
                if len(cards) == 1:
                    if tools.show_card(my_player.cards[int(cards[0])-1])[2:] == tools.show_card(my_room.stack[-1])[2:]:
                        tools.execute_burn(my_room=my_room, my_player=my_player, indexes=cards)
                    else:
                        tools.lol_burn(my_room=my_room, my_player=my_player)
                else:
                    tools.lol_burn(my_room=my_room, my_player=my_player)

            else:
                player, score = tools.player_score(player=my_player, indexes=cards)

                if score == int(tools.show_card(my_room.stack[-1])[2:]):
                    tools.execute_burn(my_room=my_room, my_player=my_player, indexes=cards)
                else:
                    tools.lol_burn(my_room=my_room, my_player=my_player)

            my_room.update_individual_player(player=[my_player])

        elif in_game == 3:
            tools.invoke_cameo(my_room=my_room, my_player=my_player)

        # else:
        #     print(f"You just got a {colors.red}POWER CARD!{colors.ENDC}  -> {colors.BOLD}{tools.show_card(power_card)}{colors.ENDC}\n")
        #     power_play(top_card=power_card)

        my_room.update_room()

    else:
        print(my_room)

    while True:
        if my_room.current_status == current_bit:
            continue
        else:
            break
