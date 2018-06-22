
# ChessStyle: Chess.com User Activity Prediction

Predicting user activity on Chess.com

Presentation at Galvanize capstone showcase: https://youtu.be/UCAHfOv-64Q

![alt text](https://raw.githubusercontent.com/Bmcgarry194/ChessStyle/master/photos/chess_picture.jpg)

## Business Understanding
With any website, understanding user behavior is paramount to maintaining a healthy and thriving online community. In social or competitive communities it is especially important to keep the number of active and engaged users as high as possible. To this end, creating a profile of players most likely to become inactive allows Chess.com to focus resources on those users which are at greatest risk of leaving the site. This information also points us in the direction of possible ways to improve the site in order to engage a wider variety of users.

## Data Understanding
I made use of the Chess.com api in order to gather information about users. The api was fairly new, so there was no way to get a complete list of users who signed up during a particular time period using just the api. 
First, I queried a list of all usernames in the US and filtered them based on time of sign up. Then, made additional queries to the api to find all of the games they had played as well as additional statistics and information about their profile and saved it to a mongoDB.


## Data Preparation
Manipulated the player data in pandas.
Parsed the games column which contained all the games from each player since they signed up.
Pulled out the number of games played after 3 months to determine whether a user was active or inactive.
All other stats about number of games played and types of games played in the first month since sign up were also recorded in their own columns.

## Evaluation
The data was split up into a train and test group, and trained three different models on the training set and evaluated performance on the test set. The models were random forest, logistic regression, and a gradient boosting classifier all from the sklearn module. Looking at the ROC curves of each of the models allowed me to choose the logistic regression model which was the most effective in this particular context. 


