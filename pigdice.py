import random
import doctest

def display_rules():
    """
    Display the rules of the Pig dice game.
    """
    print("~" * 50)
    print("Pig Dice Game Rules:")
    print("1. The game is played by two players: Player 1 and Player 2.")
    print("2. Players take turns to roll a die as many times as they wish, adding the rolled value to a turn total.")
    print("3. If a player rolls a 1, they score nothing for that turn and it becomes the next player's turn.")
    print("4. A player can choose to hold (stop rolling) to add their turn total to their score.")
    print("5. The first player to reach or exceed 20 points wins the game.")
    print("~" * 50)

def roll_die():
    """
    Roll a six-sided die and return the result.
    
    >>> result = roll_die()
    >>> 1 <= result <= 6
    True
    """
    return random.randint(1, 6)

def print_die(roll):
    """
    Print an ASCII representation of a six-sided die with
    the given roll.

    Args:
        roll (int): The number rolled on the die.
        
    Doctest:
    >>> print_die(1)
     ------- 
    |       |
    |   *   |
    |       |
     ------- 
    >>> print_die(2)
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

def print_scoreboard(player1_score, player2_score):
    """
    Print the current scores of Player 1 and Player 2.
    
    Args:
        player1_score (int): The score of Player 1.
        player2_score (int): The score of Player 2.
    
    >>> print_scoreboard(10, 15)
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
    print(f"Player 1: {player1_score}")
    print(f"Player 2: {player2_score}")
    print("*****************")
    print()

def play_turn(player):
    """
    Play a single turn for the given player.
    
    Args:
        player (str): The name of the player ("Player 1" or "Player 2").
    
    Returns:
        int: The total points scored by the player in this turn.
    
    >>> from unittest.mock import patch
    >>> with patch('builtins.input', side_effect=['y', 'y']):
    ...     with patch('random.randint', side_effect=[5, 6, 1]):
    ...         play_turn("Player 1")
    PLAYER 1'S TURN
     ------- 
    | *   * |
    |   *   |
    | *   * |
     ------- 
    Total is 5
     ------- 
    | * * * |
    |       |
    | * * * |
     ------- 
    Total is 11
     ------- 
    |       |
    |   *   |
    |       |
     ------- 
    Player 1 rolled a 1! No points earned this turn.
    0
    >>> with patch('builtins.input', side_effect=['n']):
    ...     with patch('random.randint', side_effect=[4]):
    ...         play_turn("Player 2")
    PLAYER 2'S TURN
     ------- 
    | *   * |
    |       |
    | *   * |
     ------- 
    Total is 4
    4
    """
    print(f"{player.upper()}'S TURN")
    turn_total = 0
    roll = roll_die()
    while roll != 1:
        print_die(roll)
        turn_total += roll
        print(f"Total is {turn_total}")
        choice = input("Roll again? (y/n) ")
        if choice.lower() == 'n':
            return turn_total
        roll = roll_die()
    print_die(roll)
    print(f"{player} rolled a 1! No points earned this turn.")
    return 0

def play_game():
    """
    Play a game of Pig between Player 1 and Player 2.
    Returns:
        bool: True if the game should be played again, 
        False otherwise.
    """
    scores = {"Player 1": 0, "Player 2": 0}
    while scores["Player 1"] < 20 and scores["Player 2"] < 20:
        for player in ["Player 1", "Player 2"]:
            scores[player] += play_turn(player)
            print_scoreboard(scores["Player 1"], scores["Player 2"])
            if scores[player] >= 20:
                print(f"{player} wins!")
                return input("Do you want to play again? (y/n) ").lower() == 'y'
    return False

if __name__ == "__main__":
    doctest.testmod(verbose=True)
