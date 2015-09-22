# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
import lxml.html

import urlparse
import httplib

# Recursively follow redirects until there isn't a location header
# http://www.zacwitte.com/resolving-http-redirects-in-python
def resolve_http_redirect(url, depth=0):
    if depth > 10:
        raise Exception("Redirected "+depth+" times, giving up.")
    o = urlparse.urlparse(url,allow_fragments=True)
    conn = httplib.HTTPConnection(o.netloc)
    path = o.path
    if o.query:
        path +='?'+o.query
    conn.request("HEAD", path)
    res = conn.getresponse()
    headers = dict(res.getheaders())
    if headers.has_key('location') and headers['location'] != url:
        return resolve_http_redirect(headers['location'], depth+1)
    else:
        return url

for url0 in open('urls.txt','r'):
	try:
		# Read in a page
		url0 = url0.strip()
		print url0
		url = resolve_http_redirect(url0)
		print url
		html = scraperwiki.scrape(url)

		# Find something on the page using css selectors
		root = lxml.html.fromstring(html)
		root.make_links_absolute(url)
		pdfs = set()
		for a in root.cssselect('a'):
			href = a.get('href')
			if href and 'pdf' in href.lower(): pdfs.add(href)
		print pdfs
		print

		# Write out to the sqlite database using scraperwiki library
		for pdf in pdfs:
			scraperwiki.sqlite.save(unique_keys=['pdf'], data={"pdf": pdf, "url": url, "url0": url0})
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
