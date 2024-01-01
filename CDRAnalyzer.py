#!usr/bin/python3
import pandas as pd
import pyfiglet
#import folium #for future map plotting capablity 
import os

def print_banner():
    print("=" * 50)
    print("CDR Analyzer by Haider Ali")
    print("=" * 50)
def fancy_banner(banner_text, font_name="slant", enhancements=True):
    banner = pyfiglet.figlet_format(banner_text, font=font_name)
    if enhancements:
        banner_lines = banner.splitlines()
        enhanced_banner = []
        for line in banner_lines:
            enhanced_banner.append("" + line + "")
        banner = "\n".join(enhanced_banner)
    return banner


"""
def data_standardization(df):
    print("\nColumn names and data types of uploaded CSV file:")
    for col_name, dtype in df.dtypes.items():
        print(f"({dtype}) \t\t {col_name}")

    expected_columns = {  # Unindent to function level
        "A Number": None,
        "B Number": None,
        "Start Time": None,
        "IMEI": None,
        "Longitude": None,
        "Latitude": None,
        "Location": None,
    }
    print("\n\nFollowing columns are required by this code to work properly\n")
    print("A Number:\t\t Column containing MSISDN (Phone Number) of the person whose CDR is under analysis")
    print("B Number:\t\t Column containing MSISDN (Phone Number) of communication parties")
    print("Start Time:\t Column containing Dates at which the event is logged. Most commonly available is CALL_ORIGINATING_TIME")
    print("IMEI:\t\t Column containing IMEI of the used Device")
    print("Longitude:\t\t Column containing Longitude of the tower location")
    print("Latitude:\t\t Column containing lattitude of the tower location")
    print("Location:\t\t Column containing Address of the tower location")
    print("\nIdentify these columns in your code and input there names\n")
    
    for col_name in expected_columns.keys():
        while True:
            user_input = input(f"Which column is {col_name}? ")
            if user_input in df.columns:
                expected_columns[col_name] = user_input
                break
            else:
                print(f"Invalid column name. Please enter a valid column from the list.")

    # Rename columns based on user input
    print(expected_columns[col_name])
    df.rename(columns=expected_columns, inplace=True)

    # Check for empty cells in expected columns
    empty_cells = df[expected_columns.values()].isnull().sum()
    print("Empty cells in expected columns:")
    print(empty_cells)

    # Print stats for expected columns
    print("Stats for expected columns:")
    print(df[expected_columns.values()].describe())

    # Convert IMEI column to int64
    print("Number of NA values in IMEI column:", df["IMEI"].isna().sum())
    df["IMEI"] = df["IMEI"].astype("string")  # Cast to string dtype
    df["IMEI"].fillna("-1", inplace=True)

    #print("Number of inf values in IMEI column:", df["IMEI"].isinf().sum())
    #if df["IMEI"].dtype == "float64":
    #    df["IMEI"] = df["IMEI"].astype("int64")
    df = df[expected_columns.values()]
    return df
"""
def data_standardization(df):
    print("\nColumn names and data types of uploaded CSV file:")
    for col_name, dtype in df.dtypes.items():
        print(f"({dtype}) \t\t {col_name}")
    # Prompt user for original column names
    print("\n\nFollowing columns are required by this code to work properly\n")
    print("Column 1.A Number:\t Column containing MSISDN (Phone Number) of the person whose CDR is under analysis")
    print("Column 2.B Number:\t Column containing MSISDN (Phone Number) of communication parties")
    print("Column 3.Start Time:\t Column containing Dates at which the event is logged. Most commonly available is CALL_ORIGINATING_TIME")
    print("Column 4.IMEI:\t\t Column containing IMEI of the used Device")
    print("Column 5.Longitude:\t Column containing Longitude of the tower location")
    print("Column 6.Latitude:\t Column containing lattitude of the tower location")
    print("Column 7.Location:\t Column containing Address of the tower location")
    print("\nIdentify these columns in your data and input their names in folloing prompt\n")

    expected_columns = {
        "A Number": "Caller's Number - Party A",  # Map expected names to descriptive prompts
        "B Number": "Receiver's Number - Party B",
        "Start Time": "Data Log Date",
        "IMEI": "Device IMEI",
        "Longitude": "Longitude",
        "Latitude": "Latitude",
        "Location": "Location",
    }

    # Prompt user for original column names based on expected names
    original_columns = {}
    for expected_name, prompt_name in expected_columns.items():
        while True:
            col_name = input(f"Enter the name of the column containing {prompt_name}: ")
            if col_name in df.columns:
                original_columns[expected_name] = col_name
                break
            else:
                print("Invalid column name. Please enter a valid column from the DataFrame.")

    # Select and rename the desired columns
    selected_columns = list(original_columns.values())
    df = df[selected_columns]
    df.columns = list(expected_columns.keys())  # Use expected names for consistency

    return df


