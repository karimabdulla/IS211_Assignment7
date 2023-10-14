import sys
import argparse
import random
from queue import Queue


class Players(object):


    def __init__(self, players):
        self.__players = players
        self.__current_player = players.get()

    def get_current_player(self):
        # Return the current player
        return self.__current_player

    def get_next_player(self):
        # Add current player back to the end of the queue
        self.__players.put(self.__current_player)
        # Get the next player from the queue and return it
        self.__current_player = self.__players.get()
        return self.__current_player

    def get_players(self):
        # Add current player back to the queue before returning the players
        self.__players.put(self.__current_player)
        return self.__players


class Player(object):

    def __init__(self, name):
        self.__name = name.strip()
        self.__score = 0
        self.__rolls = 0

    def get_name(self):
        # Return the player's name
        return self.__name

    def get_score(self):
        # Return the player's score
        return self.__score

    def get_rolls(self):
        # Return the player's rolls
        return self.__rolls

    def commit_score(self, score, rolls):
        # Update the player's score and roll count
        self.__score += score
        self.__rolls += rolls


class Die(object):

    def __init__(self):
        # Set the seed to 0
        random.seed(0)

    def roll(self):
        # Return a random integer between 1 and 6
        return random.randint(1, 6)


class Game(object):
    def __init__(self, players):
        # Instantiate a Players object with the players queue
        self.__players = Players(players)
        # Instantiate the Die to be used for the current game
        self.__die = Die()

    def start(self):
        # Call the private __turn method to start the game
        self.__turn()

    def __game_over(self):
        # Get the players and create the leaderboard tuple
        leaderboard = ((player.get_name(), player.get_score(), player.get_rolls())
                       for player in list(self.__players.get_players().queue))

        print("\nLEADERBOARD\n")
        # Print leaderboard header border
        print("+-{:<32}-+-{:>10}-+-{:>10}-+".format("-"*32, "-"*10, "-"*10))
        # Print the leaderboard header
        print("| {:<32} | {:>10} | {:>10} |".format(
            'Player', 'Score', '# of Rolls'))
        # Sort by highest scores first and print the details
        for player in sorted(leaderboard,
                             key=lambda player: (player[1]),
                             reverse=True):
            # Print the cell separators
            print("|-{:<32}-+-{:>10}-+-{:>10}-|".format("-"*32, "-"*10, "-"*10))
            # Print the player's details
            print("| {:<32} | {:>10} | {:>10} |".format(
                player[0], player[1], player[2]))

        # Print leaderboard footer border
        print("+-{:<32}-+-{:>10}-+-{:>10}-+".format("-"*32, "-"*10, "-"*10))

    def __turn(self, next_player=False):
        # Get the player for the current turn
        player = self.__players.get_current_player(
        ) if not next_player else self.__players.get_next_player()
        # Keep track of the current score and rolls
        current_score = 0
        rolls = 0
        # Keep track of the turn and game status
        active_turn = True
        game_over = False
        # Let the players know who's turn it is
        print("\n{}, it's your turn. Your current score is {}".format(
            player.get_name(), player.get_score()))

        while active_turn and not game_over:
            # Request the current player's desired action
            action = input(
                "Enter 'r' to roll the die, or 'h' to hold. What you you like to do? ")

            # Player chose to roll
            if action == "r":
                # Roll the die and add to roll total for the turn
                roll = self.__die.roll()
                rolls += 1

                if roll == 1:
                    current_score = 0
                    player.commit_score(current_score, rolls)
                    print("Ouch, {} you rolled a {} and lost all points you accumulated during this turn. Your score for this turn is {}. Your total score is {}.".format(
                        player.get_name(), roll, current_score, player.get_score()))
                    active_turn = False

                else:
                    current_score += roll
                    if (current_score + player.get_score()) >= 100:
                        player.commit_score(current_score, rolls)
                        print("\n\nCongratulations {}, you rolled a {} and your total score is {}. You won the game!"
                              .format(player.get_name(), roll, player.get_score()))
                        game_over, active_turn = True, False
                    else:
                        print("Nice {}! You rolled a {}. Your current score for this turn is {}. Your total score is {}".format(
                            player.get_name(),
                            roll,
                            current_score,
                            current_score + player.get_score()
                        )
                        )

            elif action == "h":
                player.commit_score(current_score, rolls)
                print("{}, you held. Your score for this turn is {}. Your total score is {}.".format(
                    player.get_name(), current_score, player.get_score()))
                active_turn = False
            # The player entered an invalid action
            else:
                print("You entered an invalid action.")

        if not game_over:
            self.__turn(True)
        else:
            self.__game_over()


def main():

    # Setup --numPlayer argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--numPlayers',
                        help='The number of players for the game.',
                        type=int
                        )
    args = parser.parse_args()

    # Check for the numPlayers argument
    player_count = args.numPlayers if args.numPlayers else 2

    # Check to see if there are less than two players
    if player_count < 2:
        print("You entered an invalid number of players. At least two players are required to play this game. Please try again.")
        sys.exit()

    # Create a queue for the players
    players = Queue()

    # Setup Player objects for each player and put them in the players Queue
    for i in range(0, player_count):
        # Request the player's name
        player = Player(input("What is Player {}'s name? "
                              .format(str(i+1))))
        # Add the player to the players queue
        players.put(player)

    # Start the game, passing the players queue to the Game class
    Game(players).start()

    # Exit the program after the game is over
    sys.exit()


if __name__ == '__main__':
    main()