import sys
import random 
deck = ['aC', 'aD', 'aH', 'aS', '2C', '2D', '2H', '2S', '3C', '3D', '3H', '3S', '4C', '4D', '4H', '4S', '5C', '5D', '5H', '5S', '6C', '6D', '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S', '9C', '9D', '9H', '9S', '10C', '10D', '10H', '10S','jC','jD','jH','jS','qC','qD','qH','qS','kC','kD','kH','kS']
random.shuffle(deck)
player = 1
number_of_players = 0
def dealer():
    dealer_hand = []
    for i in range(2):
        dealer_hand.append(deck.pop())
    return dealer_hand

def deal_card():  
    player = input("Enter the number of players (1-4): ")
    if player.isdigit() and 1 <= int(player) <= 4:
        player = int(player)
        hands = [[] for _ in range(player)]
        for i in range(2):
            for j in range(player):
                hands[j].append(deck.pop())
        return hands
    else:
        print("Invalid input. Please enter a number between 1 and 4.")
        return deal_card()

def calculate_hand_value(dealer_hand=None, player1=None, player2=None, player3=None, player4=None):
    hand_values = []
    for hand in [dealer_hand, player1, player2, player3, player4]:
        if hand is not None:
            value = 0
            aces = 0
            for card in hand:
                rank = card[:-1]
                if rank in ['j', 'q', 'k']:
                    value += 10
                elif rank == 'a':
                    aces += 1
                    value += 11
                else:
                    value += int(rank)
            while value > 21 and aces:
                value -= 10
                aces -= 1
            hand_values.append(value)
    return hand_values

def sub(playerNum,player1=None, player2=None, player3=None, player4=None):
    currentPlayer = playerNum
    choice = choices(currentPlayer, player1=player1, player2=player2, player3=player3, player4=player4)
    if choice.lower() == 'h':
        if playerNum == 1:
            player1.append(deck.pop())
            translate(dealer_hand=None, player1=player1)
            player1_value = calculate_hand_value(player1)[0]
            print("Player 1's hand value:", player1_value)
            if player1_value > 21:
                print("Player 1, bust!")
                return
            elif player1_value == 21:
                print("Player 1, has Blackjack!")
                return
            else:
                
                sub(playerNum, player1=player1)

        elif playerNum == 2:
            player2.append(deck.pop())
            translate(dealer_hand=None, player2=player2)
            player2_value = calculate_hand_value(player2)[0]
            print("Player 2's hand value:", player2_value)
            if player2_value > 21:
                print("Player 2, bust!")
                return
            elif player2_value == 21:
                print("Player 2, has Blackjack!")
                return
            else:
                
                sub(playerNum, player2=player2)
        elif playerNum == 3:
            player3.append(deck.pop())
            translate(dealer_hand=None, player3=player3)
            player3_value = calculate_hand_value(player3)[0]
            print("Player 3's hand value:", player3_value)
            if player3_value > 21:
                print("Player 3, bust!")
                return
            elif player3_value == 21:
                print("Player 3, has Blackjack!")
                return
            else:
                
                sub(playerNum, player3=player3)
        elif playerNum == 4:
            player4.append(deck.pop())
            translate(dealer_hand=None, player4=player4)
            player4_value = calculate_hand_value(player4)[0]
            print("Player 4's hand value:", player4_value)
            if player4_value > 21:
                print("Player 4, bust!")
                return
            elif player4_value == 21:
                print("Player 4, has Blackjack!")
                return
            else:
                
                sub(playerNum, player4=player4)

    elif choice.lower() == 's':
        print(f"Player {playerNum} stands.")
        return

def choices(currentPlayer, player1=None, player2=None, player3=None, player4=None):
    player_hand = []
    player_value = 0
    if currentPlayer == 1:
        if player1 is not None:
            player_value = calculate_hand_value(player1)[0]
            player_hand = translate(dealer_hand=None, player1=player1, printN=1)
    elif currentPlayer == 2:
        if player2 is not None:
            player_value = calculate_hand_value(player2)[0]
            player_hand = translate(dealer_hand=None, player2=player2, printN=1)
    elif currentPlayer == 3:
        if player3 is not None:
            player_value = calculate_hand_value(player3)[0]
            player_hand = translate(dealer_hand=None, player3=player3, printN=1)
    elif currentPlayer == 4:
        if player4 is not None:
            player_value = calculate_hand_value(player4)[0]
            player_hand = translate(dealer_hand=None, player4=player4, printN=1)
    choices = input(f"Player {currentPlayer}, your current hand value is {player_value}.\n Your hand: {player_hand}\n Do you want to hit or stand? (h/s): ")

    return choices


