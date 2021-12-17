# DEA web scraping

Proof of concept for scraping the DEA website. There are 3 implementations: Scrapy framework, Request library, Selenium web driver.

## Instalation

### Python3.9 and virtualenv installation
Follow:
1) https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/
2) https://gist.github.com/frfahim/73c0fad6350332cef7a653bcd762f08d

### Environment setup
To create python3.9 virtual environment named 'venv'

> virtualenv --python python3.9 venv

To activate virtualenv
> source venv/bin/activate

To install requirements
> pip install -r requirements.txt

### Run Scrapy project
Change directory into scrapy-dea
> cd scrapy-dea

Run scrapy command
> scrapy crawl dea

### Run request library example
Open Notebook at request-dea and execute cell by cell

### Run Selenium implementation.
Open Notebook at selenium-dea and execute cell by cell. Note, you have to wait for each page to fully load before executing the next cell.

## Scrapy-Splash implementation.

We need to run a docker container with the splash server
> docker run -p 8050:8050 scrapinghub/splash --max-timeout 3600
