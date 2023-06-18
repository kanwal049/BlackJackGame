import random

deck_values = {'Ace': 11, 'King': 10, 'Queen': 10, 'Jack': 10, 'Ten': 10, 'Nine': 9, 'Eight': 8, 'Seven': 7,
               'Six': 6, 'Five': 5, 'Four': 4, 'Three': 3, 'Two': 2}
'''ranks = ('Ace', 'Two', 'Jack')'''
ranks = ('Ace', 'King', 'Queen', 'Jack', 'Ten', 'Nine', 'Eight', 'Seven', 'Six', 'Five', 'Four', 'Three', 'Two')
suits = ('Spades', 'Diamonds', 'Clubs', 'Hearts')


player_ace = 0
dealer_ace = 0
money_in_bank = 5000


def display_card(dcard):
    s = dcard.suit
    r = dcard.rank
    spaces_need_s = 14-len(dcard.suit)
    for num in range(0, spaces_need_s):
        s += ' '

    spaces_need_r = 14 - len(dcard.rank)
    for num in range(0, spaces_need_r):
        r += ' '

    print(f"----------------")
    print(f"|              |")
    print(f"|{r}|")
    print(f"|of            |")
    print(f"|{s}|")
    print(f"|              |")
    print(f"----------------")


class Deck:
    def __init__(self):
        self.all_deck_cards = []

        for suit in suits:
            for rank in ranks:
                self.all_deck_cards.append(Card(suit, rank))

    def shuffle_deck(self):
        random.shuffle(self.all_deck_cards)

    def deal_one(self):
        return self.all_deck_cards.pop()


class Player:

    def __init__(self, name, bankroll):
        self.name = name
        self.all_cards = []
        self.cards_value = 0
        self.bankroll = bankroll

    def update_cards_value(self, card):
        self.cards_value += int(deck_values[card.rank])

    def current_cards_value(self):
        return self.cards_value


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'


