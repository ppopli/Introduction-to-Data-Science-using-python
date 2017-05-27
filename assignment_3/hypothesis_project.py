import pandas as pd
import numpy as np
from scipy.stats import ttest_ind # for t-test

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 
          'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 
          'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 
          'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 
          'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 
          'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan',
          'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 
          'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 
          'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands',
          'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 
          'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 
          'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma',
          'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 
          'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 
          'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 
          'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 
          'ND': 'North Dakota', 'VA': 'Virginia'}




def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    
    list_of_University_towns = []
    state = None
    regionName = None
    with open('university_towns.txt') as fileUni:
        for l in fileUni:
            l = l.rstrip('\n')
            if l.endswith('[edit]'):
                index = l.find('[')
                state = l[:index]
                continue
            else :
                if '(' in l :
                    regionIndex = l.find('(')
                    regionName = l[:regionIndex - 1]
                else :
                    regionName = l
            list_of_University_towns.append([state, regionName])
    
    return  pd.DataFrame(list_of_University_towns,
                                     columns = ['State', 'RegionName'])




def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    gdp_data = pd.read_excel('gdplev.xls', skiprows = 220, header = None,
                                      parse_cols = "E,G", names = np.array([
                                             'Quater', '$Value']))
    quater_values = gdp_data['$Value']
    recession_start = None
        
    for i in range(quater_values.count()):
        if quater_values.iloc[i] <  quater_values.iloc[i-1] and \
                quater_values.iloc[i+1] < quater_values.iloc[i]:
                    recession_start = gdp_data.iloc[i]['Quater']
                    break;
            
    return recession_start




def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    gdp_data = pd.read_excel('gdplev.xls', skiprows = 220, header = None,
                                      parse_cols = "E,G", names = np.array([
                                             'Quater', '$Value']))
    recession_start_quater = get_recession_start()
    recession_start_index  = gdp_data[
                gdp_data['Quater'] == recession_start_quater].index[0]
    
    quater_values = gdp_data.loc[recession_start_index:,:]
    values = quater_values['$Value']
    recession_end = None
       
    for i in range(values.count()):
        if values.iloc[i] > values.iloc[i - 1] and \
            values.iloc[i - 1] > values.iloc[i - 2]:
                recession_end =  quater_values.iloc[i]['Quater']
                break;
                 
    return recession_end



def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
   
    gdp_data = pd.read_excel('gdplev.xls', skiprows = 220, header = None,
                                      parse_cols = "E,G", names = np.array([
                                             'Quater', '$Value']))
    recession_start = get_recession_start()
    recession_end   = get_recession_end()
       
    recession_start_index  = gdp_data[
            gdp_data['Quater'] == recession_start].index[0]
        
    recession_end_index  = gdp_data[
            gdp_data['Quater'] == recession_end].index[0]
         
    quater_values = gdp_data.loc[
                recession_start_index:recession_end_index,:].set_index('Quater')
        
    return quater_values['$Value'].idxmin()



def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    m_all_homes_data = pd.read_csv('City_Zhvi_AllHomes.csv')
        
    cols = m_all_homes_data.columns
    cols = cols [cols.get_loc('2000-01') : ]
    tdf = m_all_homes_data[cols]
    tdf.columns = pd.to_datetime(tdf.columns)
    main_df = tdf.resample('Q',axis = 1).mean().rename(columns = 
                              lambda x : '{}q{}'.format(x.year,x.quarter))
        
    main_df['State'] = m_all_homes_data['State']
    main_df['State'].replace(to_replace = 
            {'OH': 'Ohio', 'KY': 'Kentucky', 
            'AS': 'American Samoa', 'NV': 'Nevada', 
            'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama',
            'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 
            'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois',
            'TN': 'Tennessee', 'DC': 'District of Columbia', 
            'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 
            'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 
            'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 
            'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 
            'MS': 'Mississippi', 'PR': 'Puerto Rico', 
            'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota',
            'MP': 'Northern Mariana Islands', 'IA': 'Iowa',
            'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia',
            'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 
            'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 
            'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 
            'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 
            'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands',
            'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia',
            'ND': 'North Dakota', 'VA': 'Virginia'},inplace = True)
        
    main_df['RegionName'] = m_all_homes_data['RegionName']
    main_df.set_index(['State','RegionName'],inplace = True)
    
    return main_df




def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    
    hdf = convert_housing_data_to_quarters()
    recession_start = get_recession_start()
    recession_bottom = get_recession_bottom()
    university_towns = get_list_of_university_towns()
    quater_before_recession_start = hdf.columns[hdf.columns.
                                                get_loc(recession_start)-1] 
        
    hdf['price ratio'] = hdf[quater_before_recession_start].div(hdf[
            recession_bottom])
        
    ul_tuple = [ tuple(x) for x in university_towns.values]
        
    ul_towns = hdf.loc[ul_tuple]
    non_ul_towns = hdf.loc[~hdf.index.isin(ul_tuple)]
        
    t_result  = ttest_ind(non_ul_towns['price ratio'], ul_towns['price ratio'],
                            nan_policy = 'omit' )
    different = t_result.pvalue < 0.01 
    p = t_result.pvalue
    better = ("non-university town","university town")[ 
            ul_towns['price ratio'].mean() < non_ul_towns['price ratio'].mean()]
    return (different,p,better)



if __name__ == '__main__':
    ttest_result = run_ttest()
    print (ttest_result)