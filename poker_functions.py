import pandas as pd
from collections import Counter
from phevaluator.evaluator import evaluate_cards

# definition of all the functions 
# Chen Formula for Texas Hold'em starting hand evaluation
# This program calculates the Chen score for any two-card starting hand.
RANK_VALUES = {
    'A': 10,  # Ace
    'K': 8,
    'Q': 7,
    'J': 6,
    'T': 5,   # Ten
    '9': 4.5,
    '8': 4,
    '7': 3.5,
    '6': 3,
    '5': 2.5,
    '4': 2,
    '3': 1.5,
    '2': 1
}

def chen_score(card1: str, card2: str) -> float:
    """
    This function gets only the 2 starting cards as an input
    and return a calculated chen score. It uses the Chen formula : https://en.wikipedia.org/wiki/Texas_hold_%27em_starting_hands
    
    Arguments
    ---------
    c1: string
           Card 1
    c2: string
           Card 2

    Returns
    --------
    score: float
         Number which represent the strength of the cards analyzed in the input. The higher the number is the stronger the 2 cards are
    """
    try:
        if ((card1 == '') or (card2 == '')):
            return 0

        # Extract rank and suit
        rank1, suit1 = card1[0].upper(), card1[1].lower()
        rank2, suit2 = card2[0].upper(), card2[1].lower()

        if rank1 not in RANK_VALUES or rank2 not in RANK_VALUES:
            raise ValueError("Invalid card rank.")
        if suit1 not in "shdc" or suit2 not in "shdc":
            raise ValueError("Invalid card suit.")

        # Step 1: Base score = highest card value
        high_rank, low_rank = (rank1, rank2) if RANK_VALUES[rank1] >= RANK_VALUES[rank2] else (rank2, rank1)
        score = RANK_VALUES[high_rank]

        # Step 2: Pair bonus
        if rank1 == rank2:
            score *= 2
            if score < 5:
                score = 5  # Minimum for low pairs

        # Step 3: Suited bonus
        if suit1 == suit2:
            score += 2

        # Step 4: Gap penalty
        gap = abs(list(RANK_VALUES.keys()).index(high_rank) - list(RANK_VALUES.keys()).index(low_rank)) - 1
        if gap == 1:
            score -= 1
        elif gap == 2:
            score -= 2
        elif gap == 3:
            score -= 4
        elif gap >= 4:
            score -= 5

        # Step 5: Small gap + connectedness bonus
        if gap <= 1 and RANK_VALUES[low_rank] >= 5:  # 5 or higher
            score += 1

        return round(max(score, 0), 1)  # No negative scores

    except Exception as e:
        print(f"Error: {e}")
        return 0.0
        
