import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york city', 'washington']

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['all','sunday', 'monday', 'tuesday', 'wednesday', \
        'thursday', 'friday', 'saturday' ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input('Which city do you want to analyse? Choose between: Chicago, New york city or Washington. ').lower()
    while city not in CITIES:
        print('\n Please choose only between:', CITIES)
        city=input('\n Which city do you want to analyse?? ').lower()


    # get user input for month (all, january, february, ... , june)
    month=input('\n Ok, awesome, you want to analyse: {} ! Good choice. \n \n Which month do you want to analyse? Please write out month (all, january, february, ...) '.format(city)).lower()
    while month not in MONTHS:
        print('\n\nYou can only choose between: ', MONTHS)
        month=input('\nPlease choose a month: ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=input('\n Ok, cool, you want to look at {}. I got it. \n \n Which day of the week do you want to analyse? (all, monday, tuesday, ... sunday) '.format(month)).lower()
    while day not in DAYS:
        print('Please choose between:', DAYS)
        day=input('\n Enter your choice for day of the week again. ').lower()
    print('\n {}, fantastic choice\n'.format(day))
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

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week'] == day.title()]

    return df

    # ask if use wants to see a part of the raw data



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]


    print('Most common day of week:', most_common_day)
    print('Most common month:', most_common_month)
    print('Most common start hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].value_counts().idxmax()
    print('The most popular start station is: ', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].value_counts().idxmax()
    print('The most popular end station is: ', popular_end)

    # display most frequent combination of start station and end station trip
    df['Start End'] = df['Start Station'].map(str) + '&' + df['End Station']
    popular_start_end = df['Start End'].value_counts().idxmax()
    print('The most commonly used start station and end station: ', popular_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The total travel time is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:\n')
    user_counts = df['User Type'].value_counts()

    # iteratively print out the total numbers of user types
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))

    # Display counts of gender
    try:
        print('\n Counts of gender:\n')
        gender_counts = df['Gender'].value_counts()
        for index, gender_count in enumerate(gender_counts):
              print('    {}: {}'.format(gender_counts.index[index], gender_count))
    except:
        print('There is no gender data in the source.')


    # Display earliest, most recent, and most common year of birth
    try:
        print('\nStatistics about the year of birth. \n')
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].value_counts().idxmax())
        print('The earliest year of birth is: {}. \n The most recent year of birth is: {}. \n The most common year of birth is: {}.'.format(earliest, most_recent, most_common))
    except:
        print('There is no year of birth data in the source.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def disp_raw_data(df):
    '''
    Displays the data used to compute the stats
    Input:
        the df with all the bikeshare data
    Returns:
       raw data if they want.
    '''
    #omit irrelevant columns from visualization
    row_index = 0

    see_data = input("\n Would you like to see a sample of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()
    while True:
        if see_data == 'no':
            return
        if see_data == 'yes':
            print(df[row_index: row_index + 5])
            row_index = row_index + 5
        see_data = input("\n Would you like to see 5 more rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        disp_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
