import random, time, datetime

class Person:
    def __init__(self, role):
        # "role" is used for purposes of "print_cards" and "print_total"
        self.role = role

    def deal_card(self):
        dealt_card = random.choice(card_deck.available_cards)
        self.cards.append(dealt_card)
        card_deck.remove_card(dealt_card)
        self.update_total()

    def update_total(self):
        # Reset "self.total" and "self.ace" as previous calculations must be disregarded
        self.total = 0
        self.ace = ""
        # First count total of all non-ace cards - only then can value of aces be determined correctly
        for card in self.cards:
            if card[0] != "A":
                self.total += card_deck.cards[card]
        # Then add total of every ace and set value of "self.ace" for purposes of "print_total"
        for card in self.cards:
            if card[0] == "A":
                if self.total <= 10:
                    self.total += 11
                    self.ace = "soft/hard"
                else:
                    self.total += 1
                    # Set "self.ace" to "hard" only if it's not already "soft/hard" -
                    # if 1st ace was counted as 11 (i.e. soft total exists),
                    # "self.ace" should stay "soft/hard" even if there is 2nd/3rd/4th ace afterwards
                    if self.ace == "":
                        self.ace = "hard"

    def print_cards(self):
        time.sleep(1)
        if self.role == "player":
            print(f"\nYour cards: {', '.join(self.cards)}")
        else:
            print(f"\nDealer's cards: {', '.join(self.cards)}")

    def print_total(self):
        if self.role == "player":
            # When blackjack is achieved, total is raised by 100 to ensure victory over "non-blackjack" total of 21
            if self.total == 121:
                print("Your total: 21 (blackjack)")
            # Both soft and hard totals are relevant
            elif self.ace == "soft/hard":
                print(f"Your total: {self.total} (soft) / {self.total - 10} (hard)")
            # Only hard total is relevant as soft total exceeds 21
            elif self.ace == "hard":
                print(f"Your total: {self.total} (hard)")
            # No blackjack is achieved and no ace is present in hand - there is no soft or hard total
            else:
                print(f"Your total: {self.total}")
        else:
            if self.total == 121:
                print("Dealer's total: 21 (blackjack)")
            elif self.ace == "soft/hard":
                # Dealer's round ends when soft total is 17 or higher - hard total is then irrelevant
                if self.total >= 17:
                    print(f"Dealer's total: {self.total} (soft)")
                else:
                    print(f"Dealer's total: {self.total} (soft) / {self.total - 10} (hard)")
            elif self.ace == "hard":
                print(f"Dealer's total: {self.total} (hard)")
            else:
                print(f"Dealer's total: {self.total}")

class CardDeck:
    # Complete deck of cards including card values
    # Ace has value of either 1 or 11 - counting is done in "update_total" function
    cards = {"2 ♣": 2, "3 ♣": 3, "4 ♣": 4, "5 ♣": 5, "6 ♣": 6, "7 ♣": 7, "8 ♣": 8, "9 ♣": 9, "10 ♣": 10, "J ♣": 10, "Q ♣": 10, "K ♣": 10, "A ♣": None, "2 ♦": 2, "3 ♦": 3, "4 ♦": 4, "5 ♦": 5, "6 ♦": 6, "7 ♦": 7, "8 ♦": 8, "9 ♦": 9, "10 ♦": 10, "J ♦": 10, "Q ♦": 10, "K ♦": 10, "A ♦": None, "2 ♥": 2, "3 ♥": 3, "4 ♥": 4, "5 ♥": 5, "6 ♥": 6, "7 ♥": 7, "8 ♥": 8, "9 ♥": 9, "10 ♥": 10, "J ♥": 10, "Q ♥": 10, "K ♥": 10, "A ♥": None, "2 ♠": 2, "3 ♠": 3, "4 ♠": 4, "5 ♠": 5, "6 ♠": 6, "7 ♠": 7, "8 ♠": 8, "9 ♠": 9, "10 ♠": 10, "J ♠": 10, "Q ♠": 10, "K ♠": 10, "A ♠": None}

    def __init__(self):
        self.available_cards = list(self.cards.keys())

    def remove_card(self, dealt_card):
        self.available_cards.remove(dealt_card)

