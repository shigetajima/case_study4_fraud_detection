# case_study4_fraud_detection
Fraud Detection case study.  

## Detection of fraud transactions
The data is confidential, and it is not shared here. Build a model to predict fraud transactions, and it is used to detect fraud transactions in the future.

## EDA and feature selection
Feature selection was done to find features that are correlated with the fraud events. A "fraud" column was added to the dataframe to indicate that the event is fraud or not. If the account type value contains a 'fraud' phrase ('fraudster', 'fraudster_att', 'fraudster_event') the column is labeled as "fraud".

The data are preprocessed by applying several conditions based on EDA to find what kind of events are likely to contain fraud events.
1. a new user
2. venue name exists or not
3. \# of payouts (>30)
4. delivery method is zero
5. length of previous payouts value
6. name is all capped or not

## Run the code
1. Run model.py to load and preprocess data, and save the model based on Random Forest classifier into a pickle.
2. Run predict.py to predict the fraud risk level.
3. The prediction is stored in a mongoDB and results appear in a web app.

## Rough timeline
Day 1: Project scoping, Model building, and an intro to Web apps<br>
Day 2: Web app and deployment
