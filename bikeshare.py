import pandas as pd
import calendar



CITY_DATA={'Chicago':'chicago.csv',
           'New York':'new_york_city.csv',
           'Washington':'washington.csv'}


acceptable_input = {'city':['Chicago','New York','Washington'],
                        'data filters':['Month','Day','Both','None'],
                        'month':['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                        'day': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']}
   
print('Hello! Let\'s explore US bikeshare data.')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city_input - name of the city to analyze
        (str) month_input - abbreviation of the month's name to filter or 'no month filter'
        (str) day_input - name of the day of week to filter or 'no day filter'
    """
    
    while True:
        city_input = input('Would you like to see data for Chicago, New York or Washington?\nYour input: ').title()
        
        if city_input in acceptable_input['city']:
            print('We will look into {} data'.format(city_input))
            
            filters_input = input('Would you like to use a filter?\nPossible filters:{}\nYour input:'.format(acceptable_input['data filters'])).title()
            
            if filters_input in acceptable_input['data filters']:
                if filters_input == 'Month':
                    month_input = input('Which month?\nPossible answers:{}\nYour input:'.format(acceptable_input['month'])).title()
                    if month_input in acceptable_input['month']: 
                        print ('Filter to be used: {}'.format(month_input))
                        break
                    else:
                        print('Wrong input')
                        continue
                    
                elif filters_input == 'Day':
                    day_input = input('Which day?\nPossible answers:{}\nYour input:'.format(acceptable_input['day'])).title()
                    if day_input in acceptable_input['day']:
                        print ('Filter to be used: {}'.format(day_input))
                        break
                    else:
                        print('Wrong input')
                        continue
                    
                elif filters_input == 'Both':
                    month_input = input('Which month?\nPossible answers:{}\nYour input:'.format(acceptable_input['month'])).title()
                    if month_input in acceptable_input['month']:
                        day_input = input('Which day?\nPossible answers:{}\nYour input:'.format(acceptable_input['day'])).title()
                        if day_input in acceptable_input['day']:
                            print('Filters to be used: month: {}, day: {}'.format(month_input,day_input))
                            break
                        else: 
                            print('Wrong input.')          
                        continue
                    else:
                        print('Wrong input')
                        continue
                elif filters_input == 'None':
                    print('No filter will be applied for {} data'.format(city_input))
                    break
            else: 
                print('Inccorect input.')          
                continue
        else: 
            end = True
            while end:
                end_input = input('Would you like to end? (yes/no)').title()
           
                if end_input not in 'Yes' and end_input not in 'No':
                    print('Please write Yes or No')
                    continue        
                elif end_input == 'Yes':
                    print('Bye Bye')
                    break
                else:
                    end=False
                    break
    try:
        month_input
    except NameError:
        month_input='no month filter'
    
    try:
        day_input
    except NameError:
        day_input='no day filter'          
    
    return city_input,month_input,day_input

def load_data(city_input,month_input,day_input):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city_input - name of the city to analyze
        (str) month_input - abbreviation of the month's name to filter or 'no month filter'
        (str) day_input - name of the day of week to filter or 'no day filter'
    
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city_input])
    df=df.drop(df.iloc[:,0:1],axis=1)        
    
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])
    
    df['month']=df['Start Time'].dt.month
    df['month_name']=df['month'].apply(lambda x: calendar.month_abbr[x])
    
    df['day']=df['Start Time'].dt.day_name()
    
    df['start_hour']=df['Start Time'].dt.time
    df['start_hour']=df['Start Time'].dt.hour
    
    df['start_stop_station']='From station: '+df['Start Station']+' to station: '+df['End Station']
   
    if 'Gender' not in df.columns:
        df['Gender'] ='Lack of data'
    
    if month_input !='no month filter' and day_input !='no day filter' :
        df=df[df['month_name']==month_input]
        df=df[df['day']==day_input]
    elif month_input !='no month filter':
        df=df[df['month_name']==month_input]
    elif day_input !='no day filter' :
        df=df[df['day']==day_input]
        
    return df
        

def travel_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    df_tot = df[(['start_hour','day','month_name'])]
    tot = df_tot.mode()
    print('\nmost common hour: {}\nmost common day of week: {}\nmost common month: {}'.format(tot['start_hour'].dropna(axis=0).to_string(index=False),tot['day'].dropna(axis=0).to_string(index=False),tot['month_name'].dropna(axis=0).to_string(index=False)))

def trip_stats(df): 
    """Displays statistics on the most common stations and routes of travel."""
    
    df_station = df[(['Start Station', 'End Station','start_stop_station'])]
    stations = df_station.mode()
    print('\nmost common Start Station: {}\nmost common End Station: {}\nmost common trip:\n{}'.format(stations['Start Station'].dropna(axis=0).to_string(index=False),stations['End Station'].dropna(axis=0).to_string(index=False),stations['start_stop_station'].dropna(axis=0).to_string(index=False)))

def time_stats(df): 
    """Displays statistics on the time of travel."""    
    
    df['time_diff'] = df['End Time']-df['Start Time']
    df['time_diff'] = df['time_diff'].dt.total_seconds()
    total_travel_sec = df['time_diff'].sum()
    avg_travel_sec = df['time_diff'].mean()
    print('Total travel time was: {} (sec)\nAverage travel time was:{}(sec)'.format(total_travel_sec,avg_travel_sec))

def user_stats(df): 
    """Displays statistics on the users.""" 
    
    user_type = df['User Type'].fillna('Lack of data').value_counts()
    
    if 'Gender' not in df.columns:
        print ('We do not collect Gender data')
    else:
        user_gender = df['Gender'].fillna('Lack of data').value_counts()
        print('Users type split looks like that:\n{}\nand theirs gender split like that:\n{}'.format(user_type,user_gender))
    
    if 'Birth Year' not in df.columns:
        print ('We do not collect Birth Year data')
    else:
        df_birth = df['Birth Year'].dropna(axis=0)
        if len(df_birth) !=0:
            earliest_birth = df_birth.min()
            recent_birth = df_birth.max()
            common_birth = df_birth.mode()
            print('Users earliest birth year is: {}\nUsers recent birth year is: {}\n'.format(earliest_birth,recent_birth))
            print('Users most common birth year(s) is/are: {}'.format(common_birth.to_string(index=False)))
        else:
            print('No Birth Year data for chosen filter(s)')
            
def raw_data_examples(df):
    """Ask if examples of raw data behind statistics should be presented"""
    
    i=0
    while True:
        examples_input = input('\nWould you like to see raw data? Enter yes or no.\n').lower()
        if examples_input in 'yes':
            print(df.iloc[range(i,i+6)])
            i+=6
        else:
            break            
    
    
def main():
    """If possible run all statistics"""
    while True:
        city_input,month_input,day_input = get_filters()
        df = load_data(city_input,month_input,day_input)
        if df.empty:
            print('No data for those filters')
        else:
            travel_stats(df)
            trip_stats(df)
            time_stats(df)
            user_stats(df)
            raw_data_examples(df)
            
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