def load_cdr_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully.")

        while True:
            is_formatted = input("Is the data formatted as per code requirements (1 for Yes, 0 for No)? ")
            if is_formatted in ["0", "1"]:
                break
            else:
                print("Invalid input. Please enter 1 or 0.")

        if is_formatted == "1":
            return df
        else:
            df = data_standardization(df)
            return df

    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: File is empty.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: File is empty.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def format_imei(imei):
    if pd.isna(imei):  # Check for NaN
        return "NaN"  # Return a string representation for NaN
    else:
        formatted_imei = "{:015d}".format(int(imei))
        formatted_imei = " ".join([formatted_imei[i:i+4] for i in range(0, 15, 4)]) #Not gonna lie not sure why I did this but its still here
        return formatted_imei
    
def print_data(df):
    print("\nImported Data Preview:\n")
    # Select the specified columns (using a list for multiple columns)
    subset_df = df[["A Number", "B Number","Start Time", "Location", "Latitude", "Longitude"]]  # Enclose column names in a list
    print(subset_df.to_string())

"""
def search_contact_date(df):

    try:
        # Get user input for contact and date range
        contact = input("Enter the contact to search: ")
        start_date = pd.to_datetime(input("Enter the start date (YYYY-MM-DD): "))
        end_date = pd.to_datetime(input("Enter the end date (YYYY-MM-DD): "))
        print(start_date)
        print(end_date)
        # Apply filtering conditions
        filtered_df = df[
            (df["A Number"] == contact) | (df["B Number"] == contact)
        ]

        
        filtered_df["Start Time"] = pd.to_datetime(filtered_df["Start Time"])
        print(filtered_df)
        filtered_df = filtered_df[
            (filtered_df["Start Time"] >= start_date) & (filtered_df["Start Time"] <= end_date)
        ]
        print(filtered_df)
        # Display results
        if not filtered_df.empty:
            print("\nResults for", contact, "within the date range:")
            print(filtered_df)
        else:
            print("\nNo results found for the specified contact and date range.")

        return filtered_df

    except ValueError as e:
        print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
        return None
"""
def search_contact_date(df):
    """
    Searches for a specific contact and date range within a DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to search.

    Returns:
        pandas.DataFrame: The filtered DataFrame containing results, or None if no results found or errors occur.
    """

    try:
        # Get user input for contact and date range
        contact = input("Enter the contact to search (B Number): ")
        start_date_str = input("Enter the start date and time (YYYY-MM-DD HH:MM:SS): ")
        end_date = pd.to_datetime(input("Enter the end date (YYYY-MM-DD HH:MM:SS): "))

        # Convert start date string to datetime object, including time
        start_date = pd.to_datetime(start_date_str)

        # Filter DataFrame
        df_filtered_by_number = df[df["B Number"] == contact]  # Filter by B Number
        df_with_datetime = df_filtered_by_number.copy()  # Create an explicit copy for datetime conversion
        df_with_datetime["Start Time"] = pd.to_datetime(df_with_datetime["Start Time"])  # Convert "Start Time"

        df_filtered_by_date = df_with_datetime[
        (df_with_datetime["Start Time"] >= start_date) & (df_with_datetime["Start Time"] <= end_date)
        ]

        # Display results
        if not df_with_datetime.empty:
            print("\nResults for", contact, "between the date and time range:")
            sub_df = df_with_datetime[["A Number", "B Number", "Start Time", "Location", "Latitude", "Longitude"]]
            print(sub_df.to_string())
            #print(df_with_datetime)
            return sub_df
        else:
            print("\nNo results found for the specified contact and date range.")
            return None

    except ValueError as e:
        print("Invalid input format. Please enter valid dates, time, and contact information.")
        return None

    
def analyze_cdr_data(df):
    while True:
        print("\nSelect analysis option:")
        print("0. Data Preview")
        print("1. Identify frequent callers")
        print("2. Conduct IMEI analysis")
        print("3. Location Analysis")
        print("4. Search for Specific Contact")
        print("5. Sort using Contact and Date Range")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == "0":
            # Code for Data Preview
            print_data(df)
                        
        elif choice == "1": 
            # Code for frequent caller analysis
            identify_frequent_callers(df)
            
        elif choice == "2": 
            # Code for IMEI analysis
            #df["IMEI"] = df["IMEI"].str.replace(" ","")
            #df["IMEI"] = pd.to_numeric(df["IMEI"], errors='coerce')
            print("\nCount of NaN values in each column:\n", df.isna().sum())
            print("\nColumn DataType is:\n",df["IMEI"].dtype)
            print("\nSample IMEIs:\n",df["IMEI"].sample(5))
            analyze_imei_data(df)
        
        elif choice == "3": 
            # Code for location analysis
            analyze_location_data(df)
        
        elif choice == "4": 
            # Code for contact search
            search_for_contact(df)
        elif choice == "5": 
            # Code for date search
            search_contact_date(df)
        
        elif choice == "9":
            break
        else:
            print("Invalid choice. Please try again.")

