# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 07:43:49 2023

@author: space

"""

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CITY_DATA = { 'Chicago': 'D:/42_Amie Projects/Python/Udacity/all-project-files/chicago.csv',
              'New York City': 'D:/42_Amie Projects/Python/Udacity/all-project-files/new_york_city.csv',
              'Washington': 'D:/42_Amie Projects/Python/Udacity/all-project-files/washington.csv' }

def get_filters():
    """Ask user to specify a city, month, and day to analyze; Returns: city, month, day"""

    city_choices = ['Chicago', 'New York City', 'Washington']
    month_choices = ['January', 'February', 'March', 'April', 'May', 'June', 'All', ""]
    day_choices = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All', ""]
    
    print('\nHello! Let\'s explore some US bikeshare data!')

# get user input for city (chicago, new york city, washington)
    while True:
        city = str(input('Choose one of these major cities to begin the exploration: Chicago, New York City, or Washington. \n\nPlease type the name of the city and hit ENTER:  ')).title()
        if city not in city_choices:
            print('\nI\'m sorry, I don\'t understand that city entry, please try again')
        else:
            print('\nGreat, you want to learn more about bikeshare data in', city) 
            break
 
# get user input for month (all, january, february, ... , june)
    while True:
        month = str(input('\nNow, which specific month would you like to learn more about? You can choose among: January, February, March, April, May, or June. You can also choose all by typing \'All\'. \n\nPlease type the name of the month or type \'All\' and hit ENTER:  ')).capitalize()
        if month not in month_choices:
            print('\nI\'m sorry, I don\'t understand that month entry, please try again')
        elif month != 'All':
            print('\nGreat, you chose to learn more about bikeshare data in', city, 'in the month of', month)
            break
        elif month == 'All':
            print('\nGreat, you chose to learn more about bikeshare data in all available months in', city)
            break

#get user input for day (all, Monday, ..., Sunday)
    while True:
        day = str(input('Finally, before revealing the bikeshare data, please choose a specific day of the week that you are most interested in (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) or you can choose \'All\' by typing \'All\':  ')).capitalize()
        if day not in day_choices:
            print('\nI\'m sorry, I don\'t understand that day entry, please try again')
        elif day !=  'All':
            print('\nGreat! So you want to learn more about bikeshare data in ', city, ' on ', day + 's', 'in', month)
            break
        elif day == 'All':
            if month == 'All':
                print('\nGreat! So you want to learn more about bikeshare data in ', city, 'throughout the week for all months')
                break
            elif month != 'All':
                print('\nGreat! So you want to learn more about bikeshare data in ', city, 'throughout the week in', month)
                break

    while True:
        answer = str(input('\nIs that correct? Please type \'Yes\' to continue or \'No\' to re-start the search: ')).capitalize()

        if answer == 'Yes':
            print('\nGreat, just a moment, retrieving your requested bikeshare data ...\n')
            break
        elif answer == 'No':
            print('\nBeginning the search again ... \n')
            main()
        elif answer != 'Yes' or 'No':
            print('\nI\'m sorry, I don\'t understand that entry, please try again')
    print('- '*25)
    return city, month, day

def load_data(city, month, day):
    """ Loads data for the filtered inputs and returns a filtered pandas df """

    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])       
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month                     
    df['day_of_week'] = df['Start Time'].dt.day_name()     
   
    # filter by month if applicable
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    if month != 'All':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
    # filter by month to create the new dataframe
        df = df[df['month'] == month]
                      
    # now filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df, city, month='All'):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    if month == 'All':
        df['month'] = df['Start Time'].dt.month
#       mo_counts = df['month'].value_counts()
        max_mo_count = df['month'].value_counts().keys().tolist()
        popular_month = max_mo_count[0]
        print('The most popular month is: ', months[popular_month-1])

    # display the most common day of week
    day_counts = df['day_of_week'].value_counts()
    max_day_count = df['day_of_week'].value_counts().keys().tolist()
    popular_day = max_day_count[0]
    print('The most popular day is: ', popular_day)

    print('\nNumber of Users By Day of the Week:\n', day_counts, '\n')
    plt.pie(day_counts, labels=day_counts.index[:], autopct='%1.1f%%')
    plt.title('Bikeshare Usage by Day in ' + city, bbox={'facecolor':'0.8', 'pad':6})
    plt.show()

    # display the most common start hour - GOOD
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')

# find the most common hour (from 0 to 23)
    df['hour'] = df['Start Time'].dt.hour
#   hour_counts = df['hour'].value_counts()
    max_count = df['hour'].value_counts().keys().tolist()
    popular_hour = max_count[0]
    print('The most popular hour is: ', popular_hour)
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('- '*25)
        
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    max_pop_station = df['Start Station'].value_counts().keys().tolist()
    popular_station = max_pop_station[0]
    print('The most popular start station is: \n', popular_station)

    # display most commonly used end station
    max_pop_endstation = df['End Station'].value_counts().keys().tolist()
    popular_endstation = max_pop_endstation[0]
    print('\nThe most popular ending station is: \n', popular_endstation)

    # display most frequent combination of start station and end station trip
    # created a series from two columns to be able to use .value_counts()
    route_counts = pd.Series((df['Start Station'] + '   to   ' + (df['End Station'])))
    max_pop_route = route_counts.value_counts().keys().tolist()
    popular_route = max_pop_route[0]
    print('\nThe most frequent route is: \n', popular_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('- '*25)


def convert_to_hours_mins(sec):
    """ Converts seconds into HH:MM:SS"""
    time_format = time.strftime("%H:%M:%S", time.gmtime(sec))  
    return time_format

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time for all trips was: ', convert_to_hours_mins(df['Trip Duration'].sum()), '(hh:mm:ss)')
    
    # display mean travel time
    print('The mean travel time for all trips was: ', convert_to_hours_mins(int(df['Trip Duration'].mean())), '(hh:mm:ss)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('- '*25)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print('Number of User Types, Subscriber vs Customer:\n', user_types, '\n')
    plt.pie(user_types, labels=user_types.index[:], autopct='%1.1f%%')

    plt.title('Bikeshare Usage by User Type in ' + city, bbox={'facecolor':'0.8', 'pad':6})
    plt.show()

    if city != 'Washington':
        # Display counts of gender
        counts_by_gender = df['Gender'].value_counts()

        print('Number of Users By Gender:\n', counts_by_gender, '\n')
        plt.pie(counts_by_gender, labels=counts_by_gender.index[:], autopct='%1.1f%%')

        plt.title('Bikeshare Usage by Gender in ' + city, bbox={'facecolor':'0.8', 'pad':6})
        plt.show()
        # Display earliest, most recent, and most common year of birth
        print('\nThe earliest birth year was:', int(df['Birth Year'].min()))
        print('\nThe most recent birth year was:', int(df['Birth Year'].max()))
        print('\nThe most common birth year was:', int(df['Birth Year'].mode()))
    elif city == 'Washington':
        print('Note: There is no Rideshare data available by gender or birth year for', city)
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('- '*25)
    
def raw_data(df, city):
    """Ask user if they want to see the raw data associated with their search? If yes, display five lines at a time"""

# get user input seeing raw data or not
    i = 5
    while True:
        display_raw = str(input('Would you also like to see the raw data associated with your search? Type \'Yes\' or \'No\' : ')).title()
        if display_raw == 'Yes':
            print('\nRetrieving filtered, raw data...\n')
            start_time = time.time()
            print('Displaying the first five lines of filtered raw data for ', city, ': ', df.head())
            while True:
                more_lines = str(input('\nTo display the next five lines of data, type \'M\', or you can type \'Q\' to exit out of this view : ').title())

                if more_lines == "M":
                    j = df.shape[0] - 1  # use as index limit to raw data
                    print('\nThere are ', j + 1, ' rows in your filtered search:')
                    if i + 5 == j:
                        print('Displaying rows ', i+1, ' through ', j+1, 'of the filtered raw data: ', df[i:j+1])
                        print('That is the end of the raw data for your search.')
                        break
                    elif i + 5 > j and i < j:
                        print('Displaying rows ', i+1, ' through ', j+1, 'of the filtered raw data: ')
                        print(df[i:j+1])
                        print('That is the end of the raw data for your search.')
                        break
                    elif i + 5 < j:
                        print('Displaying rows ', i+1, ' through ', i+5, ' of the filtered raw data: ')
                        print(df[i:i+5])
                    i += 5
                elif more_lines == 'Q':
                    print("\nThis took %s seconds." % (time.time() - start_time))
                    break
                elif more_lines != 'M' or 'Q':
                    print('I\'m sorry, I don\'t understand that response, please try again.')
            break
        elif display_raw == 'No':
            break
        elif display_raw != 'Yes' or 'No':
            print('\nI\'m sorry, I don\'t understand that that response, please try again')
    
    print('- '*25)

# # # # # # # # # # # # # # #    main()    # # # # # # # # # # # # # # # # # # # # #

def main():
    """ This is the main function to run the other functions """
    city, month, day = get_filters()
# comment the line above to use 'canned' inputs; this is just to run testing without having to type each entry
#   city = 'Chicago'
#   month = 'All'
#   day = 'All'

    df = load_data(city, month, day)
    time_stats(df, city, month)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df, city)
    raw_data(df, city)
        
    while True:
        restart = str(input('Would you like to restart your search? Please type \'Yes\' or \'No\': ')).capitalize()
        if restart == 'Yes':
            main()
        elif restart == 'No':
            print('\nThank you for learning about bikeshare data in the US! Good-bye')
            break
        elif restart.title() != 'Yes' or 'No':
            print('\nI\'m sorry, I don\'t understand that entry, please try again')
            
# the following returns true when running the script and kicks off the process/program
if __name__ == "__main__":
	main()
   
    

""" 
Note: The following links are also copied in a text file separately.

