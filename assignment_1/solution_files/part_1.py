# Solution to Part 1 of the assignment.

# The columns are organized as # of Summer games, Summer medals,
# # of Winter games, Winter medals, total # number of games, total # of medals

# creating and shapping data set to be used for answering question.


import pandas as pd

# reading csv file, setting index to column 0 , skipping first row.
df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

#updating column names.
for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


''' Question 1:
Which country has won the most gold medals in summer games?'''

def answer_one():
    return df['Gold'].idxmax()


''' Question 2:
Which country had the biggest difference between their summer
and winter gold medal counts? '''

def answer_two():
    return abs((df['Gold'] - df['Gold.1'])).idxmax()


''' Question 3:
Which country has the biggest difference between their summer gold medal counts and winter gold medal
counts relative to their total gold medal count? '''

def answer_three():

    #filtering out countries which did not win any gold. 
    temp_df = df[(df['Gold'] > 0) & (df['Gold.1'] > 0)]
    return (abs(temp_df['Gold'] - temp_df['Gold.1']) / (temp_df['Gold'] + temp_df['Gold.1'])).idxmax()


''' Question 4:
Write a function that creates a Series called "Points" which is a weighted value
where each gold medal (Gold.2) counts for 3 points, silver medals (Silver.2) for
2 points, and bronze medals (Bronze.2) for 1 point.The function should return
only the column (a Series object) which you created. '''

def answer_four():

    #creating series of weighted values of medals.
    Points = df['Gold.2'] * 3 + df['Silver.2'] * 2 + df['Bronze.2'] * 1
    return Points


