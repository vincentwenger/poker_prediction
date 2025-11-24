# Is it possible to predict the most profitable moves to play in a poker game ?

**Assignment notebooks:** 
1) Data preprocessing: https://github.com/vincentwenger/poker_prediction/blob/main/01_Poker_data_preprocessing.ipynb
2) Exploratory data analysis: https://github.com/vincentwenger/poker_prediction/blob/main/02_Poker_exploratory_data_analysis.ipynb
3) Baseline modeling: https://github.com/vincentwenger/poker_prediction/blob/main/03_Poker_baseline_modeling.ipynb

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

## What are the findings?

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

## What do I recommend?

- In general, it is better to create coupons which have more time before they expire
- Distribute bar coupons only to people who go to bars often
- Distribute Carry out & Take away coupons :
  - in places where people are older, with no kids around
  - when it doesn't rain
  - near places with construction zones or hospitals, or near residential neighborhoods where people with lower income live
- Distribute Coffee House coupons:
  - in places with young people who are less than 21
  - near residential neighborhoods where people with lower income live
  - when it doesn't snow and the temperature is hot.
- Distribute Cheap restaurant coupons:
  - when weather is sunny and the temperature is not too cold
  - to people who go to restaurants often and never order take away food
  - to restaurants which are not located too far from the drivers
- Distribute Expensive restaurant coupons:
  - when weather is sunny and the temperature is not too cold
  - to single or unmarried drivers with higher income
  - who people who already go often to bars and restaurants
