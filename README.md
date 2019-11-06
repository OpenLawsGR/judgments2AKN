# judgments2AKN
Automatic Transformation of Greek Court Decisions and Legal Opinions into the Akoma Ntoso format

judgments2AKN is a project for the automated collection and transformation of Greek court decisions and legal opinions into Akoma Ntoso XML files. Supported legal sources are the judgments of the [Supreme Civil and Criminal Court](http://www.areiospagos.gr/), the judgments of the [Council of State](http://www.adjustice.gr) and the legal opinions of the [Legal Council of State](http://www.adjustice.gr).

## Prerequisites
### Scrappers
- [Python](https://www.python.org/) v2.7
- [Scrapy](https://scrapy.org/)
- [Python binding for Selenium WebDriver](https://pypi.org/project/selenium/) (tested with v3.9.0) and [Mozilla geckodriver](https://github.com/mozilla/geckodriver/releases) (tested with v0.26.0)

### Transformation software
- [Python](https://www.python.org/) v2.7
- [lxml](https://lxml.de/) Python library
- [Antlr (ANother Tool for Language Recognition)](https://www.antlr.org/) v4

## Instructions
### Scrappers
The scrapper for the Council of State is based on Selenium (scrappers/ste_scrapper.py). It takes as input argument the year and downloads in plain text all court decisions that can be found for this year. Usage:

```console
user@foo:~$ python ste_scrapper.py 2016
```

### Transformation software

## License
Software is licensed under the MIT license.
