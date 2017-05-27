# Solution to Part 2 of the assignment.

# reading data from csv.
import pandas as pd

census_df = pd.read_csv('census.csv')
census_df.head()

''' Question 5:
Which state has the most counties in it? 
(hint: consider the sumlevel key carefully! You'll need this for 
future questions too...)'''

def answer_five():
    y = list()
    
    #extracting rows where 'SUMLEV' = 50 (i.e counties)
    census_df_temp = census_df[census_df['SUMLEV'] == 50] 
    
    unique_states = census_df_temp['STNAME'].unique()
    
    for st in unique_states:
        # creating a list of state name with their count of counties.
        y.append((len(census_df_temp[census_df_temp['STNAME'] == st]),st))
        
    y.sort(reverse = True)
    
    return y[0][1]


'''Question 6:
Only looking at the three most populous counties for each state, what are the 
three most populous states (in order of highest population to lowest 
population)? Use CENSUS2010POP.'''


def answer_six():
    
    census_cp = census_df.copy()
    census_cp = census_cp[census_cp['SUMLEV']==50] # extracting counties.
    census_cp = census_cp[['STNAME','CTYNAME','CENSUS2010POP']] #Keeping Columns STNAME, CTYNAME, CENSUS2010POP only
    unique_states = census_cp['STNAME'].unique()
    states_top3_cty_pop = list()
    
    for st in unique_states:  # loop to find top three most populous counties states.
        temp = census_cp[census_cp['STNAME']==st]
        temp = temp.sort_values('CENSUS2010POP',ascending=False) # sorting in descending order
        if len(temp) >= 3 :
            temp = temp.head(3)
            states_top3_cty_pop.append((temp['CENSUS2010POP'].sum(),st)) #appending sum of three most populous counties of each state.
        else:
            temp = temp.head(len(temp)) # case where state has less than 3 counties.
            states_top3_cty_pop.append((temp['CENSUS2010POP'].sum(),st)) 
        
    states_top3_cty_pop.sort(reverse = True)
    top3states = states_top3_cty_pop[:3] # extraction top 3 populous states.
    top3states = [top3states[0][1], top3states[1][1], top3states[2][1]]
    return top3states


'''Question 7:
Which county has had the largest absolute change in population within the period
2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 
through POPESTIMATE2015, you need to consider all six columns.)'''

def answer_seven():
    temp = census_df[census_df['SUMLEV']==50]
    # subsetting data frame, keeping all rows and only columns mentioned.
    temp = temp.loc[:,
                         ['CTYNAME','POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012', 
                          'POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']]
    temp = temp.set_index('CTYNAME')
    
    return abs(temp['POPESTIMATE2015']-temp['POPESTIMATE2010']).idxmax()


''' Question 8:
In this datafile, the United States is broken up into four regions using the 
"REGION" column. 
Create a query that finds the counties that belong to regions 1 or 2, 
whose name starts with 'Washington', and whose POPESTIMATE2015 was greater 
than their POPESTIMATE 2014.'''


def answer_eight():
    census_df_temp = census_df[census_df['SUMLEV'] == 50]
    
    return census_df_temp[(census_df_temp['CTYNAME'].str.startswith('Washington')) & ((census_df_temp['REGION'] == 1) | (census_df_temp['REGION'] == 2)) & ((census_df_temp['POPESTIMATE2015'] > census_df_temp['POPESTIMATE2014']))].loc[:,['STNAME','CTYNAME']]