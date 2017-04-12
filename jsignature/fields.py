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

class JSignatureField(models.Field):
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
        #print "fields.JSignatureField.to_python(value=%s, type=%s)" % (value, type(value))
        value = JSignature(value)
        value.set_signatory(None, self.signatory_field)
        return value
        
    def clean(self, value, model_instance):
        #print "JSignatureField.clean(name=%s value=%s, model_instance=%s)" % (self.name, value, model_instance)

        if model_instance.pk and not value.content:
            orig = getattr(model_instance, '_orig', None)
            if not orig:
               orig = type(model_instance).objects.get(pk=model_instance.pk)
               setattr(model_instance, '_orig', orig)
            orig_value = getattr(orig, self.name)
            if orig_value.is_signed():
                value = orig_value
                #print "%s: used database value." % self.name

        if self.signatory_field and not value.signatory_name:
            if hasattr(model_instance, self.signatory_field):
                signatory = getattr(model_instance, self.signatory_field, None)
                value.set_signatory(signatory, self.signatory_field)

        return super(JSignatureField, self).clean(value, model_instance)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)
        
    def get_prep_value(self, value):
        #print "JSignatureField.get_prep_value(name=%s value=%s)" % (self.name, value)
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
