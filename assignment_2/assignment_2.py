
import pandas as pd
import numpy as np

# global variabl will be used in answer 1 and answer 2
joined_df = None 
odf = None



def change_energy_supply(df, column): #function to convert energy supply to gigajoules
    
    df[column] = df[column] * 1000000
      

def remove_pranthesis(df): # function to remove paranthesis from the name of countries.
   
    for i in df['Country'].index:
        if '(' in df['Country'].iloc[i]:
            index = df['Country'].iloc[i].find('(')
            df['Country'][i] = df['Country'][i][:index - 1]

def remove_numbers_from_end(df): #function to remove numbers from end of the country names.
    
    df['Country'] = df['Country'].str.extract('(^[A-z].*[a-z])',expand = True)
    df.replace(to_replace={"Republic of Korea": "South Korea",
                       "United States of America": "United States",
                       "United Kingdom of Great Britain and Northern Ireland": 
                           "United Kingdom",
                       "China, Hong Kong Special Administrative Region":
                           "Hong Kong"}, inplace=True)


def load_and_clean_energy_indicators(file_name):
    
    df = pd.read_excel(file_name,header = None, skiprows = 18)
    
    df = df.loc[:,[2,3,4,5]].rename(columns = {2:'Country',3:'Energy Supply',
                                 4:'Energy Supply per Capita',
                                 5:'% Renewable'}).dropna().replace('...',np.NaN)
    remove_numbers_from_end(df)
    remove_pranthesis(df)
    change_energy_supply(df,'Energy Supply')
    

    return df
    
def load_and_clean_gdp(file_name):
    df = pd.read_csv(file_name, skiprows = 4)
    df.replace(to_replace = {"Korea, Rep.": "South Korea",
                             "Iran, Islamic Rep.": "Iran",
                             "Hong Kong SAR, China": "Hong Kong"},inplace = True)
    return df

def load_and_clean_scimen(file_name):
    return pd.read_excel(file_name)




''' Question 1: For description refer README.md.
Extracting and cleaning data from 3 sources as mentioned in README.md.
This data set will be used in entire assignment.'''

def answer_one():
    
    file_energy = 'Energy Indicators.xls'
    file_gdp    = 'world_bank.csv'
    file_scimen = 'scimagojr-3.xlsx'
    energy = load_and_clean_energy_indicators(file_energy)
    
    GDP = load_and_clean_gdp(file_gdp)
    GDP.rename(columns = {'Country Name':'Country'},inplace = True)
    ScimEn = load_and_clean_scimen(file_scimen)
    
    global joined_df # referring global variable
    global odf # referring global variable
    
    joined_df = pd.merge(ScimEn,pd.merge(GDP, energy, how='inner', left_on='Country',
                           right_on='Country'), how='inner', left_on='Country',
                        right_on='Country')  # merging three data frames on Country.
    #print (joined_df.shape[0])
    odf = pd.merge(ScimEn,pd.merge(GDP, energy, how='outer', left_on='Country',
                           right_on='Country'), how='outer', left_on='Country',
                        right_on='Country') # merging data frame using outer join.
    #print(odf.shape[0])
    joined_df.set_index('Country', inplace = True) # setting index to Country

    cols_required = ['Rank', 'Documents', 'Citable documents', 'Citations',
                 'Self-citations', 'Citations per document', 'H index', 
                 'Energy Supply', 'Energy Supply per Capita', '% Renewable',
                 '2006', '2007', '2008', '2009', '2010', '2011', '2012',
                 '2013', '2014', '2015'] #Required Columns.
 
    return joined_df[cols_required].head(15) 




''' Question 2:
The previous question joined three datasets then reduced this to just the top 15
entries. When you joined the datasets, but before you reduced this to the top 15 
items, how many entries did you lose? '''


def answer_two():
    f = answer_one() # creating data frame.
    
    #odf contains all the rows of the data frame created using outer join.
    #joined_df cointains rows of the data frame created using inner join.
    
    entries_lost = odf.shape[0] - joined_df.shape[0] # number of rows lost.
    return entries_lost




'''Question 3:
What is the average GDP over the last 10 years for each country? 
(exclude missing values from this calculation.) '''


def answer_three():
    Top15 = answer_one()#.replace(np.NaN,0) #getting top 15 countries and their data
    rows = ['2006', '2007', '2008', '2009', 
                '2010', '2011', '2012',
                '2013', '2014', '2015'] # columns on which mean has to be calculated for each country.
    
    avgGDP = Top15.apply(lambda x: np.mean(x[rows]),axis = 1).sort_values(ascending = False)#calculating mean of each country using np.mean().
    #avgGDP.sort_values(ascending = False, inplace = True)
    
    return avgGDP