def hit_or_stand(number_of_players, player1, player2=None, player3=None, player4=None):
    player1_value = calculate_hand_value(player1)[0]
    player2_value = calculate_hand_value(player2)[0] if player2 is not None else None
    player3_value = calculate_hand_value(player3)[0] if player3 is not None else None
    player4_value = calculate_hand_value(player4)[0] if player4 is not None else None
    
    for i in range(number_of_players):
        if i == 0 and player1_value == 21:
            print("Player 1, has Blackjack!")
            continue
        if i == 1 and player2_value == 21:
            print("Player 2, has Blackjack!")
            continue
        if i == 2 and player3_value == 21:
            print("Player 3, has Blackjack!")
            continue
        if i == 3 and player4_value == 21:
            print("Player 4, has Blackjack!")
            continue
        currentPlayer = i + 1

        choice = choices(currentPlayer=currentPlayer, player1=player1, player2=player2, player3=player3, player4=player4)
        if choice.lower() == 'h':
            if i == 0:
                player1.append(deck.pop())
                translate(dealer_hand=None, player1=player1)
                player1_value = calculate_hand_value(player1)[0]
                print("Player 1's hand value:", player1_value)
                if player1_value > 21:
                    print("Player 1, bust!")
                    continue
                elif player1_value == 21:
                    print("Player 1, has Blackjack!")
                    continue
                else:
                    
                    playerNum = 1
                    sub(playerNum, player1=player1)

                    

            elif i == 1:
                player2.append(deck.pop())
                translate(dealer_hand=None, player2=player2)
                player2_value = calculate_hand_value(player2)[0]
                print("Player 2's hand value:", player2_value)
                if player2_value > 21:
                    print("Player 2, bust!")
                    continue
                elif player2_value == 21:
                    print("Player 2, has Blackjack!")
                    continue

                else:
                    
                    playerNum = 2
                    sub(playerNum, player2=player2)
                    

            elif i == 2:
                player3.append(deck.pop())
                translate(dealer_hand=None, player3=player3)
                player3_value = calculate_hand_value(player3)[0]
                print("Player 3's hand value:", player3_value)
                if player3_value > 21:
                    print("Player 3, bust!")
                    continue
                elif player3_value == 21:
                    print("Player 3, has Blackjack!")
                    continue
                else:
                    
                    playerNum = 3
                    sub(playerNum, player3=player3)
                    
            else:
                player4.append(deck.pop())
                translate(dealer_hand=None, player4=player4)
                player4_value = calculate_hand_value(player4)[0]
                print("Player 4's hand value:", player4_value)
                if player4_value > 21:
                    print("Player 4, bust!")
                    continue
                elif player4_value == 21:
                    print("Player 4, has Blackjack!")
                    continue
                else:
                    
                    playerNum = 4
                    sub(playerNum, player4=player4)
                    

        elif choice.lower() == 's':
            print(f"Player {i + 1} stands.")
            continue
        else:
            print("Invalid input. Please enter 'h' for hit or 's' for stand.")
            i -= 1 

