import pandas as pd
from datetime import datetime
from datetime import timedelta
import time

CITY_DATA = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' }

def get_city():
    '''Gets data for a city the user is interested in, lowercases it and loads respective CSV.'''
    city = ''
    while city.lower() not in ['chicago', 'new york', 'washington']:
        city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                     'Want to explore Chicago, New York, or Washington?\n')
        if city.lower() == 'chicago':
            return 'chicago.csv'
        elif city.lower() == 'new york':
            return 'new_york_city.csv'
        elif city.lower() == 'washington':
            return 'washington.csv'
        else:
            print('We do not have data on this city, please select Chicago, New York, or Washington.')

def get_time_period():
    '''Gets period data, lowercases and returns filter for bikeshare data.'''
    time_period = ''
    while time_period.lower() not in ['month', 'day', 'none']:
        time_period = input('\nDo you want to filter by by month, day, or none?\n')
        if time_period.lower() not in ['month', 'day', 'none']:
            print('Thats not a valid input.')
    return time_period

def get_month():
    '''Gets month the user is interested in.'''
    month_input = ''
    months_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4,'may': 5, 'june': 6}
    while month_input.lower() not in months_dict.values():
        month_input = input('\nWhich month? January, February, March, April, May, June?\n')
        if month_input.lower() not in months_dict.values():
            print('We do not have this month, please choose a valid month.')
    month = months_dict[month_input.lower()]
    return ('2017-{}'.format(month), '2017-{}'.format(month + 1))

def get_day():
    '''Gets the day of the week the user is interested in.'''
    this_month = get_month()[0]
    month = int(this_month[5:])
    valid_date = False
    while valid_date == False:    
        is_int = False
        day = input('\nWhich day you are interested in.\n')
        while is_int == False:
            try:
                day = int(day)
                is_int = True
            except ValueError:
                print('Input date as integer.')
                day = input('\nWhich day?\n')
        try:
            start_date = datetime(2017, month, day)
            valid_date = True
        except ValueError as e:
            print(str(e).capitalize())
    end_date = start_date + timedelta(days=1)
    return (str(start_date), str(end_date))

def common_month(df):
    '''Analysis respective filter for the month with the most common start time and prints it.'''
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(df['start_time'].dt.month.mode())
    most_common_month = months[index - 1]
    print('The most common month is {} for start time.'.format(most_common_month))

def common_day(df):
    '''Analysis respective filter for the weekday with the most common start time and prints it.'''
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    index = int(df['start_time'].dt.dayofweek.mode())
    most_common_day = days_of_week[index]
    print('The most common day of week is {} for start time.'.format(most_common_day))

def common_hour(df):
    '''Analysis respective filter for the hour of the day with the most common start time and prints it.'''
    most_common_hour = int(df['start_time'].dt.hour.mode())
    if most_common_hour == 0:
        am_pm = 'am'
        pop_hour_readable = 12
    elif 1 <= most_common_hour < 13:
        am_pm = 'am'
        pop_hour_readable = most_common_hour
    elif 13 <= most_common_hour < 24:
        am_pm = 'pm'
        pop_hour_readable = most_common_hour - 12
    print('The most common hour of day is {} for start time.'.format(pop_hour_readable, am_pm))

def popular_stations_trips(df):
    '''Displays statistics on the most popular stations.'''
    pop_start = df['start_station'].mode().to_string(index = False)
    pop_end = df['end_station'].mode().to_string(index = False)
    most_pop_trip = df['journey'].mode().to_string(index = False)
    print('The most commonly used start station is {} and end station is {}.'.format(pop_start, pop_end))
    print('The most common trip is {}.'.format(most_pop_trip))