def cards_score(c1: str, c2: str, c3: str, c4: str, c5: str, c6: str, c7: str):
    """
    This function gets a minimum of 2 cards and a maximum of 7 cards as an input
    and return a calculated card score. The lower the card score is, the better.
    
    Arguments
    ---------
    c1: string
           Card 1
    c2: string
           Card 2
    c3: string
           Card 3
    c4: string
           Card 4
    c5: string
           Card 5
    c6: string
           Card 6
    c7: string
           Card 7

    Returns
    --------
    cards_score_result: float
         Number which represent the strength of the cards analyzed in the input. The lower the number is the stronger the hands of cards are.
    """
    cards_score_result = 0

    if (len(c1) > 0) & (len(c2) > 0) & (len(c3) == 0) & (len(c4) == 0) & (len(c5) == 0) & (len(c6) == 0) & (len(c7) == 0):
        # find a color not in the list of the first 2 cards
        list_colors = ['d', 'h', 's', 'c']
        c1_color = c1[1:2]
        c2_color = c2[1:2]
        list_colors.remove(c1_color)
        if c1_color != c2_color:
            list_colors.remove(c2_color)
        color_pick = list_colors[0]
        # find 3 other small cards to add to the initial 2 cards
        list_cards = ['2', '3', '4', '5', '6', '7']
        temp_cards_score_result = 0
        max_cards_score_result = 0
        for card3 in list_cards:
            for card4 in list_cards:
                for card5 in list_cards:
                    try:
                        temp_cards_score_result = evaluate_cards(c1, c2, card3 + color_pick, card4 + color_pick, card5 + color_pick)
                        if temp_cards_score_result >= max_cards_score_result:
                            max_cards_score_result = temp_cards_score_result
                    except Exception:
                        pass
        cards_score_result = max_cards_score_result
    elif (len(c1) > 0) & (len(c2) > 0) & (len(c3) > 0) & (len(c4) > 0) & (len(c5) > 0) & (len(c6) == 0) & (len(c7) == 0):
        cards_score_result = evaluate_cards(c1, c2, c3, c4, c5)
    elif (len(c1) > 0) & (len(c2) > 0) & (len(c3) > 0) & (len(c4) > 0) & (len(c5) > 0) & (len(c6) > 0) & (len(c7) == 0):
        cards_score_result = evaluate_cards(c1, c2, c3, c4, c5, c6)
    elif (len(c1) > 0) & (len(c2) > 0) & (len(c3) > 0) & (len(c4) > 0) & (len(c5) > 0) & (len(c6) > 0) & (len(c7) > 0):
        cards_score_result = evaluate_cards(c1, c2, c3, c4, c5, c6, c7)
    
    return cards_score_result
    
