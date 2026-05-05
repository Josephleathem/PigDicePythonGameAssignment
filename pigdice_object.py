import random
import doctest

class Die:
    def roll(self):
        """
        Roll a six-sided die and return the result.
        
        >>> die = Die()
        >>> result = die.roll()
        >>> 1 <= result <= 6
        True
        """
        return random.randint(1, 6)

    def print_die(self, roll):
        """
        Print an ASCII representation of a six-sided die with
        the given roll.

        Args:
            roll (int): The number rolled on the die.
            
        Doctest:
        >>> die = Die()
        >>> die.print_die(1)
         ------- 
        |       |
        |   *   |
        |       |
         ------- 
        >>> die.print_die(2)
         ------- 
        | *     |
        |       |
        |     * |
         ------- 
        """
        die = [
            " ------- ",
            "|       |",
            "|       |",
            "|       |",
            " ------- "
        ]
        if roll == 1:
            die[2] = "|   *   |"
        elif roll == 2:
            die[1] = "| *     |"
            die[3] = "|     * |"
        elif roll == 3:
            die[1] = "| *     |"
            die[2] = "|   *   |"
            die[3] = "|     * |"
        elif roll == 4:
            die[1] = "| *   * |"
            die[3] = "| *   * |"
        elif roll == 5:
            die[1] = "| *   * |"
            die[2] = "|   *   |"
            die[3] = "| *   * |"
        elif roll == 6:
            die[1] = "| * * * |"
            die[3] = "| * * * |"
        for line in die:
            print(line)

class PigGame:
    def __init__(self):
        self.winning_total = 20
        self.die = Die()
        self.players = []
        self.scores = {}
        self.turns_played = {}

    def display_rules(self):
        """
        Display the rules of the Pig dice game.
        """
        print("~" * 50)
        print("Pig Dice Game Rules:")
        print("1. The game is played by two players.")
        print("2. Players take turns to roll a die as many times as they wish, adding the rolled value to a turn total.")
        print("3. If a player rolls a 1, they score nothing for that turn and it becomes the next player's turn. \n\tHowever, if rolling a 1 gives them exactly the winning point total, they win instead of busting.")
        print("4. A player can choose to hold (stop rolling) to add their turn total to their score.")
        print("5. The first player to reach the set point value without going over wins the game.")
        print("~" * 50)

    def print_scoreboard(self):
        """
        Print the current scores of the players.
        
        Doctest:
        >>> game = PigGame()
        >>> game.scores = {"Player 1": 10, "Player 2": 15}
        >>> game.print_scoreboard()
        <BLANKLINE>
        *****************
        *  SCOREBOARD   *
        *****************
        Player 1: 10
        Player 2: 15
        *****************
        <BLANKLINE>
        """
        print()
        print("*****************")
        print("*  SCOREBOARD   *")
        print("*****************")
        for player, score in self.scores.items():
            print(f"{player}: {score}")
        print("*****************")
        print()

    def play_turn(self, player):
        """
        Play a single turn for the given player.

        Args:
            player (str): The name of the player ("Player 1" or "Player 2").

        Returns:
            int: The total points scored by the player in this turn.
        
        Doctest:
        >>> from unittest.mock import patch
        >>> with patch('builtins.input', side_effect=['y', 'y']):
        ...     with patch('random.randint', side_effect=[5, 6, 1]):
        ...         PigGame().play_turn("Player 1")
        PLAYER 1'S TURN
         ------- 
        | *   * |
        |   *   |
        | *   * |
         ------- 
        You rolled a 5! 
        Your turn total is 5
        <BLANKLINE>
         ------- 
        | * * * |
        |       |
        | * * * |
         ------- 
        You rolled a 6! 
        Your turn total is 11
        <BLANKLINE>
         ------- 
        |       |
        |   *   |
        |       |
         ------- 
        Player 1 rolled a 1! No points earned this turn.
        0
        >>> with patch('builtins.input', side_effect=['n']):
        ...     with patch('random.randint', side_effect=[4]):
        ...         PigGame().play_turn("Player 2")
        PLAYER 2'S TURN
         ------- 
        | *   * |
        |       |
        | *   * |
         ------- 
        You rolled a 4! 
        Your turn total is 4
        <BLANKLINE>
        4
        """
        print(f"{player.upper()}'S TURN")
        turn_total = 0
        roll = self.die.roll()
        while roll != 1:
            self.die.print_die(roll)
            turn_total += roll
            if self.turns_played.get(player, 0) > 0:
                print(f"You rolled a {roll}! \nYour turn total is {turn_total} \nYour current score is {self.scores.get(player, 0)}")
            else:
                print(f"You rolled a {roll}! \nYour turn total is {turn_total}")

            if self.scores.get(player, 0) + turn_total > self.winning_total:
                print(f"Turn total plus current score would exceed winning total ({self.winning_total}); no points given this turn.")
                return 0

            print()
            choice = input("Want to roll again? (y/n) ")
            if choice.lower() == 'n':
                return turn_total
            roll = self.die.roll()

        self.die.print_die(roll)
        # Special rule: if rolling 1 gives exactly the winning point, award it instead of busting.
        required_to_win = self.winning_total - self.scores.get(player, 0)
        if required_to_win == 1:
            print(f"{player} rolled a 1 and needed one point to win! Great catch.")
            return 1

        print(f"{player} rolled a 1! No points earned this turn.")
        return 0

    def play_game(self):
        """
        Play a game of Pig between the two players.
        Returns:
            bool: True if the game should be played again, 
            False otherwise.
        """
        if not self.players:
            self.players.append(input("Enter name for Player 1: "))
            self.players.append(input("Enter name for Player 2: "))
            while True:
                try:
                    winning_input = int(input("Enter winning point total: "))
                    if winning_input > 0:
                        self.winning_total = winning_input
                        break
                    print("Winning point total must be greater than 0.")
                except ValueError:
                    print("Please enter a valid integer for winning point total.")
            print()
        # reset scores and turn count whenever a new game starts (first or replay)
        self.scores = {player: 0 for player in self.players}
        self.turns_played = {player: 0 for player in self.players}

        while all(score < self.winning_total for score in self.scores.values()):
            for player in self.players:
                earned = self.play_turn(player)
                self.scores[player] += earned
                self.turns_played[player] = self.turns_played.get(player, 0) + 1
                self.print_scoreboard()
                if self.scores[player] >= self.winning_total:
                    print(f"{player} wins!")
                    print()
                    again = input("Do you want to play again? (y/n) ").lower()
                    if again == 'y':
                        print()
                        print("The game has been reset.")
                        print()
                    return again == 'y'
        return False

if __name__ == "__main__":
    doctest.testmod(verbose=True)