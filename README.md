# PacktPub

Script for work with Packt Publishing account.

Can log-in into your account and download all books and code samples, that you've bought.
Script **DOESN'T** hack their servers or download all books from store. It just downloads all items, you've purchased.

Script was designed to keep track of my personal library on local computer and automatically update it with every new book purchase.

## Language:
Python 3

## Dependencies:
Install following packages before run: 
* MechanicalSoup
* html5lib
* requests
* beautifulsoup4
```
pip MechanicalSoup html5lib requests beautifulsoup4
```
## Usage:

### Direct use
For direct transfering if account credentials to script with command line:
```
python3 path_to_PacktPublishing.py --email user.name.domain.com --pass your_sofisticated_password
```
### Simple use
To define credentials inside of script and use simple run:
python3 path_to_PacktPublishing.py

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
xxxxxxxxxxxxxxxxx - your e-mail
yyyyyyyyyyyyyyyyy - your password
They need to be typed in between quotation marks.

