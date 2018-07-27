# pip install MechanicalSoup html5lib requests beautifulsoup4

import mechanicalsoup
import os, sys
import argparse

# ------------------------------------------------------------------------
# To define e-mail and password inside of script change the following lines:
email= None
password= None
# like following:
# email = r'Type e-mail in between quotation marks'
# password = r'Type password in between quotation marks'

# ------------------------------------------------------------------------

login_url = r'https://www.packtpub.com/login'
root_url = r'https://www.packtpub.com'
books_url = r'https://www.packtpub.com/account/my-ebooks'

# ------------------------------------------------------------------------

folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'books')

# ------------------------------------------------------------------------

def fix_symbols (title):
	# Remove prohibited filename symbols
	forbidden_symbols = r'\/:<>?*|'
	return title.translate({ord(symbol) :  "_" for symbol in forbidden_symbols})

# ------------------------------------------------------------------------

def create_folder (folder, overwrite = False):
	if not os.path.exists(folder): os.makedirs(folder)

# ------------------------------------------------------------------------

class PacktPub ():
	def __init__(self):
		# Will not allow to enter without "user_agent" section
		self.browser = mechanicalsoup.StatefulBrowser(
			soup_config={'features': 'html5lib'},
			raise_on_404=True,
			user_agent= r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36')
		self.browser.set_verbose(2)
		self.login_url = login_url
		self.books_url = books_url
		self.logged_in = False

	def login (self, name, password):
		self.browser.open(self.login_url)
		self.browser.select_form ('form[action="/login"]')
		self.browser["name"] = name
		self.browser["pass"] = password

		self.browser.submit_selected()
		self.browser.open(self.books_url)

		if "Account Details" in self.browser.get_current_page().text:
			print ('Log in succesfull')
			self.logged_in = True
		else:
			print("Log in failed!")

	def get_library (self):
		self.browser.open(self.books_url)
		page = self.browser.get_current_page()

		# getting list of page links
		page_list = page.find('div', {"class" : "solr-pager-page-selector"}).find_all('a', {"class" : "solr-page-page-selector-page"})
		# the active page is not a link, need to add it to array
		page_list_links = [self.books_url] + [root_url + instance['href'] for instance in page_list]
		print ('Total pages found:\t\t', len(page_list_links))

		# Running through all pages with bought books
		for page_number, page_link in enumerate (page_list_links):
			print ("Parsing page %d of %d" % (page_number+1, len(page_list_links)))
			self.browser.open(page_link)
			# Get the HTML of opened page
			page = self.browser.get_current_page()
			# Get list of all books on this page
			booklist = page.find('div', {"id" : "account-right-content"}).find_all('div', {"class" : "product-line unseen"})
			print ("Total books found on current page:\t", len(booklist))
			for book in booklist:
				title = book['title'].replace(' [eBook]', '')
				title = fix_symbols(title)
				print('\t' + title)
				download_container = book.find('div', {"class" : "download-container cf "})
				links = download_container.find_all('a')
				for link in links:
					if r"/pdf" in link["href"]:
						pdf = root_url + link["href"]
						pdf_name = os.path.join(folder, title + '.pdf')
						self.download(pdf, pdf_name)

					if r"/code" in link["href"]:
						code = root_url + link["href"]
						code_name = os.path.join(folder, title + ' - Code.zip')
						self.download(code, code_name)

		print ('Done!')

	def download (self, url, path):
		print ('\t\t'+ path + '\n\t\t\t' + url)

		# If file doesn't exist
		if not os.path.exists(path):
			# Download it
			self.direct_download(url, path)
		else:
			print ('\t\t\tAlready exists! Checking if it is valid')
			# Get file size on server
			file_on_server = self.browser.request('GET', url, stream = True).headers['content-length']
			# Get file size of local copy
			file_local = os.path.getsize (path)

			# If local file is equal to file on server
			if int(file_on_server) == int(file_local):
				print ('\t\t\t\tFile is valid')
				# Exit downloader
				return
			# Otherwise the local file is broken
			else:
				print ("\t\t\t\tLocal file is broken. Removing local copy")
				os.remove(path)
				print ("\t\t\tRestarting download")
				self.direct_download(url, path)

	def direct_download (self, url, path):
		data = self.browser.request('GET', url, stream = True)
		print ('\t\t\tDownloading...')
		with open (path, 'wb') as f:
			for chunk in data.iter_content(chunk_size = 512 * 1024):
				if chunk:
					f.write(chunk)
		print ('\t\t\tDownloaded')

# ------------------------------------------------------------------------

def main(packt):
	create_folder(folder)
	packt.get_library()

# ------------------------------------------------------------------------

if __name__ == '__main__':
	packt = PacktPub()

	parser = argparse.ArgumentParser()
	parser.add_argument('--email', dest = 'email', help="E-mail for log-in")
	parser.add_argument('--pass', dest='password', help="Password for log-in")
	args = parser.parse_args()
	if (args.email != None) and (args.password != None):
		packt.login(args.email, args.password)
	elif (email != None) and (password != None):
		packt.login(email, password)
	else:
		sys.exit("Wrong credentials!")

	if packt.logged_in == True:
		main(packt)
	else:
		sys.exit("Not logged in. Check the credentials!")
