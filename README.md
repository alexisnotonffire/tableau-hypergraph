# Hypergraph
This utility creates a Hyper extract that you can use to build reports on top of your Tableau Online metadata. 

## Setup

Firstly, make sure you have Python 3.7+ and the relevant virtual environment tooling for your system. Then clone this repository and set up your virtual environment. Make sure to run the correct command for activating your virtual env:
```bash
git clone https://github.com/alexisnotonffire/tableau-hypergraph.git
cd tableau-hypergraph
python3 -m venv venv

# WINDOWS
#./venv/scripts/Activate.ps1

# UNIX
#. ./venv/bin/activate

python3 -m pip install -r requirements.txt
```

Next, create a YAML file named `token` under the resources directory and open it up for editing. This file will need to be populated with the data required to authenticate Hypergraph against your Tableau site. Do this by replacing the `UPPERCASE` text with the attributes relevant to your server in the following code block:
```yaml
server: https://POD.online.tableau.com    # Online URL including pod; e.g. https://dub01.online.tableau.com
site: SITE                                # Site name
name: NAME                                # Personal Access Token Name
value: VALUE                              # Personal Access Token Secret
```
To create a Personal Access Token, please see the [docs](https://help.tableau.com/current/pro/desktop/en-us/useracct.htm#create-and-revoke-personal-access-tokens).

## Usage
After setup, you can run the utility from the top level folder with the following command:
```bash
python main.py
```
This will create a new directory - `build` - and populate the results of the metadata queries into a Hyper extract: `build/tableau.hyper`. You can then connect to this file in Tableau Desktop and begin creating your reports.
