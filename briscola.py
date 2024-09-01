import random
import os

clear = lambda: os.system('cls')

CARDS_FOR_PLAYER = 3

bastoni = {
    (10, "B"): "Re di bastoni",
    (9, "B"):  "Cavallo di bastoni",
    (8,"B"):  "Donna di bastoni",
    (7,"B"):  "7 di bastoni",
    (6,"B"):  "6 di bastoni",
    (5,"B"):  "5 di bastoni",
    (4,"B"):  "4 di bastoni",
    (11,"B"): "3 di bastoni",
    (2,"B"):  "2 di bastoni",
    (12,"B"): "Asso di bastoni"
}
denara = {
    (10, "D"): "Re di denara",
    (9, "D"):  "Cavallo di denara",
    (8,"D"):  "Donna di denara",
    (7,"D"):  "7 di denara",
    (6,"D"):  "6 di denara",
    (5,"D"):  "5 di denara",
    (4,"D"):  "4 di denara",
    (11,"D"): "3 di denara",
    (2,"D"):  "2 di denara",
    (12,"D"): "Asso di denara"
}
coppe = {
    (10,"C"): "Re di coppe",
    (9,"C"):  "Cavallo di coppe",
    (8,"C"):  "Donna di coppe",
    (7,"C"):  "7 di coppe",
    (6,"C"):  "6 di coppe",
    (5,"C"):  "5 di coppe",
    (4,"C"):  "4 di coppe",
    (11,"C"): "3 di coppe",
    (2,"C"):  "2 di coppe",
    (12,"C"): "Asso di coppe"
}
spade = {
    (10,"S"): "Re di spade",
    (9,"S"):  "Cavallo di spade",
    (8,"S"):  "Donna di spade",
    (7,"S"):  "7 di spade",
    (6,"S"):  "6 di spade",
    (5,"S"):  "5 di spade",
    (4,"S"):  "4 di spade",
    (11,"S"): "3 di spade",
    (2,"S"):  "2 di spade",
    (12,"S"): "Asso di spade"
}

punti = {
    12: 11,
    11: 10,
    10: 4,
    9: 3,
    8: 2,
    6:0,
    5:0,
    4:0,
    2:0,
    7:0
}

def get_text_from_value(value: list) -> str:
    if len(value) != 2:
        raise Exception("Error parsing the value of the card to string")
    else:
        if value[1] == "C":
            return coppe[tuple(value)]
        if value[1] == "B":
            return bastoni[tuple(value)]
        if value[1] == "D":
            return denara[tuple(value)]
        if value[1] == "S":
            return spade[tuple(value)]
        
        raise Exception("Invalid value")

def get_text_multiple_cards(values: list[list]):
    for value in values:
        yield get_text_from_value(value)

def shuffle_deck(mazzo):
    random.shuffle(mazzo)
    return 

def give_starting_cards(deck: list, number_of_players: int):

    if number_of_players == 2:
        player_1 = []
        player_2 = []

        for i in range(number_of_players * CARDS_FOR_PLAYER):
            if i % 2 == 0:
                player_1.append(deck[0])
            else:
                player_2.append(deck[0])
            deck.pop(0)

        briscola = deck[0]
        deck.pop(0)

        return player_1, player_2, deck, briscola
    elif number_of_players == 4:
        player_1 = []
        player_2 = []
        player_3 = []
        player_4 = []

        counter = 0
        for i in range(number_of_players * CARDS_FOR_PLAYER):
            if counter == 0:
                player_1.append(deck[0])
            elif counter == 1:
                player_2.append(deck[0])
            elif counter == 2:
                player_3.append(deck[0])
            elif counter == 3:
                player_4.append(deck[0])
                counter = -1
            
            counter += 1
            deck.pop(0)

        briscola = deck[0]
        deck.pop(0)


        return [player_1] + [player_2] + [player_3] + [player_4], briscola, random.randint(1,4)
    else:
        raise Exception("Error you can only play in 2 or 4 people")

