#!/bin/bash

export PYTHONPATH=.:./buscaminas_rest/
export FLASK_APP=buscaminas_rest
export FLASK_env=production
flask run --host=0.0.0.0 --port=5555

