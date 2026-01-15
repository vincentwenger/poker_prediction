# Is it possible to predict the most profitable moves to play in a poker game ?

**Assignment notebooks:** 
1) Data preprocessing: https://github.com/vincentwenger/poker_prediction/blob/main/01_Poker_data_preprocessing.ipynb
2) Exploratory data analysis: https://github.com/vincentwenger/poker_prediction/blob/main/02_Poker_exploratory_data_analysis.ipynb
3) Baseline modeling: https://github.com/vincentwenger/poker_prediction/blob/main/03_Poker_baseline_modeling.ipynb
4) Model improvement: https://github.com/vincentwenger/poker_prediction/blob/main/04_Poker_model_improvement.ipynb
5) Game testing: https://github.com/vincentwenger/poker_prediction/blob/main/05_game_testing.ipynb

**API endpoint and UI front-end application:** 
- API endpoint: https://github.com/vincentwenger/poker_prediction/blob/main/API_endpoint.py
- UI front-end application with streamlit: https://github.com/vincentwenger/poker_prediction/blob/main/UI_app.py (requires poker_functions.py)

## What is the problem?
We expect to build a model to answer the research question.
The input data for the model would be for each game:
- the player hands
- the community cards available
- the game step (preflop, flop, turn or river)
- the number of players left in the game
- the amount already committed in the game
- the amount required to continue playing the game
Based on this input, the model should be able to predict what the player's next action should be (fold, check/call, or raise) and in case the action is "raise", what should be the best amount to raise to be the most profitable possible.

## What is the data?
The Poker Hand History File Format Specification is described at this link https://phh.readthedocs.io/en/stable/. For the poker dataset, I am using this link https://zenodo.org/records/17136841. I downloaded the attached file "poker-hand-histories.zip". As explained on the link, the ZIP contains many files in the poker hand history (PHH) format. I extracted the ZIP and focused on the folder "pluribus". It contains 10.000 PHH files, and each file corresponds to 1 game between 5 human professional poker players and 1 poker AI named "Pluribus".
If you need the raw data, you need to download the ZIP and you will get the raw data under the folder "pluribus". 
All those 10000 Poker games have the same common attributes:
- variant : NT. The poker variant is No-limit Texas hold ‘em
- ante : 0. The poker ante is 0
- small_blind : 50. The amount for the small blind is 50
- big_blind : 100. The amount for the big blind is 100
- min_bet : 100. The minimum bet is 100
- starting_stack : 10000. The starting stack amount is 10000

In the first notebook "Data preprocessing", I transformed the raw data into a preprocessed CSV file which has 91356 rows and 31 columns. 

## What are the findings of the Initial report?

From the exploratory data analysis of the CSV file, the findings are that :
- Each row represents a turn during a poker game where a player had to decide about an action : fold, check/call, or raise his hand. It could be during the preflop, flop, turn or river stage of the game
- There are 10000 unique games played between 6 players.
- There are no duplicates in the dataset. There could be some missing values for the columns flop, turn, and river but it means the phase of the game at the moment the player had to make an action was not yet at the flop, turn or river
- The cards which are the most kept and raised in the preflop phase of a poker game are pairs and when players have 2 cards which are both higher than Jack. The 72 is the hand that players fold the most
- The preflop cards which have the best average return are the pair of Aces and the pair of Kings. JT and hands with an Ace and a low card have the worst return
- Players tend to raise when the flop cards have a potential to make a straight with connected cards like 743 or 965. They tend to avoid raising when there is already a pair in the flop cards
- The top 3 most important features to predict the action that the player will play (Fold, check/call or raise) seem to be the cards_score, amount_required and chen_score. The next 3 are the stage_int, nb_players_left and amount_committed
- Players fold more often when they have less than a Three of a kind. When they have better than that, players tend to raise more frequently. And when the previous player has raised a great amount of money, the current player tends to check/call more unless the player has a great hand
- Considering only the 2 preflop cards, players raise when they have at least a pair or some suited connected cards. Players fold more often when they have less than a pair of queens and when the previous player has raised a great amount of money
- Once players decided to raise, they tend to raise a greater amount when the chen score of their 2 initial cards is higher. The mean of the raised amount is a bit more than 6 times the minimum bet of 100. However, the 50th percentile is 2.5 times the minimum bet.

## What do I recommend for the Initial report?

