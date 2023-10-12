import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input("Enter city (chicago, new york city, washington): ").lower()
        if city in CITY_DATA:
            break
        print("Invalid city. Please try again.")
    
    months = set(['all', 'january', 'february', 'march', 'april', 'may', 'june'])
    while True:
        month = input("Enter month (all, january, february, ..., june): ").lower()
        if month in months:
            break
        print("Invalid month. Please try again.")
    
    days = set(['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
    while True:
        day = input("Enter day of week (all, monday, tuesday, ..., sunday): ").lower()
        if day in days:
            break
        print("Invalid day. Please try again.")
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months.index(month) + 1  # adding 1 as month_index should start from 1 for January
        df = df[df['Start Time'].dt.month == month_index]
    
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        df = df[df['Start Time'].dt.dayofweek == days.index(day)]
    
    return df
    
    
    

def convert_seconds(seconds):
    """
    Convert seconds into days, hours, minutes, and seconds.

    Args:
        seconds (int): Time in seconds
    
    Returns:
        str: Time in a readable format
    """
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    return f'{days} days, {hours} hours, {minutes} minutes, {seconds} seconds'

def time_stats(df):
    """
    Display statistics on the most frequent times of travel.

    Args:
        df (DataFrame): Pandas DataFrame containing city data
    
    Returns:
        None
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    common_month = df['Start Time'].dt.month.mode()[0]
    print(f'Most Common Month: {common_month}')

    common_day = df['Start Time'].dt.dayofweek.mode()[0]
    print(f'Most Common Day: {common_day}')

    common_hour = df['Start Time'].dt.hour.mode()[0]
    print(f'Most Common Hour: {common_hour}')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
        
        
        
def display_raw_data(df):
    """
    Prompt the user to view 5 lines of raw data, continue prompting until user opts out.

    Args:
        df (DataFrame): Pandas DataFrame containing city data
    
    Returns:
        None
    """
    row_index = 0
    while True:
        user_input = input("Would you like to see 5 lines of raw data? Enter yes or no: ").lower()
        if user_input == 'yes':
            print(df[row_index: row_index + 5])
            row_index += 5
        elif user_input == 'no':
            break
        else:
            print("Invalid input. Please enter yes or no.")
            
            
def station_stats(df):
    """
    Display statistics on the most popular stations and trip.

    Args:
        df (DataFrame): Pandas DataFrame containing city data
    
    Returns:
        None
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    common_start_station = df['Start Station'].mode()[0]
    print(f'Most Commonly Used Start Station: {common_start_station}')

    common_end_station = df['End Station'].mode()[0]
    print(f'Most Commonly Used End Station: {common_end_station}')

    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print(f'Most Frequent Combination of Start Station and End Station Trip: {common_trip}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def trip_duration_stats(df):
    """
    Display statistics on the total and average trip duration.

    Args:
        df (DataFrame): Pandas DataFrame containing city data
    
    Returns:
        None
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total Travel Time: {convert_seconds(total_travel_time)}')
    
    mean_travel_time = df['Trip Duration'].mean()
    print(f'Average Travel Time: {convert_seconds(int(mean_travel_time))}')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def user_stats(df):
    """
    Display statistics on bikeshare users.

    Args:
        df (DataFrame): Pandas DataFrame containing city data
    
    Returns:
        None
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types_counts = df['User Type'].value_counts()
    print(f'Counts of User Types:\n{user_types_counts}')

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f'Counts of Gender:\n{gender_counts}')

    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print(f'Earliest Year of Birth: {int(earliest_birth_year)}')
        print(f'Most Recent Year of Birth: {int(recent_birth_year)}')
        print(f'Most Common Year of Birth: {int(common_birth_year)}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def main():
    """
    Main function to run the program: 
    1. Get filters from the user 
    2. Load the data 
    3. Display raw data if the user desires
    4. Display various statistics
    5. Prompt the user to restart or exit

    Returns:
        None
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