def calculate_nb_straight_player_cards(stage, c1: str, c2: str, c3: str, c4: str, c5: str, c6: str, c7: str):
    """
    This function calculates the field nb_straight_player_cards
    
    Arguments
    ---------
    stage: string
            The stage of the game
    c1: string
           Card 1
    c2: string
           Card 2
    c3: string
           Card 3
    c4: string
           Card 4
    c5: string
           Card 5
    c6: string
           Card 6
    c7: string
           Card 7

    Returns
    --------
    nb_straight_player_cards: float
         Number which represent the number of straight player cards
    """
    # we need to know just the cards without their colors
    c1s = c1[:1]
    c2s = c2[:1]
    c3s = c3[:1]
    c4s = c4[:1]
    c5s = c5[:1]
    c6s = c6[:1]
    c7s = c7[:1]
    # Bucket 1-5
    bucket_list = ['A', '2', '3', '4', '5']
    bucket_A_5_count = 0
    if c1s in bucket_list:
        bucket_A_5_count = bucket_A_5_count + 1
    if (c2s in bucket_list) & (c1s != c2s):
        bucket_A_5_count = bucket_A_5_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list) & (c3s != c1s) & (c3s != c2s):
        bucket_A_5_count = bucket_A_5_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c1s) & (c4s != c2s) & (c4s != c3s):
        bucket_A_5_count = bucket_A_5_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) & (c5s != c1s) & (c5s != c2s) & (c5s != c3s) & (c5s != c4s):
        bucket_A_5_count = bucket_A_5_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c1s) & (c6s != c2s) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_A_5_count = bucket_A_5_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c1s) & (c7s != c2s) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_A_5_count = bucket_A_5_count + 1

    # Bucket 2-6
    bucket_list = ['2', '3', '4', '5', '6']
    bucket_2_6_count = 0
    if c1s in bucket_list:
        bucket_2_6_count = bucket_2_6_count + 1
    if (c2s in bucket_list) & (c1s != c2s):
        bucket_2_6_count = bucket_2_6_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list) & (c3s != c1s) & (c3s != c2s):
        bucket_2_6_count = bucket_2_6_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c1s) & (c4s != c2s) & (c4s != c3s):
        bucket_2_6_count = bucket_2_6_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) & (c5s != c1s) & (c5s != c2s) & (c5s != c3s) & (c5s != c4s):
        bucket_2_6_count = bucket_2_6_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c1s) & (c6s != c2s) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_2_6_count = bucket_2_6_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c1s) & (c7s != c2s) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_2_6_count = bucket_2_6_count + 1

    # Bucket 3-7
    bucket_list = ['3', '4', '5', '6', '7']
    bucket_3_7_count = 0
    if c1s in bucket_list:
        bucket_3_7_count = bucket_3_7_count + 1
    if (c2s in bucket_list) & (c1s != c2s):
        bucket_3_7_count = bucket_3_7_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list) & (c3s != c1s) & (c3s != c2s):
        bucket_3_7_count = bucket_3_7_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c1s) & (c4s != c2s) & (c4s != c3s):
        bucket_3_7_count = bucket_3_7_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) & (c5s != c1s) & (c5s != c2s) & (c5s != c3s) & (c5s != c4s):
        bucket_3_7_count = bucket_3_7_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c1s) & (c6s != c2s) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_3_7_count = bucket_3_7_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c1s) & (c7s != c2s) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_3_7_count = bucket_3_7_count + 1

    # Bucket 4-8
    bucket_list = ['4', '5', '6', '7', '8']
    bucket_4_8_count = 0
    if c1s in bucket_list:
        bucket_4_8_count = bucket_4_8_count + 1
    if (c2s in bucket_list) & (c1s != c2s):
        bucket_4_8_count = bucket_4_8_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list) & (c3s != c1s) & (c3s != c2s):
        bucket_4_8_count = bucket_4_8_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c1s) & (c4s != c2s) & (c4s != c3s):
        bucket_4_8_count = bucket_4_8_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) & (c5s != c1s) & (c5s != c2s) & (c5s != c3s) & (c5s != c4s):
        bucket_4_8_count = bucket_4_8_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c1s) & (c6s != c2s) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_4_8_count = bucket_4_8_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c1s) & (c7s != c2s) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_4_8_count = bucket_4_8_count + 1

    # Bucket 5-9
    bucket_list = ['5', '6', '7', '8', '9']
    bucket_5_9_count = 0
    if c1s in bucket_list:
        bucket_5_9_count = bucket_5_9_count + 1
    if (c2s in bucket_list) & (c1s != c2s):
        bucket_5_9_count = bucket_5_9_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list) & (c3s != c1s) & (c3s != c2s):
        bucket_5_9_count = bucket_5_9_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c1s) & (c4s != c2s) & (c4s != c3s):
        bucket_5_9_count = bucket_5_9_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) & (c5s != c1s) & (c5s != c2s) & (c5s != c3s) & (c5s != c4s):
        bucket_5_9_count = bucket_5_9_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c1s) & (c6s != c2s) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_5_9_count = bucket_5_9_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c1s) & (c7s != c2s) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_5_9_count = bucket_5_9_count + 1

    # Bucket 6-T
    bucket_list = ['6', '7', '8', '9', 'T']
    bucket_6_T_count = 0
    if c1s in bucket_list:
        bucket_6_T_count = bucket_6_T_count + 1
    if (c2s in bucket_list) & (c1s != c2s):
        bucket_6_T_count = bucket_6_T_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list) & (c3s != c1s) & (c3s != c2s):
        bucket_6_T_count = bucket_6_T_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c1s) & (c4s != c2s) & (c4s != c3s):
        bucket_6_T_count = bucket_6_T_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) & (c5s != c1s) & (c5s != c2s) & (c5s != c3s) & (c5s != c4s):
        bucket_6_T_count = bucket_6_T_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c1s) & (c6s != c2s) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_6_T_count = bucket_6_T_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c1s) & (c7s != c2s) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_6_T_count = bucket_6_T_count + 1

    # Bucket 7-J
    bucket_list = ['7', '8', '9', 'T', 'J']
    bucket_7_J_count = 0
    if c1s in bucket_list:
        bucket_7_J_count = bucket_7_J_count + 1
    if (c2s in bucket_list) & (c1s != c2s):
        bucket_7_J_count = bucket_7_J_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list) & (c3s != c1s) & (c3s != c2s):
        bucket_7_J_count = bucket_7_J_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c1s) & (c4s != c2s) & (c4s != c3s):
        bucket_7_J_count = bucket_7_J_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) & (c5s != c1s) & (c5s != c2s) & (c5s != c3s) & (c5s != c4s):
        bucket_7_J_count = bucket_7_J_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c1s) & (c6s != c2s) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_7_J_count = bucket_7_J_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c1s) & (c7s != c2s) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_7_J_count = bucket_7_J_count + 1

    # Bucket 8-Q
    bucket_list = ['8', '9', 'T', 'J', 'Q']
    bucket_8_Q_count = 0
    if c1s in bucket_list:
        bucket_8_Q_count = bucket_8_Q_count + 1
    if (c2s in bucket_list) & (c1s != c2s):
        bucket_8_Q_count = bucket_8_Q_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list) & (c3s != c1s) & (c3s != c2s):
        bucket_8_Q_count = bucket_8_Q_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c1s) & (c4s != c2s) & (c4s != c3s):
        bucket_8_Q_count = bucket_8_Q_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) & (c5s != c1s) & (c5s != c2s) & (c5s != c3s) & (c5s != c4s):
        bucket_8_Q_count = bucket_8_Q_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c1s) & (c6s != c2s) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_8_Q_count = bucket_8_Q_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c1s) & (c7s != c2s) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_8_Q_count = bucket_8_Q_count + 1

    # Bucket 9-K
    bucket_list = ['9', 'T', 'J', 'Q', 'K']
    bucket_9_K_count = 0
    if c1s in bucket_list:
        bucket_9_K_count = bucket_9_K_count + 1
    if (c2s in bucket_list) & (c1s != c2s):
        bucket_9_K_count = bucket_9_K_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list) & (c3s != c1s) & (c3s != c2s):
        bucket_9_K_count = bucket_9_K_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c1s) & (c4s != c2s) & (c4s != c3s):
        bucket_9_K_count = bucket_9_K_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) & (c5s != c1s) & (c5s != c2s) & (c5s != c3s) & (c5s != c4s):
        bucket_9_K_count = bucket_9_K_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c1s) & (c6s != c2s) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_9_K_count = bucket_9_K_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c1s) & (c7s != c2s) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_9_K_count = bucket_9_K_count + 1

    # Bucket T-A
    bucket_list = ['T', 'J', 'Q', 'K', 'A']
    bucket_T_A_count = 0
    if c1s in bucket_list:
        bucket_T_A_count = bucket_T_A_count + 1
    if (c2s in bucket_list) & (c1s != c2s):
        bucket_T_A_count = bucket_T_A_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list) & (c3s != c1s) & (c3s != c2s):
        bucket_T_A_count = bucket_T_A_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c1s) & (c4s != c2s) & (c4s != c3s):
        bucket_T_A_count = bucket_T_A_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) & (c5s != c1s) & (c5s != c2s) & (c5s != c3s) & (c5s != c4s):
        bucket_T_A_count = bucket_T_A_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c1s) & (c6s != c2s) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_T_A_count = bucket_T_A_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c1s) & (c7s != c2s) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_T_A_count = bucket_T_A_count + 1

    nb_straight_player_cards = max([bucket_A_5_count, bucket_2_6_count, bucket_3_7_count, bucket_4_8_count, bucket_5_9_count, bucket_6_T_count, bucket_7_J_count, bucket_8_Q_count, bucket_9_K_count, bucket_T_A_count])

    
    return nb_straight_player_cards
    
