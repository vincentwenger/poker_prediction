import streamlit as st
import requests
import json
from poker_functions import chen_score, cards_score, calculate_nb_straight_player_cards, calculate_nb_straight_community_cards, calculate_nb_flush_player_cards, calculate_nb_flush_community_cards, countCards

st.title("Poker Prediction app")


card_option_list = ['A hearts', 'A diamonds', 'A spades', 'A clubs',
                    'K hearts', 'K diamonds', 'K spades', 'K clubs', 
                    'Q hearts', 'Q diamonds', 'Q spades', 'Q clubs', 
                    'J hearts', 'J diamonds', 'J spades', 'J clubs', 
                    'T hearts', 'T diamonds', 'T spades', 'T clubs', 
                    '9 hearts', '9 diamonds', '9 spades', '9 clubs', 
                    '8 hearts', '8 diamonds', '8 spades', '8 clubs', 
                    '7 hearts', '7 diamonds', '7 spades', '7 clubs', 
                    '6 hearts', '6 diamonds', '6 spades', '6 clubs', 
                    '5 hearts', '5 diamonds', '5 spades', '5 clubs', 
                    '4 hearts', '4 diamonds', '4 spades', '4 clubs', 
                    '3 hearts', '3 diamonds', '3 spades', '3 clubs', 
                    '2 hearts', '2 diamonds', '2 spades', '2 clubs' 
]
position_option_list = ['Middle Position', 'Cut-off', 'Button', 'Small Blind', 'Big Blind', 'Under the Gun']

data_for_ui = {
    'player_card_1': st.selectbox('Player card 1', card_option_list, index=None),
    'player_card_2': st.selectbox('Player card 2', card_option_list, index=None),
    'community_card_1': st.selectbox('Community card 1', card_option_list, index=None),
    'community_card_2': st.selectbox('Community card 2', card_option_list, index=None),
    'community_card_3': st.selectbox('Community card 3', card_option_list, index=None),
    'community_card_4': st.selectbox('Community card 4', card_option_list, index=None),
    'community_card_5': st.selectbox('Community card 5', card_option_list, index=None),
    'amount_required': st.number_input('Amount required', min_value=0, step=500),
    'amount_committed': st.number_input('Amount committed', min_value=0, value=100, step=100),
    'position': st.selectbox('Position', position_option_list),
    'nb_players_left': st.number_input('Number of players left', min_value=2, max_value=9, value=4, step=1),
    'nb_previous_raise': st.number_input('Number of previous raises', min_value=0, max_value=9, value=0, step=1),
    'sub_stage': st.number_input('Sub stage', min_value=1, max_value=3, value=1, step=1),
}

# calculate the stage and cards 1 to 7
card1 = ''
card2 = ''
card3 = ''
card4 = ''
card5 = ''
card6 = ''
card7 = ''
stage = 'preflop'
if data_for_ui['player_card_1'] is not None:
    card1 = data_for_ui['player_card_1'][0] + data_for_ui['player_card_1'][2]
if data_for_ui['player_card_2'] is not None:
    card2 = data_for_ui['player_card_2'][0] + data_for_ui['player_card_2'][2]
if data_for_ui['community_card_1'] is not None:
    card3 = data_for_ui['community_card_1'][0] + data_for_ui['community_card_1'][2]
    stage = 'flop'
if data_for_ui['community_card_2'] is not None:
    card4 = data_for_ui['community_card_2'][0] + data_for_ui['community_card_2'][2]
    stage = 'flop'
if data_for_ui['community_card_3'] is not None:
    card5 = data_for_ui['community_card_3'][0] + data_for_ui['community_card_3'][2]
    stage = 'flop'
if data_for_ui['community_card_4'] is not None:
    card6 = data_for_ui['community_card_4'][0] + data_for_ui['community_card_4'][2]
    stage = 'turn'
if data_for_ui['community_card_5'] is not None:
    card7 = data_for_ui['community_card_5'][0] + data_for_ui['community_card_5'][2]
    stage = 'river'

# calculate stage_int
sub_stage = data_for_ui['sub_stage']
stage_int = 1
if (stage == 'preflop') & (sub_stage == 1):
    stage_int = 1
elif (stage == 'preflop') & (sub_stage == 2):
    stage_int = 2
elif (stage == 'preflop') & (sub_stage == 3):
    stage_int = 3
elif (stage == 'flop') & (sub_stage == 1):
    stage_int = 4
elif (stage == 'flop') & (sub_stage == 2):
    stage_int = 5
elif (stage == 'flop') & (sub_stage == 3):
    stage_int = 6
elif (stage == 'turn') & (sub_stage == 1):
    stage_int = 7
elif (stage == 'turn') & (sub_stage == 2):
    stage_int = 8
elif (stage == 'turn') & (sub_stage == 3):
    stage_int = 9
elif (stage == 'river') & (sub_stage == 1):
    stage_int = 10
elif (stage == 'river') & (sub_stage == 2):
    stage_int = 11
else:
    stage_int = 12
    
# calculate position_int
position = data_for_ui['position']
if position == 'Small Blind':
    position_int = 1
elif position == 'Big Blind':
    position_int = 2
elif position == 'Under the Gun':
    position_int = 3
elif position == 'Middle Position':
    position_int = 4
elif position == 'Cut-off':
    position_int = 5
else:
    position_int = 6


data_for_api = {
    'stage_int': stage_int,
    'position_int': position_int,
    'amount_required': data_for_ui['amount_required'],
    'amount_committed': data_for_ui['amount_committed'],
    'nb_players_left': data_for_ui['nb_players_left'],
    'nb_previous_raise': data_for_ui['nb_previous_raise'],
    'nb_straight_player_cards': calculate_nb_straight_player_cards(stage, card1, card2, card3, card4, card5, card6, card7),
    'nb_straight_community_cards': calculate_nb_straight_community_cards(stage, card3, card4, card5, card6, card7),
    'nb_flush_player_cards': calculate_nb_flush_player_cards(stage, card1, card2, card3, card4, card5, card6, card7),
    'nb_flush_community_cards': calculate_nb_flush_community_cards(stage, card3, card4, card5, card6, card7),
    'nb_pairs_community_cards': countCards(card3, card4, card5, card6, card7, 2),
    'nb_sets_community_cards': countCards(card3, card4, card5, card6, card7, 3),
    'nb_quads_community_cards': countCards(card3, card4, card5, card6, card7, 4),
    'chen_score': chen_score(card1, card2),
    'cards_score': cards_score(card1, card2, card3, card4, card5, card6, card7)
}


if st.button("Submit"):
    url = "http://127.0.0.1:8000/prediction"
    response = requests.post(url, json=data_for_api)
    action_prediction = json.loads(response.text)['action_prediction']
    amount_prediction = json.loads(response.text)['amount_prediction']

    if action_prediction == 'raise':
        st.success("Raise " + str(amount_prediction))
    elif action_prediction == 'call':
        st.warning("Call " + str(amount_prediction))
    else:
        st.error("Fold")