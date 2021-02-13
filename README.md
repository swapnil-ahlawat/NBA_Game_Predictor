1. Web Scraping
Run python script 'webscraping.py' to scrap raw data from websites. This will generate a lot of csv files of raw data.
This will take a lot of time as the pages are dynamically loaded and javascript clicking, and others are done by script.
All the csv files are already in the data folder.
>> python3 webscraping.py
This will save the csv files in the same folder in which the script is.

2. Feature Engineering
Run python script 'featureEngineering.py' to generate features from raw data. This will take around 10 minutes to run.
The final csv dataset is already in the data folder with the name "NBAGameDataset.csv".
>> python3 featureEngineering.py
This will save the csv files in the same folder in which the script is.

3. Running Models:-
Hyperparamter tuning code is commented as it takes hours to run. The models with tuned hyperparameters is added at the end of the scipt so that you can get the results faster.
The models will load the csv from data folder.

To see results when models were feeded only team features:- run python script 'team.py'
>> python3 team.py

To see results when models were feeded only player features:- run python script 'player.py'
>> python3 player.py

To see results when models were feeded both team and player features:- run python script 'teamAndPlayer.py'
>> python3 teamAndPlayer.py

Note: The coorelation matrix has been commented out because it gives error on running from command line. In case if you want to try that code on notebook, please have matplotlib library installed. We haven't added that requirement.txt as it can't be pip installed.
