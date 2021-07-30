# Overview

`camelcamelcamel` is a basic script to highlighting high percentage sales as scraped and tracked by the site, camelcamelcamel.com. This will scrape the top 10
pages and display results that are above a certain percentage and are for items below a certain price threshold.

# Notes

The output of the script is designed to spit out csv compatible text. This is often used in conjunction with `csv_to_tab` (versus something like column) that
understands escaped commas.

Currently this requires `click` and `feedparser` to run. Proper project setup is forthcoming.
