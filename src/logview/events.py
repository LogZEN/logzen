import cherrypy

from logview.backends import backend

from logview import templates

class Events:
    def __init__(self):
        pass

    @cherrypy.expose
    def list(self,
             page = 0):
        template = templates.get_template('eventlist.html')

        events = backend.get_events()
        return template.render(events = events,
                               page = int(page),
                               pagesize = 50)

    @cherrypy.expose
    def details(self,
                event_id):
        template = templates.get_template('event.html')

        event = backend.get_event(event_id)
        return template.render(event = event)

        pass

    @cherrypy.expose
    def filter(self,
               type,
               value,
               page = 0):
        template = templates.get_template('eventlist.html')

        events = backend.get_events({type: value})
        return template.render(events = events,
                               page = int(page),
                               pagesize = 50,
                               type = type,
                               value = value)
