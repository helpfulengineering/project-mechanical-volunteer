# -*- coding: utf8 -*-
# This file is part of PYBOSSA.
#
# Copyright (C) 2017 Scifabric LTD.
#
# PYBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PYBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PYBOSSA.  If not, see <http://www.gnu.org/licenses/>.

import time
import re
import json
import os
import math
import requests
from io import StringIO

from flask import Blueprint, request, url_for, flash, redirect, abort, Response, current_app
from flask import render_template, make_response, session
from flask import Markup
from flask_login import login_required, current_user
from flask_babel import gettext
from flask_wtf.csrf import generate_csrf
from rq import Queue

import pybossa.sched as sched

from pybossa.core import (uploader, signer, sentinel, json_exporter,
                          csv_exporter, importer, sentinel, db, anonymizer)
from pybossa.model import make_uuid
from pybossa.model.project import Project
from pybossa.model.category import Category
from pybossa.model.task import Task
from pybossa.model.task_run import TaskRun
from pybossa.model.auditlog import Auditlog
from pybossa.model.project_stats import ProjectStats
from pybossa.model.webhook import Webhook
from pybossa.model.blogpost import Blogpost
from pybossa.util import (Pagination, admin_required, get_user_id_or_ip, rank,
                          handle_content_type, redirect_content_type,
                          get_avatar_url, fuzzyboolean)
from pybossa.auth import ensure_authorized_to
from pybossa.cache import projects as cached_projects
from pybossa.cache import users as cached_users
from pybossa.cache import categories as cached_cat
from pybossa.cache import project_stats as stats
from pybossa.cache.helpers import add_custom_contrib_button_to, has_no_presenter
from pybossa.ckan import Ckan
from pybossa.extensions import misaka
from pybossa.cookies import CookieHandler
from pybossa.password_manager import ProjectPasswdManager
from pybossa.jobs import import_tasks, webhook
from pybossa.forms.projects_view_forms import *
from pybossa.forms.admin_view_forms import SearchForm
from pybossa.importers import BulkImportException
from pybossa.pro_features import ProFeatureHandler

from pybossa.core import (project_repo, user_repo, task_repo, blog_repo,
                          result_repo, webhook_repo, auditlog_repo)
from pybossa.auditlogger import AuditLogger
from pybossa.contributions_guard import ContributionsGuard
from pybossa.default_settings import TIMEOUT
from pybossa.exporter.csv_reports_export import ProjectReportCsvExporter

from pybossa.view.projects import project_by_shortname, project_title, sanitize_project_owner, pro_features

from .forms import BulkTaskHealthsitesImportForm

BLUEPRINT = Blueprint('healthsites_importer', __name__)

MAX_NUM_SYNCHRONOUS_TASKS_IMPORT = 200
auditlogger = AuditLogger(auditlog_repo, caller='web')
importer_queue = Queue('medium',
                       connection=sentinel.master,
                       default_timeout=TIMEOUT)
webhook_queue = Queue('high', connection=sentinel.master)

@BLUEPRINT.route('/<short_name>', methods=['GET', 'POST'])
@login_required
def import_healthsites_tasks(short_name):
    project, owner, ps = project_by_shortname(short_name)

    ensure_authorized_to('read', project)
    ensure_authorized_to('update', project)

    title = project_title(project, "Import Tasks")
    loading_text = gettext("Importing tasks, this may take a while, wait...")
    pro = pro_features()
    dict_project = add_custom_contrib_button_to(project, get_user_id_or_ip(), ps=ps)
    project_sanitized, owner_sanitized = sanitize_project_owner(dict_project,
                                                                owner,
                                                                current_user,
                                                                ps)
    template_args = dict(title=title, loading_text=loading_text,
                         project=project_sanitized,
                         owner=owner_sanitized,
                         n_tasks=ps.n_tasks,
                         overall_progress=ps.overall_progress,
                         n_volunteers=ps.n_volunteers,
                         n_completed_tasks=ps.n_completed_tasks,
                         target='healthsites_importer.import_healthsites_tasks',
                         pro_features=pro)

    importer_type = "healthsites"
    all_importers = importer.get_all_importer_names()
    if importer_type is not None and importer_type not in all_importers:
        return abort(404)

    form = BulkTaskHealthsitesImportForm(request.body)
    template_args['form'] = form

    if request.method == 'POST':
        if form.validate():  # pragma: no cover
            try:
                return _import_tasks(project, **form.get_import_data())
            except BulkImportException as err_msg:
                raise
                flash(err_msg, 'error')
            except Exception as inst:  # pragma: no cover
                raise
                current_app.logger.error(inst)
                msg = 'Oops! Looks like there was an error!'
                flash(gettext(msg), 'error')
        template_args['template'] = '/projects/importers/%s.html' % importer_type
        return handle_content_type(template_args)

    if request.method == 'GET':
        template_args['template'] = '/projects/importers/%s.html' % importer_type
        return handle_content_type(template_args)


def _import_tasks(project, **form_data):
    number_of_tasks = importer.count_tasks_to_import(**form_data)
    if number_of_tasks <= MAX_NUM_SYNCHRONOUS_TASKS_IMPORT:
        report = importer.create_tasks(task_repo, project.id, **form_data)
        flash(report.message)
    else:
        importer_queue.enqueue(import_tasks, project.id, **form_data)
        flash(gettext("You're trying to import a large amount of tasks, so please be patient.\
            You will receive an email when the tasks are ready."))
    return redirect_content_type(url_for('.import_healthsites_tasks',
                                         short_name=project.short_name))
