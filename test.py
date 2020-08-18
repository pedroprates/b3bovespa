from b3bovespa.scrapper import B3Scrapper

DRIVER_PATH = '/Users/pedroprates/dev/chromium/chromedriver'


def main():
    scrapper = B3Scrapper(DRIVER_PATH, output_path='data/')
    scrapper.get_companies_data()
    scrapper.close()


if __name__ == '__main__':
    main()
