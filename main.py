from pigdice_object import PigGame

def main():
    game = PigGame()
    game.display_rules()
    print("\nLet's play Pig!\n")
    while game.play_game():
        pass
    print()
    print("Thanks for playing!")
    print()

if __name__ == "__main__":
    main() 