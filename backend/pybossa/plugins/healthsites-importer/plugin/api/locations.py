# -*- coding: utf8 -*-
"""API locations module for Healthsites."""

import json
from flask import Blueprint, request, abort, make_response
from flask_login import login_required
from pybossa.core import csrf
from pybossa.core import project_repo
from pybossa.auth import ensure_authorized_to

BLUEPRINT = Blueprint('healthsites', __name__)


def respond(msg):
    """Return a basic 200 OK response."""
    data = dict(message=msg, status=200)
    response = make_response(json.dumps(data))
    response.mimetype = 'application/json'
    response.status_code = 200
    return response


@login_required
@BLUEPRINT.route('/<location_id>')
def get_location(short_name, location_id):
    """Trigger analysis for a result or set of results."""

    payload = request.json or {}
    
    return respond('OK')