In the Baseline modeling notebook, we said that we expect to build a model to answer the research question. Based on the input data, the model should be able to make 2 predictions:
1) What the player's next action should be (fold, check/call, or raise). For each move there is only one of those 3 choices. For this point, we will need a classification model to predict the action
For the baseline model, we choose to use a Decision Tree because it is interpretable and can be easily explained. Most of the models are difficult to explain to non technical users, and Decision Tree on the other hand is very intuitive to understand. That is one of the reason I am interested to use a Decision Tree, to communicate to non technical users how this machine learning model works and how it fits in a machine learning project. Also Decision Tree is a very dynamic machine learning model, as it scales with the data. The bias is low.
We saw in the exploratory_data_analysis, that the top 3 features are cards_score, amount_required and chen_score. We will keep only the 2 features cards_score and amount_required as input for a simple baseline model, since the chen_score is a metric a bit redundant from the cards_score. Also keeping only 2 features will allow us to do more easily some visualizations and plots

2) In case the action predicted is "raise", what should be the best amount to raise to be the most profitable possible. In the other cases when the choice was fold or check/call, there is no need to predict any amount as the player won't need to bet anything. For this point, we will need another regression model to predict the amount to raise.
For the baseline model, we choose to use a simple Linear regression model to predict the amount to raise once the action was already predicted to be a Raise.
We saw in the exploratory_data_analysis, that the top 3 features are cards_score, amount_required and chen_score. Just like for the above classification model with Decision trees, we will keep only the 2 features cards_score and amount_required as input for a simple baseline model, since the chen_score is a metric a bit redundant from the cards_score. Also to do the plotting we will keep only the cards_score, so that we can represent in 2D the cards score vs the amount raised by the current player, and show the line of the linear regression model in the same plot.

## Result for the baseline model
Finally, we were able to create a function for Predictions using our baseline model.
The function is called "predict_poker_moves_v1" and is available in the Baseline modeling notebook.
We were able to make some quick tests with the function by giving it some input data, and the results seem to make sense.
We will try to improve it in the future with some better models

## What are the findings of the Final report?

From the model improvement notebook, the findings are that :
- Based on the input data, the model should be able to make 2 predictions:
    - What the player's next action should be (fold, check/call, or raise). For each move there is only one of those 3 choices. For this point, we improved a classification model to predict the action
    - In case the action predicted is "raise", what should be the best amount to raise to be the most profitable possible. In the other cases when the choice was fold or check/call, there is no need to predict any amount as the player won't need to bet anything. For this point, we improved a regression model to predict the amount to raise. 
- For feature engineering, we have enriched the data with many columns calculated from the player or community cards. For example, the number of pairs, sets, quads for the player or community cards; or the number of cards which have potential to make a straight or a flush. It allowed us to have more features available to use for our models.
- The dataset has 3 classes (0 - Fold, 1 - Check/call, 2 - Raise) and the class percentage is 53%, 27% and 20%. The dataset is imbalanced.
- To be successful in a poker game, it is more important to be correct when the player raises, because he takes the risk to lose money. In case the player is incorrect when he folds, it is not as important because he will not lose money. Therefore, we will be looking to have a good precision metric. In our problem, the negative class should be the action: Fold, and the positive class is the action Call or Raise. It is important to minimize the number of false positives because being wrong can cause a loss of money. Additionally, in some cases it is also important not to miss strong hands: so not to fold when we have strong hands. Because this can cause the player to miss on potential good gains. Therefore, for this imbalanced poker dataset, we focused more to have good precision, recall, or F1 score.
- In the 3rd notebook about "Baseline modeling", we created a baseline classification model, which has train accuracy, test accuracy, test recall (weighted avg) around 0.74, and a test precision and F1 (weighted avg) around 0.73. The goal was to improve the baseline model.
- Classification models with 15 features:
     - all the classification models have better performance metrics than the baseline classification model except the Gaussian Naive Bayes model
     - the top 3 features are: Cards score, Amount required and Chen score.
     - the best classification models with 15 features are the Stacking Classifier and XGBoost Classifier:
          - Our models have 86% accuracy; this means that 86 out of 100 predictions are correct. Accuracy is easy to interpret but can be misleading in imbalanced datasets, which is our case since we have an imbalanced dataset
          - Our model's recall is 0.86, this means that it was able to find 86% of all positive cases.
          - Our model's precision is 0.86, this means that 86% of the actions the model identified as positive cases are actual positive cases
          - Our F1 score of 0.86 indicates that the model is fairly good at identifying positive cases without labeling too many false positives or missing too many actual positives. This score is generally considered quite good for most classification tasks. It is useful for balancing precision and recall and for dealing with our imbalanced dataset
          - Our AUC of 0.95 means that there is 95% chance that the model will be able to distinguish between positive class and negative class.
