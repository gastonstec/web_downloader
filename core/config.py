# Base URL for the AMLO conferences
AMLO_BASE_URL: str = "https://amlo.presidente.gob.mx/"
# Base folder where the HTML files will be saved
AMLO_CONFERENCIAS_FOLDER: str = "/Volumes/GASTONS_SSD01/amlo/conferencias/"
# Log file for the downloader
AMLO_CONFERENCIAS_LOG_FILE: str = (
    AMLO_CONFERENCIAS_FOLDER + "amlo_conferencias.log"
)
# Sleep times for the downloader
PAGE_SLEEP_TIME: int = 3  # seconds
MONTH_SLEEP_TIME: int = 60  # seconds
