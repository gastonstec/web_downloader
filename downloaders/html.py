import uuid
import requests

url = "https://amlo.presidente.gob.mx/30-09-23"  # Replace with the actual URL
output_filename = "amlo.html"  # Desired output filename


def download_html(url, output_filename):
    try:
        response = requests.get(url, stream=True)  # Use stream=True for large files
        status = response.raise_for_status()  # Raise an exception for bad status codes

        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File '{output_filename}' downloaded successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")