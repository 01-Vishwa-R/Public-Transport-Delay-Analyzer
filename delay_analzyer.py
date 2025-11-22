import csv 
from datetime import datetime

Data_file = 'data/delay_data.csv'

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
        with open(DATA_FILE, "r") as file:
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
    print(f"\nTotal Records: {len(delays)}")
    print(f"Average Delay: {avg_delay:.2f} minutes")
    print(f"Maximum Delay: {max_delay} minutes")
    print(f"Minimum Delay: {min_delay} minutes")
    print(f"On-Time Days: {on_time}")
    print(f"Late Days: {late_days}\n")

  #