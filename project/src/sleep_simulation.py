""" 
Step 3: Generate database of 100 Night objectss storing sleep data
    Each night has a unique number of minutes slept -
    this is done by having a mean number of minutes slept, i.e. 480 minutes
    and having a standard deviation of minutes slept, i.e. 30 minutes
    we can generate these unique minutes with numpy's normal distribution function.

i.e. night 1 = 470 minutes, night 2 = 500 minutes, night 3 = 490 minutes, etc.
For each night,
    for each minute, match minute with data light, sound, temp, and movement
    this will be generated also with the normal distribution function.

Finally, "what if" questions will be implemented to understand the simulated sleep data."""

import numpy as np # To generate random values through normal distribution, and perform statistical calculations.
import matplotlib.pyplot as plt # To plot graphs for visual representation of sleep data.
from data_validation import main as validate_data # Import the data validation function from the data_validation module.
from data_analysis import analyse_data # Import the data analysis function from the data_analysis module.

light_dict, sound_dict, temp_dict, movement_dict = validate_data()  # Unpack dictionaries from the validation function.

# -------------------- OBJECT DECLARATIONS -------------------
class Night:
    """Class representing a night of sleep with sensor data."""
    

    def __init__(self, night_id, mins_slept, light_dict, sound_dict, temp_dict, movement_dict):
        """
        Initalise Night object with sleep data. 
        Args: 
            night_id (int): Unique identifier for the night.
            mins_slept (int): Number of minutes slept on that night.
            light_dict (dict): Dictionary containing light data for each minute.
            sound_dict (dict): Dictionary containing sound data for each minute.
            temp_dict (dict): Dictionary containing temperature data for each minute.
            movement_dict (dict): Dictionary containing movement data for each minute.
        """
        self.night_id = night_id
        self.mins_slept = mins_slept 
        self.light_dict = light_dict
        self.sound_dict = sound_dict
        self.temp_dict = temp_dict
        self.movement_dict = movement_dict


    def __repr__(self):
        """Return a string representation of the Night object."""
        return f"Night {self.night_id}"
    

    def get_time_slept(self):
        """Return the number of minutes slept on a given night."""
        return self.mins_slept


    def get_and_show_time_slept(self):
        """Calculate and display the total sleep time in hours and minutes."""
        hours_slept = self.mins_slept // 60 

        # Handles potential ZeroDivisionError when calculating the remainder minutes.
        try:
            remainder_minutes = self.mins_slept % 60
        except ZeroDivisionError:
            remainder_minutes = 0
            
        # Displays the total sleep time in hours and minutes.    
        print(f"On night {self.night_id}, you slept {hours_slept} hours and {remainder_minutes} minute(s).")
        return self.mins_slept
        

    def present_sleep_data(self):
        """Present the sleep data for the night, including mean and standard deviation of each metric."""

        self.mean_light, self.std_light = get_mean_std(self.light_dict) # Get mean and std to use to present sleep data.
        self.mean_sound, self.std_sound = get_mean_std(self.sound_dict)
        self.mean_temp, self.std_temp = get_mean_std(self.temp_dict)
        self.mean_movement, self.std_movement = get_mean_std(self.movement_dict)
        
        print(f"\n---------- Sleep analysis for night {self.night_id} ----------\n")
        
        self.get_and_show_time_slept() # first present the time slept.

        # Present the mean and standard deviation of each metric, with appropriate formatting and units.
        print(f"Mean light level: {self.mean_light} lx. Standard deviation of light level: {self.std_light} lx.")
        print(f"Mean sound level: {self.mean_sound} dB. Standard deviation of sound level: {self.std_sound} dB.")
        print(f"Mean temperature: {self.mean_temp} °C. Standard deviation of temperature: {self.std_temp} °C.")
        print(f"Mean movement level: {self.mean_movement} mg. Standard deviation of movement level: {self.std_movement} mg.\n")
        
        # Plot four graphs together to display sleep data

        self.figure, self.axis = plt.subplots(2, 2)

        # All horizontal axes will be time in minutes, vertical axes will be the metric value.
        self.axis[0, 0].set_xlabel("Time (minutes)")
        self.axis[0, 1].set_xlabel("Time (minutes)")
        self.axis[1, 0].set_xlabel("Time (minutes)")
        self.axis[1, 1].set_xlabel("Time (minutes)")

        # Plotting the light graph in the first subplot:
        self.axis[0, 0].plot(self.light_dict.keys(), self.light_dict.values())
        self.axis[0, 0].set_title(f"Night {self.night_id}: Light vs Time")
        self.axis[0, 0].set_ylabel("Light Level (lx)")
        
        # Plotting the sound graph in the second subplot:
        self.axis[0, 1].plot(self.sound_dict.keys(), self.sound_dict.values())
        self.axis[0, 1].set_title(f"Night {self.night_id}: Sound vs Time")
        self.axis[0, 1].set_ylabel("Sound Level (dB)")
        
        # Plotting the temperature graph in the third subplot:
        self.axis[1, 0].plot(self.temp_dict.keys(), self.temp_dict.values())
        self.axis[1, 0].set_title(f"Night {self.night_id}: Temperature vs Time")
        self.axis[1, 0].set_ylabel("Temperature (°C)")
        
        # Plotting the movement graph in the fourth subplot:
        self.axis[1, 1].plot(self.movement_dict.keys(), self.movement_dict.values())
        self.axis[1, 1].set_title(f"Night {self.night_id}: Movement vs Time")
        self.axis[1, 1].set_ylabel("Movement Level (mg)")
        
        plt.show() # Display graphs.
        
    