def translate(dealer_hand=None, start=None, printN=None, number_of_players=None, player1=None, player2=None, player3=None, player4=None):
    # Translate dealer's hand
    translated_dealer_hand = []
    if dealer_hand is not None:
        translated_dealer_hand = []
        for card in dealer_hand:
            rank = card[:-1]
        
            if rank == 'a':
                rank = 'Ace'
            elif rank == 'j':
                rank = 'Jack'
            elif rank == 'q':
                rank = 'Queen'
            elif rank == 'k':
                rank = 'King'

            suit = card[-1]
            if suit == 'C':
               suit = 'Clubs'
            elif suit == 'D':
                suit = 'Diamonds'
            elif suit == 'H':
                suit = 'Hearts'
            elif suit == 'S':
                suit = 'Spades'
            translated_dealer_hand.append(f"{rank} of {suit}")
        if start == 1:
            print("Dealer's hand:", translated_dealer_hand[0], "and a hidden card")
            return
        elif start is None:
            print("Dealer's hand:", translated_dealer_hand)

    

    # Translate players' hands
    if number_of_players is not None:
        for i in range(number_of_players):
            if i == 0:
                 hand = player1
            elif i == 1:
                hand = player2
            elif i == 2:
                hand = player3
            else:
                hand = player4

            if hand is not None:
                translated_hand = []
                for card in hand:
                    rank = card[:-1]
                    
                    if rank == 'a':
                        rank = 'Ace'
                    elif rank == 'j':
                        rank = 'Jack'
                    elif rank == 'q':
                        rank = 'Queen'
                    elif rank == 'k':
                        rank = 'King'
                    suit = card[-1]
                    if suit == 'C':
                        suit = 'Clubs'  
                    elif suit == 'D':
                        suit = 'Diamonds'
                    elif suit == 'H':
                        suit = 'Hearts'
                    elif suit == 'S':
                        suit = 'Spades'
                    translated_hand.append(f"{rank} of {suit}")
            print(f"Player {i + 1}'s hand:", translated_hand)
    elif number_of_players is None:
        if player1 is not None:
            sep_translated_hand = []
            for card in player1:
                rank = card[:-1]
                
                if rank == 'a':
                    rank = 'Ace'
                elif rank == 'j':
                    rank = 'Jack'
                elif rank == 'q':
                    rank = 'Queen'
                elif rank == 'k':
                    rank = 'King'
                suit = card[-1]
                if suit == 'C':
                    suit = 'Clubs'  
                elif suit == 'D':
                    suit = 'Diamonds'
                elif suit == 'H':
                    suit = 'Hearts'
                elif suit == 'S':
                    suit = 'Spades'
                sep_translated_hand.append(f"{rank} of {suit}")
            if printN is None:
                print("Player 1's hand:", sep_translated_hand)
            elif printN is not None:
                return sep_translated_hand   
            
        elif player2 is not None:
            sep_translated_hand = []
            for card in player2:
                rank = card[:-1]
                
                if rank == 'a':
                    rank = 'Ace'
                elif rank == 'j':
                    rank = 'Jack'
                elif rank == 'q':
                    rank = 'Queen'
                elif rank == 'k':
                    rank = 'King'
                suit = card[-1]
                if suit == 'C':
                    suit = 'Clubs'  
                elif suit == 'D':
                    suit = 'Diamonds'
                elif suit == 'H':
                    suit = 'Hearts'
                elif suit == 'S':
                    suit = 'Spades'
                sep_translated_hand.append(f"{rank} of {suit}")
            if printN is None:
                print("Player 2's hand:", sep_translated_hand)
            elif printN is not None:
                return sep_translated_hand
        elif player3 is not None:
            sep_translated_hand = []
            for card in player3:
                rank = card[:-1]
                
                if rank == 'a':
                    rank = 'Ace'
                elif rank == 'j':
                    rank = 'Jack'
                elif rank == 'q':
                    rank = 'Queen'
                elif rank == 'k':
                    rank = 'King'
                
                suit = card[-1]
                if suit == 'C':
                    suit = 'Clubs'  
                elif suit == 'D':
                    suit = 'Diamonds'
                elif suit == 'H':
                    suit = 'Hearts'
                elif suit == 'S':
                    suit = 'Spades'
                sep_translated_hand.append(f"{rank} of {suit}")
            if printN is None:
                print("Player 3's hand:", sep_translated_hand)
            elif printN is not None:
                return sep_translated_hand
        elif player4 is not None:
            sep_translated_hand = []
            for card in player4:
                rank = card[:-1]
                
                if rank == 'a':
                    rank = 'Ace'
                elif rank == 'j':
                    rank = 'Jack'
                elif rank == 'q':
                    rank = 'Queen'
                elif rank == 'k':
                    rank = 'King'
                suit = card[-1]
                if suit == 'C':
                    suit = 'Clubs'  
                elif suit == 'D':
                    suit = 'Diamonds'
                elif suit == 'H':
                    suit = 'Hearts'
                elif suit == 'S':
                    suit = 'Spades'
                sep_translated_hand.append(f"{rank} of {suit}")
            if printN is None:
                print("Player 4's hand:", sep_translated_hand)
            elif printN is not None:
                return sep_translated_hand