class Game:
    def __init__(self):
        # Instantiate global objects of "player", "dealer" and "card_deck" and give player default amount of money
        global player, dealer, card_deck

        player = Person("player")
        player.money = 1000
        dealer = Person("dealer")
        card_deck = CardDeck()

        # Start game mechanism with "welcome" function
        self.welcome()

    def welcome(self):
        print(f"\nWelcome to the casino! You have arrived with {player.money:,} {self.dollars(player.money)}.")

        # Print highscore if it exists
        try:
            with open("highscore.txt") as highscore:
                print(f"\nYour best ever result was when you left the casino with {int(highscore.readline().strip()):,} dollars on {highscore.readline()}.")
        except FileNotFoundError:
            pass

        time.sleep(1)
        self.bet_input()

    def bet_input(self):
        # Input bet amount
        while True:
            try:
                player.bet = int(input(f"\nHow much money would you like to bet on the next game? You have {player.money:,} {self.dollars(player.money)} available.\n"))
                if player.bet not in range(1, player.money + 1):
                    raise ValueError
            except ValueError:
                print(f"Invalid answer. Please enter a whole number within the interval 1-{player.money:,}.")
                continue
            break

        # Immediately subtract bet amount from money and print confirmation
        player.money -= player.bet
        print(f"You have bet {player.bet:,} {self.dollars(player.bet)}. You have {player.money:,} {self.dollars(player.money)} available.")

        self.game_start()

    def game_start(self):
        # Set/reset player's and dealer's hands to empty and replenish card deck to full
        player.cards = []
        dealer.cards = []
        card_deck.available_cards = list(card_deck.cards.keys())

        # Set/reset variables used for "split" games to empty strings
        player.split_game = ""
        player.split_first_game_result = ""
        player.split_second_game_result = ""
        dealer.result = ""

        # Deal starting cards to player and dealer
        player.deal_card()
        dealer.deal_card()
        player.deal_card()

        # If player has blackjack, increase total by 100
        if player.total == 21:
            player.total += 100

        # Print starting cards and totals
        player.print_cards()
        player.print_total()
        dealer.print_cards()
        dealer.print_total()

        # If player has blackjack, print message
        if player.total == 121:
            print("\nYou have a blackjack!")

        # Dealer's first card is an ace - if player has any money, continue to player's decision on whether to take insurance
        if (dealer.cards[0])[0] == "A" and player.money > 0:
            self.insurance()
        # Dealer's first card is not an ace and/or player has no money - continue to player's first decision
        else:
            self.first_decision_input()

    def insurance(self):
        # Input decision on whether to take insurance
        while True:
            try:
                player.insurance_decision = int(input(f"""\

The dealer's first card is an ace. Would you like to take insurance?

(1): yes
(2): no

"""))
                if player.insurance_decision not in range(1, 3):
                    raise ValueError
            except ValueError:
                print("Invalid answer. Please enter a whole number within the interval 1-2.")
                continue
            break

        # Player wants to take insurance
        if player.insurance_decision == 1:

            # Maximum insurance bet is either half of game bet or player's remaining money, whichever is lower
            player.max_allowed_insurance_bet = player.bet // 2
            if player.max_allowed_insurance_bet > player.money:
                player.max_insurance_bet = player.money
            else:
                player.max_insurance_bet = player.max_allowed_insurance_bet

            # Input amount of insurance bet
            while True:
                try:
                    print(f"\nThe maximum allowed insurance bet is {player.max_allowed_insurance_bet:,} {self.dollars(player.max_allowed_insurance_bet)} and you have {player.money:,} {self.dollars(player.money)} available.")
                    player.insurance_bet = int(input(f"\nHow much money would you like to bet on the insurance?\n"))
                    if player.insurance_bet not in range(1, player.max_insurance_bet + 1):
                        raise ValueError
                except ValueError:
                    print(f"Invalid answer. Please enter a whole number within the interval 1-{player.max_insurance_bet:,}.")
                    continue
                break

            # Subtract insurance bet from money and print confirmation
            player.money -= player.insurance_bet
            print(f"You have bet {player.insurance_bet:,} {self.dollars(player.insurance_bet)} on the insurance. You have {player.money:,} {self.dollars(player.money)} available.")               

            # Immediately deal dealer's second card - deviation from standard procedure
            time.sleep(1)
            print("\nChecking the dealer's second card!")
            dealer.deal_card()
            dealer.print_cards()
            time.sleep(1)

            # Dealer has blackjack - increase total by 100, win insurance bet and evaluate game bet immediately
            if dealer.total == 21:
                dealer.total += 100
                dealer.print_total()
                print("\nThe dealer has a blackjack!")

                player.insurance_winnings = player.insurance_bet * 3
                player.money += player.insurance_winnings
                print(f"\nYou have won your insurance bet! You have won {player.insurance_winnings:,} {self.dollars(player.insurance_winnings)}. You now have {player.money:,} {self.dollars(player.money)} available.")

                self.evaluate()

            # Dealer doesn't have blackjack - lose insurance bet and continue to player's first decision
            else:
                dealer.print_total()
                print("\nThe dealer does not have a blackjack!")
                print(f"\nYou have lost your insurance bet! You have {player.money:,} {self.dollars(player.money)} available.")
                time.sleep(1)

                print("\nContinuing your round!")
                player.print_cards()
                player.print_total()
                self.first_decision_input()

        # Player doesn't want to take insurance - continue to player's first decision
        else:
            self.first_decision_input()

    def first_decision_input(self):
        # When playing "split" with two aces, player receives only exactly one more card for each hand, then round ends
        if player.split_game == "first" and (player.cards[0])[0] == "A":
            self.split_second_game_start()
        elif player.split_game == "second" and (player.cards[0])[0] == "A":
            self.dealer_round_start()

        # Player has blackjack
        elif player.total == 121:
            # If dealer can't also have blackjack (i.e. their first card is not 10, J, Q, K or A), player wins immediately
            if (dealer.cards[0])[0] not in ["1", "J", "Q", "K", "A"]:
                self.win()
            # If dealer may also have blackjack, begin dealer's round
            else:
                self.dealer_round_start()

        # Player doesn't have blackjack - input first decision
        else:
            time.sleep(1)

            # Options "hit", "stand" and "surrender" are always enabled
            player.options_list = ["(1): hit", "(2): stand", "(3): surrender"]
            # Other options are enabled only if player has enough money to double their bet and if hand hasn't been split
            if player.money >= player.bet and player.split_game == "":
                # In cases described above, always enable "double" option
                player.options_list.append("(4): double")
                # If both first cards are of same value, enable also "split" option
                if (player.cards[0])[0] == (player.cards[1])[0]:
                    player.options_list.append("(5): split")
            # Join list into one string with each option on new line
            player.options_string = "\n".join(player.options_list)

            # Input player's decision
            while True:
                try:
                    player.first_decision = int(input(f"""\

What would you like to do?

{player.options_string}

"""))
                    if player.first_decision not in range(1, len(player.options_list) + 1):
                        raise ValueError
                except ValueError:
                    print(f"Invalid answer. Please enter a whole number within the interval 1-{len(player.options_list)}.")
                    continue
                break

            # Continue according to player's decision
            if player.first_decision == 1:
                self.hit(player)
            elif player.first_decision == 2:
                # If playing first split hand, continue to second split hand - otherwise continue to dealer's round
                if player.split_game == "first":
                    self.split_second_game_start()
                else:
                    self.dealer_round_start()
            elif player.first_decision == 3:
                self.surrender()
            elif player.first_decision == 4:
                self.double()
            else:
                self.split_first_game_start()

    def decision_input(self):
        time.sleep(1)

        # Options "surrender" and "split" are never enabled anymore
        # Options "hit" and "stand" are always enabled
        player.options_list = ["(1): hit", "(2): stand"]
        # If player has enough money to double their bet and if hand hasn't been split, enable "double" option
        if player.money >= player.bet and player.split_game == "":
            player.options_list.append("(3): double")
        # Join list into one string with each option on new line
        player.options_string = "\n".join(player.options_list)

        # Input player's decision
        while True:
            try:
                player.decision = int(input(f"""\

What would you like to do?

{player.options_string}

"""))
                if player.decision not in range(1, len(player.options_list) + 1):
                    raise ValueError
            except ValueError:
                print(f"Invalid answer. Please enter a whole number within the interval 1-{len(player.options_list)}.")
                continue
            break

        # Continue according to player's decision
        if player.decision == 1:
            self.hit(player)
        elif player.decision == 2:
            # If playing first split hand, continue to second split hand - otherwise continue to dealer's round
            if player.split_game == "first":
                self.split_second_game_start()
            else:
                self.dealer_round_start()
        else:
            self.double()

    def player_total_check(self):
        # If total exceeds 21, player is busted
        if player.total > 21:
            time.sleep(1)
            print("\nYou are busted!")
            time.sleep(1)

            # If playing "split", only the current hand is lost - evaluation is done later within "split_evaluate_game"
            if player.split_game == "first":
                player.split_first_game_result = "bust"
                self.split_second_game_start()
            elif player.split_game == "second":
                player.split_second_game_result = "bust"
                # If first hand was also busted or surrendered, dealer's round is skipped and game is evaluated
                if player.split_first_game_result in ["bust", "surrender"]:
                    self.split_evaluate_start()
                # Otherwise, begin dealer's round
                else:
                    self.dealer_round_start()

            # If not playing "split", player loses game immediately
            else:
                self.lose()

        # If total is 21 - but not soft 21 - player's round ends automatically
        elif player.total == 21 and player.ace != "soft/hard":
            # If playing first split hand, continue to second split hand - otherwise continue to dealer's round
            if player.split_game == "first":
                self.split_second_game_start()
            else:
                self.dealer_round_start()

        # If total is less than 21 or equal to soft 21, input player's decision
        else:
            self.decision_input()

    def hit(self, person):
    # Deal one new card from deck, print new cards and total, run total check to determine further procedure
        if person == player:
            player.deal_card()
            player.print_cards()
            player.print_total()
            self.player_total_check()
        else:
            dealer.deal_card()
            dealer.print_cards()
            dealer.print_total()
            self.dealer_total_check()

    def surrender(self):
        # If playing split hand, only the current hand is surrendered - evaluation is done later within "split_evaluate_game"
        if player.split_game == "first":
            player.split_first_game_result = "surrender"
            self.split_second_game_start()
        elif player.split_game == "second":
            player.split_second_game_result = "surrender"
            # If first hand was also surrendered or busted, dealer's round is skipped and game is evaluated
            if player.split_first_game_result in ["bust", "surrender"]:
                self.split_evaluate_start()
            # Otherwise, begin dealer's round
            else:
                self.dealer_round_start()

        # If not playing split hand, player is returned half of bet and game immediately ends - move to "play_again"
        else:
            player.payback = player.bet // 2
            player.money += player.payback
            print(f"\nYou have surrendered! You have been returned {player.payback:,} {self.dollars(player.payback)}. You now have {player.money:,} {self.dollars(player.money)} available.")
            self.play_again()

    def double(self):
        # Subtract money, print confirmation and double bet amount
        player.money -= player.bet
        print(f"You have bet an additional {player.bet:,} {self.dollars(player.bet)}. You have {player.money:,} {self.dollars(player.money)} available.")               
        player.bet *= 2

        # Deal one more card and print confirmation
        player.deal_card()
        player.print_cards()
        player.print_total()

        # If total exceeds 21, player loses immediately
        if player.total > 21:
            print("\nYou are busted!")
            self.lose()
        # If total doesn't exceed 21, dealer's round begins
        else:
            self.dealer_round_start()

    def split_first_game_start(self):
        # Subtract money for additional bet and print confirmation
        player.money -= player.bet
        print(f"You have bet an additional {player.bet:,} {self.dollars(player.bet)} on the second hand. You have {player.money:,} {self.dollars(player.money)} available.")               

        # Deal two more cards, create second hand and move 2nd and 4th dealt card into it
        # This leaves 1st and 3rd dealt card in first hand - both starting hands are created now
        player.deal_card()
        player.deal_card()
        player.second_cards = []
        player.second_cards.append(player.cards.pop(1))
        player.second_cards.append(player.cards.pop(2))

        # Play first split hand - print cards and total, continue to player's first decision
        player.split_game = "first"
        print("\nPlaying your first hand!")
        player.update_total()
        player.print_cards()
        player.print_total()
        self.first_decision_input()

    def split_second_game_start(self):
    # Play second split hand
        player.split_game = "second"
        print("\nPlaying your second hand!")

        # Switch active hand and total - store all cards dealt to first hand aside, then replace cards with second hand
        player.first_cards = player.cards
        player.cards = player.second_cards
        player.update_total()

        # Print cards and total, continue to player's first decision
        player.print_cards()
        player.print_total()
        self.first_decision_input()

    def split_evaluate_start(self):
        # Switch back active hand and total - store all cards dealt to second hand aside, then replace cards with first hand
        player.second_cards = player.cards
        player.cards = player.first_cards
        player.update_total()

        # Set "player.ace" and "dealer.ace" to empty string so that "print_total" never includes soft/hard info
        player.ace = ""
        dealer.ace = ""

        time.sleep(1)
        print("\nEvaluation:")
        print("-----------")
        time.sleep(1)
        print("First hand:")
        print("-----------")

        # Evaluate first game
        self.split_evaluate_game("first")

        # Switch back active hand and total - replace cards with second hand (and discard first hand)
        player.cards = player.second_cards
        player.update_total()

        # Set "player.ace" to empty string again so that "print_total" never includes soft/hard info
        player.ace = ""

        time.sleep(1)
        print("\nSecond hand:")
        print("------------")

        # Evaluate second game
        self.split_evaluate_game("second")

        time.sleep(1)

        # Print confirmation of current available money and move to "play_again"
        print(f"\nYou now have {player.money:,} {self.dollars(player.money)} available.")
        self.play_again()

    def split_evaluate_game(self, game_number):
        if game_number == "first":
            game_result = player.split_first_game_result
        else:
            game_result = player.split_second_game_result

        time.sleep(1)

        # First, check for special results of player or dealer which would mean no actual comparison of totals takes place
        # If player busted or surrendered hand, result doesn't depend on whether dealer busted as well
        if game_result == "bust":
            print("You got busted!")
            print("You have lost!")
        elif game_result == "surrender":
            player.payback = player.bet // 2
            player.money += player.payback
            print("You surrendered!")
            print(f"You have been returned {player.payback:,} {self.dollars(player.payback)}.")
        # Only if player didn't bust or surrender, check whether dealer busted
        elif dealer.result == "bust":
            player.print_total()
            print("The dealer got busted!")
            player.winnings = player.bet * 2
            player.money += player.winnings
            time.sleep(1)
            print(f"\nCongratulations, you have won! You have received {player.winnings:,} {self.dollars(player.winnings)}.")
        # If there are no special results of player or dealer, compare totals
        else:
            player.print_total()
            dealer.print_total()
            time.sleep(1)
            if player.total > dealer.total:
                player.winnings = player.bet * 2
                player.money += player.winnings
                print(f"\nCongratulations, you have won! You have received {player.winnings:,} {self.dollars(player.winnings)}.")                
            elif player.total < dealer.total:
                print("\nYou have lost!")
            else:
                player.money += player.bet
                print(f"\nIt's a tie! You have been returned {player.bet:,} {self.dollars(player.bet)}.")

    def dealer_round_start(self):
        print("\nDealer's round!")

        # If dealer only has one card (i.e. no insurance was taken), deal second card and check for blackjack
        if len(dealer.cards) == 1:
            dealer.deal_card()

            # Dealer has blackjack - increase total by 100, print confirmation and evaluate game immediately
            if dealer.total == 21:
                dealer.total += 100
                dealer.print_cards()
                dealer.print_total()
                print("\nThe dealer has a blackjack!")

                # If playing "split", this "dealer_round_start" function is always called after player's second hand
                # Therefore player's "split_game" will always be "second" at this point - then call "split_evaluate_start"
                if player.split_game == "second":
                    self.split_evaluate_start()
                # If not playing "split", call standard "evaluate"
                else:
                    self.evaluate()

            # Dealer doesn't have blackjack - continue to "dealer_total_check"
            else:
                dealer.print_cards()
                dealer.print_total()
                self.dealer_total_check()

        # If second card was already dealt as part of insurance procedure, continue to "dealer_total_check" right away
        else:
            dealer.print_cards()
            dealer.print_total()
            self.dealer_total_check()

    def dealer_total_check(self):
        # If dealer's total exceeds 21, player wins
        if dealer.total > 21:
            time.sleep(1)
            print("\nThe dealer is busted!")

            # If playing "split", both hands are still evaluated within "split_evaluate_start" function
            if player.split_game == "second":
                dealer.result = "bust"
                self.split_evaluate_start()
            # If not playing "split", continue to "win" right away
            else:
                self.win()

        # If dealer's total is between 17 and 21, dealer's round ends and game is evaluated
        elif dealer.total >= 17:
            time.sleep(1)
            print("\nEnd of dealer's round!")

            # Call respective evaluate function depending on whether playing "split"
            if player.split_game == "second":
                self.split_evaluate_start()
            else:
                self.evaluate()

        # If dealer's total is 16 or less, dealer hits another card (and total is checked again)
        else:
            self.hit(dealer)

    def evaluate(self):
        # Set "player.ace" and "dealer.ace" to empty strings so that "print_total" never includes soft/hard info
        player.ace = ""
        dealer.ace = ""

        time.sleep(1)

        # Print final totals
        print("\nEvaluation:")
        print("-----------")
        player.print_total()
        dealer.print_total()

        time.sleep(1)

        # Evaluate result of game
        if player.total > dealer.total:
            self.win()
        elif player.total < dealer.total:
            self.lose()
        else:
            self.tie()

    def win(self):
        # Bet multiplies by 2.5 if winning hand is blackjack
        if player.total == 121:
            player.winnings = int(player.bet * 2.5)
        # Otherwise bet multiplies by 2
        else:
            player.winnings = player.bet * 2
        player.money += player.winnings
        print(f"\nCongratulations, you have won! You have received {player.winnings:,} {self.dollars(player.winnings)}. You now have {player.money:,} {self.dollars(player.money)} available.")
        self.play_again()

    def lose(self):
        print(f"\nYou have lost! You have {player.money:,} {self.dollars(player.money)} available.")
        self.play_again()

    def tie(self):
        # Bet is returned to player
        player.money += player.bet
        print(f"\nIt's a tie! You have been returned {player.bet:,} {self.dollars(player.bet)}. You have {player.money:,} {self.dollars(player.money)} available.")
        self.play_again()

    def play_again(self):
        time.sleep(1)

        # If player has no more money, print goodbye message and end session
        if player.money == 0:
            print("\nYou have lost all your money! You have been kicked out of the casino.\n")

        # Otherwise input player's decision whether to play another game
        else:
            while True:
                try:
                    player.play_again_decision = int(input("""\

Would you like to play again?

(1): yes
(2): no

"""))
                    if player.play_again_decision not in range(1, 3):
                        raise ValueError
                except ValueError:
                    print("Invalid answer. Please enter a whole number within the interval 1-2.")
                    continue
                break

            if player.play_again_decision == 1:
                # Start new game
                self.bet_input()
            else:
                # Print goodbye message and end session
                print(f"See you later then! You are leaving the casino with {player.money:,} {self.dollars(player.money)}.\n")

                # If highscore file exists, update highscore and date if current score is equal or higher
                try:
                    with open("highscore.txt") as highscore:
                        if player.money >= int(highscore.readline()):
                            with open("highscore.txt", "w") as highscore:
                                highscore.writelines([f"{player.money}\n", f"{datetime.date.today().strftime('%d %b %Y')}"])
                            time.sleep(1)
                            print("Congratulations, this is your best ever result!\n")

                # If highscore file doesn't exist, create one with current score and date
                except FileNotFoundError:
                    with open("highscore.txt", "w") as highscore:
                        highscore.writelines([f"{player.money}\n", f"{datetime.date.today().strftime('%d %b %Y')}"])

    def dollars(self, number):
        # Return singular "dollar" if amount is 1, otherwise return plural "dollars"
        if number == 1:
            return "dollar"
        return "dollars"

# Run entire session mechanism via instantiating "Game" class
game = Game()