# -------------------- HELPER FUNCTION DECLARATIONS --------------------

def get_mean_std(dictionary):
    """
    Calculate mean and standard deviation of dictionary values.
    Args:
        dictionary (dict): contains numeric values.
    Returns:
        mean_val (float): rounded to 2 decimal places.
        standard_deviation (float): Standard deviation, rounded to 2 decimal places.
    """
    arr = np.array(list(dictionary.values())) # Convert the dictionary values to a numpy array for statistical calculations.

    mean_val = round(np.mean(arr), 2) # Mean value, affected by outliers
    standard_deviation = round(np.std(arr), 2) # Standard deviation, affected by outliers
    
    return mean_val, standard_deviation


def get_normal_distribution(mean, std, size):
    """
    Generates a normal distribution of random values based on the provided mean, standard deviation, and size.
    Args:
        mean (float): mean of the normal distribution.
        std (int): standard deviation of the normal distribution.
        size (int): number of random values to generate.
    Returns:
        list: A list of random values generated from the normal distribution, rounded to the nearest integer."""

    return [round(abs(val)) for val in (np.random.normal(mean, std, size)).tolist()] # abs() used to avoid invalid negative values. 
    

# -------------------- GENERATING DATA --------------------

NUMBER_OF_NIGHTS = 100 # this is the number of Nights in the database
MEAN_MINUTES = 480 # this is the mean number of minutes slept
STD_MINUTES = 20 # this is the standard deviation of minutes slept

mins_slept_per_night = get_normal_distribution(MEAN_MINUTES, STD_MINUTES, NUMBER_OF_NIGHTS) # Contains a list of integers representing the minutes slept per night

list_of_nights = [] # a list of Night objects
# This is the main dataset of the file, storing Night objects, which each object contains its own night's sleep data.

# For each night, generate a unique number of minutes slept, and then generate light, sound, temp, and movement values for each minute slept.
for index in range(len(mins_slept_per_night)):
    night_id = index + 1 # Night ID starts from 1, not 0.
    mins_slept = mins_slept_per_night[index] # Mins slept on a given night.
    
    # Generate light values, the light value recorded for every minute.
    light_mean, light_std = get_mean_std(light_dict) # gets light mean and std from other file
    light_values_per_min = get_normal_distribution(light_mean, light_std, mins_slept) # now contains a list of the light value recorded for each minute
    
    # Repeat for other metrics.
    sound_mean, sound_std = get_mean_std(sound_dict)
    sound_values_per_min = get_normal_distribution(sound_mean, sound_std, mins_slept)
    
    temp_mean, temp_std = get_mean_std(temp_dict)
    temp_values_per_min = get_normal_distribution(temp_mean, temp_std, mins_slept)
    
    movement_mean, movement_std = get_mean_std(movement_dict)
    movement_values_per_min = get_normal_distribution(movement_mean, movement_std, mins_slept)
    
    min_by_min_list = list(range(1, mins_slept + 1)) # contains a list of integers [1, 2, 3, ... , mins_slept - 1, mins_slept]
    current_light_dict = dict(zip(min_by_min_list, light_values_per_min))
    current_sound_dict = dict(zip(min_by_min_list, sound_values_per_min))
    current_temp_dict = dict(zip(min_by_min_list, temp_values_per_min))
    current_movement_dict = dict(zip(min_by_min_list, movement_values_per_min))
    
    # set up a new Night object. pass in id, mins slept, and all dictionaries containing data.
    new_night = Night(night_id, mins_slept, current_light_dict, current_sound_dict, current_temp_dict, current_movement_dict)
    list_of_nights.append(new_night)
    

