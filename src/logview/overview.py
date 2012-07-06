import cherrypy

from logview.backends import backend

from logview import templates


class Overview:
    def __init__(self):
        pass

    @cherrypy.expose
    def __call__(self):
        template = templates.get_template('overview.html')

        return template.render(count = 100,
                               count_last_hour = 30,
                               count_this_hour = 42)
