"""
    Provides a django form widget to handle a signature capture field with
    with jSignature jQuery plugin
"""
import json
import six

from django.template.loader import render_to_string
from django.forms.widgets import HiddenInput
from django.core import validators
from django.core.exceptions import ValidationError

from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from jsignature.settings import JSIGNATURE_DEFAULT_CONFIG

JSIGNATURE_EMPTY_VALUES = validators.EMPTY_VALUES + ('[]', )
import forms

class JSignatureWidget(HiddenInput):
    """
    A widget handling a signature capture field with with jSignature
    """

    # Actually, this widget has a display so we want it to behave like a
    # normal field, not a hidden one
    is_hidden = False
    is_readonly = None
    is_inline = None

    class Media:
        js = ('js/jSignature.min.js',
              'js/django_jsignature.js')

    def __init__(self, attrs=None, jsignature_attrs=None):
        super(JSignatureWidget, self).__init__(attrs)
        # Store jSignature js config
        self.jsignature_attrs = jsignature_attrs or {}

    def value_from_datadict(self, data, files, name):
        #print "value_from_datadict(name=%s, value=%s)" % (name, data.get(name))
        return forms.JSignature(data.get(name), data.get('native_' + name, None))

    def build_jsignature_config(self):
        """ Build javascript config for jSignature initialization.
            It's a dict with for which default values come from settings
            and can be overriden by jsignature_attrs, given at widget
            instanciation time """
        jsignature_config = JSIGNATURE_DEFAULT_CONFIG.copy()
        jsignature_config.update(self.jsignature_attrs)
        return jsignature_config

    def build_jsignature_id(self, name):
        """ Build HTML id for jsignature container.
            It's important because it's used in javascript code """
        return 'jsign_%s' % name

    def render(self, name, value, attrs=None):
        """ Render widget """
        
        #print "JSignatureWidget.render(value=%s, type=%s)" % (value, type(value))

        jsign_id = self.build_jsignature_id(name)
        jsignature_config = self.build_jsignature_config()
        
        #print "self.attrs: %s, attrs: %s" % (self.attrs, attrs)
        if self.is_readonly is None:
            self.is_readonly = self.attrs.pop('readonly', False) or self.attrs.pop('disabled', False) 
        if self.is_inline is None:
            self.is_inline = self.attrs.pop('inline', False)

        context = {
            'signature': value,
            'readonly': self.is_readonly,
            'hidden': super(JSignatureWidget, self).render(name, value, attrs),
            'native': super(JSignatureWidget, self).render(
                'native_' + name, value.native or '' if value else '', { 'id': attrs['id'].replace('id_', 'id_native_')}),
            'jsign_id': jsign_id,
            'reset_btn_text': _('Reset'),
            'ok_btn_text': _('Ok'),
            'config': jsignature_config,
            'js_config': mark_safe(json.dumps(jsignature_config)),
            'inline': 'inline' if self.is_inline else ''
        }
        
        return mark_safe(render_to_string('jsignature/widget.html', context))
