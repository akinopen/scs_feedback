#!/bin/sh

gunicorn scs_feedback.wsgi -b 0.0.0.0:8000
