**# CDR Analyzer V.1.0 by Haider Ali**

**A Python tool for analyzing Call Detail Records (CDRs) to extract valuable insights.**

**Call Detail Records (CDRs) act as a digital breadcrumb trail, and their analysis plays a crucial role in cyber investigations. CDRs offer investigators a detailed picture of communication patterns, revealing connections between individuals, devices, and locations. This information is invaluable in reconstructing timelines of events, identifying perpetrators, and uncovering hidden networks within cybercriminal activities.**

**## Features**

- Loads and processes CDR data from CSV files.
- Presents a user-friendly menu for selecting analysis options.
- Analyzes frequent callers and their communication patterns.
- Conducts IMEI analysis to identify unique devices and their usage periods.
- Performs location analysis to determine frequently visited places and their timestamps.
- Allows searching for specific contacts or dates within the CDR data.
- **Future feature:** Visualizes location data on interactive maps (using folium).

**## Installation**

1. Clone this repository:
   ```bash
   git clone https://github.com/Vega-4n6/CDR_Analyzer.git
   ```
2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```
**## Input file requirements**

To ensure successful analysis, please adhere to the following input file guidelines:

File format: Only CSV (Comma Separated Values) files are accepted.
Essential columns: The file must contain at least five of the following columns:
PartyA    - MSISDN of phone number whose record is under analysis.
PartyB    - Communication participants of main number. 
IMEI      - IMEI of device in use
LogDate   - In most CDRs this column is displayed as Call_Originating_time 
LAT
LNG
ADDR

Column header: The first row of the CSV file must contain column headers (names) for each data field.
Data format: Ensure that the data within each column is of the appropriate format (e.g., numbers for IMEI, timestamps for LogDate).
Missing values: Missing values should be represented as empty cells or using a consistent placeholder (e.g., "N/A").
Failure to meet these requirements may lead to errors during the analysis process.

For now all of these coulumns are mandatory. Will definately work in future to make it more friendly.

**## Usage**

1. Run the main script:
   ```bash
   python CDRAnalyzer.py
   ```
2. Provide the path to your CDR data file when prompted.
3. Follow the interactive prompts to select the desired analysis options.

**## Code Structure**

- **CDRAnalyzer.py:** The main script that handles user interaction and analysis flow.

**## Contributing**

We welcome contributions! Please feel free to submit pull requests or open issues for suggestions and improvements.

**## Future Development**

- Abilty to handle different structures and formats of Call Records.
- Implement proper data processing to ensure more deeper analysis.
- Implement map visualization for location analysis using the folium library.
- Explore additional analysis features, such as:
    - Network analysis to identify relationships between contacts.
    - Time-series analysis to uncover patterns in communication behavior.
- Enhance code efficiency and maintainability.
- Better exceptions handling
  
**## Author**

Haider Ali - Vega4n6
haider.ali.siddiki@gmail.com
[https://www.linkedin.com/in/haideralisiddiki/]
For any queries or feedback.
 

