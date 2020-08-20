# B3Bovespa

This repository scraps all the companies listed on the Bovespa B3 using 
[Selenium](https://selenium-python.readthedocs.io).

## Drivers

To allow web scrapping, it is necessary to download the driver accordingly to your preferred
browser. Currently, the only supported browsers are *Chrome* and *Firefox*.

* [Chrome's chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* [Firefox's geckodriver](https://github.com/mozilla/geckodriver/releases)

It is necessary that the *driver's* version is compatible with the current version
of the installed browser. 

## Installation

The package could be installed via `pip`

```bash
pip install b3bovespa
```

It will install as dependencies [Selenium](https://github.com/baijum/selenium-python) (used for the web scrapping), 
[Pandas](https://github.com/pandas-dev/pandas) (used to handle the output data) and 
[tqdm](https://github.com/tqdm/tqdm) (used for progress tracking).

 ## Usage
 
 `B3Bovespa` package is based on the `B3Scrapper` class, which will control the web scrapping of the Bovespa website.
 The web-scrapping is really straight-forward, you will need to instantiate a `B3Bovespa` object, passing
 the path of the browser driver (as discussed in [here](#Drivers)), the chosen driver (`B3Bovespa` supports both Firefox
 and Chrome) and the output path to export the company list on a CSV format.
 
```python
from b3bovespa import B3Scrapper

DRIVER_PATH = 'path/to/drive'
b3 = B3Scrapper(path=DRIVER_PATH, browser="Chrome", output_path="/usr/companies/")
```

With the `B3Scrapper` object, it is simple to get the information from all the companies listed on Bovespa,
a simple call to `get_companies_data()` will return a Pandas Dataframe containing all the info.

The `get_companies_data()` will also save a `csv` file containing all the information on the output
path given to the object. If no output path was given, it will just save a `csv` file on the file directory.

```python
companies = b3.get_companies_data()
```

If necessary, it is possible to close the current session of the driver by calling the `close()` method.

```python
b3.close()
```