# -------------------- TESTING THE DATABASE --------------------

# Present the sleep data for the first 3 nights
for night in list_of_nights[:3]:
    night.present_sleep_data()

# -----------------------------------------------------------------

# Step 4: Implement ‘what if’ questions
# "What if" questions are used to understand the simulated sleep data and provide insights into the user's sleep patterns and environment.

# ---------- WHAT IF QUESTION 1: "Am I getting enough sleep?" -----------

username = input("What is your name? ")
target_hours = input(f"Hi {username.title()}! How many hours of sleep do you want to get every night (1-24)? ")

# Validate the target_hours input to ensure it is an integer between 1 and 24.
if not target_hours.isdigit() or int(target_hours) > 24 or int(target_hours) < 1:
    # If the input is not valid, prompt the user to enter a valid integer.
    while not target_hours.isdigit() or int(target_hours) > 24 or int(target_hours) < 1:
        target_hours = input("Invalid entry. Please enter an integer between 1-24. ")
        
target_hours = int(target_hours) # convert to integer


def enough_sleep(name, target_hours, nights_data):
    """
    Understanding if the user is getting enough sleep involves checking:
    1. Last night's sleep - see if it meets the target
    2. Getting last week's sleep duration average and checking if it exceeds the target
    3. Getting last month's sleep duration average and checking if it exceeds the target

    Args:
        name (str): The name of the user.
        target_hours (int): The target number of hours of sleep per night.
        nights_data (list): A list of Night objects containing sleep data.
    """

    print("\n---------- What If Q1: Am I getting enough sleep? -----------\n")
    
    print(f"Hi {name.title()}. Lets see if you're getting enough sleep.")

    # 1. get last night's sleep - see if it meets the target
    last_night = nights_data[0] # this will be Night 1
    
    hours_slept = last_night.get_time_slept() // 60 # get the hours slept
    try:
        remaining_minutes = hours_slept % 60 # get the additional minutes slept as well
    except ZeroDivisionError:
        remaining_minutes = 0 # line runs if a ZeroDivisionError raises (i.e. 8 hours slept on the dot)
        
    print(f"\nLast night, you slept for {hours_slept} hours and {remaining_minutes} minute(s).")
    
    if hours_slept >= target_hours:
        print(f"You met your recommended sleep duration of {target_hours} hours last night! Keep it up!")
    else:
        print(f"You didn't meet your recommended sleep duration of {target_hours} hours last night.")
        print("Consider going to bed earlier to improve your sleep quality.")
        
    # 2. get last week's sleep duration average and check if it exceeds the target
    last_week = nights_data[:7] # This is Nights 1-7
    mins_slept_per_day = [night.get_time_slept() for night in last_week] # Get the mins slept per night and store it in a list. No display messages.
    MEAN_MINUTES_slept = int(sum(mins_slept_per_day) / 7) # Find the mean mins slept over the week
    
    mean_hours = MEAN_MINUTES_slept // 60 # Get the mean hours slept
    try:
        remaining_minutes = MEAN_MINUTES_slept % 60 # Get the additional minutes slept as well
    except ZeroDivisionError:
        remaining_minutes = 0 # Line runs if a ZeroDivisionError raises (i.e. 8 hours slept on the dot)
        
    # Display the average sleep duration for the last week.    
    print(f"\nLast week, you slept on average {mean_hours} hours and {remaining_minutes} minute(s).")
    
    # Check if the average sleep duration meets the target.
    # If it does, congratulate the user; if not, suggest going to bed earlier.
    if mean_hours >= target_hours:
        print(f"On average, you met your recommended sleep duration of {target_hours} hours last week! Well done!")
    else:
        print(f"On average, you didn't meet your recommended sleep duration of {target_hours} hours last week.")
        print("Consider going to bed earlier to improve your sleep quality.")
        
    
    # 3. get last month's sleep duration average, check if it exceeds the target
    last_month = nights_data[:30] # this is Nights 1-30
    mins_slept_per_day = [night.get_time_slept() for night in last_month] # get the mins slept per night and store it in a list. no display messages
    mean_mins_slept = int(sum(mins_slept_per_day) / 30) # find the mean mins slept over the week
    
    mean_hours = mean_mins_slept // 60 # get the mean hours slept
    try:
        remaining_minutes = mean_mins_slept % 60 # get the additional minutes slept as well
    except ZeroDivisionError:
        remaining_minutes = 0 # line runs if a ZeroDivisionError raises (i.e. 8 hours slept on the dot)
        
    # Display the average sleep duration for the last month.
    print(f"\nLast month, your average sleep duration is {mean_hours} hours and {remaining_minutes} minute(s).")
    
    # Check if the average sleep duration meets the target.
    # If it does, congratulate the user; if not, suggest going to bed earlier.
    if mean_hours >= target_hours:
        print(f"On average, you met your recommended sleep duration of {target_hours} hours last month! Great work!")
    else:
        print(f"On average, you didn't meet your recommended sleep duration of {target_hours} hours last month.")
        print("Consider going to bed earlier to improve your sleep quality.")


