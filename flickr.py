"""
flickr.py - Phenny Flickr Module
copyme 2009, Fredrik Stark, http://flickr.com/photos/schmilblick/
No license, no rights reserved. Be creative!

http://inamidst.com/phenny/
"""

import re, urllib
from phenny import web

def do_flickr(term):
   if isinstance(term, unicode): 
      print 'Term is unicode'
      t = term.encode('utf-8')
   else:
      print 'Term is NOT unicode'
      t = term

   q = urllib.quote(t)
   u = 'http://www.flickr.com/search/?q=%s&w=all' % q
   bytes = web.get(u)
   print u

   # A bit nasty to have three regexes for this, I'll have to clean this mess up
   savos = ""
   r_links = re.compile(r'(?ims)<a[^>]*href="/photos/[^/]*/[^/]*/"[^>]*>')

   # Find all photo links on the result page
   links = r_links.findall(bytes)
   if not links:
      return None

   r_link  = re.compile(r'(?ims)<a[^>]*href="(/photos/[^/]*/[^/]*/)"[^>]*>')
   r_title = re.compile(r'(?ims)<a[^>]*title="([^"]*)"[^>]*>')

   i = 0 # Count the links
   j = 0 # Sometimes links are missing title, we need this to count links WITH titles
   for link in links:
      i += 1
      midi = r_title.findall(link)
      if midi:
         j += 1
         mmx = r_link.findall(link)
         if mmx:
            savos += "http://flickr.com"+mmx[0]+" - "+midi[0]+"       "
      if i > 10 or j > 3 or len(savos) > 250:
         break

   if not savos:
      return None

   return savos

def flickr(phenny, input):
   origterm = input.groups()[1]
   if not origterm: 
      return phenny.say('TRORU JA E DUM LR')

   origterm = origterm.encode('utf-8')

   term = urllib.unquote(origterm)
   term = term[0].upper() + term[1:]

   try:
      result = do_flickr(term)
   except IOError: 
      error = "flickr.com verkar vara paj"
      return phenny.say(error)

   if result is not None: 
      phenny.say(result)
   else:
      phenny.say('Hittar int %s @ flickr' % origterm)

flickr.commands = ['flickr']
flickr.priority = 'high'

if __name__ == '__main__': 
   print __doc__.strip()
