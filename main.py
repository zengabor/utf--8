#!/usr/bin/env python
# encoding: utf-8
from google.appengine.ext import db
import webapp2

class Foo(db.Model):
  bar = db.StringProperty()

class HomeHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body><form action="/post" method="post" accept-charset="utf-8">')
    self.response.out.write('<p><label for="bar">Try submitting some accented characters:</label><br />')
    self.response.out.write('<input type="text" name="bar" id="bar" maxlength="125" value="äáéíóöőúüű">')
    self.response.out.write('<input type="submit" value="submit"></p></form>')
    self.response.out.write('<p>Your user agent: <pre>%s</pre></p>' % self.request.headers['USER_AGENT'])
    self.response.out.write('</body></html>')

class PostHandler(webapp2.RequestHandler):
  def post(self):
    bar=self.request.POST['bar']
    if bar and len(bar) > 125:
      bar = bar[:125]
    try:
      foo = Foo(bar=bar) # you would think that this works. this should be transparent
      foo.put()
      self.response.out.write('Saved successfully.')
    except Exception, ex:
      self.response.out.write('Exception: %s' % ex)

app = webapp2.WSGIApplication([
    webapp2.Route('/', HomeHandler),
    webapp2.Route('/post', PostHandler),
], debug=True)

def main():
    app.run()

if __name__ == '__main__':
	main()
