# judgments2AKN
Automatic Transformation of Greek Court Decisions and Legal Opinions into the Akoma Ntoso format

judgments2AKN is a project for the automated collection and transformation of Greek court decisions and legal opinions into Akoma Ntoso XML files. Supported legal sources are the judgments of the [Supreme Civil and Criminal Court](http://www.areiospagos.gr/), the judgments of the [Council of State](http://www.adjustice.gr) and the legal opinions of the [Legal Council of State](http://www.adjustice.gr).

## Prerequisites

### Scrappers
- [Python](https://www.python.org/) v2.7
- [Scrapy](https://scrapy.org/) (tested with v1.6). Installation instructions [here](https://docs.scrapy.org/en/latest/intro/install.html).
- [Python binding for Selenium WebDriver](https://pypi.org/project/selenium/) (tested with v3.9.0) and [Mozilla geckodriver](https://github.com/mozilla/geckodriver/releases) (tested with v0.26.0)

### Transformation software
- [Python](https://www.python.org/) v2.7
- [lxml](https://lxml.de/) Python library (tested with v4.3.1)
- [Antlr (ANother Tool for Language Recognition)](https://www.antlr.org/) v4 (tested with v4.7.2)

## Instructions

### Scrappers
The scrapper for the Council of State is based on Selenium (legal_crawlers/ste_scrapper/scrapper.py). It takes as input argument the year and downloads in plain text all court decisions that can be found for this year. Files are saved in legal_crawlers/data/ste/year folder. Usage:

```console
user@foo:~/legal_crawlers/ste_scrapper$ python scrapper.py 2016
```

The crawler for the Supreme Civil and Criminal Court (Arios Pagos) is based on Scrapy. Again the year is given as input argument. Usage:

```console
user@foo:~/legal_crawlers$ scrapy crawl CyLaw -a year=2016
```

The crawler for the Legal Council is also based on Scrapy. Usage:

```console
user@foo:~/legal_crawlers$ scrapy crawl clarity -a fileType=Α.4 -a org=50024 -a from_date=2019-01-01
```

Please notice that Α.4 for the fileType argument is writen with a greek character Α and not with a latin one. The crawler dowloads the PDF files and the metadata from the Diavgeia platform (saved in txt files).

### Preprocessing
Preprocessing (including conversion of PDF files for legal opinions to plain text) is done in the preprocessing.py file. The user has to change the value of the FOLDER_PATH according to the document type ('nsk' for legal opinions, 'ste' for decisions of the Council of State, 'areios_pagos' for decisions of the Supreme Civil and Criminal Court.

TODO: preprocessing.py refactoring and use of arguments in order to be more user-friendly.

### Transformation software
Transformation is possible using the following files and providing the name of the txt file to transform:
- createCouncilOfStateJudgmentsAkn.py
- createAreiosPagosJudgmentsAkn.py
- createLegalOpinionsAkn.py

```console
user@foo:~$ python createCouncilOfStateJudgmentsAkn.py 'A1367_2006.txt'
```

TODO: allow user to provide full path to file instead of using default folders for storage of files.

Parallelization is possible using [GNU Parallel](https://www.gnu.org/software/parallel/). In this case multiple calls of the above python commands can be included in a single file (one command per line) which is passed in GNU parallel e.g.

```console
user@foo:~$ parallel < commands.txt
```

### Validation
Generated XML files can be validated against the Akoma Ntoso Schema using the checkValidXML.py file. The validation is done in a folder base and the user has again to declare the folder as a value of the FOLDER_PATH variable.

## License
Software is licensed under the MIT license.
