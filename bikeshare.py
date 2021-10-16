import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
Months = ['all', 'january', 'february','march','april','may' , 'june']
#,'july','august','september','october','november','december'
#Months_reduced = ['jan','feb','mar','apr','jun','jul','aug','sep','oct','nov','dec']
days = ['all','saturday','sunday' ,'monday', 'tuesday','wednesday','thursday','friday']
cities = ['chicago', 'new york city','washington']
user_answer = ['yes','no']

def validate_input(user_input,list_inputs):
    # function returns false if input isn't in list
    if user_input in list_inputs:
        return True
    else:
        return False
    
    
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
    print("Enter the city you want to discover: chicago, new york city or washington")
    city = input("City: ").lower()
    print("Enter the month you want: ex:all, january, february, ... , june")
    month = input("Month: ").lower()
     # get user input for day of week (all, monday, tuesday, ... sunday)
    print("Enter the day you want: ex:all, monday, tuesday, ... sunday")
    day = input("Day: ").lower()
    # get user input for month (all, january, february, ... , june)
    while not (validate_input(city,cities) & validate_input(month,Months)& validate_input(day,days)):
        print("please enter valid input.")
        city = input("City: ").lower()
        month = input("Month: ").lower()
        day = input("Day: ").lower()
        
   
    
    month = Months.index(month)
    day = days.index(day)
    print("Thank you! Let's start discovering")
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
    city_df = pd.read_csv(CITY_DATA[city])
    # convert start time and end time to datetume type
    city_df["Start Time"] = pd.to_datetime(city_df["Start Time"])
    city_df["End Time"] = pd.to_datetime(city_df["End Time"])
    
    # getting month and day of the week
    city_df["month"] = city_df["Start Time"].dt.month
    city_df["Week day"] = city_df["Start Time"].dt.weekday
    #print(city_df['Week day'].unique())
    #Extracting hour because will need it in stats function
    city_df["hour"] = city_df["Start Time"].dt.hour 
    #My list: ['all','saturday','sunday' ,'monday', 'tuesday','wednesday','thursday','friday']
    #Monday=0, Sunday=6. >> day of week mapping in pandas
    #Mapping to numbers in my list
    city_df["day"]=city_df['Week day'].map({5:1,6:2,0:3,1:4,2:5,3:6,4:7})
    
    #filter by month 
    # 0 means 'all'
    if month != 0:
        city_df = city_df[city_df['month']==month]
         
        
    #filter by day
    # 0 means 'all'
    if day != 0:
        city_df = city_df[city_df['day']==day]
    
    
    
    return city_df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
     
    '''
    if the user choose specific month & day, they'll be the most common 
    and if the user choose all, it will return the mode, so in this function i choose not to make special function
    just return the mode
    '''
    # Display the most common month
    
    common_month = df['month'].mode()[0]
    print("The most common month: ",Months[common_month])
    
    # Display the most common day of week
    common_day = df['day'].mode()[0]
    print("The most common day: ",days[common_day])
    

    # Display the most common start hour
    common_hour = df['hour'].mode()[0]
    if common_hour > 12:
        print("The most common start hour: ",common_hour - 12," PM.")
    elif common_hour < 12:
        print("The most common start hour: ",common_hour," AM.")
    else:
        print("The most common start hour: 12 PM.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("The most used start station is ", common_start )

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("The most used end station is ", common_end )

    # display most frequent combination of start station and end station trip
    common_comb = (df['Start Station'] + '-' + df['End Station']).mode()[0]
    print("The most used start and end stations are ", common_comb )
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # convert the trip duration in seconds to hours and minutes to be more readable
    df['Trip Duration']= pd.to_timedelta(df['Trip Duration'], unit='s')
    
    #tracing error
    print(df['Trip Duration'])
    #print(df['Trip Duration'].dtype)
    
    print("The total travel time = ",df['Trip Duration'].sum())

    # display mean travel time
    print("The average trip duration = ",df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_types = df.groupby('User Type')['User Type'].count()
    print("How many users in every type: ", count_types)
    # if the city 
    if "Gender" in df.columns:
        
        # Display counts of gender
        count_gender = df['Gender'].value_counts()
        print("How many users in every type: ", count_gender)

        # Display earliest, most recent, and most common year of birth
        print("/The most common year of birth between users: ", int(df['Birth Year'].mode()[0]))
        print("The earliest birth year (The oldest user) : ",int(df['Birth Year'].min()))
        print("The most recent birth year (The youngest user) : ",int(df['Birth Year'].max()))
        
    else:
        print("There is no information of users in this city")
 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_raw_data(df):
    '''
    This function asks the user if he/she wants to display raw data or not
    '''
    print('\nGetting raw Data...\n')
    start_time = time.time()
    answer = input("Do you like to show 5 rows of data? [yes,no]: ").lower()
    while not validate_input(answer,user_answer):
        print("please enter valid input.")
        answer = input("[yes,no]: ").lower()
    # variable row to make it easier to work with multible chices of the user
    row = 5 
    if answer == 'yes':
        
        while True:
            print(df.head(row))
            answer = input("Do you like to show another 5 rows of data? [yes,no]: ").lower()
            while not validate_input(answer,user_answer):
                  print("please enter valid input.")
                  answer = input("[yes,no]: ").lower()
            if answer != 'yes':
                print("\nThis took %s seconds." % (time.time() - start_time))
                print('-'*40)
                return
            row += 5
            
    
   
        
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
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
