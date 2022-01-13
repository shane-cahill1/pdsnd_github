import time
import pandas as pd
import datetime as dt
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

    city = input("Please input city name, chicago, new york city or washington? \nIf you would like more than one city, please sepereate your list with a comma: ").lower()
    while city not in CITY_DATA:
        city = input("City name is invalid, please input a valid City: ").lower()


    month = input("Please input months from January to June, \nIf you would like to analyze every month please type 'all': ").lower()
    while month != 'all' and month not in ['january', 'february', 'march', 'april', 'may', 'june']:
        month = input("Month is invalid, please select months between January and June: ").lower()


    day = input("Please choose a day of the week between Sunday and Saturday, \nIf you would like to analyze every day, please type 'all': ").lower()
    while day != 'all' and day not in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
        day = input("Day is invalid, please select a day between Sunday and Saturday:")

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
    df['Start Hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        days_of_week = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = days_of_week.index(day) + 1

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    df['most_common_month'] = df['Start Time'].dt.month_name()
    most_common_month = df['most_common_month'].mode().values[0]
    print("The most common month within the selected filter is: ", most_common_month)



    most_common_day = df['day'].mode().values[0]
    print("The most common day of the week within the selected filter is: ", str(most_common_day))


    most_common_hour = df['Start Hour'].mode().values[0]
    print("The most common start hour for the selected filter is: ", str(most_common_hour) +".00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    most_common_start_station = df['Start Station'].mode().values[0]
    print("For the selected filters, the most common start station is: ", most_common_start_station)


    most_common_end_station = df['End Station'].mode().values[0]
    print("For the selected filters, the most common end station is: ", most_common_end_station)


    most_popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("For the selected filters, the most popular start and end stations are: ", most_popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = df['Trip Duration'].sum()


    print("In seconds, the total travel time was", total_time, "seconds, and in hours the total travel time was", total_time/3600, "hours.")


    avg_travel_time = df['Trip Duration'].mean()
    print("The average travel time in seconds was", avg_travel_time, "seconds, and in hours the avergae travel time was", avg_travel_time/3600, "hours.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    user_type_count = df['User Type'].value_counts()
    print('The counts of user types:', user_type_count)


    if 'Gender' in df:
        print('The counts of gender types:', df['Gender'].value_counts())

    if 'Birth Year' in df:
        print('The earliest year of birth for a user is: ', df['Birth Year'].min())
        print('The youngest user has a year of birth of: ', df['Birth Year'].max())
        print('The most common year of birth is: ', df['Birth Year'].mode().values[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    while True:
        response=['yes', 'no']
        choice = input("Would you like to see 5 lines of individual bikeshare data? Type 'yes' or 'no': ").lower()
        if choice in response:
            if choice == 'yes':
                start = 0
                end = 5
                data = df.iloc[start:end,:9]
                print(data)
            break
        else:
            choice = input("This is an invalid answer, please hit 'enter' to return to the previous question").lower()
    if choice == 'yes':
        while True:
            choice_2 = input("Would you like to view 5 additional lines of individual bikeshare data? Type 'yes' or 'no': ").lower()
            if choice_2 in response:
                if choice_2 == 'yes':
                    start += 5
                    end += 5
                    data = df.iloc[start:end,:9]
                    print(data)
                else:
                    break
            else:
                choice_2 = input("This is an invalid answer, please hit 'enter' to return to the previous question")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
