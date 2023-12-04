from GameLogger import GameLogger
import random

class Game:
    def __init__(self, players):
        self.players = players
        self.logger = GameLogger()
        self.deck = CardManager.initialize_deck()
        self.turn_manager = TurnManager(self)
        self.action_handler = ActionHandler(self)
        self.challenge_handler = ChallengeHandler(self)

    def action_requires_coins(self, action):
        """Check if the given action requires coins."""
        actions_requiring_coins = ['coup', 'assassinate']
        return action in actions_requiring_coins

    def start_game(self):
        self.logger.log("Game has started")
        CardManager.distribute_cards(self.players, self.deck, self.logger)
        while not self.is_game_over():
            self.turn_manager.play_turn()
        self.announce_winner()
        self.ask_restart_game()

    def is_game_over(self):
        # The game is over if only one or no players have cards left
        active_players = [player for player in self.players if player.has_cards()]
        return len(active_players) <= 1

    def announce_winner(self):
        winner = next((player for player in self.players if player.has_cards()), None)
        if winner:
            self.logger.log(f"Game over! The winner is {winner.name}.")
        else:
            self.logger.log("Game over! No winner.")

    def ask_restart_game(self):
        while True:  # Loop until a valid input is received
            choice = input("Do you want to play again? (yes/no): ").lower().strip()
            if choice == 'yes':
                self.reset_game()
                break  # Break the loop if valid input is received
            elif choice == 'no':
                self.logger.log("Exiting game. Thank you for playing!")
                break  # Break the loop if valid input is received
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    def reset_game(self):
        self.logger.log("Resetting game...")
        # Reset the game state
        self.deck = CardManager.initialize_deck()
        for player in self.players:
            player.cards = []
            player.coins = 2
        # Now pass the logger to the distribute_cards method
        CardManager.distribute_cards(self.players, self.deck, self.logger)
        self.turn_manager.current_turn = 0
        self.start_game()

    def choose_target(self, acting_player):
        valid_targets = [player for player in self.players if player != acting_player and player.has_cards()]
        print("Choose a target:")
        for i, player in enumerate(valid_targets):
            print(f"{i + 1}: {player.name}")

        while True:
            choice = input("Enter the number of the target player: ")
            if choice.isdigit():
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(valid_targets):
                    return valid_targets[choice_index]
                else:
                    print("Invalid choice. Please select a valid target.")
            else:
                print("Invalid input. Please enter a number.")



class TurnManager:
    def __init__(self, game):
        self.game = game
        self.current_turn = 0

    def play_turn(self):
        turn_player = self.game.players[self.current_turn]
        self.game.logger.log(f"{turn_player.name}'s turn begins.")

        action_successful = False  # Initialize action_successful
        while not action_successful:
            action = turn_player.choose_action(self.game)
            action_result = self.game.action_handler.handle_action(turn_player, action)

            # Ensure action_result is a tuple for consistency
            if not isinstance(action_result, tuple):
                action_result = (action_result, 'success' if action_result else 'unspecified')

            action_successful, reason = action_result

            self.game.logger.log(f"Action Result: {action_result}, Successful: {action_successful}, Reason: {reason}")

            if action_successful:
                self.game.logger.log(f"{turn_player.name}'s action was successful.")
            else:
                self.game.logger.log(f"Action failed. Reason: {reason}")
                if reason not in ['insufficient_coins', 'no_target']:
                    break  # End turn on block or challenge failure

        self.next_turn()


    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.game.players)
        self.game.logger.log(f"Turn moves to player index {self.current_turn}.")