def dealer_play(dealer_hand, player1_value, player2_value=None, player3_value=None, player4_value=None, number_of_players=None):
    print("Dealer's turn:")
    dealer_value = calculate_hand_value(dealer_hand)[0]
    start = 0
    translate(dealer_hand, start)
    print("Dealer's hand value:", dealer_value)
    if dealer_value < 17:
        while dealer_value < 17:
            dealer_hand.append(deck.pop())
            dealer_value = calculate_hand_value(dealer_hand)[0]
            print("Dealer hits.")
            translate(dealer_hand=dealer_hand)
            print("Dealer's hand value:", dealer_value)
            if dealer_value > 21:
                print("Dealer busts!")
                if number_of_players == 1:
                    if player1_value <= 21:
                        print("Player 1 wins against the dealer!")
                else:
                    for i in range(number_of_players):
                        if i == 0:
                            if player1_value <= 21:
                                print("Player 1 wins against the dealer!")
                            else:
                                print("Player 1 busts and loses with the dealer!")
                        elif i == 1:
                            if player2_value <= 21:
                                print("Player 2 wins against the dealer!")
                            else:
                                print("Player 2 busts and loses with the dealer!")
                        elif i == 2:
                            if player3_value <= 21:
                                print("Player 3 wins against the dealer!")
                            else:
                                print("Player 3 busts and loses with the dealer!")
                        elif i == 3:
                            if player4_value <= 21:
                                print("Player 4 wins against the dealer!")
                            else:
                                print("Player 4 busts and loses with the dealer!")

                return
    if dealer_value >= 17:
        if dealer_value == 21:
            print("Dealer has Blackjack!")
            for i in range(number_of_players):
                if i == 0:
                    if player1_value == 21:
                        print("Player 1 ties with the dealer!")
                    else:
                        print("Dealer wins against Player 1!")
                elif i == 1:
                    if player2_value == 21:
                        print("Player 2 ties with the dealer!")
                    else:
                        print("Dealer wins against Player 2!")
                elif i == 2:
                    if player3_value == 21:
                        print("Player 3 ties with the dealer!")
                    else:
                        print("Dealer wins against Player 3!")
                elif i == 3:
                    if player4_value == 21:
                        print("Player 4 ties with the dealer!")
                    else:
                        print("Dealer wins against Player 4!")
        elif dealer_value > 21:
            print("Dealer busts!")
            for i in range(number_of_players):
                if i == 0:
                    if player1_value <= 21:
                        print("Player 1 wins against the dealer!")
                    else:
                        print("Player 1 busts and loses with the dealer!")
                elif i == 1:
                    if player2_value <= 21:
                        print("Player 2 wins against the dealer!")
                    else:
                        print("Player 2 busts and loses with the dealer!")
                elif i == 2:
                    if player3_value <= 21:
                        print("Player 3 wins against the dealer!")
                    else:
                        print("Player 3 busts and loses with the dealer!")
                elif i == 3:
                    if player4_value <= 21:
                        print("Player 4 wins against the dealer!")
                    else:
                        print("Player 4 busts and loses with the dealer!")
        else:
            for i in range(number_of_players):
                if i == 0:
                    if player1_value > dealer_value and player1_value <= 21:
                        print("Player 1 wins against the dealer!")
                    elif player1_value < dealer_value or player1_value > 21:
                        print("Dealer wins against Player 1!")
                    else:
                        print("Player 1 ties with the dealer!")
                elif i == 1:
                    if player2_value > dealer_value and player2_value <= 21:
                        print("Player 2 wins against the dealer!")
                    elif player2_value < dealer_value or player2_value > 21:
                        print("Dealer wins against Player 2!")
                    else:
                        print("Player 2 ties with the dealer!")
                elif i == 2:
                    if player3_value > dealer_value and player3_value <= 21:
                        print("Player 3 wins against the dealer!")
                    elif player3_value < dealer_value or player3_value > 21:
                        print("Dealer wins against Player 3!")
                    else:
                        print("Player 3 ties with the dealer!")
                elif i == 3:
                    if player4_value > dealer_value and player4_value <= 21:
                        print("Player 4 wins against the dealer!")
                    elif player4_value < dealer_value or player4_value > 21:
                        print("Dealer wins against Player 4!")
                    else:
                        print("Player 4 ties with the dealer!")
        
        return
    





dealer_hand = dealer()
start = 1 
translate(dealer_hand, start=1)
dealer_value = calculate_hand_value(dealer_hand)[0]

