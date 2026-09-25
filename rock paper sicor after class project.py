import random

# Possible choices
choices = ["rock", "paper", "scissors"]


def determine_winner(player, ai):
    """Determine the winner of a round."""
    if player == ai:
        return "tie"

    if (
        (player == "rock" and ai == "scissors")
        or (player == "paper" and ai == "rock")
        or (player == "scissors" and ai == "paper")
    ):
        return "player"

    return "ai"


def ai_choice(history):
    """
    AI strategy:
    - First few rounds: choose randomly.
    - Afterwards: predict the player's most common choice.
    - Choose the move that beats that prediction.
    """
    if len(history) < 3:
        return random.choice(choices)

    # Count the player's previous choices
    counts = {
        "rock": history.count("rock"),
        "paper": history.count("paper"),
        "scissors": history.count("scissors")
    }

    predicted_move = max(counts, key=counts.get)

    # Choose the move that beats the predicted move
    counter_moves = {
        "rock": "paper",
        "paper": "scissors",
        "scissors": "rock"
    }

    return counter_moves[predicted_move]


def main():
    player_score = 0
    ai_score = 0
    ties = 0
    player_history = []

    print("=== Rock Paper Scissors with AI ===")
    print("Type rock, paper, or scissors.")
    print("Type quit to stop playing.\n")

    while True:
        player = input("Your choice: ").lower().strip()

        if player == "quit":
            break

        if player not in choices:
            print("Invalid choice. Please try again.\n")
            continue

        # AI selects its move
        ai = ai_choice(player_history)

        print(f"AI chose: {ai}")

        # Determine winner
        result = determine_winner(player, ai)

        if result == "player":
            player_score += 1
            print("You win!")

        elif result == "ai":
            ai_score += 1
            print("AI wins!")

        else:
            ties += 1
            print("It's a tie!")

        # Remember player's choice
        player_history.append(player)

        # Display score
        print(
            f"Score - You: {player_score} | "
            f"AI: {ai_score} | Ties: {ties}"
        )
        print()


    print("\n=== Final Score ===")
    print(f"You: {player_score}")
    print(f"AI: {ai_score}")
    print(f"Ties: {ties}")
    print("Thanks for playing!")


if __name__ == "__main__":
    main()