from django.conf import settings
from django.urls.converters import SlugConverter, register_converter

if 'allow_unicode' in settings.FAQ_SETTINGS:
    class UnicodeSlugConverter(SlugConverter):
        regex = '[0-9\w_-]+'


    register_converter(UnicodeSlugConverter, 'uslug')

else:
    register_converter(SlugConverter, 'uslug')
