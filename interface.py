import random
from Character import Character, Duke, Assassin, Captain, Ambassador, Contessa   # Make sure to import necessary classes
from GameManagement import Game, TurnManager, ActionHandler, ChallengeHandler, CardManager
from Player import Player
from GameLogger import GameLogger

def main_menu():
    print("Welcome to the Game!")
    print("1: Start New Game")
    print("2: Exit")
    choice = input("Enter your choice: ")
    return choice

def create_1v1_game():
    # Human Player
    human_name = input("Enter your name: ")
    human_character = choose_character()
    human_player = Player(human_name, human_character, is_ai=False)

    # AI Player
    ai_character = choose_character()
    ai_player = Player("AI_Opponent", ai_character, is_ai=True)

    return [human_player, ai_player]

def choose_character():
    characters = ['Duke', 'Assassin', 'Captain', 'Ambassador', 'Contessa']
    return Character(random.choice(characters), 'color')  # Replace 'color' with appropriate logic

def play_game(players):
    game = Game(players)
    game.start_game()
    while not game.is_game_over():
        for player in game.players:
            if player.has_cards():
                player_action(player, game)
            if game.is_game_over():
                break
        game.turn_manager.next_turn()
    game.announce_winner()

def player_action(player, game):
    if player.is_ai:
        ai_action(player, game)
    else:
        # Display player's cards at the start of their turn
        print(f"\n{player.name}'s turn. Coins: {player.coins}, Cards: {', '.join(player.cards)}")
        print("Choose an action:")
        print("1: Income")
        print("2: Foreign Aid")
        print("3: Coup")
        print("4: Tax (Duke)")
        print("5: Assassinate (Assassin)")
        print("6: Steal (Captain)")
        print("7: Exchange (Ambassador)")
        print("8: Block Assassinate (Contessa)")
        # Add more actions as per your game rules if necessary i.e. expansion pack inclusion
        action = input("Enter your action: ")
        handle_action(action, player, game)


def ai_action(player, game):
    # AI logic to choose an action
    action = player.ai_choose_action(game)  # Assuming this method exists in the Player class
    print(f"{player.name} (AI) chooses {action}")
    handle_action(action, player, game)

def handle_action(action, player, game):
    # Map the input to the corresponding action
    if action == '1':
        player.character.action('income', player, game)
    elif action == '2':
        player.character.action('foreign_aid', player, game)
    elif action == '3':
        target_player = choose_target(game, player)
        if target_player:
            player.character.action('coup', player, game, target_player)
    elif action == '4':
        player.character.action('tax', player, game)
    elif action == '5':
        target_player = choose_target(game, player)
        if target_player:
            player.character.action('assassinate', player, game, target_player)
    elif action == '6':
        target_player = choose_target(game, player)
        if target_player:
            player.character.action('steal', player, game, target_player)
    elif action == '7':
        player.character.action('exchange', player, game)
    elif action == '8':
        player.character.counteraction('block_assassinate', player, game)
    else:
        print("Invalid action. Please try again.")

def choose_target(game, acting_player):
    print("Choose a target:")
    for i, player in enumerate(game.players):
        if player != acting_player:
            print(f"{i + 1}: {player.name}")

    while True:
        choice = input("Enter the number of the target player: ")
        if choice.isdigit():
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(game.players) and game.players[choice_index] != acting_player:
                return game.players[choice_index]
            else:
                print("Invalid choice. Please select a valid target.")
        else:
            print("Invalid input. Please enter a number.")


if __name__ == '__main__':
    while True:
        choice = main_menu()
        if choice == '1':
            players = create_1v1_game()
            play_game(players)
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")
