# building the API endpoint
from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import pandas as pd

classification_model = joblib.load('models/StackingClassifier_GradientBoostingClassifier_6.pkl')
regression_model = joblib.load('models/StackingRegressor_Ridge_7.pkl')

def format_predictions(action_prediction, amount_prediction, amount_required):
    if action_prediction == 1:
        final_action = 'call'
        final_amount = amount_required
    elif action_prediction == 2:
        final_action = 'raise'
        final_amount = round(amount_prediction, 0)
    else:
        final_action = 'fold'
        final_amount = 0
    return final_action, final_amount

class input_vars(BaseModel):
    stage_int: int
    position_int: int
    amount_required: float
    amount_committed: float
    nb_players_left: int
    nb_previous_raise: int
    nb_straight_player_cards: int
    nb_straight_community_cards: int
    nb_flush_player_cards: int
    nb_flush_community_cards: int
    nb_pairs_community_cards: int
    nb_sets_community_cards: int
    nb_quads_community_cards: int
    chen_score: float
    cards_score: float

app = FastAPI()

@app.get('/')
def root():
    return "API endpoint for Poker prediction"
    
@app.post("/prediction")
def action_prediction(independent_variables: input_vars):
    # accept the independent features
    df = pd.DataFrame(independent_variables.model_dump(), index=[0])
    # pass the features to the model
    # get predictions from the model
    action_predictions = classification_model.predict(df)
    amount_predictions = regression_model.predict(df)
    # return predictions back
    action_prediction = int(action_predictions)
    amount_prediction = int(amount_predictions)
    amount_required = int(df['amount_required'])
    final_action, final_amount = format_predictions(action_prediction, amount_prediction, amount_required)
    
    return {"action_prediction": final_action, "amount_prediction": final_amount}