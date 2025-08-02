import uuid
from downloaders.html import download_html


target_directory = "/Volumes/GASTONS_SSD01/amlo/conferencias/"
url = "https://amlo.presidente.gob.mx/25-09-21"

if __name__ == "__main__":
    print("Starting download...")
    output_filename = str(uuid.uuid4()) + "_amlo.html"  # Ensure the output filename is set
    download_html(url, target_directory + output_filename)
    print("Download complete.")