from core import config
from downloaders import amlo_conf as amlo_conferencias


def amlo_main():
    base_url = config.AMLO_BASE_URL
    base_folder = config.AMLO_CONFERENCIAS_FOLDER
    log_file = config.AMLO_CONFERENCIAS_LOG_FILE
    amlo_conferencias.start_downloader(
        base_url=base_url,
        year=2019,
        start_month=1,
        end_month=12,
        base_folder=base_folder,
        log_file=log_file
    )


def main():
    amlo_main()


if __name__ == "__main__":
    main()