def calculate_nb_straight_community_cards(stage, c3: str, c4: str, c5: str, c6: str, c7: str):
    """
    This function calculates the field nb_straight_community_cards
    
    Arguments
    ---------
    stage: string
            The stage of the game
    c3: string
           Card 3
    c4: string
           Card 4
    c5: string
           Card 5
    c6: string
           Card 6
    c7: string
           Card 7

    Returns
    --------
    nb_straight_community_cards: float
         Number which represent the number of straight community cards
    """
    # we need to know just the cards without their colors
    c3s = c3[:1]
    c4s = c4[:1]
    c5s = c5[:1]
    c6s = c6[:1]
    c7s = c7[:1]
    # Bucket 1-5
    bucket_list = ['A', '2', '3', '4', '5']
    bucket_A_5_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list):
        bucket_A_5_count = bucket_A_5_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c3s):
        bucket_A_5_count = bucket_A_5_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) &  (c5s != c3s) & (c5s != c4s):
        bucket_A_5_count = bucket_A_5_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_A_5_count = bucket_A_5_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_A_5_count = bucket_A_5_count + 1

    # Bucket 2-6
    bucket_list = ['2', '3', '4', '5', '6']
    bucket_2_6_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list):
        bucket_2_6_count = bucket_2_6_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c3s):
        bucket_2_6_count = bucket_2_6_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) &  (c5s != c3s) & (c5s != c4s):
        bucket_2_6_count = bucket_2_6_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_2_6_count = bucket_2_6_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_2_6_count = bucket_2_6_count + 1

    # Bucket 3-7
    bucket_list = ['3', '4', '5', '6', '7']
    bucket_3_7_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list):
        bucket_3_7_count = bucket_3_7_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c3s):
        bucket_3_7_count = bucket_3_7_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) &  (c5s != c3s) & (c5s != c4s):
        bucket_3_7_count = bucket_3_7_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_3_7_count = bucket_3_7_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_3_7_count = bucket_3_7_count + 1

    # Bucket 4-8
    bucket_list = ['4', '5', '6', '7', '8']
    bucket_4_8_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list):
        bucket_4_8_count = bucket_4_8_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c3s):
        bucket_4_8_count = bucket_4_8_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) &  (c5s != c3s) & (c5s != c4s):
        bucket_4_8_count = bucket_4_8_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_4_8_count = bucket_4_8_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_4_8_count = bucket_4_8_count + 1

    # Bucket 5-9
    bucket_list = ['5', '6', '7', '8', '9']
    bucket_5_9_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list):
        bucket_5_9_count = bucket_5_9_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c3s):
        bucket_5_9_count = bucket_5_9_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) &  (c5s != c3s) & (c5s != c4s):
        bucket_5_9_count = bucket_5_9_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_5_9_count = bucket_5_9_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_5_9_count = bucket_5_9_count + 1

    # Bucket 6-T
    bucket_list = ['6', '7', '8', '9', 'T']
    bucket_6_T_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list):
        bucket_6_T_count = bucket_6_T_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c3s):
        bucket_6_T_count = bucket_6_T_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) &  (c5s != c3s) & (c5s != c4s):
        bucket_6_T_count = bucket_6_T_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_6_T_count = bucket_6_T_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_6_T_count = bucket_6_T_count + 1

    # Bucket 7-J
    bucket_list = ['7', '8', '9', 'T', 'J']
    bucket_7_J_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list):
        bucket_7_J_count = bucket_7_J_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c3s):
        bucket_7_J_count = bucket_7_J_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) &  (c5s != c3s) & (c5s != c4s):
        bucket_7_J_count = bucket_7_J_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_7_J_count = bucket_7_J_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_7_J_count = bucket_7_J_count + 1

    # Bucket 8-Q
    bucket_list = ['8', '9', 'T', 'J', 'Q']
    bucket_8_Q_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list):
        bucket_8_Q_count = bucket_8_Q_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c3s):
        bucket_8_Q_count = bucket_8_Q_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) &  (c5s != c3s) & (c5s != c4s):
        bucket_8_Q_count = bucket_8_Q_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_8_Q_count = bucket_8_Q_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_8_Q_count = bucket_8_Q_count + 1

    # Bucket 9-K
    bucket_list = ['9', 'T', 'J', 'Q', 'K']
    bucket_9_K_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list):
        bucket_9_K_count = bucket_9_K_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c3s):
        bucket_9_K_count = bucket_9_K_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) &  (c5s != c3s) & (c5s != c4s):
        bucket_9_K_count = bucket_9_K_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_9_K_count = bucket_9_K_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_9_K_count = bucket_9_K_count + 1

    # Bucket T-A
    bucket_list = ['T', 'J', 'Q', 'K', 'A']
    bucket_T_A_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3s in bucket_list):
        bucket_T_A_count = bucket_T_A_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4s in bucket_list) & (c4s != c3s):
        bucket_T_A_count = bucket_T_A_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5s in bucket_list) &  (c5s != c3s) & (c5s != c4s):
        bucket_T_A_count = bucket_T_A_count + 1
    if (stage in ['turn', 'river']) & (c6s in bucket_list) & (c6s != c3s) & (c6s != c4s) & (c6s != c5s):
        bucket_T_A_count = bucket_T_A_count + 1
    if (stage in ['river']) & (c7s in bucket_list) & (c7s != c3s) & (c7s != c4s) & (c7s != c5s) & (c7s != c6s):
        bucket_T_A_count = bucket_T_A_count + 1

    nb_straight_community_cards = max([bucket_A_5_count, bucket_2_6_count, bucket_3_7_count, bucket_4_8_count, bucket_5_9_count, bucket_6_T_count, bucket_7_J_count, bucket_8_Q_count, bucket_9_K_count, bucket_T_A_count])

    
    return nb_straight_community_cards
    