def trip_duration(df):
    '''Displays statistics on total and average trip duration.'''
    total_duration = df['trip_duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print('Total trip duration is {} hours, {} minutes and {} seconds.'.format(hour, minute, second))
    average_duration = round(df['trip_duration'].mean())
    m, s = divmod(average_duration, 60)
    if m > 60:
        h, m = divmod(m, 60)
        print('The average trip duration is {} hours, {} minutes and {} seconds.'.format(h, m, s))
    else:
        print('The average trip duration is {} minutes and {} seconds.'.format(m, s))


def users(df):
    '''Displays statistics on users regarding unser type.'''
    subs = df.query('user_type == "Subscriber"').user_type.count()
    cust = df.query('user_type == "Customer"').user_type.count()
    print('There are {} Subscribers and {} Customers.'.format(subs, cust))

def gender(df):
    '''Displays statistics on users regarding gender.'''
    male_count = df.query('gender == "Male"').gender.count()
    female_count = df.query('gender == "Female"').gender.count()
    print('There are {} male and {} female users.'.format(male_count, female_count))

def birth_years(df):
    '''Displays statistics on users regarding birth year.'''
    earliest = int(df['birth_year'].min())
    latest = int(df['birth_year'].max())
    mode = int(df['birth_year'].mode())
    print('Oldest users are born in {} and youngest users are born in {}.\nThe most common birth year is {}.'.format(earliest, latest, mode))

def display_data(df):
    '''Displays 5 lines of data if user intents to'''
	start_loc = 0
    end_loc = 5

    display_active = input("Do you want to see the raw data?: ").lower()

    if display_active == 'yes':
        while end_loc <= df.shape[0] - 1:

            print(df.iloc[start_loc:end_loc,:])
            start_loc += 5
            end_loc += 5

            end_display = input("Do you wish to continue?: ").lower()
            if end_display == 'no':
                break

def main():
    '''Filters, calculates and prints statistics about a city and time the user inputed.'''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()
    print('Load data...')
    df = pd.read_csv(city, parse_dates = ['Start Time', 'End Time'])

	# change column names to lowercase letters and replace spaces with underscores
    new_labels = []
    for col in df.columns:
        new_labels.append(col.replace(' ', '_').lower())
    df.columns = new_labels
    
    # create a 'journey' column
    df['journey'] = df['start_station'].str.cat(df['end_station'], sep=' to ')

    # Filter by time period (month, day, none)
    time_period = get_time_period()
    if time_period == 'none':
        df_filtered = df
    elif time_period == 'month' or time_period == 'day':
        if time_period == 'month':
            filter_lower, filter_upper = get_month()
        elif time_period == 'day':
            filter_lower, filter_upper = get_day()
        df_filtered = df[(df['start_time'] >= filter_lower) & (df['start_time'] < filter_upper)]
    print('\nFiltering & calculating statistic...')

    if time_period == 'none':
        start_time = time.time()
        
        # Most common month for start time.
        common_month(df_filtered)
        print("This took %s seconds." % (time.time() - start_time))
    
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()
        
        # Most common weekday for start time.
        common_day(df_filtered)
        print("This took %s seconds." % (time.time() - start_time))  
        start_time = time.time()

    # Most common hour for start time.
    common_hour(df_filtered)
    print("This took %s seconds." % (time.time() - start_time))
    start_time = time.time()

    # Total and average trip duration.
    trip_duration(df_filtered)
    print("This took %s seconds." % (time.time() - start_time))
    start_time = time.time()

    # Common start / end station & trips.
    popular_stations_trips(df_filtered)
    print("This took %s seconds." % (time.time() - start_time))
    start_time = time.time()

    # Counts user type.
    users(df_filtered)
    print("This took %s seconds." % (time.time() - start_time))
    
    if city == 'chicago.csv' or city == 'new_york_city.csv':
        start_time = time.time()
        
        # Counts gender.
        gender(df_filtered)
        print("This took %s seconds." % (time.time() - start_time))
        start_time = time.time()

        # Statistic birth years.
        birth_years(df_filtered)
        print("This took %s seconds." % (time.time() - start_time))
	
	# Display five lines of raw data if user chooses to
    display_data(df_filtered)

    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() == 'yes':
        main()

if __name__ == "__main__":
	main()