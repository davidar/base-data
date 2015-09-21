# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import lxml.html

for url in open('urls.txt','r'):
	try:
		# Read in a page
		url = url.strip()
		html = scraperwiki.scrape(url)

		# Find something on the page using css selectors
		root = lxml.html.fromstring(html)
		pdfs = set()
		for a in root.cssselect('a'):
			href = a.get('href')
			if href and 'pdf' in href: pdfs.add(href)
		print url, pdfs

		# Write out to the sqlite database using scraperwiki library
		for pdf in pdfs:
			scraperwiki.sqlite.save(unique_keys=['pdf'], data={"pdf": pdf, "url": url})
	except Exception as e:
		print e
		#break

# An arbitrary query against the database
#print scraperwiki.sql.select("* from data")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