Resources used in writing this project:

For user input until validation passes:
https://bobbyhadz.com/blog/python-input-validation

For a refresher on funcationality of the  expression: __name__ == "__main__"
https://realpython.com/if-name-main-python/

Exporting a df to a csv:
https://www.freecodecamp.org/news/dataframe-to-csv-how-to-save-pandas-dataframes-by-exporting/#:~:text=to_csv()%20Method,format%20for%20storing%20tabular%20data.

https://www.digitalocean.com/community/tutorials/pandas-to_csv-convert-dataframe-to-csv

https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html

GroupBy refresher:
https://stackoverflow.com/questions/35268817/unique-combinations-of-values-in-selected-columns-in-pandas-data-frame-and-count

Converting seconds to H/M/S:
https://www.digitalocean.com/community/tutorials/python-convert-time-hours-minutes-seconds

Creating a pie chart:
https://www.w3schools.com/python/matplotlib_pie_charts.asp

Accessing the index labels of a series - pulled these into the labels for the pie chart
https://stackoverflow.com/questions/18327624/find-elements-index-in-pandas-series

Adding a title and percentages to a piechart
https://www.w3resource.com/graphics/matplotlib/piechart/matplotlib-piechart-exercise-2.php

Reminder about how to get the number of rows in a dataframe:
https://stackoverflow.com/questions/20297332/how-do-i-retrieve-the-number-of-columns-in-a-pandas-data-frame
    
"""
