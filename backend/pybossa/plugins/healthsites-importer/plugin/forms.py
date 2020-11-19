from flask import current_app
from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired
from wtforms import IntegerField, DecimalField, TextField, BooleanField, \
    SelectField, validators, TextAreaField, PasswordField, FieldList, SelectMultipleField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.widgets import HiddenInput
from flask_babel import lazy_gettext, gettext
from iiif_prezi.loader import ManifestReader

class BulkTaskHealthsitesImportForm(Form):
    form_name = TextField(label=None, widget=HiddenInput(), default='healthsites')
    msg_required = lazy_gettext("You must provide a Country")
    #msg_url = lazy_gettext("Oops! That's not a valid URL. "
    #                       "You must provide a valid URL")
    country = TextField(lazy_gettext('Country'),
                             [validators.Required(message=msg_required)])
    version = SelectField(lazy_gettext('Presentation API version'), choices=[
        (ctx, ctx) for ctx in ManifestReader.contexts
    ], default='2.1')

    def get_import_data(self):
        return {
            'type': 'healthsites',
            'country': self.country.data
        }