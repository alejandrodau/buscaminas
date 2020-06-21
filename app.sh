#!/bin/bash

export PYTHONPATH=.:./buscaminas_rest/
export FLASK_APP=buscaminas_rest/__init__.py
flask run
