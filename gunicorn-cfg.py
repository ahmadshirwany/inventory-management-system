# -*- encoding: utf-8 -*-
"""
Gunicorn configuration for Inventory Management System.
"""

bind = '0.0.0.0:5005'
workers = 2
timeout = 60
accesslog = '-'
errorlog = '-'
loglevel = 'info'
capture_output = True
enable_stdio_inheritance = True
