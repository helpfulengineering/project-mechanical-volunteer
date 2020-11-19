# -*- coding: utf8 -*-
"""Main package for pybossa-healthsites."""

import os
import json
from flask import current_app as app
from flask_plugins import Plugin
from pybossa.extensions import importer

from . import default_settings
from .healthsites_importer import BulkTaskHealthsitesImporter


__plugin__ = "Healthsites"
__version__ = json.load(open(os.path.join(os.path.dirname(__file__),
                                          'info.json')))['version']


class Healthsites(Plugin):
    """A PYBOSSA plugin for managing HealthSites data integration."""

    def setup(self):
        """Setup plugin."""
        self.configure()
        self.setup_blueprints()
        self.setup_healthsites_importer()

    def configure(self):
        """Load configuration settings."""
        settings = [key for key in dir(default_settings) if key.isupper() and
                    not key.startswith('#')]
        for s in settings:
            if not app.config.get(s):
                app.config[s] = getattr(default_settings, s)

    def setup_blueprints(self):
        """Setup blueprints."""
        from .api.locations import BLUEPRINT as locations
        from .views import BLUEPRINT as importer
        app.register_blueprint(locations, url_prefix='/healthsites/locations')
        app.register_blueprint(importer, url_prefix='/healthsites/import')

    def setup_healthsites_importer(self):
        """Setup the healthsites importer."""
        importer._importers['healthsites'] = BulkTaskHealthsitesImporter
        importer._importer_constructor_params['healthsites'] = {'api_key': app.config['HEALTHSITES_API_KEY']}

    