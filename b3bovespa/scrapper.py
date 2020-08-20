import os
import time
from logging import warning, error
from datetime import datetime
from collections import deque
from typing import Optional
import pandas as pd
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tqdm import tqdm
from .utils.utils import path_browser_driver, grouper
from .utils.constants import B3_URL, B3_FRAME, STARTING_CLASS_NAME, B3_COMPANY_FRAME, COMPANY_CLASS


class B3Scrapper:
    def __init__(self, path, browser: str = 'Chrome', output_path: Optional[str] = None):
        """
        Creates the base browser object for the web scrapping (using selenium). Currently it only supports
        Chrome or Firefox.

        You must download either the path for [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
        or [Firefox](https://sites.google.com/a/chromium.org/chromedriver/downloads) and pass the following link
        as a parameter.

        Remember to call the method .close() after using the B3Scrapper.

        Args:
            path: Path of the browser driver.
            browser: The type of the browser, must be either 'Chrome' or 'Firefox'
            output_path: Path to save the generated dataframe
        """
        browser = browser.lower()
        assert browser in ['chrome', 'firefox'], f'Browser {browser} not supported, it should be either ' \
                                                 f'"chrome" or "firefox'

        self._is_chrome = browser == 'chrome'
        self._output_path = output_path
        self._df = None
        _browser = Chrome if self._is_chrome else Firefox

        path = path_browser_driver(is_chrome=self._is_chrome, path=path)
        self.driver = _browser(executable_path=path)

    def __del__(self):
        self.close()

    def load_companies_data(self, path: str):
        """
        Load a CSV file with companies data

        Returns:
        """
        if not os.path.isfile(path):
            raise FileNotFoundError(f'File {path} not found')

        self._df = pd.read_csv(path)

    def get_companies_data(self) -> pd.DataFrame:
        """
        Get the data from all companies listed on B3 Bovespa.

        Returns:
            pd.DataFrame: dataframe containing the name, link and code for each company on B3 Bovespa.
        """
        df = self._get_companies_link()
        tqdm.pandas(desc='Getting Codes', bar_format='{l_bar}  {bar}|  {n_fmt}/{total_fmt} companies')
        df['Code'] = df.progress_apply(self._get_company_codes, axis=1)
        self._df = df

        self._save_dataframe()
        return self._df

    def close(self):
        """
        Closes the browser driver

        Returns:
        """
        self.driver.close()

    def _get_companies_link(self) -> pd.DataFrame:
        """
        Gets the link for each company in B3 Bovespa, allowing to scrap the company code.

        Returns:
            pd.DataFrame: dataframe containing the name, link for each company on B3 Bovespa.
        """
        starting_list = self._get_start_list()
        df = pd.DataFrame(columns=['Razao Social', 'Nome Pregao', 'Inicial', 'Link'])
        self.driver.get(B3_URL)
        t = tqdm(desc='Getting Initial Data', total=len(starting_list),
                 bar_format='{l_bar}  {bar}|  {n_fmt}/{total_fmt}{postfix}')

        while starting_list:
            starting_char = starting_list.pop()
            try:
                frame = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, B3_FRAME)))
            except TimeoutException:
                error('B3 site is not responding')
                self.driver.get(B3_URL)
                continue

            self.driver.switch_to.frame(frame)

            element = WebDriverWait(self.driver, 10)\
                .until(EC.presence_of_element_located((By.LINK_TEXT, starting_char)))
            element.click()

            # Todo: Dynamic wait for page loading
            t.update(1)
            t.set_postfix_str(f'Starting {starting_char}')
            time.sleep(10)

            a_tags = self.driver.find_elements_by_tag_name('a')
            companies_list = [a for a in a_tags if a.get_attribute('class') != 'itemBullet']

            for element_a, element_b in grouper(companies_list, 2):
                t.set_postfix_str(f'Scrapping {element_b.get_attribute("text")}')
                link = ' | '.join({element_a.get_attribute('href'), element_b.get_attribute('href')})

                data = {
                    'Razao Social': element_a.get_attribute('text'),
                    'Nome Pregao': element_b.get_attribute('text'),
                    'Inicial': starting_char,
                    'Link': link
                }

                company_series = pd.Series(data)
                df = df.append(company_series, ignore_index=True)

            self.driver.back()

        t.close()
        return df

    def _get_company_codes(self, series: pd.Series) -> Optional[str]:
        """
        Function to get the codes of a company given its link.

        Args:
            series: The series of the base dataframe, containing company name and link

        Returns:
            str: the company codes. If more than one, will be separated by ;, None if no code is found.
        """
        self.driver.get(series.Link)

        try:
            frame = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, B3_COMPANY_FRAME)))
        except TimeoutException:
            warning('Site is not responding')
            return None

        self.driver.switch_to.frame(frame)

        codes = self.driver.find_elements_by_class_name(COMPANY_CLASS)
        codes = [c.text for c in codes if len(c.text)]
        codes_output = ';'.join(codes) if len(codes) else None

        return codes_output

    def _get_start_list(self) -> deque:
        """
        Queries a list of start character to scrap the companies list

        Returns:
            deque: a queue with each character
        """
        self.driver.get(B3_URL)
        frame = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, B3_FRAME)))
        self.driver.switch_to.frame(frame)

        elements = self.driver.find_elements_by_class_name(STARTING_CLASS_NAME)
        keys = [e.text for e in elements if len(e.text) > 0]

        return deque(keys)

    def _save_dataframe(self):
        """
        Save the dataframe on the output_path

        Returns:
        """
        output_path = ''

        if self._output_path is not None:
            if not os.path.isdir(self._output_path):
                warning(f'{self._output_path} not a valid directory')
            else:
                output_path = self._output_path

        now = datetime.now()
        current_time = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}'

        self._df.to_csv(os.path.join(output_path, current_time + '.csv'))
