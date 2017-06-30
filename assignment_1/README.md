## Part 1
Load the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table).

### Answer the following Questions: -
	
* Question 1 : - Which country has won the most gold medals in summer games?

* Question 2 : - Which country had the biggest difference between their summer and winter gold medal counts?
* Question 3 : - Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold  medal count? 
	* Only include countries that have won at least 1 gold in both summer and winter.

* Question 4 :- Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created.
	
## Part 2
For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov/popest/data/counties/totals/2015/CO-EST2015-alldata.html). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](http://www.census.gov/popest/data/counties/totals/2015/files/CO-EST2015-alldata.pdf) for a description of the variable names.
The census dataset (census.csv) should be loaded as census_df. 

### Answer questions using this as appropriate: -
* Question 5 : - Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
	
* Question 6 : Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
	
* Question 7 : - Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)

* Question 8 : - In this datafile, the United States is broken up into four regions using the "REGION" column. 
	Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.

