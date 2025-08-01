

if __name__ == "__main__":
    print("Starting download...")
    output_filename = str(uuid.uuid4()) + "_amlo.html"  # Ensure the output filename is set
    download_file(url, output_filename)
    print("Download complete.")