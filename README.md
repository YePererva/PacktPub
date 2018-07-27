# PacktPub

Script for work with Packt Publishing account.


It can log-in into your account and download all books and code samples, that you've bought.
Script **DOES NOT** hack their servers or download all books from store. It just downloads all items, you've purchased.

Script was designed to keep track of my personal library on local computer and automatically update it with every new book purchased.

## Language:
Python 3

## Dependencies:
Install following packages before run:
* MechanicalSoup
* html5lib
* requests
* beautifulsoup4
```
python -m pip install --upgrade pip
pip install MechanicalSoup html5lib requests beautifulsoup4
```
### NB! If using Python 3.7:
Current version of MechanicalSoup available with pip can't be installed for Python 3.7. Use following to install dependencies on Python 3.7 [Windows]:
```
python -m pip install --upgrade pip
git clone https://github.com/MechanicalSoup/MechanicalSoup.git
cd MechanicalSoup
python setup.py install
pip install html5lib requests beautifulsoup4
```

## Usage:

### Direct use
For direct transfering of account credentials to script with command line:
```
python3 path_to_PacktPublishing.py --email username@domain.com --pass your_sofisticated_password
```
### Simple use
To define credentials inside of script and use simple run:
```
python3 path_to_PacktPublishing.py
```
Change following lines:
```
email = None
password= None
```
to:
```
email    = r'xxxxxxxxxxxxxxxxx'
password = r'yyyyyyyyyyyyyyyyy'
```
where:
- xxxxxxxxxxxxxxxxx - your e-mail
- yyyyyyyyyyyyyyyyy - your password

They need to be typed in between quotation marks.

### Tested platforms:
- Windows 10 [x64] + Python 3.6.3 and Python 3.7.0
- Fedora 27 [x64] + Python 3.6.1
