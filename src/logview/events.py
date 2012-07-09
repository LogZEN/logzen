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
               page = 0,
               host = None,
               facility = None,
               severity = None,
               tag = None,
               program = None,
               message = None):
        template = templates.get_template('eventlist.ajax.html')

        filters = {}
        if host is not None:
            filters['host'] = '%' + host + '%'
        if facility is not None:
            filters['facility'] = '%' + facility + '%'
        if severity is not None:
            filters['severity'] = '%' + severity + '%'
        if tag is not None:
            filters['tag'] = '%' + tag + '%'
        if program is not None:
            filters['program'] = '%' + program + '%'
        if message is not None:
            filters['message'] = '%' + message + '%'

        events = backend.get_events(filters)
        return template.render(events = events,
                               page = int(page),
                               pagesize = 50)
