import pandas as pd
import numpy as np

#Enginering Features from Raw Data
playerDF= pd.DataFrame(columns=['Match Up', 'Game Date', 'PTS', 'FG%', '3P%', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', '+/-'])
astypeDict= {'Team':str, 'Match Up':str, 'Game Date':str, 'MIN':float, 'PTS':float, 'FG%':float, '3P%':float, 'FT%':float, 'OREB':float, 'DREB':float, 'AST':float, 'STL':float, 'BLK':float, 'TOV':float, 'PF':float, '+/-':float}
groupingDict= {'Team':'first', 'Match Up':'first', 'Game Date':'first', 'MIN':'sum', 'PTS':'sum', 'FG%':'sum', '3P%':'sum', 'FT%':'sum', 'OREB':'sum', 'DREB':'sum', 'AST':'sum', 'STL':'sum', 'BLK':'sum', 'TOV':'sum', 'PF':'sum', '+/-':'sum'}
frames=[]
for year in range(8, 20):
    print(year)
    df = pd.read_csv('PlayerSchedule'+str(year//10) + str(year%10) + '-'+ str((year+1)//10) + str((year+1)%10) +'.csv')
    df=df.drop(columns=["Player", "Season", "W/L", "FGM", "FGA", "3PM", "3PA", "FTM", "FTA", "REB"])
    ftMean = np.mean([float(val) for val in df["FT%"] if val!='-'])
    p3Mean = np.mean([float(val) for val in df["3P%"] if val!='-'])
    fgMean = np.mean([float(val) for val in df["FG%"] if val!='-'])
    df["FT%"].replace('-', str(ftMean), inplace=True)
    df["3P%"].replace('-', str(p3Mean), inplace=True)
    df["FG%"].replace('-', str(fgMean), inplace=True)
    df=df.astype(astypeDict)
    df['PTS']= df['PTS']*df['MIN']
    df['FG%']= df['FG%']*df['MIN']
    df['3P%']= df['3P%']*df['MIN']
    df['+/-']= df['+/-']*df['MIN']
    df['FT%']= df['FT%']*df['MIN']
    df['OREB']= df['OREB']*df['MIN']
    df['DREB']= df['DREB']*df['MIN']
    df['AST']= df['AST']*df['MIN']
    df['STL']= df['STL']*df['MIN']
    df['BLK']= df['BLK']*df['MIN']
    df['TOV']= df['TOV']*df['MIN']
    df['PF']= df['PF']*df['MIN']
    df["key"]= [match + game for match, game in df[['Match Up', 'Game Date']].values]
    df= df.groupby(df['key']).aggregate(groupingDict).reindex(columns=df.columns)
    df['PTS']= df['PTS']/df['MIN']
    df['FG%']= df['FG%']/df['MIN']
    df['3P%']= df['3P%']/df['MIN']
    df['+/-']= df['+/-']/df['MIN']
    df['FT%']= df['FT%']/df['MIN']
    df['OREB']= df['OREB']/df['MIN']
    df['DREB']= df['DREB']/df['MIN']
    df['AST']= df['AST']/df['MIN']
    df['STL']= df['STL']/df['MIN']
    df['BLK']= df['BLK']/df['MIN']
    df['TOV']= df['TOV']/df['MIN']
    df['PF']= df['PF']/df['MIN']
    df=df.drop(columns=['MIN','key'])
    frames.append(df)
playerDF= pd.concat(frames)

df = pd.read_csv("schedule.csv")

df= df[::-1]



df["W/L"].replace('W', 1, inplace=True)
df["W/L"].replace('L', 0, inplace=True)

df['W/L'].replace('2012-13',0.5,inplace= True)
df = df[df['W/L'] != 0.5]

df.drop(columns=['Season','MIN','PTS','FGM','FGA','3PM', '3PA' , 'FTM', 'FTA','REB'],inplace = True)

for i,column in enumerate(df.columns):
    if (i > 2):
        x = np.mean([float(val) for val in df[column] if val!='-'])
        df[column].replace('-', str(x), inplace=True)

matchesPlayed = {}
homeMatches = {}
homeCumm = {}
cummulativeFeatures = {}
for team in df['Team'].unique():
    matchesPlayed[team] = 0
    cummulativeFeatures[team]= [0 for i in range(14)]
    homeMatches[team] = 0
    homeCumm[team] = 0
   

dictx = {}
for team in df['Team'].unique():
    dictx[team] = []
    for i in range(50):
       dictx[team].append([-1])


for i in range(0,len(df),2):
    homeNum = -1
    awayNum = -1
    homeTeam = ''
    awayTeam = ''
    if  'vs.' in df.iloc[i]['Match Up']:
        homeTeam = df.iloc[i]['Team']
        awayTeam = df.iloc[i+1]['Team']
        homeNum = i
        awayNum = i+1
    else:
        homeTeam = df.iloc[i+1]['Team']
        awayTeam = df.iloc[i]['Team']
        homeNum = i+1
        awayNum = i
    
    A = -1
    B = -1
    if (homeMatches[homeTeam]):
        A = homeCumm[homeTeam]/homeMatches[homeTeam]
    
    if (matchesPlayed[awayTeam] - homeMatches[awayTeam]):
        B = (cummulativeFeatures[awayTeam][0]-homeCumm[awayTeam])/(matchesPlayed[awayTeam] - homeMatches[awayTeam])
     
    homeCumm[homeTeam] = homeCumm[homeTeam] + float(df.iloc[homeNum][3])
    dictx[homeTeam][12].append(A)
    dictx[awayTeam][13].append(B)
    dictx[homeTeam][13].append(dictx[homeTeam][13][-1])
    dictx[awayTeam][12].append(dictx[awayTeam][12][-1])
 
        
    for j in range(12):
        A = -1
        B = -1
        
        if (matchesPlayed[homeTeam]):
            A = cummulativeFeatures[homeTeam][j]/matchesPlayed[homeTeam]
        if (matchesPlayed[awayTeam]):
            B = cummulativeFeatures[awayTeam][j]/matchesPlayed[awayTeam]
        dictx[homeTeam][j].append(A)
        dictx[awayTeam][j].append(B)
        cummulativeFeatures[homeTeam][j] = cummulativeFeatures[homeTeam][j] + float(df.iloc[homeNum][j+3])
        cummulativeFeatures[awayTeam][j] = cummulativeFeatures[awayTeam][j] + float(df.iloc[awayNum][j+3])
    
    homeMatches[homeTeam] = homeMatches[homeTeam]+1
    matchesPlayed[homeTeam] = matchesPlayed[homeTeam]+1
    matchesPlayed[awayTeam] = matchesPlayed[awayTeam]+1
    
    
        
matchesPlayed = {}
cummulativeFeatures = {}
for team in df['Team'].unique():
    matchesPlayed[team] = 0
    cummulativeFeatures[team]= [0 for i in range(12)]
    

for i in range(0,len(df)):
    homeTeam =  df.iloc[i]['Team']
    homeID = df.iloc[i]['Match Up']+df.iloc[i]['Game Date']
        
    

        
    for j in range(12):
        A = -1
        if (matchesPlayed[homeTeam]):
            A = cummulativeFeatures[homeTeam][j]/matchesPlayed[homeTeam]
        
        dictx[homeTeam][j+26].append(A)
        cummulativeFeatures[homeTeam][j] = cummulativeFeatures[homeTeam][j] + float(playerDF.loc[homeID][j+3])
        
    
    
    matchesPlayed[homeTeam] = matchesPlayed[homeTeam]+1
    

matchesPlayed = {}
cummulativeFeatures = {}
for team in df['Team'].unique():
    matchesPlayed[team] = 0
    cummulativeFeatures[team]= [[0] for i in range(13)]
    


for i in range(0,len(df),2):
    homeNum = -1
    awayNum = -1
    homeTeam = ''
    awayTeam = ''
    if  'vs.' in df.iloc[i]['Match Up']:
        homeTeam = df.iloc[i]['Team']
        awayTeam = df.iloc[i+1]['Team']
        homeNum = i
        awayNum = i+1
    else:
        homeTeam = df.iloc[i+1]['Team']
        awayTeam = df.iloc[i]['Team']
        homeNum = i+1
        awayNum = i
   
 
        
    for j in range(12):
        A = -1
        B = -1
        
        if (matchesPlayed[homeTeam]):
            if ( matchesPlayed[homeTeam] < 8):
                A = cummulativeFeatures[homeTeam][j][matchesPlayed[homeTeam]]/matchesPlayed[homeTeam]
            else:
                A = (cummulativeFeatures[homeTeam][j][matchesPlayed[homeTeam]]-cummulativeFeatures[homeTeam][j][matchesPlayed[homeTeam]-8])/8
        if (matchesPlayed[awayTeam]):
            if ( matchesPlayed[awayTeam] < 8):
                B = cummulativeFeatures[awayTeam][j][matchesPlayed[awayTeam]]/matchesPlayed[awayTeam]
            else:
                B = (cummulativeFeatures[awayTeam][j][matchesPlayed[awayTeam]]-cummulativeFeatures[awayTeam][j][matchesPlayed[awayTeam]-8])/8
        dictx[homeTeam][j+14].append(A)
        dictx[awayTeam][j+14].append(B)
        cummulativeFeatures[homeTeam][j].append(cummulativeFeatures[homeTeam][j][-1] + float(df.iloc[homeNum][j+3]))
        cummulativeFeatures[awayTeam][j].append(cummulativeFeatures[awayTeam][j][-1] + float(df.iloc[awayNum][j+3]))
    
  
    matchesPlayed[homeTeam] = matchesPlayed[homeTeam]+1
    matchesPlayed[awayTeam] = matchesPlayed[awayTeam]+1


matchesPlayed = {}
cummulativeFeatures = {}
for team in df['Team'].unique():
    matchesPlayed[team] = 0
    cummulativeFeatures[team]= [[0] for i in range(13)]


#features last 8

for i in range(0,len(df)):
    homeTeam =  df.iloc[i]['Team']
    homeID = df.iloc[i]['Match Up']+df.iloc[i]['Game Date']
        
    

        
    for j in range(12):
        A = -1
        if (matchesPlayed[homeTeam]):
            if ( matchesPlayed[homeTeam] < 8):
                A = cummulativeFeatures[homeTeam][j][matchesPlayed[homeTeam]]/matchesPlayed[homeTeam]
            else:
                A = (cummulativeFeatures[homeTeam][j][matchesPlayed[homeTeam]]-cummulativeFeatures[homeTeam][j][matchesPlayed[homeTeam]-8])/8
        dictx[homeTeam][j+38].append(A)
        cummulativeFeatures[homeTeam][j].append(cummulativeFeatures[homeTeam][j][-1] + float(playerDF.loc[homeID][j+3]))
       
    
  
    matchesPlayed[homeTeam] = matchesPlayed[homeTeam]+1
 


matchesPlayed = {}
for team in df['Team'].unique():
    matchesPlayed[team] = 1


features = []
for i,match in enumerate(df['Match Up']):
    if '@' in match:
        continue
    homeTeam = match[0:3]
    awayTeam = match[8:11]
    examples = [match,df['Game Date'].iloc[i],df['W/L'].iloc[i]]
    examples.extend([dictx[homeTeam][i][matchesPlayed[homeTeam]] for i in range(50) if i != 13])
    examples.extend([dictx[awayTeam][i][matchesPlayed[awayTeam]] for i in range(50) if i != 12])
    matchesPlayed[homeTeam] = matchesPlayed[homeTeam] + 1
    matchesPlayed[awayTeam] = matchesPlayed[awayTeam] + 1
    if (examples[15] != -1 and examples[64] != -1):
        features.append(examples)
    
    
headers = ["Match Up", "Game Date", "W/L", "H Win Avg", "H FG%", "H 3P%", "H FT%", "H OREB", "H DREB", "H AST", "H STL", "H BLK", "H TOV", "H PF", "H Pts Diff Avg", "H Win Avg At Home", "H Win Avg Last 8", "H FG% Last 8", "H 3P% Last 8", "H FT% Last 8", "H OREB Last 8", "H DREB Last 8", "H AST Last 8", "H STL Last 8", "H BLK Last 8", "H TOV Last 8", "H PF Last 8", "H Pts Diff Avg Last 8", "H Player Pts Diff Avg", "H Player FG%", "H Player 3P%", "H Player FT%", "H Player OREB", "H Player DREB", "H Player AST", "H Player STL", "H Player BLK", "H Player TOV", "H Player PF", "H Player +/-", "H Player Pts Diff Avg Last 8", "H Player FG% Last 8", "H Player 3P% Last 8", "H Player FT% Last 8", "H Player OREB Last 8", "H Player DREB Last 8", "H Player AST Last 8", "H Player STL Last 8", "H Player BLK Last 8", "H Player TOV Last 8", "H Player PF Last 8", "H Player +/- Last 8", "V Win Avg", "V FG%", "V 3P%", "V FT%", "V OREB", "V DREB", "V AST", "V STL", "V BLK", "V TOV", "V PF", "V Pts Diff Avg", "V Win Avg On Visit", "V Win Avg Last 8", "V FG% Last 8", "V 3P% Last 8", "V FT% Last 8", "V OREB Last 8", "V DREB Last 8", "V AST Last 8", "V STL Last 8", "V BLK Last 8", "V TOV Last 8", "V PF Last 8", "V Pts Diff Avg Last 8", "V Player Pts Diff Avg", "V Player FG%", "V Player 3P%", "V Player FT%", "V Player OREB", "V Player DREB", "V Player AST", "V Player STL", "V Player BLK", "V Player TOV", "V Player PF",  "V Player +/-", "V Player Pts Diff Avg Last 8", "V Player FG% Last 8", "V Player 3P% Last 8", "V Player FT% Last 8", "V Player OREB Last 8", "V Player DREB Last 8", "V Player AST Last 8", "V Player STL Last 8", "V Player BLK Last 8", "V Player TOV Last 8", "V Player PF Last 8", "V Player +/- Last 8"]


pd.DataFrame(features).to_csv('NBAGameDataset.csv',header=headers,index = None)