class ActionHandler:
    def __init__(self, game):
        self.game = game

    def handle_action(self, player, action):
        # Extract action and target if action is a tuple (for actions like coup, assassinate, steal)
        target = None
        if isinstance(action, tuple):
            action, target = action

        self.game.logger.log(f"{player.name} decides to perform action: {action}")
        # Match the action to the corresponding method
        if action == 'income':
            return self.income(player)
        elif action == 'foreign_aid':
            return self.foreign_aid(player)
        elif action == 'coup':
            return self.coup(player, target)
        elif action == 'tax':
            return self.tax(player)
        elif action == 'assassinate':
            return self.assassinate(player, target)  # Pass target as a separate argument
        elif action == 'steal':
            return self.steal(player, target)  # Pass target as a separate argument
        elif action == 'exchange':
            return self.exchange(player)
        else:
            return False, 'invalid_action'

    def income(self, player):
        self.game.logger.log(f"{player.name} takes Income action.")
        player.gain_coins(1)
        return True, 'success'


    def foreign_aid(self, player):
        self.game.logger.log(f"{player.name} attempts Foreign Aid action.")
        if not self.game.challenge_handler.check_block(player, 'foreign_aid'):
            player.gain_coins(2)
            return True
        return (False, 'blocked')

    def coup(self, player, target=None):
        self.game.logger.log(f"{player.name} attempts Coup action.")
        if player.coins < 7:
            self.game.logger.log(f"{player.name} does not have enough coins to perform a Coup.")
            return False, 'insufficient_coins'

        # If the player is human and no target is specified, prompt for target selection
        if not player.is_ai and target is None:
            target = self.game.choose_target(player)

        # If no target is chosen or available, return a 'no_target' failure
        if target is None:
            self.game.logger.log("No target specified for Coup.")
            return False, 'no_target'

        player.lose_coins(7)
        target.lose_influence()

        return True, 'success'
    
    def tax(self, player):
        self.game.logger.log(f"{player.name} attempts Tax action.")
        if self.game.challenge_handler.resolve_challenge(player, 'tax'):
            return (False, 'challenge_failed')
        player.gain_coins(3)
        return True

    def assassinate(self, player, target=None):
        self.game.logger.log(f"{player.name} attempts Assassinate action.")
        if player.coins < 3:
            self.game.logger.log(f"{player.name} does not have enough coins to perform an Assassination.")
            return False, 'insufficient_coins'

        # If the player is AI, target is already determined.
        # If the player is human, choose a target.
        if not player.is_ai and target is None:
            target = self.game.choose_target(player)

        if target is None:
            self.game.logger.log("No target specified for Assassinate.")
            return False, 'no_target'

        player.lose_coins(3)
        if not self.game.challenge_handler.check_block(player, 'assassinate'):
            target.lose_influence()
            return True, 'success'
        else:
            return False, 'blocked'



    def steal(self, player, target=None):
        self.game.logger.log(f"{player.name} attempts Steal action.")

        # If the player is AI, the target is already determined.
        # If the player is human, choose a target.
        if not player.is_ai and target is None:
            target = self.game.choose_target(player)

        if target is None:
            self.game.logger.log("No target specified for Steal.")
            return False, 'no_target'

        if not self.game.challenge_handler.check_block(player, 'steal'):
            stolen_amount = min(target.coins, 2)
            target.lose_coins(stolen_amount)
            player.gain_coins(stolen_amount)
            return True, 'success'
        return False, 'blocked'


    def exchange(self, player):
        self.game.logger.log(f"{player.name} attempts Exchange action.")
        if self.game.challenge_handler.resolve_challenge(player, 'exchange'):
            return (False, 'challenge_failed')  # Unsuccessful if challenged and lost

        num_cards_to_exchange = min(len(player.cards), 2)  # Number of cards to exchange

        # Check if the player is AI
        if player.is_ai:
            # AI logic for card exchange
            returned_cards = player.cards[:num_cards_to_exchange]
            player.cards = player.cards[num_cards_to_exchange:] + [self.game.deck.pop() for _ in range(num_cards_to_exchange)]
            self.game.deck.extend(returned_cards)
        else:
            # Human player chooses cards to exchange
            print(f"Your cards: {player.cards}")
            chosen_indices = []

            for i in range(num_cards_to_exchange):
                while True:
                    try:
                        choice = int(input(f"Choose card {i + 1} to exchange (1-{len(player.cards)}): ")) - 1
                        if 0 <= choice < len(player.cards) and choice not in chosen_indices:
                            chosen_indices.append(choice)
                            break
                        else:
                            print("Invalid choice. Please enter a valid card number.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")

            # Exchange the chosen cards with the deck
            chosen_cards = [player.cards[i] for i in chosen_indices]
            for i in sorted(chosen_indices, reverse=True):
                player.cards.pop(i)  # Remove chosen cards from player's hand

            player.cards.extend([self.game.deck.pop() for _ in range(num_cards_to_exchange)])
            self.game.deck.extend(chosen_cards)

        random.shuffle(self.game.deck)  # Shuffle the deck after the exchange

        # Display player's new cards after exchange
        if not player.is_ai:
            print(f"{player.name}'s new cards: {', '.join(player.cards)}")
        self.game.logger.log(f"{player.name} has exchanged cards.")
        
        return True  # Successful exchange


