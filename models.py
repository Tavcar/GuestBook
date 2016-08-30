from google.appengine.ext import ndb

class Guestbook(ndb.Model):
    ime = ndb.StringProperty()
    email = ndb.StringProperty()
    vnos = ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)