def check_winner(move1, move2):
    """
    Logic game: 
    0: Hòa
    1: Người 1 thắng
    2: Người 2 thắng
    """
    if move1 == move2:
        return 0
    
    # Quy tắc: Búa (ROCK) > Kéo (SCISSORS) > Bao (PAPER) > Búa
    if (move1 == "ROCK" and move2 == "SCISSORS") or \
       (move1 == "SCISSORS" and move2 == "PAPER") or \
       (move1 == "PAPER" and move2 == "ROCK"):
        return 1
    
    return 2