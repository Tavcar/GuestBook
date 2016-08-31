#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
from models import Guestbook

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("base.html")


class RezultatHandler(BaseHandler):
    def post(self):

        ime = self.request.get("ime") or "Neznanec"
        email = self.request.get("email")
        vnos = self.request.get("vnos")

        guestbook = Guestbook(ime=ime, email=email, vnos=vnos)
        guestbook.put()

        return self.redirect_to("message-list")


class SeznamSporocilHandler(BaseHandler):
    def get(self):
        seznam = Guestbook.query(Guestbook.deleted == False).fetch()
        params = {"seznam": seznam}
        return self.render_template("message_list.html", params=params)


class PosameznoSporociloHandler(BaseHandler):
    def get(self, guestbook_id):
        guestbook = Guestbook.get_by_id(int(guestbook_id))
        params = {"guestbook": guestbook}
        return self.render_template("single_message.html", params=params)


class UrediSporociloHandler(BaseHandler):
    def get(self, guestbook_id):
        guestbook = Guestbook.get_by_id(int(guestbook_id))
        params = {"guestbook": guestbook}
        return self.render_template("edit_message.html", params=params)

    def post(self, guestbook_id):
        ime = self.request.get("ime")
        email = self.request.get("email")
        vnos = self.request.get("vnos")
        guestbook = Guestbook.get_by_id(int(guestbook_id))
        guestbook.ime = ime
        guestbook.email = email
        guestbook.vnos = vnos
        guestbook.put()
        return self.redirect_to("message-list")


class IzbrisiSporociloHandler(BaseHandler):
    def get(self, guestbook_id):
        guestbook = Guestbook.get_by_id(int(guestbook_id))
        params = {"guestbook": guestbook}
        return self.render_template("delete_message.html", params=params)

    def post(self, guestbook_id):
        guestbook = Guestbook.get_by_id(int(guestbook_id))
        guestbook.deleted = True
        guestbook.put()
        return self.redirect_to("message-list")


class SeznamIzbrisanihSporocilHandler(BaseHandler):
    def get(self):
        seznam = Guestbook.query(Guestbook.deleted == True).fetch()
        params = {"seznam": seznam}
        return self.render_template("deleted_list.html", params=params)


class TrajenIzbrisSporocilHandler(BaseHandler):
    def get(self, guestbook_id):
        guestbook = Guestbook.get_by_id(int(guestbook_id))
        params = {"guestbook": guestbook}
        return self.render_template("final.html", params=params)

    def post(self, guestbook_id):
        guestbook = Guestbook.get_by_id(int(guestbook_id))
        guestbook.key.delete()
        return self.redirect_to("deleted-list")

class PosameznoDSporociloHandler(BaseHandler):
    def get(self, guestbook_id):
        guestbook = Guestbook.get_by_id(int(guestbook_id))
        params = {"guestbook": guestbook}
        return self.render_template("single_dmessage.html", params=params)

class PovrnitevSporocilaHandler(BaseHandler):
    def get(self, guestbook_id):
        guestbook = Guestbook.get_by_id(int(guestbook_id))
        params = {"guestbook": guestbook}
        return self.render_template("return.html", params=params)

    def post(self, guestbook_id):
        guestbook = Guestbook.get_by_id(int(guestbook_id))
        guestbook.deleted = False
        guestbook.put()
        return self.redirect_to("deleted-list")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/results', RezultatHandler),
    webapp2.Route('/message-list', SeznamSporocilHandler),
    webapp2.Route('/message/<guestbook_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/message/<guestbook_id:\d+>/edit', UrediSporociloHandler),
    webapp2.Route('/message-list', SeznamSporocilHandler, name="message-list"),
    webapp2.Route('/message/<guestbook_id:\d+>/delete', IzbrisiSporociloHandler),
    webapp2.Route('/deleted-list', SeznamIzbrisanihSporocilHandler),
    webapp2.Route('/deleted-list', SeznamIzbrisanihSporocilHandler, name="deleted-list"),
    webapp2.Route('/message/<guestbook_id:\d+>/final', TrajenIzbrisSporocilHandler),
    webapp2.Route('/message/<guestbook_id:\d+>/return', PovrnitevSporocilaHandler),
    webapp2.Route('/message/<guestbook_id:\d+>/d', PosameznoDSporociloHandler),
], debug=True)