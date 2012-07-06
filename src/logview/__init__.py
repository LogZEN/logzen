import os

import jinja2
templates = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.join(os.getcwd(), 'templates')))