class ChallengeHandler:
    def __init__(self, game):
        self.game = game

    def check_block(self, acting_player, action):
        self.game.logger.log(f"Checking for blocks against {acting_player.name}'s action: {action}")
        for player in self.game.players:
            if player != acting_player and player.wants_to_block(acting_player, action):
                self.game.logger.log(f"{player.name} is attempting to block {acting_player.name}'s {action}.")
                if self.resolve_block(acting_player, player, action) is None:
                    self.game.logger.log("Error resolving block. Continuing without block.")
                    return False
                return True
        return False

    def resolve_block(self, acting_player, blocking_player, action):
        self.game.logger.log(f"{acting_player.name} is facing a block attempt by {blocking_player.name} on {action}.")
        challenge_decision = acting_player.wants_to_challenge(blocking_player, 'block')
        if challenge_decision is None:
            self.game.logger.log(f"Error getting {acting_player.name}'s decision to challenge the block.")
            return None
        if challenge_decision:
            self.game.logger.log(f"{acting_player.name} challenges {blocking_player.name}'s block!")
            return self.challenge_action(blocking_player, acting_player, 'block')
        return True  # Block is successful if not challenged

    def resolve_challenge(self, acting_player, action):
        self.game.logger.log(f"Resolving challenges against {acting_player.name}'s action: {action}")
        for player in self.game.players:
            if player != acting_player and player.wants_to_challenge(acting_player, action):
                self.game.logger.log(f"{player.name} challenges {acting_player.name}'s {action}!")
                if self.challenge_action(acting_player, player, action) is None:
                    self.game.logger.log("Error resolving challenge. Continuing without resolution.")
                    return False
                return True
        return False

    def challenge_action(self, acting_player, challenging_player, action):
        self.game.logger.log(f"{acting_player.name} is being challenged by {challenging_player.name} on {action}.")
        is_bluffing = not acting_player.verify_card(action)
        if is_bluffing is None:
            self.game.logger.log("Error verifying card in challenge.")
            return None

        if is_bluffing:
            self.game.logger.log(f"{acting_player.name} was bluffing during {action}!")
            acting_player.lose_influence()  # The acting player loses an influence
            return True
        else:
            self.game.logger.log(f"{acting_player.name} was not bluffing during {action}!")
            challenging_player.lose_influence()  # The challenging player loses an influence

            # Shuffle and draw a new card for the acting player, if they have less than 2 cards
            if len(acting_player.cards) < 2:
                acting_player.shuffle_in_card(action, self.game.deck)
                acting_player.draw_card(self.game.deck)

            if action == 'block':
                self.game.logger.log(f"The block attempt by {challenging_player.name} has failed.")
                return False  # Block fails if the challenge is unsuccessful

            self.game.logger.log(f"The action by {acting_player.name} is successful after the challenge.")
            return True  # Action is successful if the challenge is unsuccessful



class CardManager:
    @staticmethod
    def initialize_deck():
        characters = ['Duke', 'Assassin', 'Captain', 'Ambassador', 'Contessa']
        deck = characters * 3
        random.shuffle(deck)
        return deck

    @staticmethod
    def distribute_cards(players, deck, logger):
        for player in players:
            player.cards = [deck.pop() for _ in range(2)]
            if player.is_ai:
                logger.log(f"{player.name} received initial cards.")
            else:
                logger.log(f"{player.name} received initial cards: {', '.join(player.cards)}")


