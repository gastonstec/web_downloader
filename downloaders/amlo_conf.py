import time
import os
import uuid
import requests
from bs4 import BeautifulSoup
import calendar
import datetime
from loguru import logger

# Constants
# Base URL for the AMLO conferences
BASE_URL = "https://amlo.presidente.gob.mx/"
# Base folder where the HTML files will be saved
BASE_FOLDER = "/Volumes/GASTONS_SSD01/amlo/conferencias/"
# Log file for the downloader
LOG_FILE = BASE_FOLDER + "amlo_conferencias.log"


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
            raise ValueError(f"Error parsing date: {e}")

        # Increment the date by one day
        date += datetime.timedelta(days=1)
        i += 1

    # Return the list of formatted days
    return day_list


# This function should download the HTML content from the given
# URL and save it to the specified output filename.
def save_html(url, output_filename):

    # Get the HTML content from the URL
    try:
        resp = requests.get(url)
        resp.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.HTTPError as e:
        raise ValueError(f"HTTP error occurred while fetching {url}: {e}")

    # Check if the resp is valid and not a maintenance page
    if resp.status_code != 200:
        raise ValueError(
            f"Failed to retrieve {url}: Status code {resp.status_code}"
        )

    # Parse the HTML content using BeautifulSoup
    try:
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        raise ValueError(f"Error parsing HTML content at {url}: {e}")

    # Check if the response contains a valid HTML structure
    if not soup or not soup.find("html"):
        raise ValueError(f"Invalid HTML content at {url}")

    # Check if the response contains a valid title
    title_tag = soup.find('title')

    # Check if the title contains a maintenance message
    if title_tag.string.startswith("Sitio en mantenimiento"):
        logger.info(f"Maintenance message found at {url}: {title_tag}")
        return

    # Save the HTML content to the specified output filename
    with open(output_filename, "wb") as f:
        try:
            f.write(
                soup.prettify()
                .encode('utf-8')
            )
        except Exception as e:
            raise ValueError(
                f"Error saving HTML content to {output_filename}: {e}"
            )

        logger.info(f"Saved HTML content to {output_filename}")

    return


# This function should download the HTML files for each day of
# the specified month and year.
def download_conferencias(base_folder: str, year: int, month: int):
    # Get the list of days in the specified month and year
    try:
        day_list = get_month_days(year, month)
    except ValueError as e:
        raise ValueError(f"Error getting days for {year}-{month}: {e}")

    # Loop through the list of days and download the HTML files
    for day in day_list:
        # Format the URL for the specific day
        url = f"{BASE_URL}{day}"
        # Format the date for the output filename
        conf_date = f"20{day[6:8]}_{day[3:5]}_{day[0:2]}"
        # Generate a unique identifier for the file
        conf_id = str(uuid.uuid4())
        # Create the output filename
        output_filename = \
            f"{base_folder}amlo_conferencia_{conf_date}_{conf_id}.html"
        # Get the HTML content and save it
        try:
            logger.info(f"Downloading {url} to {output_filename}")
            save_html(url, output_filename)
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")
        # Sleep for a short time to avoid overwhelming the server
        time.sleep(15)  # Adjust the sleep time as needed
    return


# Configure the logger
logger.add(LOG_FILE)

# Set the year and month for which to download the conferences
year = 2024
current_month = 2
end_month = 8

while True:
    # Set the base folder for the current year and month
    folder = BASE_FOLDER + f"{year}/{current_month:02d}/"
    # Create the base folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    try:
        # Download the conferences for the specified month and year
        download_conferencias(folder, year, current_month)
        break  # Exit the loop if successful
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    # Increment the month
    current_month += 1
    # Exit the loop if the month exceeds the end month
    if current_month > end_month:
        break

    # Sleep before retrying
    logger.info(f"Retrying in 2 minutes for month {current_month}...")
    time.sleep(120)  # Wait before retrying
