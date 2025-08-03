from core import config
import time
import os
import uuid
from utils import get_month_days, save_html

from loguru import logger


# Configuration for the downloader
PAGE_SLEEP_TIME = config.PAGE_SLEEP_TIME  # seconds
MONTH_SLEEP_TIME = config.MONTH_SLEEP_TIME  # seconds


# This function should download the HTML files for each day of
# the specified month and year.
def download_html_conferencias(
    base_url: str,
    base_folder: str,
    year: int,
    month: int
):
    # Get the list of days in the specified month and year
    try:
        day_list = get_month_days(year, month)
    except ValueError as e:
        raise ValueError(f"Error getting days for {year}-{month}: {e}")

    # Loop through the list of days and download the HTML files
    for day in day_list:
        # Format the URL for the specific day
        url = f"{base_url}{day}"
        # Format the date for the output filename
        conf_date = f"20{day[6:8]}_{day[3:5]}_{day[0:2]}"
        # Generate a unique identifier for the file
        conf_id = str(uuid.uuid4())
        # Create the output filename
        output_filename = (
            f"{base_folder}amlo_conferencia_{conf_date}_{conf_id}.html"
        )
        # Get the HTML content and save it
        logger.info(f"Downloading {url} to {output_filename}")
        try:
            # Call the save_html function to download and save the HTML content
            save_html(url, output_filename)
            logger.info(f"Saved HTML content to {output_filename}")
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")

        # Sleep to avoid overwhelming the server
        time.sleep(PAGE_SLEEP_TIME)
    return


# This function should start the downloader
def start_html_downloader(
    year: int, start_month: int, end_month: int,
    base_url: str = "", base_folder: str = "", log_file: str = ""
):
    # Validate the input parameters
    if base_folder == "" or log_file == "" or base_url == "":
        raise ValueError("folder, log file, and base URL must be specified.")
    if start_month < 1 or start_month > 12:
        raise ValueError("Invalid start month. Must be between 1 and 12.")
    if end_month < 1 or end_month > 12:
        raise ValueError("Invalid end month. Must be between 1 and 12.")

    # Configure the logger
    logger.add(log_file, rotation="25 MB", level="INFO")

    # Set current month
    current_month = start_month
    while True:
        # Set the base folder for the current year and month
        folder = f"{base_folder}{year}/{current_month:02d}/"
        # Create the base folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)

        try:
            # Download the conferences for the specified month and year
            download_html_conferencias(
                base_url=base_url,
                base_folder=folder,
                year=year,
                month=current_month
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")

        # Increment the month
        current_month += 1
        # Exit the loop if the month exceeds the end month
        if current_month > end_month:
            break
        # Sleep before retrying
        logger.info(f"Retrying in 2 minutes for month {current_month}...")
        # Sleep for 2 minutes before retrying
        time.sleep(MONTH_SLEEP_TIME)


# This function should download the HTML files for each day of
# the specified month and year.
def download_mp3_conferencias(
    base_url: str,
    base_folder: str,
    year: int,
    month: int
):
    # Get the list of days in the specified month and year
    try:
        day_list = get_month_days(year, month)
    except ValueError as e:
        raise ValueError(f"Error getting days for {year}-{month}: {e}")

    # Loop through the list of days and download the HTML files
    for day in day_list:
        # Format the URL for the specific day
        url = f"{base_url}{day}"
        # Format the date for the output filename
        conf_date = f"20{day[6:8]}_{day[3:5]}_{day[0:2]}"
        # Generate a unique identifier for the file
        conf_id = str(uuid.uuid4())
        # Create the output filename
        output_filename = (
            f"{base_folder}amlo_conferencia_{conf_date}_{conf_id}.html"
        )
        # Get the HTML content and save it
        logger.info(f"Downloading {url} to {output_filename}")
        try:
            # Call the save_html function to download and save the HTML content
            save_html(url, output_filename)
        except Exception as e:
            logger.error(f"Error downloading {url}: {e}")

        # Sleep to avoid overwhelming the server
        time.sleep(PAGE_SLEEP_TIME)
    return