enough_sleep(username, target_hours, list_of_nights) # run "What If" Q1



# ---------- WHAT IF QUESTION 2: "Is my sleeping environment good for quality sleep?" ----------

print("\n---------- What If Q2: Is my sleeping environment good for quality sleep? -----------\n")
    
print(f"Hi {username.title()}. Lets see if your sleep environment is good for quality sleep.") 

# Ask the user which night they would like to analyse.
night_to_analyse = input("Which night (1-100) would you like to analyse? ")
# Error handling for the night_to_analyse input to ensure it is an integer between 1 and 100.
if (not night_to_analyse.isdigit()) or (night_to_analyse == "0") or (int(night_to_analyse) > 100):
    while (not night_to_analyse.isdigit()) or (night_to_analyse == "0") or (int(night_to_analyse) > 100):
        night_to_analyse = input("Invalid entry. Please enter an integer between 1-100. ")

night_to_analyse = int(night_to_analyse) - 1 # the index to access whichever night in the data list


def sleep_quality(name, night_id, nights_data): 
    """
    This function analyses the sleep environment for a given night.
    Three main components that relate to sleep environment are light, sound, and temperature.
    Using the analyse_data() function from data_analysis_v2, we'll find maximum values and
    check if they fall within the interquartile range.
    Args:
        name (str): The name of the user.
        night_id (int): The ID of the night to analyse (1-100).
        nights_data (list): A list of Night objects containing sleep data.
    Returns:
        None
    """

    # First, check which night we need to analyse.
    night = nights_data[night_id] #  get the Night object for the specified night_id

    # Present the sleep data for the specified night, using the analyse_data function from the data_analysis module.
    print(f"{name.title()}, let's analyse your sleep environment on Night {night_id + 1}.")
    analyse_data(night.light_dict, "light")
    analyse_data(night.sound_dict, "sound")
    analyse_data(night.temp_dict, "temp")
    
    # Prompt the user to analyse another night, or exit the program.
    go_again = input("Would you like to analyse another night? (Y for yes, anything else for no.) ")

    # If the user wants to analyse another night, prompt for the night number and validate the input.
    if go_again.upper() == "Y": 
        new_night = input("Which night (1-100) would you like to analyse? ")
        if (not new_night.isdigit()) or (new_night == "0") or (int(new_night) > 100):
            while (not new_night.isdigit()) or (new_night == "0") or (int(new_night) > 100):
                new_night = input("Invalid entry. Please enter an integer between 1-100. ")
        new_night = int(new_night) 
        sleep_quality(name, new_night, nights_data) # Recurisve call to the function to analyse another night.
    else:
        print("Goodbye!") # Exit the program if the user does not want to analyse another night.


sleep_quality(username, night_to_analyse, list_of_nights) # run "What If" Q2.