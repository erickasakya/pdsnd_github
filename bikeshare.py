import json
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


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
    month = day = 'all'
    city = input('Would you like to see data for Chicago, New York, or Washington?\n')
    while city.lower() not in ['chicago', 'new york', 'washington']:
        city = input('Invalid input, Would you like to see data for Chicago, New York, or Washington?\n')

    # get user desired filter option
    time_filter = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time '
                        'filter\n')
    while time_filter.lower() not in ['month', 'day', 'both','none']:
        time_filter = input(
            'Invalid input, Would you like to filter the data by month, day, both or not at all? Type "none" for no '
            'time filter\n')

    if time_filter.lower() == 'both':
        month = capture_month_filter()
        day = capture_day_filter()
    elif time_filter.lower() == 'month':
        month = capture_month_filter()
    elif time_filter.lower() == 'day':
        day = capture_day_filter()

    print('-' * 40)
    return city.lower(), month.lower(), day.lower()


def capture_month_filter():
    """
        Asks user to specify a month to analyze the data.

        Returns:
            (str) month - name of the month to filter by, or "all" to apply no month filter
    """
    valid_input = ['january', 'jan', 'february', 'feb', 'march', 'mar', 'april', 'apr', 'may', 'june', 'jun', 'all']
    valid_month = {'jan': 'january', 'feb': 'february', 'mar': 'march', 'apr': 'april', 'jun': 'june'}
    # get user input for month (all, january, february, ... , june)
    month = input('Which month? (January(Jan), February(Feb), March(Mar), April(Apr), May, June) Type "all" to apply '
                  'no month filter\n')
    while month not in valid_input:
        month = input(
            'Invalid input! Which month? (January(Jan), February(Feb), March(Mar), April(Apr), May, June(Jun)) Type "all" '
            'to apply no month filter\n')
    if month in ['jan', 'feb', 'mar', 'apr', 'jun']:
        return valid_month[month]
    return month


def capture_day_filter():
    """
        Asks user to specify a day to analyze the data.

        Returns:
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    valid_input = ['1', '2', '3', '4', '5', '6', '7', 'all']
    week_day = {'1': 'Sunday', '2': 'Monday', '3': 'Tuesday', '4': 'Wednesday', '5': 'Thursday', '6': 'Friday',
                '7': 'Saturday', 'all': 'all'}
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day? Please type your response as an integer (e.g. 1= Sunday). Type "all" to apply no day '
                'filter\n')
    while day not in valid_input:
        day = input('Invalid input Please type your response as an integer (e.g. 1= Sunday). Type "all" to apply no '
                    'day filter\n')
    return week_day[day]


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()
    print('Month popular month:', common_month[0])

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()
    print('\nMost Popular day of the week:', common_day_of_week[0])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()
    print('\nMost popular hour:', common_hour[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most popular start station\n', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('\nMost popular End Station\n',common_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end_station = (df['Start Station'] + ' ' + df['End Station']).mode()[0]
    print('\nMost popular start & End station combined\n',popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel Time ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Type counts')
    print(user_types)

    # Display counts of gender
    print('\nGender counts')
    try:
        gender_types = df['Gender'].value_counts()
        print(gender_types)
    except:
        # Incase the dataset is missing the gender data this message will be displayed
        print('No Gender data to share')

    # Display earliest, most recent, and most common year of birth
    print('\nEarliest Year, Most Recent Year and the Most Popular year')
    try:
        ealiest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print((ealiest_year, recent_year, common_year))
    except:
        # Incase the dataset is missing the year of birth data this message will be displayed
        print('No birth year data to share')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def get_raw_data(df):
    """Displays of raw data for bikeshare data."""

    print('\nRetrieving raw data for bikeshare...\n')
    start_time = time.time()

    start_point = 0
    end_point = 5
    while True:
        print_raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')
        if print_raw_data.lower() != 'yes':
            break

        raw_data = df.iloc[start_point:end_point]
        result = raw_data.to_json(orient="records")
        parsed = json.loads(result)
        print(json.dumps(parsed, indent=4))

        start_point = end_point
        end_point += 5

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