def calculate_nb_flush_player_cards(stage, c1: str, c2: str, c3: str, c4: str, c5: str, c6: str, c7: str):
    """
    This function calculates the field nb_flush_player_cards
    
    Arguments
    ---------
    stage: string
            The stage of the game
    c1: string
           Card 1
    c2: string
           Card 2
    c3: string
           Card 3
    c4: string
           Card 4
    c5: string
           Card 5
    c6: string
           Card 6
    c7: string
           Card 7

    Returns
    --------
    nb_flush_player_cards: float
         Number which represent the number of flush player cards
    """
    # we need to know just the cards with their colors only
    c1c = c1[1:]
    c2c = c2[1:]
    c3c = c3[1:]
    c4c = c4[1:]
    c5c = c5[1:]
    c6c = c6[1:]
    c7c = c7[1:]

    clubs_count = 0
    if c1c == 'c':
        clubs_count = clubs_count + 1
    if c2c == 'c':
        clubs_count = clubs_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3c == 'c'):
        clubs_count = clubs_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4c == 'c'):
        clubs_count = clubs_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5c == 'c'):
        clubs_count = clubs_count + 1
    if (stage in ['turn', 'river']) & (c6c == 'c'):
        clubs_count = clubs_count + 1 
    if (stage in ['river']) & (c7c == 'c'):
        clubs_count = clubs_count + 1

    spades_count = 0
    if c1c == 's':
        spades_count = spades_count + 1
    if c2c == 's':
        spades_count = spades_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3c == 's'):
        spades_count = spades_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4c == 's'):
        spades_count = spades_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5c == 's'):
        spades_count = spades_count + 1
    if (stage in ['turn', 'river']) & (c6c == 's'):
        spades_count = spades_count + 1 
    if (stage in ['river']) & (c7c == 's'):
        spades_count = spades_count + 1 

    hearts_count = 0
    if c1c == 'h':
        hearts_count = hearts_count + 1
    if c2c == 'h':
        hearts_count = hearts_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3c == 'h'):
        hearts_count = hearts_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4c == 'h'):
        hearts_count = hearts_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5c == 'h'):
        hearts_count = hearts_count + 1
    if (stage in ['turn', 'river']) & (c6c == 'h'):
        hearts_count = hearts_count + 1 
    if (stage in ['river']) & (c7c == 'h'):
        hearts_count = hearts_count + 1

    diamonds_count = 0
    if c1c == 'd':
        diamonds_count = diamonds_count + 1
    if c2c == 'd':
        diamonds_count = diamonds_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c3c == 'd'):
        diamonds_count = diamonds_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4c == 'd'):
        diamonds_count = diamonds_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5c == 'd'):
        diamonds_count = diamonds_count + 1
    if (stage in ['turn', 'river']) & (c6c == 'd'):
        diamonds_count = diamonds_count + 1 
    if (stage in ['river']) & (c7c == 'd'):
        diamonds_count = diamonds_count + 1

    nb_flush_player_cards = max([clubs_count, spades_count, hearts_count, diamonds_count])
    
    return nb_flush_player_cards
    
