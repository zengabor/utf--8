#!/usr/bin/env python
# encoding: utf-8
from google.appengine.ext import db
import webapp2
from urllib import quote_plus, unquote_plus

_COOKIE_NAME = 'test'

class Foo(db.Model):
  bar = db.StringProperty()

class HomeHandler(webapp2.RequestHandler):
  def get(self):
    bar = 'äáéíóöőúüű'
    self.response.out.write('<html><body><form action="/post" method="post" accept-charset="utf-8">')
    if _COOKIE_NAME in self.request.cookies:
      try: # this works:
        bar = unquote_plus(str(self.request.cookies.get(_COOKIE_NAME))).decode('utf-8')
        self.response.out.write('<p>Cookie content when first converted to str: <strong>%s</strong></p>' % bar)
      except Exception, ex:
        self.response.out.write('<p><strong>Exception while retrieving cookie via str:</strong></p><pre>  %s</pre>' % ex)
      try: # will throw an exception as self.request.cookies.get() returns unicode instead of str:
        bar = unquote_plus(self.request.cookies.get(_COOKIE_NAME)).decode('utf-8')
        self.response.out.write('<p>Cookie content as it should work: <strong>%s</strong></p>' % bar)
      except Exception, ex:
        self.response.out.write('<p><strong>Exception while retrieving cookie normally:</strong></p><pre>  %s</pre>' % ex)
    self.response.out.write('<p><label for="bar">Try submitting some accented characters:</label><br />')
    self.response.out.write('<input type="text" name="bar" id="bar" maxlength="125" value="%s">' % bar)
    self.response.out.write('<input type="submit" value="submit"></p></form>')
    # self.response.out.write('<p>Your user agent: <pre>%s</pre></p>' % self.request.headers['USER_AGENT'])
    self.response.out.write('</body></html>')

class PostHandler(webapp2.RequestHandler):
  def post(self):
    bar = self.request.POST['bar']
    if bar and len(bar) > 125:
      bar = bar[:125]
    try:
      foo = Foo(bar=bar)
      foo.put()
      # setting the cookie works alright:
      self.response.set_cookie(_COOKIE_NAME, quote_plus(bar.encode('utf-8'), safe='~'), path='/')
      self.redirect_to('home')
    except Exception, ex:
      self.response.out.write('Exception: %s' % ex)

app = webapp2.WSGIApplication([
    webapp2.Route('/', HomeHandler, name='home'),
    webapp2.Route('/post', PostHandler),
], debug=True)

def main():
    app.run()

if __name__ == '__main__':
	main()