def get_points(carte: list):
    total_points = 0

    for card in carte:
        if len(card) != 2:
            raise Exception("Error during counting final poins")
        else:
            total_points += punti[card[0]]

    return total_points

def get_sorted_player_hands(hands: dict, starting_index: int):
    clone_dict = {}

    restart_dict = {}
    for x in range(1,5):
        restart_dict[x] = hands[x]

    key_list = list(restart_dict.keys())

    for k,v in restart_dict.items():
        if k != starting_index:
            key_list.remove(k)
            key_list.append(k)
        else:
            break

    for x in key_list:
        clone_dict[x] = restart_dict[x]

    return clone_dict 

def get_last_valid_card(cards_played: list, briscola):
    if len(cards_played) == 1:
        return cards_played[0]
    
    if len(cards_played) == 2:
        return check_winner_2(cards_played[0], cards_played[1], briscola, True )

    carta_vincente = None
    index_player = 0
    for index, card in enumerate(cards_played):
        if carta_vincente == None:
            carta_vincente = card
            index_player = index + 1
            continue
        else:
            if card[1] == carta_vincente[1] and card[0] > carta_vincente[0]:
                carta_vincente = card
                index_player = index + 1
                continue
            elif card[1] == briscola[1] and carta_vincente[1] != briscola[1]:
                carta_vincente = card
                index_player = index + 1
                continue
    
    return carta_vincente, index_player

def select_card(hand: list):
    while True:
        card_to_play = input("Quale carta vuoi giocare? (1,2,3) ")

        if card_to_play.isdigit():
            card_to_play = int(card_to_play)
            if card_to_play != 1 and card_to_play != 2 and card_to_play != 3:
                print("Inserisci una carta valida.")
            else:
                if card_to_play > len(hand):
                    print("Attenzione selezionare una carta valida! ")
                else:
                    card_chosen = hand[card_to_play - 1]

                    print("Hai scelto: ", get_text_from_value(card_chosen))
                    return card_chosen
        else:
            print("Inserisci una carta valida.")

def select_bot_card(hand: list, is_starting_hand: bool, briscola, card_played):

    if len(hand) == 1:
        print("L'avversario ha giocato: ", get_text_from_value(hand[0]))
        return hand[0]

    clone_hand = hand[:]

    clone_hand.sort(key=lambda x: x[0])
    lowest_card = clone_hand[0]

    if is_starting_hand:
        if lowest_card[1] != briscola[1]:
            # lowest card non è briscola
            # la gioco sempre
            print("L'avversario ha giocato: ", get_text_from_value(lowest_card))
            return lowest_card
        else:
            # lowest card è briscola
            
            # controllo se la seconda carta più alta non è di briscola e se non è un carico la gioco 
            if clone_hand[1][1] != briscola[1]:

                if clone_hand[1][0] < 10:
                    print("L'avversario ha giocato: ", get_text_from_value(clone_hand[1]))
                    return clone_hand[1]
                else:
                    print("L'avversario ha giocato: ", get_text_from_value(lowest_card))
                    return lowest_card
            else:
                # ho anche la seconda carta a briscola 
                # controllo la terza
                if len(hand) == 3:

                    if clone_hand[2][1] != briscola[1]:

                        if clone_hand[2][0] < 10:
                            print("L'avversario ha giocato: ", get_text_from_value(clone_hand[2]))
                            return clone_hand[2]
                        else:
                            print("L'avversario ha giocato: ", get_text_from_value(lowest_card))
                            return lowest_card
                    else:
                        # ho tutte le carte a briscola gioco la più bassa
                        print("L'avversario ha giocato: ", get_text_from_value(lowest_card))
                        return lowest_card
                else:
                    # ho tutte le carte a briscola gioco la più bassa
                    print("L'avversario ha giocato: ", get_text_from_value(lowest_card))
                    return lowest_card

    else:
        if card_played[1] != briscola[1]:
            value_of_opponent_card = card_played[0]
            seed_of_opponent_card = card_played[1]

            # se il bot può prendere prende sempre
            for card in clone_hand:
                if card[0] > value_of_opponent_card and card[1] == seed_of_opponent_card:
                    print("L'avversario ha giocato: ", get_text_from_value(card))
                    return card

            # se non puà prendere gioca la carta più bassa
            if lowest_card[0] < 8 and lowest_card[1] != briscola[1]:
                print("L'avversario ha giocato: ", get_text_from_value(lowest_card))
                return lowest_card
            
            # se l'avversario ha giocato un 3 o un asso non di briscola prendi con la briscola 
            if value_of_opponent_card > 10 and seed_of_opponent_card != briscola[1]:
                for card in clone_hand:
                    if card[1] == briscola[1]:
                        print("L'avversario ha giocato: ", get_text_from_value(card))
                        return card


        card_value = random.choice(clone_hand)
        print("L'avversario ha giocato: ", get_text_from_value(card_value))

        return card_value

