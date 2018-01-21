#!/bin/bash

pipenv run pycodestyle . && echo 'No PEP-8 violations found.'
