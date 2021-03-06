[![Build Status](https://travis-ci.org/montoyjh/postdoc_challenge.svg?branch=master)](https://travis-ci.org/montoyjh/postdoc_challenge)
[![Coverage Status](https://coveralls.io/repos/github/montoyjh/postdoc_challenge/badge.svg?branch=master&service=github)](https://coveralls.io/github/montoyjh/postdoc_challenge?branch=master)
## Installation
Requirements may be installed via `pip install -r requirements.txt` from within the package folder.

## Usage

* Generate files and nodes files using `python gen_test_data.py -o OUTPUT_FILENAME -n NUM_DATA`
* Run solution using `python solution.py -f INPUT_FILES_FILENAME -n INPUT_NODES_FILENAME`
* Help for either function (include optional arguments for plotting, etc.) can be
shown using `python gen_test_data.py --help` or `python solution.py --help`
* Plot the results using `python solution.py -f INPUT_FILES_FILENAME -n INPUT_NODES_FILENAME --plot` or `python solution.py -f INPUT_FILES_FILENAME -n INPUT_NODES_FILENAME --plotly` (for matplotlib and plotly, respectively)

## Web

A web implementation of this package is available at [https://filenode-distributor.herokuapp.com/](https://filenode-distributor.herokuapp.com/)
