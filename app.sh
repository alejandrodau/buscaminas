#!/bin/bash

export PYTHONPATH=.:./buscaminas_rest/
export FLASK_APP=buscaminas_rest
export FLASK_env=development

flask run
