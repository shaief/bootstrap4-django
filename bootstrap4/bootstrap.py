# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from importlib import import_module

from django import VERSION as DJANGO_VERSION
from django.conf import settings

# Do we support set_required and set_disabled?
# See GitHub issues 337 and 345
# TODO: Get rid of this after support for Django 1.8 LTS ends
DBS3_SET_REQUIRED_SET_DISABLED = DJANGO_VERSION[0] < 2 and DJANGO_VERSION[1] < 10

# Default settings
BOOTSTRAP4_DEFAULTS = {
    'jquery_url': '//code.jquery.com/jquery-3.1.1.slim.min.js',
    'jquery_integrity': 'sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n',
    'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/',
    'css_url': None,
    'css_integrity': 'sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ',
    'theme_url': None,
    'javascript_url': None,
    'javascript_integrity': "sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn",
    'include_jquery': False,
    'horizontal_label_class': 'col-md-3',
    'horizontal_field_class': 'col-md-9',

    'set_placeholder': True,
    'required_css_class': '',
    'error_css_class': 'has-error',
    'success_css_class': 'has-success',
    'formset_renderers': {
        'default': 'bootstrap4.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'bootstrap4.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap4.renderers.FieldRenderer',
        'inline': 'bootstrap4.renderers.InlineFieldRenderer',
    },
}

if DBS3_SET_REQUIRED_SET_DISABLED:
    BOOTSTRAP4_DEFAULTS.update({
        'set_required': True,
        'set_disabled': False,
    })

# Start with a copy of default settings
BOOTSTRAP4 = BOOTSTRAP4_DEFAULTS.copy()

# Override with user settings from settings.py
BOOTSTRAP4.update(getattr(settings, 'BOOTSTRAP4', {}))


def get_bootstrap_setting(setting, default=None):
    """
    Read a setting
    """
    return BOOTSTRAP4.get(setting, default)


def bootstrap_url(postfix):
    """
    Prefix a relative url with the bootstrap base url
    """
    return get_bootstrap_setting('base_url') + postfix


def jquery_url():
    """
    Return the full url to jQuery file to use
    """
    return get_bootstrap_setting('jquery_url')

def jquery_integrity():
    """
    Return the full url to jQuery file to use
    """
    return get_bootstrap_setting('jquery_integrity')


def javascript_url():
    """
    Return the full url to the Bootstrap JavaScript file
    """
    return get_bootstrap_setting('javascript_url') or \
           bootstrap_url('js/bootstrap.min.js')


def javascript_url_integrity():
    """
    Return the full url integrity to the Bootstrap JavaScript file
    """
    return get_bootstrap_setting('javascript_integrity') or \
           BOOTSTRAP4_DEFAULTS['javascript_integrity']

def css_url():
    """
    Return the full url to the Bootstrap CSS file
    """
    return get_bootstrap_setting('css_url') or \
           bootstrap_url('css/bootstrap.min.css')

def css_url_integrity():
    """
    Return the full css integrity to the Bootstrap JavaScript file
    """
    return get_bootstrap_setting('css_integrity') or \
           BOOTSTRAP4_DEFAULTS['css_integrity']


def theme_url():
    """
    Return the full url to the theme CSS file
    """
    return get_bootstrap_setting('theme_url')


def get_renderer(renderers, **kwargs):
    layout = kwargs.get('layout', '')
    path = renderers.get(layout, renderers['default'])
    mod, cls = path.rsplit(".", 1)
    return getattr(import_module(mod), cls)


def get_formset_renderer(**kwargs):
    renderers = get_bootstrap_setting('formset_renderers')
    return get_renderer(renderers, **kwargs)


def get_form_renderer(**kwargs):
    renderers = get_bootstrap_setting('form_renderers')
    return get_renderer(renderers, **kwargs)


def get_field_renderer(**kwargs):
    renderers = get_bootstrap_setting('field_renderers')
    return get_renderer(renderers, **kwargs)
