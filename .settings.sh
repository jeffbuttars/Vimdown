#!/bin/bash

TOP_DIR=$(readlink -f $(dirname $BASH_SOURCE))

# Poject name
PROJ_NAME='vimdown'
PROJ_VER='1.0.0'
# Name of the virtualenv
VENV_NAME='.venv'

function vactivate() 
{
	echo "Activating virtualenv $VENV_NAME"
	cd $TOP_DIR
	. "$VENV_NAME/bin/activate"
	cd -
} #vactivate()

function buildenv() 
{
	echo "Building and Activating virtualenv $VENV_NAME, then starting the Django project."

	oldir=$PWD
	cd $TOP_DIR

	if [[ ! -d "$VENV_NAME" ]]; then
		# Install a virutalvenv
		test -d "$VENV_NAME" || virtualenv $VENV_OPTIONS $VENV_NAME;

		# If there are requirements, install them.
		if [[ -f "./requirements.txt" ]]; then
			vactivate
			if [[ -f "$PROJ_NAME.pybundle"  ]]; then
				pip install "$PROJ_NAME.pybundle"
			fi
			pip install $(cat ./requirements.txt)
		fi
	fi

	cd $oldir 
} #buildenv()

