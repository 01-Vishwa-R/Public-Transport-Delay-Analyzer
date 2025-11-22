import csv 
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

Data_file = 'data/delay_data.csv'

def initialize_csv():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(Data_file):
        with open(Data_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "bus_number", "source", "destination",
                             "scheduled_time", "actual_time", "delay"])

# Creating the First option of adding entry to the CSV file
def add_entry():
    print("/n Add New Delay Entry")
    date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if date_input == "":
        date_input = datetime.today().strftime("%Y-%m-%d")

    # Bus Details Input
    bus_number = input("Enter bus number: ").strip()
    source = input("Enter source location: ").strip()
    destination = input("Enter destination location: ").strip()

    # time Inputs
    scheduled_time = input('Enter the scheduled arrival time (HH:MM):').strip()
    actual_time = input('Enter the actual arrival time (HH:MM):').strip()

    # Conversion of time from the given format to numbers
    sh, sm = map(int, scheduled_time.split(":"))
    ah, am = map(int, actual_time.split(":"))

    scheduled_minutes = sh * 60 + sm
    actual_minutes = ah * 60 + am

    delay = max(0 , actual_minutes - scheduled_minutes)

    #Finally writing the data to the CSV file
    with open(Data_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date_input, bus_number, source, destination, scheduled_time, actual_time, delay])
    print("Entry added successfully!")
    print(f"Total Delay: {delay} minutes")

# viewing the entries

def view_entries():
    print("\n All bus delay records")
    try:
        with open(Data_file, mode='r') as file:
            reader = csv.reader(file)
            # format for displaying the data
            print("\nDate        Bus  Source → Destination        Scheduled  Actual   Delay")
            print("-" * 80)

            next(reader)

            # reading data from file
            found = False
            for row in reader:
                found = True
                date, bus, src, dst, scheduled, actual, delay = row
                print(f"{date:10}  {bus:5}  {src:10} → {dst:12}  {scheduled:8}  {actual:6}  {delay} mins")
    
    except FileNotFoundError:
        print("No data found, add some entries")


# Another function to analyze the given data

def analyze_data():
    print("\n Delay Statistics")
    delay = []
    try:
        with open(Data_file, "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                delay.append(int(row[6]))
    except FileNotFoundError:
        print("No data found, add some entries")

    #calculating everything
    avg_delay = sum(delay) / len(delay) 
    max_delay = max(delay)
    min_delay = min(delay)
    on_time = delay.count(0)
    late_in_days = len(delay) - on_time

    # printing the stats
    print(f"\nTotal Records: {len(delay)}")
    print(f"Average Delay: {avg_delay:.2f} minutes")
    print(f"Maximum Delay: {max_delay} minutes")
    print(f"Minimum Delay: {min_delay} minutes")
    print(f"On-Time Days: {on_time}")
    print(f"Late Days: {late_in_days}\n")

#Visually representing the data using graphs

def data_graph():
    print("\n Bus Delay Graph")
    print("")
    bus_number = input("\n Enter the bus number to get the graph: ")
    delays = []
    dates = []
    scheduled_times = []
    actual_times = []
    sample_set_days = datetime.today() - timedelta(days=30)

    try:
        with open(Data_file, "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                date_str, bus, src, dst, scheduled, actual, delay = row
                if bus != bus_number:
                    continue  # ignore other buses
                entry_date = datetime.strptime(date_str, "%Y-%m-%d")
                if entry_date >= sample_set_days:
                        sh, sm = map(int, scheduled.split(":"))
                        ah, am = map(int, actual.split(":"))

                        scheduled_minutes = sh * 60 + sm
                        actual_minutes = ah * 60 + am

                        dates.append(date_str)
                        scheduled_times.append(scheduled_minutes)
                        actual_times.append(actual_minutes)  
                        if entry_date < sample_set_days:
                            dates.append(date_str)
                            delays.append(int(delay))

    except FileNotFoundError:
        print("No data found, add some entries")
        return
    
    if len(dates) <= 29:
        print("Not enough data to plot graph (need at least 30 days of data).")
        return
    
    if len(dates) == 0:
        print(f"No data found for bus number {bus_number}.")
        return
    
    # plotting the graph
    plt.figure(figsize=(11, 5))

    plt.plot(dates, scheduled_times, marker='o', label="Scheduled Time")
    plt.plot(dates, actual_times, marker='o', label="Actual Arrival Time")

    plt.xlabel("Date")
    plt.ylabel("Time (Minutes after midnight)")
    plt.title(f"Scheduled vs Actual Arrival Time - Bus {bus_number}")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

#Main Menu function to call all other functions

def main_menu():    
    initialize_csv     
    while True:
            print("\n==============================")
            print(" Public Transport Delay Analyzer")
            print("==============================")
            print("1. Add Bus Delay Entry")
            print("2. View All Entries")
            print("3. Analyze Delay Statistics")
            print("4. Monthly Delay Graph")
            print("5. Exit")

            choice = input("\nEnter choice: ")

            if choice == "1":
                add_entry()
            elif choice == "2":
                view_entries()
            elif choice == "3":
                analyze_data()
            elif choice == "4":
                data_graph()
            elif choice == "5":
                print("\nExiting program...\n")
                break
            else:
                print("Invalid choice. Try again.")

main_menu()