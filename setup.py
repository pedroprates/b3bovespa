from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()


setup_args = dict(
    name='B3Bovespa',
    version='0.1',
    description='Package for web-scrapping companies from B3Bovespa',
    long_description_content_type='text/markdown',
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Pedro Prates',
    author_email='phprates@me.com',
    keywords=['b3', 'bovespa', 'web', 'scrap', 'company', 'stock', 'market'],
    url='https://github.com/pedroprates/b3bovespa',
    download_url='https://pypi.org/project/b3bovespa/'
)

install_requires = [
    "selenium>=3.141.0",
    "pandas>=1.1.0",
    "tqdm>=4.48.2"
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