def check_winner_2(card_1, card_2, briscola, startp1: bool):
    if len(card_1) != 2 and len(card_2) != 2 and len(briscola) != 2:
        raise Exception("Error during checking cards")
    else:
        if card_1[1] == briscola[1] and card_2[1] != briscola[1]:
            return card_1
        elif card_2[1] == briscola[1] and card_1[1] != briscola[1]:
            return card_2
        elif card_1[1] == card_2[1]:
            if card_1[0] > card_2[0]:
                return card_1
            else:
                return card_2
        else:
            if startp1:
                return card_1
            else:
                return card_2

def draw_cards_4(hands: list, deck: list, briscola):

    last_hand = False
    for key, hand in hands.items():
        if last_hand != True:
            if len(deck) > 0:
                hand.append(deck[0])
                deck.pop(0)
            else:
                hand.append(briscola)
                last_hand = True

    return hands, last_hand

def pop_card_played_from_hands(hands: dict[int:list], cards_played):

    counter = 0
    for index, hand in hands.items():
        hand.remove(cards_played[counter])
        counter += 1
        

    return hands

def play_4(players_cards: list[list[tuple]], briscola: tuple, deck: list, starting_player_index: int):
    hands = {}


    points_s1 = []
    points_s2 = []

    for i in range(len(players_cards)):
        hands[i + 1] = players_cards[i]

    hands  = get_sorted_player_hands(hands, starting_player_index)
    last_hand = False

    while len(hands[1]) > 0:

        print("Ecco la tua mano: ")
        for card in get_text_multiple_cards(hands[1]):
            print(card, end=" | ")
        
        print("La briscola è: ", get_text_from_value(briscola))

        cards_played = []
        for key, val in hands.items():

            if key == 1:
                cards_played.append(select_card(hand=val))
            else:
                start_this_player = False
                last_card = None

                if any(cards_played):
                    last_card = get_last_valid_card(cards_played, briscola)

                    if len(cards_played) > 2:
                        last_card = last_card[0]
                else:
                    start_this_player = True

                cards_played.append(select_bot_card(val, start_this_player, briscola, last_card))

        winner_card, index_player = get_last_valid_card(cards_played, briscola)
        print("Prende il giocatore numero", index_player)

        key_player_winning = list(hands.keys())[index_player - 1]

        if key_player_winning % 2 == 0:
            for x in cards_played:
                points_s2.append(x)
        else:
            for x in cards_played:
                points_s1.append(x)

        hands = pop_card_played_from_hands(hands, cards_played)

        hands = get_sorted_player_hands(hands, key_player_winning)

        if last_hand != True:
            hands, last_hand = draw_cards_4(hands, deck, briscola)

        input("Premere invio per proseguire.")
        clear()

    punteggio_s1 = get_points(points_s1)
    punteggio_s2 = get_points(points_s2)

    if punteggio_s1 != 60:
        if punteggio_s1 > punteggio_s2:
            print(f"Complimenti hai vinto insieme al giocatore numero 3, con un punteggio di {punteggio_s1}.")
        else:
            print(f"Purtroppo ha vinto la squadra composta dal giocatore 2 e dal giocatore 4, con un punteggio di {punteggio_s2}.")
    else:
        print(f"Attenzione, pareggio perfetto di {punteggio_s1} punti, complimenti ad entrambe le squadre.")

