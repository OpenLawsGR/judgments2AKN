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
The scrapper for the Council of State is based on Selenium (*legal_crawlers/ste_scrapper/scrapper.py*). It takes as input argument the year and downloads in plain text all court decisions that can be found for this year. Files are saved in *legal_crawlers/data/ste/year* folder. Usage:

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

Please notice that Α.4 for the fileType argument is written with a greek character Α and not with a latin one. The crawler downloads Legal Opinions as PDF files and the metadata (saved in txt files) from the Diavgeia platform. More information on available parameters can be found in [Diavgeia API](https://diavgeia.gov.gr/api/help)

### Preprocessing
Preprocessing (including conversion of PDF files for Legal Opinions to plain text) is implemented through the command line interface preprocessing.py. The user can provide year (redundant for Legal Council of State) and filename parameters in order to process specific texts. 

usage example:

```console
user@foo:~$ python preprocessing.py ste -year=2016
```

By default post-processing texts will be stored to a base folder *legal_texts* (for the example provided path will be *legal_texts/ste/2016*). Accordingly, for the decisions of the Supreme Civil and Criminal Court "Areios Pagos" the path will be *legal_texts/areios_pagos/year* and for Legal Opinions path will be *legal_texts/nsk*. In addition, this module will automatically store metadata files (if available) in a similar way (for example, for the Council of State metadata files will be stored to *legal_texts/ste_metadata/2016*). 

### Transformation software
Transformations is possible using the following files and providing either a specific year or the name of the txt file to transform:
- createCouncilOfStateJudgmentsAkn.py
- createAreiosPagosJudgmentsAkn.py
- createLegalOpinionsAkn.py

```console
user@foo:~$ python createCouncilOfStateJudgmentsAkn.py -year=2016 'A1367_2006.txt'
```

By default Akoma Ntoso XML files will be stored to a base folder *XML* (for the example provided path will be *XML/ste/2016*). Accordingly, for the decisions of the Supreme Civil and Criminal Court "Areios Pagos" storage path will be *XML/areios_pagos/year* and for Legal Opinions *XML/nsk*.

Transformation to XML files also supports Named Entity Recognition in order to build the appropriate nodes based on Akoma Ntoso prototype. A beta version is available if NER results are provided in [GATE XML](https://gate.ac.uk/) format and are stored in similar paths, for example, for the Council of State (ste) in *NER/ste/year*.  If no Gate XML file is available the appropriate nodes will not be created.

Parallelization is possible using [GNU Parallel](https://www.gnu.org/software/parallel/). In this case multiple calls of the above python commands can be included in a single file (one command per line) which is passed in GNU parallel e.g.

```console
user@foo:~$ parallel < commands.txt
```

### Validation
Generated XML files can be validated against the Akoma Ntoso Schema using the checkValidXML.py file. User can provide the name of the legal_authority (ste, areios_pagos, nsk) and year (optional) paramenter in order to perform validation for specific years. 

Example:

```console
user@foo:~$ python checkValidXML.py ste -year=2016
```

## License
Software is licensed under the MIT license.

## Funding
The project "Automated Analysis and Processing of Legal Texts for their Transformation into Legal Open Data" is implemented through the Operational Program "Human Resources Development, Education and Lifelong Learning" and is co-financed by the European Union (European Social Fund) and Greek national funds.
