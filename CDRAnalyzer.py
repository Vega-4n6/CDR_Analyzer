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

def print_data(df):
    #df["IMEI"] = df["IMEI"].apply(format_imei)  # Perils of not preprocessing data properly
    print("\nImported Data Preview:\n")
    print(df.to_string())


def data_standardization(df):
    print("\nColumn names and data types of uploaded CSV file:")
    for col_name, dtype in df.dtypes.items():
        print(f"({dtype}) \t\t {col_name}")

    expected_columns = {  # Unindent to function level
        "PartyA": None,
        "PartyB": None,
        "LogDate": None,
        "IMEI": None,
        "LNG": None,
        "LAT": None,
        "ADDR": None,
    }
    print("\n\nFollowing columns are required by this code to work properly\n")
    print("PartyA:\t\t Column containing MSISDN (Phone Number) of the person whose CDR is under analysis")
    print("PartyB:\t\t Column containing MSISDN (Phone Number) of communication parties")
    print("LogDate:\t Column containing Dates at which the event is logged. Most commonly available is CALL_ORIGINATING_TIME")
    print("IMEI:\t\t Column containing IMEI of the used Device")
    print("LNG:\t\t Column containing Longitude of the tower location")
    print("LAT:\t\t Column containing lattitude of the tower location")
    print("ADDR:\t\t Column containing Address of the tower location")
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
    if df["IMEI"].dtype == "float64":
        df["IMEI"] = df["IMEI"].astype("int64")
    df = df[expected_columns.values()]
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
    #df["IMEI"] = df["IMEI"].apply(format_imei)  # Perils of not preprocessing data properly
    print("\nImported Data Preview:\n")
    print(df.to_string())

def analyze_cdr_data(df):
    while True:
        print("\nSelect analysis option:")
        print("0. Data Preview")
        print("1. Identify frequent callers")
        print("2. Conduct IMEI analysis")
        print("3. Location Analysis")
        print("4. Search for Specific Contact")
        print("5. Search for Sepecific Date")
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
            analyze_location_data(df)
        
        elif choice == "9":
            break
        else:
            print("Invalid choice. Please try again.")

def identify_frequent_callers(df):
    numbers_to_remove = set(df["PartyA"])  # Create a set of numbers in PartyA for efficient removal
    df = df[~df["PartyB"].isin(numbers_to_remove)]  # Remove rows where PartyB is in the set
    top_callers = df["PartyB"].value_counts().head(5)  # Count occurrences in the modified DataFrame

    for number, frequency in top_callers.items():
        first_appearance = df.loc[df["PartyB"] == number, "LogDate"].min()
        last_appearance = df.loc[df["PartyB"] == number, "LogDate"].max()

        print("\n______________________________________________________________________________________________________")
        print("Number\t\t\tFirst Appearance in CDR\t\tLast Appearance in CDR\t\tComm Frequency")
        print(f"{number}\t\t{first_appearance}\t\t{last_appearance}\t\t\t{frequency}")
        print("_________________________________________________________________________________________________________")

def analyze_imei_data(df):
    unique_imeis = df["IMEI"].dropna().unique()  # Get unique IMEI values
    number_of_imeis = len(unique_imeis)  # Calculate total number

    print(f"\nThere are a total of {number_of_imeis} unique IMEIs in the data.")

    for imei in unique_imeis:
        first_appearance = df.loc[df["IMEI"] == imei, "LogDate"].min()
        last_appearance = df.loc[df["IMEI"] == imei, "LogDate"].max()

        print("\n________________________________________________________________________________________________________")
        print("IMEI\t\t\tFirst use\t\tLast use")
        print(f"{(imei)}\t\t{first_appearance}\t\t{last_appearance}")
        print("_________________________________________________________________________________________________________")

def analyze_location_data(df):
    # Identify most frequent 5 addresses
    df_fitered = df[df[["LAT", "LNG", "ADDR"]].notnull().all(axis=1)]
    top_locations = df_fitered.groupby("ADDR").agg(
        count=("ADDR", "count"),
        lat=("LAT", "first"),
        lng=("LNG", "first")
    ).sort_values(by=["count"], ascending=False).head(5)

    # Print detailed information for each top location
    print("\nTop Five Visited Locations Are As Follow:\n")
    for i, (addr, details) in enumerate(top_locations.iterrows(), start=1):
        print(f"{i}.\n------------------------------------------------------------------------------")
        print(f"Location Address:    {addr} (No. {i} Frequent)")
        print(f"Location Coordinates: {details['lat']:.6f}, {details['lng']:.6f}")
        print(f"Location Visit Details (Chronological Timestamps from LogDate):\n")
        for timestamp in df.loc[df["ADDR"] == addr, "LogDate"].sort_values():
            print(f"    {timestamp}")
        print("__________________________\n")
        print("\nLocations Summary\n")
    print("------------------------------------------------------------------------------")
    print("Top 5 Location Addresses along with coordinates are:\n")
    for i, (addr, details) in enumerate(top_locations.iterrows(), start=1):
        first_visit = df.loc[df["ADDR"] == addr, "LogDate"].min()
        last_visit = df.loc[df["ADDR"] == addr, "LogDate"].max()
        print(f"{i}.{addr},with coordinates {details['lat']:.6f}, {details['lng']:.6f}\n First Appeared {first_visit},Last Appeared {last_visit}\n and appeared ({int(details['count'])}) times\n")
    print("______________________________________________________________________________\n\n")

    #Will have to revisit this part
    # Create a base map centered on the first location
    #print(top_locations.iloc[0, "lat"])    
    #map = folium.Map(location=[int(top_locations.iloc[0, "lat"]), int(top_locations.iloc[0, "lng"])], zoom_start=12)
    # Add markers for each top location
    #for i, (addr, details) in enumerate(top_locations.iterrows(), start=1):
    #   folium.Marker([details["lat"], details["lng"]],
    #                   popup=f"{addr}<br>Visits: {int(details['count'])}<br>First Visit: {first_visit}<br>Last Visit: {last_visit}").add_to(map)

def search_for_contact(df):
    contact_number = input("Enter the contact number to search: ")

    # Filter DataFrame for matching records
    filtered_df = df[df["PartyB"] == contact_number]

    # Print header if any matches found
    if not filtered_df.empty:
        print(f"\nCommunication with {contact_number}")
        print("------------------------------------------------------------------------------")
        print("PartyA\t\tPartyB\t\tLogDate\t\t\tIMEI\t\t\tADDR")

        # Print formatted entries
        for index, row in filtered_df.iterrows():
            print(f"{row['PartyA']}\t{row['PartyB']}\t{row['LogDate']}\t{row['IMEI']}\t{row['ADDR']}")

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
    analyze_cdr_data(df)

if __name__ == "__main__":
    main()