def play_2(player_1_hand: list, player_2_hand: list, deck: list, briscola):

    points_p1 = []
    points_p2 = []

    start_p1 = True

    while len(player_1_hand) > 0:

        print("Ecco la tua mano: ")
        for card in get_text_multiple_cards(player_1_hand):
            print(card, end=" | ")
        
        print("La briscola è: ", get_text_from_value(briscola))

        if start_p1 == True:
            card_chosen = select_card(player_1_hand)
            opponent_card = select_bot_card(player_2_hand,False, briscola, card_chosen)
        else:
            opponent_card = select_bot_card(player_2_hand, True, briscola, None)
            card_chosen = select_card(player_1_hand)


        winner_card = check_winner_2(card_chosen, opponent_card, briscola, start_p1)

        if winner_card == card_chosen:
            points_p1.append(card_chosen)
            points_p1.append(opponent_card)

            print("Hai preso tu!")
            start_p1 = True
        else:
            points_p2.append(card_chosen)
            points_p2.append(opponent_card)

            print("Prende l'avversario!")
            start_p1 = False

        player_1_hand.remove(card_chosen)
        player_2_hand.remove(opponent_card)

        if len(deck) > 0:
            if len(deck) == 1:
                if start_p1:
                    player_1_hand.append(deck[0])
                    deck.pop(0)

                    player_2_hand.append(briscola)
            else:
                if start_p1:
                    player_1_hand.append(deck[0])
                    deck.pop(0)

                    player_2_hand.append(deck[0])
                    deck.pop(0)
                else:
                    player_2_hand.append(deck[0])
                    deck.pop(0)

                    player_1_hand.append(deck[0])
                    deck.pop(0)
        input("Premere invio per proseguire.")
        clear()


    print("Partita finita ecco il risultato")

    punti_p1 = get_points(points_p1)
    punti_p2 = get_points(points_p2)

    if punti_p1 > punti_p2:
        print(f"Complimenti hai vinto per {punti_p1} a {punti_p2}! 😀")
    else:
        print(f"Accidenti hai perso per {punti_p2} a {punti_p1} 😞")

def main():
    deck = list(bastoni.keys()) + list(denara.keys()) + list(coppe.keys()) + list(spade.keys())
    shuffle_deck(deck)
    
    number_of_players = None
    while True:
        number_of_players = input("Con quante persone vuoi simulare una partita 2 o 4? ")
        
        if number_of_players.isdigit():
            if int(number_of_players) != 2 and int(number_of_players) != 4:
                print("Inserisci un numero di giocatori valido.")
            else:
                number_of_players = int(number_of_players)
                break
        else:
            print("Inserisci un numero di giocatori valido.")

    if number_of_players == 2:
        player1, player2, deck, briscola = give_starting_cards(deck, number_of_players)

        print("La briscola è il ", get_text_from_value(briscola))
        input("Premi invio per cominciare! ")
        clear()

        play_2(player1, player2, deck, briscola)
    elif number_of_players == 4:

        list_of_hands, briscola, starting_player = give_starting_cards(deck, number_of_players)

        print("La briscola è il ", get_text_from_value(briscola))
        input("Premi invio per cominciare! ")
        clear()
        
        play_4(list_of_hands, briscola, deck,starting_player)

if __name__ == '__main__':
    while True:
        start = input("Il mazzo è stato correttamente mischiato. Vuoi cominciare? premi invio per giocare. (q per uscire)")
        if start != 'q':
            main()    
        else:
            break
