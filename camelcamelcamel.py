#!/usr/local/bin/python3
import concurrent.futures
import csv
import functools
import io
import re

import feedparser
import click


def _parse_title(text):
    info = text.split(" - ")
    parts = ["- down ", "down ", "(", ")", "to ", "from ", "%", "$", ","]
    drop, _, _, price, *_ = map(
        float, functools.reduce(lambda x, y: x.replace(y, ""), parts, info[-1]).split()
    )
    return " - ".join(info[:-1]), f"{drop:5.2f}% => ${price:6.2f}", drop, price


def _parse_url(text):
    return re.findall(r"http.*/go", text)[0]


def _run(url, price, drop):
    data = []
    for e in feedparser.parse(url)["entries"]:
        title, display, drop_, price_ = _parse_title(e["title"])
        if drop_ >= drop and price_ <= price:
            data.append((title, display, _parse_url(e["summary"])))
    return data


@click.command()
@click.option("-p", "--price", default=150.00)
@click.option("-d", "--drop", default=60.00)
def main(price, drop):
    url = "https://camelcamelcamel.com/top_drops/feed?bn=&d=0.01&i=1&s=absolute&t=relative&p={}"
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(_run, url.format(i + 1), price, drop) for i in range(10)
        ]
        data = sum((f.result() for f in futures), [])
    f = io.StringIO()
    csv.writer(f, quoting=csv.QUOTE_MINIMAL).writerows(data[::-1])
    click.echo(f.getvalue())


if __name__ == "__main__":
    main()