'''Question 4:
By how much had the GDP changed over the 10 year span for the country with the 
6th largest average GDP? '''

def answer_four():
    Top15 = answer_one()
    rows = ['2006', '2007', '2008', '2009', 
            '2010', '2011', '2012',
            '2013', '2014', '2015']
        
    avgGDP = Top15.apply(lambda x: np.mean(x[rows]),axis = 1).sort_values(ascending = False) 
    
    countries = avgGDP.index[5]
    return Top15.loc[countries,'2015'] - Top15.loc[countries,'2006']




'''Question 5:
What is the mean Energy Supply per Capita?'''

def answer_five():
    Top15 = answer_one()
    return Top15['Energy Supply per Capita'].mean()




'''Question 6:
What country has the maximum % Renewable and what is the percentage?'''

def answer_six():
    Top15 = answer_one()
    max_renewable = Top15['% Renewable'].max() #finding maximum 
    max_index = Top15['% Renewable'].idxmax() # finding maximum index(country)
    return (max_index,max_renewable)



'''Question 7:
Create a new column that is the ratio of Self-Citations to Total Citations. 
What is the maximum value for this new column, and what country has the 
highest ratio?'''

def answer_seven():
    Top15 = answer_one()
    Top15['Ratio self/total'] = Top15['Self-citations'] / Top15['Citations'] # adding new column Ratio self/total
    return (Top15['Ratio self/total'].idxmax(), 
            Top15['Ratio self/total'].max())



'''Question 8:
Create a column that estimates the population using Energy Supply and 
Energy Supply per capita. What is the third most populous country according to 
this estimate?'''

def answer_eight():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15.sort_values('PopEst', ascending = False, inplace = True)
    return Top15.index[2]



'''Question 9:
Create a column that estimates the number of citable documents per person. 
What is the correlation between the number of citable documents per capita and 
the energy supply per capita? Use the .corr() method, (Pearson's correlation).'''

def answer_nine():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents']/Top15['PopEst']
    return Top15['Citable docs per Capita'].corr(Top15['Energy Supply per Capita'])




'''Question 10:
Create a new column with a 1 if the country's % Renewable value is at or above 
the median for all countries in the top 15, and a 0 if the country's % Renewable
value is below the median.
This function should return a series named HighRenew whose index is the country 
name sorted in ascending order of rank. '''


def answer_ten():
    Top15 = answer_one()
    Top15_r_median = Top15['% Renewable'].median()
    Top15['HighRenew'] = np.where(Top15['% Renewable'] >= Top15_r_median,1,0) #this will put 1 for HighRow column for rows having value greater than median and 0 for others.
    return Top15['HighRenew']




'''Question 11:
Use the dictionary mentioned in README.md to group the Countries by Continent, 
then create a dateframe that displays the sample size (the number of countries 
in each continent bin), and the sum, mean, and std deviation for the estimated 
population of each country.

This function should return a DataFrame with index named Continent 
['Asia', 'Australia', 'Europe', 'North America', 'South America'] and 
columns ['size', 'sum', 'mean', 'std']'''

def answer_eleven():
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
        
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita'] # calculating poplulation estimate
    Top15['Continent'] = pd.Series(ContinentDict) #adding continent column
        
    return Top15.set_index('Continent').groupby(level = 0)['PopEst'].agg({
            'size':np.count_nonzero,
            'sum':np.sum,'mean':np.mean,
            'std':np.std})



'''Question 12:
Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these 
new % Renewable bins. How many countries are in each of these groups?
This function should return a Series with a MultiIndex of Continent, 
then the bins for % Renewable. Do not include groups with no countries.'''


def answer_twelve():
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
        
    Top15 = answer_one() 
    Top15.reset_index()
    Top15['Continent'] = pd.Series(ContinentDict)
    Top15['bin'] = pd.cut(Top15['% Renewable'],5) #cutting in bins.
    return Top15.groupby(['Continent','bin']).size()



'''Question 13:
Convert the Population Estimate series to a string with thousands separator 
(using commas). Do not round the results.
e.g. 317615384.61538464 -> 317,615,384.61538464
This function should return a Series PopEst whose index is the country name 
and whose values are the population estimate string.'''


def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
        
    return Top15['PopEst'].apply(lambda x : '{:,}'.format(x))