- In the 3rd notebook about "Baseline modeling", we created a baseline regression model, which has test mean absolute error around 452, test root mean squared error around 947, test R2 score around 0.31. The goal was to improve the baseline model
- Regression models with 15 features:
     - all the models have better performance metrics than the baseline regression model
     - the top 3 features are Amount required, Amount committed and Stage of the game.
     - Players will bet more if the previous players already betted an important amount or if they already committed a great amount in the pot or as we advance further into the game's stages. Players will bet less if the community cards show that there is potential for a straight, a flush, or if there are pairs
     - the best regression models with 15 features is the Stacking regressor, which has:
          - a MAE (Mean absolute error) of 172.3, which means that on average, our predictions on the amount to raise are off by 172.3. So, when predicting the amount that a poker player needs to raise, in a game where the starting stack amount is 10000 and the minimum bet is 100, if the model predicts an amount to raise of 600, we can expect the actual amount to raise to be anywhere between 427.7 and 772.3
          - a RMSE (Root Mean Squared Error) of 526.33, which indicates that, in a game where the starting stack amount is 10000 and the minimum bet is 100, the standard deviation of our prediction errors is roughly 526.33. Essentially, this tells us that our predictions are scattered on average by 526.33 from the actual amount to raise.
          - A R² of 0.79 which means that 79% of the variation in the amount raised by the player can be explained by the variables in the model. A R² close to 1 indicates that the model has a very good fit. In this case, a value of 0.79 is a good sign that the model is capturing a significant amount of the variability in the data, though there is still 21% of the variation that the model does not explain.
          - Given that the RMSE is a bit high and the R² is only 0.79, the model is not perfect, but it already offers clear insights into which factors are driving the amount that the player needs to raise
- By reducing the number of features to 5 using backward sequential feature selection to improve the KNN regressor model, we were able to further improve the test mean absolute error to 161, the test root mean squared error to 521 and the test R2 to 0.7928

## What are the suggestions for next steps for the Final report?

The recommendations for the next steps are:
- Make all our models play against each other’s using a poker game engine. Then create some tournaments to figure out which models beat the others in real poker games. We could explore if the winners will be the same ones that we found have the best performance metrics in the 4th notebook about "Model improvement". I did this in the 5th notebook about "Game testing". The results from it are that:
     - We are able to make our models play against each other’s using a poker game engine. We created some tournaments to figure out which models beat the others in reel poker games. To play the poker games, we used the python library "pypokerengine"
     - The player using the Baseline model has won 92% of the tournaments against some players using basic algorithms.
     - The best classifiers are in this order: 1) K-Nearest Neighbors Classifier, 2) Voting Classifier, 3) Random Forest Classifier, 4) Stacking Classifier
     - The best regressors are in this order: 1) Decision Tree Regressor, 2) Stacking Regressor, 3) Linear Regression, 4) Voting Regressor
     - For those top 4 classifiers, we can see that in the 4th notebook they were all in the top 6 classifiers by order of "Test F1 (weighted avg)". So the results from the game testing seem to be aligned with results of the ranking by the best performance metrics from the 4th notebook. However, we note that one of the top 2 classifiers from the 4th notebook got disappointing results in the game testing: the XGBoost Classifier, as it didn't make it in the top 4 for the game testing
     - For those top 4 regressors, we can see that in the 4th notebook they were all in the top 4 regressors by order of "Test R2 Score", except for the Linear regression which is 3rd in the game testing but only 7th in the 4th notebook by order of "Test R2 Score". Globaly, the results from the game testing seem to be aligned with results of the ranking by the best performance metrics from the 4th notebook
- Using one of the best model in the PKL file, we could produce an API which will load the model from the file. Then we could make calls to the API using a front-end application : streamlit. It is a user interface framework that will call the API in order to produce predictions and display that on the screen: I did this, as I created an API endpoint: API_endpoint.py and an UI front-end application with streamlit: UI_app.py (requires poker_functions.py)
- Once we have poker models which can play against each other’s, we could analyze the logs of the games they play, to see if it would make sense to retrain some new models based on what those poker models have already been playing, after recreating some new datasets of their new games. We could also add a part of randomness in what the models play and then select in new datasets only the successful games. We could explore this possibility to see if it would make any impact or improve the strength of the poker models
- We could ask some human poker players to play against the AI poker models we created and ask the human players for feedback to see if they think those are good AI models or not
- We could also explore reinforcement learning to see how we could train machines to beat human at poker using this technique
