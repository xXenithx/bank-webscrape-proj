# Python Bank Web Scraper

This script was more of a proof of concept if anything but allows the user to web scrape their bank account statement (assuming there is a .csv file that can be downloaded)
  - Uses the Selenium Library to web scrape and grab the .csv file
  - Parses the .csv using the Pandas Library 
  - Currently only supports one bank, GECU


### Installation

The Web Scraper currently requires [Python](python.org) v2.7+ , [Selenium](https://selenium.dev/downloads/), and [Pandas](https://pandas.pydata.org/) to run.

Install the dependencies to start pulling the information

```sh
$ cd bank-webscrape-proj
$ pip install selenium pandas
```
Once installed you need to take `example.config` and copy it to `app.config` and input the neccessary information.

To get the script running simply run the following:

```sh
$ python app.py
````


### Todos

 - Add more banks to intergrate with
 - client side encryption
 - future tools to manage financials
 - cleaner implementation

License
----

MIT
