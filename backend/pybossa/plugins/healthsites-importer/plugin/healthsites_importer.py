# -*- coding: utf8 -*-
"""Importer for Healthsites Data"""

from flask import url_for
from pybossa.importers.base import BulkTaskImport, BulkImportException

import requests, time

class BulkTaskHealthsitesImporter(BulkTaskImport):
    """Import healthsites data."""

    importer_id = "healthsites"

    def __init__(self, api_key, country=None):
        """Init method."""
        self.api_key = api_key
        self.country = country

    def tasks(self):
        """Generate the tasks."""
        task_data = self._get_healthsites_data(self.country)
        return task_data

    def _get_healthsites_data(self, country: str):
        """Call the Healthsites API"""
        empty = False
        page = 1
        results = []
        while not empty:
            url = f"https://healthsites.io/api/v2/facilities/?api-key={self.api_key}&page={page}&country={self.country}&flat-properties=true"
            response = requests.get(url).json()
            empty = 0 == len(response) 
            if not empty:
                for item in response:
                    results.append({"info": item})
            
            page = page + 1

            if page > 100:
                break

            time.sleep(0.25)

        return results
