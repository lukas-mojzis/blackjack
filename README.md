# Blackjack
Simple text-based simulator of the gambling game blackjack written in Python.

![Blackjack Demo](https://github.com/lukas-mojzis/blackjack/blob/main/demo.gif "Blackjack Demo")

## Getting Started
You need to install [Python](https://www.python.org/) (version 3.1 or above) to run the game.

The game can then be started from the command line by navigating into the directory where the file `blackjack.py` is placed and running the command `python blackjack.py`.

## Controls
The entire game runs in the command line environment and is controlled by entering numerical commands whenever prompted.

In most cases, a list of all available options is displayed. Each option is assigned a number at the beginning of the line, e.g. (1), (2) or (5). To pick an option, enter its assigned number.

In some cases (when asked how much money you would like to bet), no list of options is displayed. To answer, simply enter a number of your choice.

## Rules Overview
For an explanation of the rules, please refer to the [Wikipedia article on blackjack](https://en.wikipedia.org/wiki/Blackjack) (mainly the section on [rules of play at casinos](https://en.wikipedia.org/wiki/Blackjack#Rules_of_play_at_casinos)). In addition to that, please consider the following:
- There are no other players than you.
- You always play only one position at the table (i.e. you are drawn only one pair of cards at the beginning of each game).
- One standard 52-card deck is used.
- A dealer's hand with a total of "soft 17" must stand (i.e. no more cards are drawn to it).
- Blackjack wins are paid out at 3 to 2 odds (i.e. 1.5 times the bet).
- An insurance side bet is offered when the dealer's first card is an ace.
- After an insurance bet, the dealer is immediately dealt a second card and the insurance bet is immediately evaluated.
- A hand may only be split when both first cards are of the same rank.
- Doubling and re-splitting after splitting are not allowed.
- A 10-valued card and an ace resulting from a split isn't considered a blackjack.
- Hitting split aces is not allowed (i.e. you receive exactly one more card to each split ace).
- The option to surrender a hand (early surrender) is always available, but only as the first decision.
- You start the game with $1,000.

If you lose a hand and have no more money left, the game ends. Otherwise, you are asked whether you want to play another hand. Leave the casino with enough money and you will earn a highscore record!

## Contributing
Any feedback, suggestions and pull requests are welcome!

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Author
[Lukas Mojzis](https://github.com/lukas-mojzis)

You can also contact me via [e-mail](mailto:mojzis.lukas@gmail.com) or [LinkedIn](https://www.linkedin.com/in/lukas-mojzis/).
