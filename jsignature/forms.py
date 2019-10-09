"""
    Provides a django form field to handle a signature capture field with
    with jSignature jQuery plugin
"""
import json, base64, six
from datetime import datetime
from decimal import Decimal
from pytz import utc
import xml.etree.ElementTree as et

from django.forms.fields import Field
from django.core import validators
from django.core.exceptions import ValidationError
from .widgets import JSignatureWidget
from django.utils.safestring import mark_safe
from django.utils import dateparse, timezone

JSIGNATURE_EMPTY_VALUES = validators.EMPTY_VALUES + ('[]', )

class JSignature(object):
    def __init__(self, initial=None, native=None):
        #print "JSignature.__init__(initial=%s)" % initial
    
        self.data = {}

        if initial:
            if isinstance(initial, JSignature):
                self.data = initial.data
            elif initial.startswith('['):
                l = json.loads(initial)
                if len(l) == 2:
                    self.data.update({ 'content-type': l[0], 'content': l[1] })
            elif initial.startswith('{'):
                self.data = json.loads(initial)
        if native:
            self.data['native'] = native
        #print "  JSignature.data: %s" % self.data

    def set_signatory(self, signatory, field_name):
        if field_name:
            self.data['signatory-field'] = field_name
        if signatory:
            name = six.text_type(signatory or '')
            if name:
                self.data['signatory-name'] = name
            if hasattr(signatory, 'pk'):
                self.data['signatory-pk'] = getattr(signatory, 'pk')
                self.data['signatory-model'] = type(signatory).__name__

    def validate(self, content = None):
        content = content or self.content
        if not content:
            return False

        try:
            svg = et.fromstring(content)
        except Exception as e:
            return 'Got Invalid Signature Data.  Error was: %s' % e
        if not svg:
            return 'No signature image found.'
        #print svg.attrib
        width, height = svg.get('width', '-1'), svg.get('height', '-1')
        width = -1 if width.lower() in ('nan', 'infinity',) else int(Decimal(width))
        height = -1 if height.lower() in ('nan', 'infinity',) else int(Decimal(height))

        #print 'width: %s (%s), height: %s' % (width, type(width), height)
        if width < 90 or height < 30:
            return 'Signature is too small.'

        return None

    def as_db_json(self):
        data = dict(self.data)
        data.pop('native', None)
        if self.content and not self.signed_dt:
            data['signed-dt'] = datetime.now(utc).isoformat()
        return json.dumps(data)

    def is_signed(self):
        # for now -BEN
        #if self.validate():
        #    return False
        return bool(self.data.get('signed-dt', None))

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
    def signatory_field(self):
        return self.data.get('signatory-field', None)

    @property
    def signatory_name(self):
        return self.data.get('signatory-name', None)

    @property
    def signatory_id(self):
        return self.data.get('signatory-id', None)

    @property
    def native(self):
        return self.data.get('native', '')

    def __str__(self):
       return json.dumps(self.data)


class JSignatureField(Field):
    widget = JSignatureWidget

    def to_python(self, value):
        #print "forms.JSignatureField.to_python(value=%s)" % value
        return JSignature(value)

    def validate(self, value):
        if not value:
            return
        if not hasattr(value, 'validate'):
            raise ValidationError('Signature object should have a "validate" method but does not.  Something is wrong.')
        error = value.validate()
        if error:
            raise ValidationError(error)
