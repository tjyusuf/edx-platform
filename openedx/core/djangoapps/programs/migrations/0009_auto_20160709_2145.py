# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0008_programsapiconfig_program_details_enabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programsapiconfig',
            name='authoring_app_css_path',
        ),
        migrations.RemoveField(
            model_name='programsapiconfig',
            name='authoring_app_js_path',
        ),
    ]
