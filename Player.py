import random
from GameLogger import GameLogger


class Player:
    def __init__(self, name, character, is_ai=False):
        self.name = name
        self.character = character
        self.coins = 2  # Starting coins
        self.cards = []  # Starting cards (represents influence)
        self.is_ai = is_ai  # Flag to indicate if this player is AI-controlled

    def display_cards(self):
        """Displays the current cards held by the player, if not AI."""
        if not self.is_ai:
            if self.cards:
                print(f"{self.name}'s cards: {', '.join(self.cards)}")
            else:
                print(f"{self.name} has no cards left.")

    def choose_action(self, game):
        """Allows the player to choose an action, including bluffing."""
        actions = ['income', 'foreign_aid', 'coup', 'tax', 'assassinate', 'steal', 'exchange']
        
        if self.is_ai:
            return self.ai_choose_action(game, actions)
        else:
            print(f"\n{self.name}'s turn. Coins: {self.coins}, Cards: {len(self.cards)}")
            for i, action in enumerate(actions):
                print(f"[{i + 1}] {action}")

            while True:  # Loop until valid input is received
                choice = input("Enter your choice: ")
                if choice.isdigit():
                    choice_index = int(choice) - 1
                    if 0 <= choice_index < len(actions):
                        return actions[choice_index]
                    else:
                        print("Invalid choice. Please enter a number corresponding to an action.")
                else:
                    print("Invalid input. Please enter a number.")

    def draw_card(self, deck):
        """
        Draws a card from the deck and adds it to the player's hand.
        """
        if deck:
            new_card = deck.pop()  # Remove a card from the top of the deck
            self.cards.append(new_card)  # Add the new card to the player's hand
            print(f"{self.name} draws a new card: {new_card}")
        else:
            print(f"No more cards in the deck to draw for {self.name}.")

    def ai_choose_action(self, game, actions):
        """AI randomly chooses an action and a target (if necessary)."""
        chosen_action = random.choice(actions)
        if chosen_action in ['coup', 'assassinate', 'steal']:
            targets = self.get_available_targets(game)
            if targets:
                chosen_target = random.choice(targets)
                print(f"{self.name} (AI) chooses to {chosen_action} targeting {chosen_target.name}")
                return chosen_action, chosen_target
        print(f"{self.name} (AI) chooses to {chosen_action}")
        return chosen_action
        
    def get_available_targets(self, game):
        """Returns a list of players that can be targeted for certain actions."""
        return [player for player in game.players if player != self and player.has_cards()]

    def take_action(self, game):
        """The player takes an action using their character."""
        action = self.choose_action(game)
        target_player = None

        if isinstance(action, tuple):  # Handling AI's action and target
            action, target_player = action

        if action in ['coup', 'assassinate', 'steal']:
            target_player = game.choose_target(self)

        # Execute action through the character, passing the game and target player (if any)
        self.character.action(self, game, target_player)

    def wants_to_challenge(self, acting_player, action):
        """Determines if the player wants to challenge an action."""
        if self.is_ai:
            # AI logic to decide whether to challenge
            # For simplicity, this could be a random decision or based on certain conditions
            return random.choice([True, False])
        else:
            # Ask the human player if they want to challenge
            while True:
                choice = input(f"Do you want to challenge {acting_player.name}'s {action}? (yes/no): ").lower().strip()
                if choice in ['yes', 'no']:
                    return choice == 'yes'
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

    def wants_to_block(self, acting_player, action):
        """Determines if the player wants to block an action."""
        if self.is_ai:
            # AI logic to decide whether to block
            # For simplicity, this could be a random decision or based on certain conditions
            return random.choice([True, False])
        else:
            # Ask the human player if they want to block
            while True:
                choice = input(f"Do you want to block {acting_player.name}'s {action}? (yes/no): ").lower().strip()
                if choice in ['yes', 'no']:
                    return choice == 'yes'
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
    
    def gain_coins(self, amount):
        """Method for the player to gain coins."""
        self.coins += amount

    def lose_coins(self, amount):
        """Method for the player to lose coins. Ensures coins don't go negative."""
        self.coins = max(self.coins - amount, 0)

    def lose_influence(self):
        """Method for the player to lose influence. Influence represents cards in hand."""
        if self.cards:
            lost_card = self.cards.pop()  # Remove a card when losing influence
            if self.is_ai:
                print(f"{self.name} loses a card. Remaining cards: {len(self.cards)}")
            else:
                print(f"{self.name} loses a card: {lost_card}. Remaining cards: {len(self.cards)}")
            if not self.cards:
                print(f"{self.name} has no more influence and is out of the game!")

    def has_cards(self):
        """Check if the player still has cards (influence)."""
        return bool(self.cards)
    
    
    def verify_card(self, action):
        """Verifies if the player has the card related to the action."""

        # Map actions to character names
        action_to_card_map = {
            'income': None,              # Any character can take 'income' action
            'foreign_aid': None,         # Any character can take 'foreign_aid' action
            'coup': None,                # 'Coup' can be done by anyone, doesn't require a specific card
            'tax': 'Duke',               # 'Duke' can take the 'tax' action
            'assassinate': 'Assassin',   # 'Assassin' can take the 'assassinate' action
            'steal': 'Captain',          # 'Captain' can take the 'steal' action
            'exchange': 'Ambassador',    # 'Ambassador' can take the 'exchange' action
            'block_foreign_aid': 'Duke', # 'Duke' can block 'foreign_aid'
            'block_steal': 'Captain',    # 'Captain' can block 'steal'
            'block_steal_ambassador': 'Ambassador', # 'Ambassador' can also block 'steal'
            'block_assassinate': 'Contessa',        # 'Contessa' can block 'assassinate'
    }    

        required_card = action_to_card_map.get(action, None)
        if required_card is None:  # If no specific card is required for the action
            return True  # Cannot bluff if the action doesn't require a card

        # Check if the player has the required card in their hand
        return required_card in self.cards
    
    def shuffle_in_card(self, action, deck):
        """
        Shuffles the player's card associated with the action back into the deck 
        and draws a new card from the deck.
        """
        # Map actions to character names
        action_to_card_map = {
            'income': None,              # Any character can take 'income' action
            'foreign_aid': None,         # Any character can take 'foreign_aid' action
            'coup': None,                # 'Coup' can be done by anyone, doesn't require a specific card
            'tax': 'Duke',               # 'Duke' can take the 'tax' action
            'assassinate': 'Assassin',   # 'Assassin' can take the 'assassinate' action
            'steal': 'Captain',          # 'Captain' can take the 'steal' action
            'exchange': 'Ambassador',    # 'Ambassador' can take the 'exchange' action
            'block_foreign_aid': 'Duke', # 'Duke' can block 'foreign_aid'
            'block_steal': 'Captain',    # 'Captain' can block 'steal'
            'block_steal_ambassador': 'Ambassador', # 'Ambassador' can also block 'steal'
            'block_assassinate': 'Contessa',        # 'Contessa' can block 'assassinate'
        }    

        card_to_shuffle_back = action_to_card_map.get(action, None)
        if card_to_shuffle_back and card_to_shuffle_back in self.cards:
            # Remove the card from the player's hand and add it to the deck
            self.cards.remove(card_to_shuffle_back)
            deck.append(card_to_shuffle_back)

            # Shuffle the deck
            random.shuffle(deck)

            # Draw a new card from the deck
            if deck:
                new_card = deck.pop()
                self.cards.append(new_card)
                print(f"{self.name} draws a new card: {new_card}")
            else:
                print(f"No more cards in the deck to draw for {self.name}.")

    
