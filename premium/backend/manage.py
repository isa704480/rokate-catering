#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    from django.core.management.commands.runserver import Command as _Runserver

    _Runserver.default_port = "8000"  # Premium Minimal: backend porti

    execute_from_command_line(sys.argv)
