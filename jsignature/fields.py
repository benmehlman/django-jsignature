"""
    Provides a django model field to store a signature captured
    with jSignature jQuery plugin
"""
import json
import six

from django.db import models
from django.core.exceptions import ValidationError

from .forms import (
    JSignatureField as JSignatureFormField,
    JSignature,
    JSIGNATURE_EMPTY_VALUES)

class JSignatureField(six.with_metaclass(models.SubfieldBase, models.Field)):
    """
    A model field handling a signature captured with jSignature
    """
    description = "A signature captured with jSignature"

    def __init__(self, *args, **kwargs):
        self.signatory_field = kwargs.pop('signatory_field', None)
        super(JSignatureField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'TextField'

    def to_python(self, value):
        print "fields.JSignatureField.to_python(value=%s, type=%s)" % (value, type(value))
        rv = JSignature(value)
        print "   returning: value=%s, type=%s" % (rv, type(rv))
        return rv
        
    def clean(self, value, model_instance):
        print "JSignatureField:clean(value=%s, model_instance=%s)" % (value, model_instance)

        if model_instance.pk and not value.content:
            orig = type(model_instance).objects.get(pk=model_instance.pk)
            value = getattr(orig, self.name)
            #print "orig value: %s" % value
            print "%s USING ORIGINAL VALUE" % self.name

        if self.signatory_field and not value.signatory_name:
            if hasattr(model_instance, self.signatory_field):
                signatory = getattr(model_instance, self.signatory_field, None)
                value.set_signatory(signatory)

        return super(JSignatureField, self).clean(value, model_instance)

    def get_prep_value(self, value):
        #if value is None:
        #    return None
        if not isinstance(value, JSignature):
            raise ValidationError('JSignatureField: expected JSignature instance got "%s".' % value)

        return value.as_db_json() if value.content else None  

    def formfield(self, **kwargs):
        defaults = {'form_class': JSignatureFormField}
        defaults.update(kwargs)
        return super(JSignatureField, self).formfield(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["jsignature.fields.JSignatureField"])
except ImportError:
    pass
