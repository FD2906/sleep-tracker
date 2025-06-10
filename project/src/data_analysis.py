""" Step 2: Analyse processed sleep data and provide insights and recommendations."""

import numpy as np # For numerical operations.
import matplotlib.pyplot as plt # For plotting graphs.
from data_validation import main as validate_data # Import function from the data_validation module.

light_dict, sound_dict, temp_dict, movement_dict = validate_data() # Unpack dictionaries.


def plot_graph(row, column, title, xlabel, ylabel):
    """
    Plot a simple graph with given parameters.
    Args: 
        row: x-axis data.
        column: y-axis data.
        title: Title of the graph.
        xlabel: Label for the x-axis.
        ylabel: Label for the y-axis.
    """
    plt.plot(row, column)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    

def analyse_data(dictionary, measuring, time_interval = "mins"): 
    """Analyze sleep data and display insights.

    Args:
        dictionary: Dictionary containing sensor data
        measuring: Type of measurement (light/sound/temp/movement)
        time_interval: Time unit for measurements (default: mins)

    Returns:
        mean_value, standard_deviation
    """
    arr = np.array(list(dictionary.values()))

    # Measures of central tendency.
    mean_val = np.mean(arr) # mean value, affected by outliers
    median_val = np.median(arr) # median value, not affected by outliers

    # Measures of dispersion.
    standard_deviation = np.std(arr) # standard deviation
    first_quarter = np.percentile(arr, 25) # 1/4 of values
    third_quarter = np.percentile(arr, 75) # 3/4 of values
    interquartile_range = third_quarter - first_quarter # IQR of values

    # Outliers.
    min_value = np.min(arr) # min value
    max_value = np.max(arr) # max value

    # Define units based on the type of measurement.
    units = {
        "light": "lux", # Light intensity in lux.
        "sound": "dB", # Sound level in decibels.
        "movement": "mg", # Movement in milligravity (mg).
        "temp": "°C" # Temperature in degrees Celsius.
    }

    unit = units.get(measuring, "") # Get the unit for the measurement type.

    # Print analysis results.
    print(f"\nAnalyzing {measuring} levels in your sleeping environment.\n")
    print(f"Mean: {round(mean_val, 3)} {unit}, Median: {round(median_val, 3)} {unit}")
    print(
        f"IQR: {round(interquartile_range, 3)} {unit}, "
        f"StdDev: {round(standard_deviation, 3)} {unit}"
    )
    print(
        f"Min: {round(min_value, 3)} {unit}, Max: {round(max_value, 3)} {unit}"
    )

    # Check if the maximum value is outside the normal range.
    if max_value > third_quarter:
        # Get the time corresponding to the maximum value.
        corresponding_time = max(
            dictionary.items(), key=lambda x: x[1] # Finds the key (time) corresponding to the max value
        )[0]

        # Print a warning message if the maximum value is outside the normal range.
        print(
            f"\nAt {corresponding_time} {time_interval}, {measuring} levels reached "
            f"{max_value} {unit}, outside normal range of "
            f"{round(first_quarter, 3)}-{round(third_quarter, 3)} {unit}."
        )
        # Suggest adjustments based on the measurement type.
        print(f"Consider adjusting your {measuring} levels for better sleep.")

    # Otherwise, print a message indicating that levels are within the optimal range.
    else:
        print(f"\n{measuring.capitalize()} levels are within optimal range.")
        print("Your sleeping environment is excellent for optimal sleep!")

    # Plot the graph of the measurement levels over time.
    plot_graph(
        dictionary.keys(),
        dictionary.values(),
        f"{measuring.capitalize()} Level vs Time",
        f"Time ({time_interval})",
        f"{measuring.capitalize()} Level ({unit})"
    )
        
    return mean_val, standard_deviation # Return the mean and standard deviation - this is used to simulate sleep data in sleep_simulation.py



def main():
    """Execute sleep data analysis and display results."""
    print("----------- Statistics for light values ----------") 
    light_mean, light_std = analyse_data(light_dict, "light", "s")
    print("\nSee graph for light level vs time.\n")


    print("----------- Statistics for sound values -----------")
    sound_mean, sound_std = analyse_data(sound_dict, "sound", "s")
    print("\nSee graph for sound level vs time.\n")


    print("----------- Statistics for movement values -----------")
    movement_mean, movement_std = analyse_data(movement_dict, "movement", "s")
    print("\nSee graph for movement level vs time.\n")


    print("----------- Statistics for temperature values -----------")
    temp_mean, temp_std = analyse_data(temp_dict, "temp", "s")
    print("\nSee graph for temperature level vs time.\n")



if __name__ == "__main__":
    main()  # Call the main function to execute the data analysis when this script is run directly.