def calculate_nb_flush_community_cards(stage, c3: str, c4: str, c5: str, c6: str, c7: str):
    """
    This function calculates the field nb_flush_community_cards
    
    Arguments
    ---------
    stage: string
            The stage of the game
    c3: string
           Card 3
    c4: string
           Card 4
    c5: string
           Card 5
    c6: string
           Card 6
    c7: string
           Card 7

    Returns
    --------
    nb_flush_player_cards: float
         Number which represent the number of flush community cards
    """
    # we need to know just the cards with their colors only
    c3c = c3[1:]
    c4c = c4[1:]
    c5c = c5[1:]
    c6c = c6[1:]
    c7c = c7[1:]

    clubs_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3c == 'c'):
        clubs_count = clubs_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4c == 'c'):
        clubs_count = clubs_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5c == 'c'):
        clubs_count = clubs_count + 1
    if (stage in ['turn', 'river']) & (c6c == 'c'):
        clubs_count = clubs_count + 1 
    if (stage in ['river']) & (c7c == 'c'):
        clubs_count = clubs_count + 1

    spades_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3c == 's'):
        spades_count = spades_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4c == 's'):
        spades_count = spades_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5c == 's'):
        spades_count = spades_count + 1
    if (stage in ['turn', 'river']) & (c6c == 's'):
        spades_count = spades_count + 1 
    if (stage in ['river']) & (c7c == 's'):
        spades_count = spades_count + 1 

    hearts_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3c == 'h'):
        hearts_count = hearts_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4c == 'h'):
        hearts_count = hearts_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5c == 'h'):
        hearts_count = hearts_count + 1
    if (stage in ['turn', 'river']) & (c6c == 'h'):
        hearts_count = hearts_count + 1 
    if (stage in ['river']) & (c7c == 'h'):
        hearts_count = hearts_count + 1

    diamonds_count = 0
    if (stage in ['flop', 'turn', 'river']) & (c3c == 'd'):
        diamonds_count = diamonds_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c4c == 'd'):
        diamonds_count = diamonds_count + 1
    if (stage in ['flop', 'turn', 'river']) & (c5c == 'd'):
        diamonds_count = diamonds_count + 1
    if (stage in ['turn', 'river']) & (c6c == 'd'):
        diamonds_count = diamonds_count + 1 
    if (stage in ['river']) & (c7c == 'd'):
        diamonds_count = diamonds_count + 1

    nb_flush_community_cards = max([clubs_count, spades_count, hearts_count, diamonds_count])
    
    return nb_flush_community_cards
    
def countCards(c1: str, c2: str, c3: str, c4: str, c5: str, nb_cards_occurence):
    """
    This function counts cards in order to calculate the number of pairs ,sets or quads in the community cards
    
    Arguments
    ---------
    nb_cards_occurence: string
            Number of occurences for the cards (2 to calculate the number of pairs in the community cards, 3 for the sets and 4 for the quads)
    c1: string
           Card 1
    c2: string
           Card 2
    c3: string
           Card 3
    c4: string
           Card 4
    c5: string
           Card 5

    Returns
    --------
    number: float
         Number of pairs ,sets or quads in the community cards
    """
    # we need to know just the cards without their colors
    c1s = c1[:1]
    c2s = c2[:1]
    c3s = c3[:1]
    c4s = c4[:1]
    c5s = c5[:1]
    input_list = [c1s, c2s, c3s, c4s, c5s]
    # remove empty elements from the input list
    filtered_prelist = [x for x in input_list if not pd.isnull(x)]
    filtered_list = [x for x in filtered_prelist if x]
    # Count occurrences
    counts = Counter(filtered_list)
    
    # Filter duplicates
    duplicates = {item: count for item, count in counts.items() if count >= nb_cards_occurence}

    dict_length = len(duplicates)
    
    return dict_length