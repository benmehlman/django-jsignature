"""
    Provides a django form field to handle a signature capture field with
    with jSignature jQuery plugin
"""
import json, base64
from django.forms.fields import Field
from django.core import validators
from django.core.exceptions import ValidationError
from .widgets import JSignatureWidget
from django.utils.safestring import mark_safe
from django.utils import dateparse, timezone

JSIGNATURE_EMPTY_VALUES = validators.EMPTY_VALUES + ('[]', )

class JSignature(object):
    def __init__(self, browser_json=None, db_json=None):    
        self.data = {}
        self.browser_json = browser_json

        if browser_json:
            l = json.loads(browser_json)
            self.data.update({ 'content-type': l[0], 'content': l[1] })
        elif db_json:
            self.data = json.loads(db_json)

    def set_signatory(self, signatory):
        if not signatory:
            return False
        name = unicode(signatory or '')
        if name:
            self.data['signatory-name'] = name
        if hasattr(signatory, 'pk'):
            self.data['signatory-pk'] = getattr(signatory, 'pk')

    def as_db_json(self):
        if not self.signed_dt:
            from datetime import datetime
            from pytz import utc
            self.data['signed-dt'] = datetime.now(utc).isoformat()
        return json.dumps(self.data)

    @property
    def content_type(self):
        return self.data.get('content-type', None)

    @property
    def content(self):
        return self.data.get('content', None)

    @property
    def content_base64(self):
        return base64.b64encode(self.content)

    @property
    def signed_dt(self):
        s = self.data.get('signed-dt', None)
        return dateparse.parse_datetime(s) if s else s

    @property
    def signed_on(self):
        return timezone.localtime(self.signed_dt).strftime('%x %X')

    @property
    def signatory_name(self):
        return self.data.get('signatory-name', None)

    @property
    def signatory_id(self):
        return self.data.get('signatory-id', None)

    def __str__(self):
       return str(self.data)


class JSignatureField(Field):
    """
    A field handling a signature capture field with with jSignature
    """
    widget = JSignatureWidget()

    def to_python(self, value):
            """
            Validates that the input can be red as a JSON object.
            Returns a Python list (JSON object unserialized).
            """
            print "forms.JSignatureField.to_python(value=%s)" % value
            if value in JSIGNATURE_EMPTY_VALUES:
                return None
            try:
                return JSignature(browser_json=value)
            except ValueError:
                raise ValidationError('forms.JSignatureField could not parse browser JSON.')
