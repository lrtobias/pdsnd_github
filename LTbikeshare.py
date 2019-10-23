import time
import pandas as pd
import numpy as np
import csv

global all_stats
all_stats = False

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

""" Used repeatedly in this program when raw input is invalid"""
def valid_entry():
    print ("Please enter a valid number for your selection")

""" To print options of a given menu from csv file"""
def menu_generator(menu_option):
    with open('menu_info.csv') as menufile:
        readmenu = csv.reader(menufile, delimiter=',')
        for row in readmenu:
            if (row[1]) == menu_option:
                print(row[2],": ",row[3])


""" Sub-menu to select calculations to perform.  Broken into 4 sections
    allow user to view the results before continuing.  An option enables
    running all of the calculations with one selection. """
def calculation_menu():
    print (50 * '*')
    print (50 * '-')
    print ("        Select Statistics To View")
    print (50 * '-')
    print ("1. Time: Most frequent travel times")
    print ("2. Station: Start/Stop and combination")
    print ("3. Trip: Duration information")
    print ("4. User: Types, Gender and year of birth")
    print ("5. All: Review all of the above statistics")
    print ("6. LIST records - Show raw data from selections")
    print ("0. To exit program")
    print (50 * '-')
    print ('Filters: city(',city.title(),'), month(',month.title(),'),\n         day(',day.title(),')' )
    print (50 * '-')

    while True:
        try:
            selection = int(input("Enter your selection: "))
            break
        except ValueError:
             valid_entry()
    if selection == 1:
        time_stats(df)
    elif selection == 2:
        station_stats(df)
    elif selection == 3:
        trip_duration_stats(df)
    elif selection == 4:
        user_stats(df)
    elif selection == 5:
        global all_stats
        all_stats = True
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        all_stats = False
        anykey = input("Press Any key to continue")
        calculation_menu()
    elif selection == 6:
        print('Displaying row detail...')
        start_no = 0
        end_no = start_no+5
        while True:
            print(df.iloc[start_no:end_no])
            start_no += 5
            end_no += 5
            next_group = input("Type 'N' to exit, any other key to continue: ")
            if next_group.upper() =='N':
                break
        print("Detail ended.  Entering calculation menu....")
        calculation_menu()
    elif selection == 0:
        print('Thank you for reviewing bikeshare information.')
        quit()
    else:
        valid_entry()

""" Main menu for selection options that defines the city, month and day
    selections"""

# First section is a menu to select city
def main_menu():
    print (40 * '-')
    print ("             BIKESHARE DATA")
    print ("                Main Menu")
    print (40 * '-')
    print ("    Which city's data would you")
    print ("         like to review?")

    menu_generator('pick_city')
    #with open('menu_info.csv') as menufile:
    #    readmenu = csv.reader(menufile, delimiter=',')
    #    for row in readmenu:
    #        if (row[1]) == ""'pick_city'"":
    #            print(row[2],": ",row[3])

    print (40 * '-')
    while True:
        selection = input("Enter your selection: ")
        try:
            selection = int(selection)
            if 0 <= selection <= 3:
                break
            else:
                valid_entry()
        except ValueError:
            valid_entry()
    global city
    if selection == 1:
        print ("You picked Chicago")
        city = 'chicago'
    elif selection == 2:
        print ("You picked New York")
        city = 'new york city'
    elif selection == 3:
        print ("You picked Washington")
        city = 'washington'
    elif selection == 0:
        print ("Thanks for viewing bikeshare data!")
        quit()
    else:
        valid_entry()

    if selection > 0:
        # Second menu prompts user to select month for review
        print (40 * '-')
        print ("Data from: "+ city.title())
        print ("     Which month do you want to view?")
        print ("1. January         2. February")
        print ("3. March           4. April")
        print ("5. May             6. June")
        print ("0. All")
        print (40 * '-')
        while True:
            selection = input("Enter your selection: ")
            try:
                selection = int(selection)
                if 0 <= selection <= 6:
                    break
                else:
                    valid_entry()
            except ValueError:
                valid_entry()

        global month
        if selection == 1:
            month = 'january'
        elif selection == 2:
            month = 'february'
        elif selection == 3:
            month = 'march'
        elif selection == 4:
            month = 'april'
        elif selection == 5:
            month = 'may'
        elif selection == 6:
            month = 'june'
        elif selection == 0:
            month = 'all'
        else:
            valid_entry()

    # This section is for the day of the week menu
        print (40 * '-')
        print ("Data from: "+ month.title())
        print ("     Which day do you want to view?")
        print ("1. Monday          2. Tuesday")
        print ("3. Wednesday       4. Thursday")
        print ("5. Friday          6. Saturday")
        print ("7. Sunday          0. All days")
        print (40 * '-')
        while True:
            selection = input("Enter your selection: ")
            try:
                selection = int(selection)
                if 0 <= selection <= 7:
                    break
                else:
                    valid_entry()
            except ValueError:
                valid_entry()

        global day
        if selection == 1:
            day = 'monday'
        elif selection == 2:
            day = 'tuesday'
        elif selection == 3:
            day = 'wednesday'
        elif selection == 4:
            day = 'thursday'
        elif selection == 5:
            day = 'friday'
        elif selection == 6:
            day = 'saturday'
        elif selection == 7:
            day = 'sunday'
        elif selection == 0:
            day = 'all'
        else:
            valid_entry()
        print('************| LOADING DATA |************\n')
        load_data(city,month,day)
        calculation_menu()
    return

""" Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
"""

def load_data(city, month, day):
    global df
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

""" Displays statistics on the most frequent times of travel."""
def time_stats(df):
    print (40 * '-')
    print('       Most Frequent Travel Times')
    print (40 * '-')
    start_time = time.time()


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    if month != 'all':
        print('Month selected for review is: ',month.title())
    else:
        # extract month from the Start Time column to create a month name column
        df['month_name'] = df['Start Time'].dt.month_name()

        # find the most common month name
        popular_month = df.month_name.mode()[0]
        print('Most Frequent Month of travel is: ', popular_month.title())

    # display the most common day of week
    if day != 'all':
        print('The day selected for review is: ',day.title())
    else:
        # extract day of the week from the Start Time column to create an dow column
        df['weekday_name'] =df['Start Time'].dt.weekday_name

        # find the most common hour (from 0 to 23)
        popular_day = df.weekday_name.mode()[0]
        print('Most Frequent Rental day:', popular_day.title())

    ## display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] =df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df.hour.mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    ## Section timer completed and displayed
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #prompt to continue displaying statistics
    if all_stats == False:
        input('Press ANY key to continue  ')
        calculation_menu()

""" Displays statistics on the most popular stations and trip."""
def station_stats(df):
    print (40 * '-')
    print('     Most Popular Stations and Trips')
    print (40 * '-')

    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts()[:1]
    print('Most Frequent Starting Station:')
    for index, value in popular_start_station.items():
        print("     Station : {} \n     Count   : {}".format(index, value))

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts()[:1]
    print('Most Frequent Ending Station:')
    for index, value in popular_end_station.items():
        print("     Station : {} \n     Count   : {}".format(index, value))

    # display most frequent combination of start station and end station trip
    most_freq_combo = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('Most Frequent Station Start/End Combination:')
    for index, value in most_freq_combo.items():
        print("     Stations : {} \n     Count   : {}".format(index, value))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Section to enable printing of all sections with one option
    if all_stats == False:
        input('Press ANY key to continue  ')
        calculation_menu()

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print (40 * '-')
    print('  Calculating trip duration statistics')
    print (40 * '-')

    #print('\nCalculating Trip Duration Statistics...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time (minutes):')
    print(df[('Trip Duration')].sum()/60)

    # display mean travel time
    print('Mean Travel Time (minutes):')
    print(df[('Trip Duration')].mean()/60)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Section to enable printing of all sections with one option
    if all_stats == False:
        input('Press ANY key to continue  ')
        calculation_menu()

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print (40 * '-')
    print('  Statistics regarding bikeshare users')
    print (40 * '-')

    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nNumber of each type of user:')
    print(user_types)

    # Display counts of gender
    if city == 'washington':
        print('\nGender is not available for ',city.title())
    else:
        gender_types = df['Gender'].value_counts()
        print('\nGender of users:')
        print(gender_types)

    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('\nBirth year is not available for ',city.title())
    else:
        print('\nEarliest Birth Year   : ',int(df['Birth Year'].min()))
        print('Latest Birth Year     : ',int(df['Birth Year'].max()))
        print('Most Common Birth Year: ',int(df['Birth Year'].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Section to enable printing of all sections with one option
    if all_stats == False:
        input('Press ANY key to continue  ')
        calculation_menu()


if __name__ == "__main__":
	main_menu()
