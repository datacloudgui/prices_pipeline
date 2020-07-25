# prices_pipeline

This code call three more python codes to automatize ETL Extract Transform and Load scraped data form a sales page.

## Functions to call

_extract(), call the free repository named "[prices_scraper](https://github.com/datacloudgui/prices_scraper)" to extract data using beautifulsoup.

_transform(), call the free repository named "[prices_cleaner](https://github.com/datacloudgui/prices_cleaner)" to transform numeric values and clean titles scraped.

_load(), call the free repository named "[prices_load](https://github.com/datacloudgui/prices_load)" to merge csv files created in the transform stage.

## Requerements

You need to clone the three repositores related above **into this repository**, example:

1. Clone this repository
2. Move to prices_pipeline folder
3. Clone prices_scraper
4. Clone prices_cleaner
5. Clone prices_load

Next, create a folder named "raw" into the prices_scraper folder.

Also, create a folder named "prices_db" and other named "backup" in prices_pipeline folder.

## For first use

Run the pipeline_prices.py without run the ** load ** function and rename the cleaned file to:

<category>+'_db.csv'
  
This is necessary because the load data merge two diferents files a **db** file and the today data.

## Next step

Simply run:

python3 pipeline_prices.py

and see the magic!!

## Contribute

If you want contribute let me know or make a pull request
I try to come daily to github to see what happen.

Enjoy!
