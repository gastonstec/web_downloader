import uuid
import requests
import calendar
import datetime
import re
from loguru import logger

BASE_URL = "https://amlo.presidente.gob.mx/"  # Replace with the actual URL
BASE_FOLDER = "/Volumes/GASTONS_SSD01/amlo/conferencias/"  # Folder to save downloaded files
LOG_FILE = BASE_FOLDER + "_amlo_conferencias.log"


# This function should return a list of days in the specified month and year.
def get_month_days(year: int, month: int) -> list:
    # Initialize an empty list to hold the formatted days
    day_list: list = []
    # Get the number of days in the month
    num_days = calendar.monthrange(year, month)[1]
    # Get the first day of the month
    date = datetime.date(year=year, month=month, day=1)

    # Loop through the number of days in the month
    i = 0
    while i < num_days:
        # Format the date as "dd-mm-yy" and append to the list
        try:
            day_list.append(date.strftime("%d-%m-%y"))
        except Exception as e:
            print(f"Error parsing date: {e}")
            raise ValueError("Invalid date format")
        
        # Increment the date by one day
        date += datetime.timedelta(days=1)
        i += 1

    # Return the list of formatted days
    return day_list


# This function should download the HTML content from the given URL and save it to the specified output filename.
def save_html(url, output_filename):

    # Get the HTML content from the URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return

    # Check if the response is valid and not a maintenance page
    if response.status_code != 200:
        logger.error(f"Failed to retrieve {url}: Status code {response.status_code}")
        return

    # Check if the response contains a maintenance message
    if response.head('title').startswith('Sitio en Mantenimiento'):
        logger.info(f"Unexpected content at {url}: {response.text[:100]}")
        return

    with open(output_filename, 'wb') as f:
        f.write(response.content)
        logger.info(f"Saved HTML content to {output_filename}")

    return


 # This function should download the HTML files for each day of the specified month and year.
def download_conferencias(year: int, month: int):
    # Get the list of days in the specified month and year
    day_list = get_month_days(year, month)
    
    # Loop through the list of days and download the HTML files
    for day in day_list:
        url = f"{BASE_URL}{day}"
        # Format the date for the output filename
        conf_date = f"20{day[6:8]}_{day[3:5]}_{day[0:2]}"
        # Generate a unique identifier for the file
        conf_id = str(uuid.uuid4())
        # Create the output filename
        output_filename = f"{BASE_FOLDER}amlo_conferencia_{conf_date}_{conf_id}.html"
        print(output_filename)
        save_html(url, output_filename)

# # Initialize logging
# logger.add(LOG_FILE)
# logger.info("New logging session started")
# # Initialize the main function
# start_download()

