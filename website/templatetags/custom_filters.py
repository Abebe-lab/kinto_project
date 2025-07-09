from django import template
import os

register = template.Library()

@register.filter
def basename(value):
    """Extracts just the filename from a full path"""
    return os.path.basename(value)