players_hands = deal_card()
len_players = len(players_hands)
if len_players == 1:
    player1 = players_hands[0]
    translate(number_of_players=1, player1=player1)
    number_of_players = int(1)
    player1_value = calculate_hand_value(player1)[0]
    print("Player 1's hand value:", player1_value)
    if player1_value > 21:
        print("Player 1, bust!")
    elif player1_value == 21:
        print("Player 1, has Blackjack!")

    hit_or_stand(number_of_players, player1, None, None, None)
    player1_value = calculate_hand_value(player1)[0]
    dealer_play(dealer_hand, player1_value, None, None, None, number_of_players)



elif len_players == 2:
    player1 = players_hands[0]
    player2 = players_hands[1]
    translate(number_of_players=2, player1=player1, player2=player2)
    number_of_players = int(2)
    player1_value = calculate_hand_value(player1)[0]
    player2_value = calculate_hand_value(player2)[0]
    print("Player 1's hand value:", player1_value)
    if player1_value > 21:
        print("Player 1, bust!")
    elif player1_value == 21:
        print("Player 1, has Blackjack!")
    print("Player 2's hand value:", player2_value)
    if player2_value > 21:
        print("Player 2, bust!")
    elif player2_value == 21:
        print("Player 2, has Blackjack!")
    hit_or_stand(number_of_players, player1, player2, None, None)
    player1_value = calculate_hand_value(player1)[0]
    player2_value = calculate_hand_value(player2)[0]
    dealer_play(dealer_hand, player1_value, player2_value, None, None, number_of_players)

elif len_players == 3:
    player1 = players_hands[0]
    player2 = players_hands[1]
    player3 = players_hands[2]
    translate(number_of_players=3, player1=player1, player2=player2, player3=player3)
    number_of_players = int(3)
    player1_value = calculate_hand_value(player1)[0]
    player2_value = calculate_hand_value(player2)[0]
    player3_value = calculate_hand_value(player3)[0]
    print("Player 1's hand value:", player1_value)
    if player1_value > 21:
        print("Player 1, bust!")
    elif player1_value == 21:
        print("Player 1, has Blackjack!")
    print("Player 2's hand value:", player2_value)
    if player2_value > 21:
         print("Player 2, bust!")
    elif player2_value == 21:
        print("Player 2, has Blackjack!")
    print("Player 3's hand value:", player3_value)
    if player3_value > 21:
        print("Player 3, bust!")
    elif player3_value == 21:
        print("Player 3, has Blackjack!")
    hit_or_stand(number_of_players, player1, player2, player3, None)
    player1_value = calculate_hand_value(player1)[0]
    player2_value = calculate_hand_value(player2)[0]
    player3_value = calculate_hand_value(player3)[0]
    dealer_play(dealer_hand, player1_value, player2_value, player3_value, None, number_of_players)

elif len_players == 4:
    player1 = players_hands[0]
    player2 = players_hands[1]
    player3 = players_hands[2]
    player4 = players_hands[3]
    translate(number_of_players=4, player1=player1, player2=player2, player3=player3, player4=player4)
    number_of_players = int(4)
    player1_value = calculate_hand_value(player1)[0]
    player2_value = calculate_hand_value(player2)[0]
    player3_value = calculate_hand_value(player3)[0]
    player4_value = calculate_hand_value(player4)[0]
    print("Player 1's hand value:", player1_value)
    if player1_value > 21:
         print("Player 1, bust!")
    elif player1_value == 21:
        print("Player 1, has Blackjack!")
    print("Player 2's hand value:", player2_value)
    if player2_value > 21:
         print("Player 2, bust!")
    elif player2_value == 21:
        print("Player 2, has Blackjack!")
    print("Player 3's hand value:", player3_value)
    if player3_value > 21:
         print("Player 3, bust!")
    elif player3_value == 21:
        print("Player 3, has Blackjack!")
    print("Player 4's hand value:", player4_value)
    if player4_value > 21:
         print("Player 4, bust!")
    elif player4_value == 21:
        print("Player 4, has Blackjack!")
    hit_or_stand(number_of_players, player1, player2, player3, player4)
    player1_value = calculate_hand_value(player1)[0]
    player2_value = calculate_hand_value(player2)[0]
    player3_value = calculate_hand_value(player3)[0]
    player4_value = calculate_hand_value(player4)[0]
    dealer_play(dealer_hand, player1_value, player2_value, player3_value, player4_value, number_of_players)
print("Game over. Thanks for playing!")