def identify_frequent_callers(df):
    
    top_callers = df["B Number"].value_counts().head(5)  # Count occurrences in the modified DataFrame

    for number, frequency in top_callers.items():
        first_appearance = df.loc[df["B Number"] == number, "Start Time"].min()
        last_appearance = df.loc[df["B Number"] == number, "Start Time"].max()

        print("\n______________________________________________________________________________________________________")
        print("Number\t\t\tFirst Appearance in CDR\t\tLast Appearance in CDR\t\tComm Frequency")
        print(f"{number}\t\t{first_appearance}\t\t{last_appearance}\t\t\t{frequency}")
        print("_________________________________________________________________________________________________________")

def analyze_imei_data(df):
    unique_imeis = df["IMEI"].dropna().unique()  # Get unique IMEI values
    number_of_imeis = len(unique_imeis)  # Calculate total number

    print(f"\nThere are a total of {number_of_imeis} unique IMEIs in the data.")

    for imei in unique_imeis:
        first_appearance = df.loc[df["IMEI"] == imei, "Start Time"].min()
        last_appearance = df.loc[df["IMEI"] == imei, "Start Time"].max()

        print("\n________________________________________________________________________________________________________")
        print("IMEI\t\t\tFirst use\t\tLast use")
        print(f"{(imei)}\t\t{first_appearance}\t\t{last_appearance}")
        print("_________________________________________________________________________________________________________")

def analyze_location_data(df):
    # Identify most frequent 5 addresses
    df_fitered = df[df[["Latitude", "Longitude", "Location"]].notnull().all(axis=1)]
    top_locations = df_fitered.groupby("Location").agg(
        count=("Location", "count"),
        lat=("Latitude", "first"),
        lng=("Longitude", "first")
    ).sort_values(by=["count"], ascending=False).head(5)

    # Print detailed information for each top location
    print("\nTop Five Visited Locations Are As Follow:\n")
    for i, (addr, details) in enumerate(top_locations.iterrows(), start=1):
        print(f"{i}.\n------------------------------------------------------------------------------")
        print(f"Location Address:    {addr} (No. {i} Frequent)")
        print(f"Location Coordinates: {details['lat']:.6f}, {details['lng']:.6f}")
        print(f"Location Visit Details (Chronological Timestamps from Start Time):\n")
        for timestamp in df.loc[df["Location"] == addr, "Start Time"].sort_values():
            print(f"    {timestamp}")
        print("__________________________\n")
        print("\nLocations Summary\n")
    print("------------------------------------------------------------------------------")
    print("Top 5 Location Addresses along with coordinates are:\n")
    for i, (addr, details) in enumerate(top_locations.iterrows(), start=1):
        first_visit = df.loc[df["Location"] == addr, "Start Time"].min()
        last_visit = df.loc[df["Location"] == addr, "Start Time"].max()
        print(f"{i}.{addr},with coordinates {details['lat']:.6f}, {details['lng']:.6f}\n First Appeared {first_visit},Last Appeared {last_visit}\n and appeared ({int(details['count'])}) times\n")
    print("______________________________________________________________________________\n\n")

    #Will have to revisit this part
    #Create a base map centered on the first location
    #print(top_locations.iloc[0, "lat"])    
    #map = folium.Map(location=[int(top_locations.iloc[0, "lat"]), int(top_locations.iloc[0, "lng"])], zoom_start=12)
    # Add markers for each top location
    #for i, (addr, details) in enumerate(top_locations.iterrows(), start=1):
    #   folium.Marker([details["lat"], details["lng"]],
    #                   popup=f"{addr}<br>Visits: {int(details['count'])}<br>First Visit: {first_visit}<br>Last Visit: {last_visit}").add_to(map)

def search_for_contact(df):
    contact_number = input("Enter the contact number to search: ")

    # Filter DataFrame for matching records
    filtered_df = df[df["B Number"] == contact_number]

    # Print header if any matches found
    if not filtered_df.empty:
        print(f"\nCommunication with {contact_number}")
        print("------------------------------------------------------------------------------")
        print("A Number\t\tPartyB\t\tLogDate\t\t\tIMEI\t\t\tADDR")

        # Print formatted entries
        for index, row in filtered_df.iterrows():
            print(f"{row['A Number']}\t{row['B Number']}\t{row['Start Time']}\t{row['IMEI']}\t{row['Location']}")

        print("------------------------------------------------------------------------------")
    else:
        print("\nNo entries found for the specified contact number.")


def main():
    os.system("cls" if os.name == "nt" else "clear")
    banner = fancy_banner("CDR Analyzer", font_name="slant", enhancements=True)
    print(banner)
    print_banner()
    file_path = input("Enter the path to the CDR data file: ")
    df = load_cdr_data(file_path)
    print("Data type of 'Start Time' column:", df["Start Time"].dtype)
    print("Number of empty cells in 'Start Time' column:", df["Start Time"].isna().sum())
    df["Start Time"] = pd.to_datetime(df["Start Time"], format="%d/%m/%Y %H:%M")
    #print("Data type of 'Start Time' column:", df["Start Time"].dtype)
    #print(df["Start Time"])
    analyze_cdr_data(df)

if __name__ == "__main__":
    main()