game = True
while game:
    dealer_num_cards_already_updated = 0
    player_num_cards_already_updated = 0
    player_ace = 0
    dealer_ace = 0
    hit = True
    '''create deck & shuffle'''
    new_deck = Deck()
    new_deck.shuffle_deck()

    '''create Player'''
    player = Player('kanwal', money_in_bank)

    '''ask how much the player wants to bet'''
    while True:
        try:
            bet = input(f'{player.name} You have {player.bankroll}$ in your bankroll. '
                        f'How much money do you want to bet? : ')

            if type(bet) == int:
                raise TypeError()

            '''convert to integer'''
            bet = int(bet)

            '''check if bet is less than or equal to bankroll'''
            if bet > player.bankroll:
                print("You don't have enough money in your bank to bet this much")
                raise TypeError()
        except:
            print("Wrong Input!!!")

        else:
            break

    '''create_DealerPlayer'''
    dealer = Player('Dealer', 0)

    '''give dealer cards'''
    '''card1'''
    dealer.all_cards.append(new_deck.deal_one())
    dealer.update_cards_value(dealer.all_cards[0])

    '''dealer_num_cards_already_updated += 1'''
    print(f'------------------------------------------------------------------------')
    print(f'                             {dealer.name}                                     ')
    display_card(dealer.all_cards[0])

    '''check if dealer got an ace'''
    if dealer.all_cards[-1] == 'Ace':
        dealer_ace = +1

    '''display value of the first clard only'''
    print(f"Current value of {dealer.name}'s displayed card is {deck_values[dealer.all_cards[0].rank]}")

    '''card2'''
    dealer.all_cards.append(new_deck.deal_one())

    '''second card is not displayed'''

    '''give player 2 cards & display them'''
    '''card1'''
    player.all_cards.append(new_deck.deal_one())
    player.update_cards_value(player.all_cards[0])
    player_num_cards_already_updated += 1
    print(f'------------------------------------------------------------------------')
    print(f'                             {player.name}                                     ')
    display_card(player.all_cards[0])

    '''check if player got an ace'''
    if player.all_cards[0].rank == 'Ace':
        player_ace += 1


    '''card2'''
    player.all_cards.append(new_deck.deal_one())
    player.update_cards_value(player.all_cards[1])
    display_card(player.all_cards[1])

    '''check whether player got an ace again'''
    if player.all_cards[1].rank == 'Ace':
        player_ace += 1

    '''check if player won(hit the jackpot)'''
    if player.cards_value == 21:
        print(f'{player.name} won!!! :) ')

        '''update bankroll'''
        player.bankroll = player.bankroll + (bet * 2)
        money_in_bank = player.bankroll
        hit = False

    #if player got 2 ace adjust the value of one'''
    elif player_ace == 2:
        player.cards_value = player.cards_value - 10
        player_ace -= 1

    '''display total value'''
    print(f"Current Total of {player.name}'s cards is {player.current_cards_value()}")

    while hit:
        while True:
            '''ask for player's decision to hit or stay'''
            try:

                decision = input(f'{player.name} Please enter decision (H or S) : ')
                if decision not in ['H', 'h', 'S', 's']:
                    raise TypeError()

            except:
                print('Wrong Input!!!')

            else:
                break

        '''if player chooses hit'''
        if decision in ['H', 'h']:

            '''deal_one_card'''
            new_player_card = new_deck.deal_one()
            player.all_cards.append(new_player_card)
            print(f'------------------------------------------------------------------------')
            print(f'                             {player.name}                                     ')
            '''display new cards again and calculate current total value'''
            for i, card in enumerate(player.all_cards):
                display_card(card)

                '''because the value of the first 2 cards is already updated'''
                if i > player_num_cards_already_updated:
                    player.update_cards_value(card)
                    player_num_cards_already_updated += 1

            '''check if new card is ace'''
            if new_player_card.rank == 'Ace':
                player_ace += 1

            '''if there is an ace and current value is greater than 21 adjust it'''
            if player_ace > 0:
                if player.current_cards_value() > 21:
                    player.cards_value -= 10
                    player_ace -= 1

            '''display current total cards value'''
            print(f"Current Total of {player.name}'s cards is {player.current_cards_value()}")

            '''check if player won'''
            if player.cards_value == 21:
                print(f'{player.name} won!!! :) ')

                '''update bankroll'''
                player.bankroll = player.bankroll + (bet * 2)
                money_in_bank = player.bankroll
                hit = False
                break

            #check if bust, if not ask decision again'''
            elif player.cards_value > 21:
                '''check if there are ace cards'''
                '''there can be atleast 4'''
                print(f'{player.name} Busted!!! :( ')

                '''update Bankroll'''
                player.bankroll = player.bankroll - bet
                money_in_bank = player.bankroll
                hit = False
                break

            else:
                continue

        #if player chooses stay
        else:
            hit = False
            hit_dealer = True
            # reveal dealers second card
            print(f'------------------------------------------------------------------------')
            print(f'                             {dealer.name}                                     ')
            display_card(dealer.all_cards[0])
            display_card(dealer.all_cards[1])
            dealer.update_cards_value(dealer.all_cards[1])
            dealer_num_cards_already_updated += 1

            '''check if it is an ace then num of ace adjust value'''
            if dealer.all_cards[-1] == 'Ace':
                dealer_ace = +1

            #check if dealer got 2 ace if yes adjust the value
            elif dealer_ace == 2:
                dealer.cards_value = dealer.cards_value - 10
                dealer_ace -= 1

            '''after revealing dealer's second card check if he won'''
            if dealer.current_cards_value() > player.current_cards_value():
                print(f"Dealer has beaten {player.name}. ")
                print(f'{player.name} Lost!!! ')

                # update bankroll
                player.bankroll = player.bankroll - bet
                money_in_bank = player.bankroll
                hit_dealer = False


            '''display total dealer value'''
            print(f"Current Total of {dealer.name}'s cards is {dealer.current_cards_value()}")

            '''hit_dealer = True'''
            while hit_dealer:

                '''deal one to dealer'''
                new_dealer_card = new_deck.deal_one()
                dealer.all_cards.append(new_dealer_card)

                '''display all cards of dealer and calculate total value'''
                print(f'------------------------------------------------------------------------')
                print(f'                             {dealer.name}                                     ')
                for i, card in enumerate(dealer.all_cards):
                    display_card(card)
                    '''because the value of the first card is already updated'''
                    if i > dealer_num_cards_already_updated:
                        dealer_num_cards_already_updated += 1
                        dealer.update_cards_value(card)

                '''check if dealer got an ace adjust num of ace value'''
                if new_dealer_card.rank == 'Ace':
                    dealer_ace += 1

                '''if there is an ace and current value is greater than 21 adjust it'''
                if dealer_ace > 0:
                    if dealer.current_cards_value() > 21:
                        dealer.cards_value -= 10
                        dealer_ace -= 1

                '''display current total cards value'''
                print(f"Current Total of {dealer.name}'s cards is {dealer.current_cards_value()}")

                '''check if dealer is busted'''
                if dealer.current_cards_value() > 21:
                    print(f'{dealer.name} Busted!!! ')
                    print(f'{player.name} Won!!! ')

                    '''update bankroll'''
                    player.bankroll = player.bankroll + (bet * 2)
                    money_in_bank = player.bankroll
                    hit_dealer = False
                    break

                #check if dealer cards' value is more than the player's
                elif dealer.current_cards_value() > player.current_cards_value():
                    print(f"Dealer has beaten {player.name}. ")
                    print(f'{player.name} Lost!!! ')

                    '''update bankroll'''
                    player.bankroll = player.bankroll - bet
                    money_in_bank = player.bankroll
                    hit_dealer = False
                    break

                else:
                    continue


    '''ask if player wants to play again'''
    while True:
        try:
            print(f'{player.name} you have now {player.bankroll}$ in your bank!!!')
            play = input('Do you want to play again (Y or N) : ')
            if play not in ['Y', 'y', 'N', 'n']:
                raise TypeError()
        except TypeError:
            print("Wrong Input!!!")

        else:
            if play in ['Y', 'y']:
                game = True
                break
            else:
                game = False
                break





