'''
Author : Public
'''

import time
import logging
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
month_data = {'all', 'january', 'february', 'march', 'april', 'may', 'june'}
day_data = [
    'all',
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday']

logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bike share data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid
    # inputs
    city = input("Please enter a city name: ").lower()
    while city not in CITY_DATA:
        city = input(
            "Oh sorry, Please choose from these three cities "
            "(chicago, new york city, washington): ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input(
        "Please select a month or choose all for all months: ").lower()
    while month not in month_data:
        month = input(
            "Sorry, Please select a month between january and june or "
            "choose all for all months:").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter a day or choose all for all days: ").lower()
    while day not in day_data:
        day = input(
            "Sorry, Please choose a day of the week or choose all for all months:").lower()

    logging.info('-' * 40)
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

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    logging.info('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    logging.info("the recurring month is:", common_month)

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    logging.info("the weekday most frequently used is:", day_data[common_day])

    # TO DO: display the most common start hour
    start_hour = df['hour'].mode()[0]
    logging.info(f'the most frequently start time is: {start_hour}')

    logging.info(f'\nThis took %s seconds. % {(time.time() - start_time)}')
    logging.info('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    logging.info('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    logging.info("The most popular starting point is: ", start_station)

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    logging.info("The most frequently end station: ", end_station)

    # TO DO: display most frequent combination of start station and end
    # station trip
    group_station = df.groupby(['Start Station', 'End Station'])
    start_end_station = group_station.size().sort_values(ascending=False).head(1)
    logging.info(
        "The most common route between a start station and an end station: ",
        start_end_station)

    logging.info(f'This took %s seconds. % f{(time.time() - start_time)}')
    logging.info('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    logging.info('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    logging.info("The total travel time is: " + str(round(total_duration)))

    # TO DO: display mean travel time
    mean_duration = df['Trip Duration'].mean()
    logging.info("The mean travel time is: " + str(round(mean_duration)))

    logging.info(f'\nThis took %s seconds. % {(time.time() - start_time)}')
    logging.info('-' * 40)


def user_stats(df, city):
    """Displays statistics on bike share users."""

    logging.info('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    logging.info('The user type is:')
    logging.info(df['User Type'].value_counts())
    if city != 'washington':
        # Display counts of gender
        logging.info('The user gender is:')
        logging.info(df['Gender'].value_counts())
        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_date = df['Birth Year'].min()
        newest_date = df['Birth Year'].max()
        common_date = df['Birth Year'].mode()[0]
        logging.info(f'Earliest birth records are: {format(int(earliest_date))}\n')
        logging.info(f'Newest birth records are: {format(int(newest_date))}\n')
        logging.info(f'Most common birth data are: {format(int(common_date))}\n')

    logging.info(f'This took %s seconds.% {(time.time() - start_time)}')
    logging.info('-' * 40)


def raw_data(df):
    """shows the data after filtering.
       Each press will add 5 rows.
       """
    print("Enter to display row data, no to skip.")
    x = 0
    while input() != 'no':
        x = x + 5
        print(df[x:x + 5])


def main():
    '''
    main method
    :return: nothing
    '''
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
