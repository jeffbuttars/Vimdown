#!/bin/bash

# source the settings and activate the virtualenv
THIS_DIR=$(readlink -f $(dirname $BASH_SOURCE))
. $THIS_DIR/../.settings.sh

buildenv
vactivate

cd $TOP_DIR

# if [[ ! -f "$TOP_DIR/requirements.txt" ]]; then
# 	echo "No requirements.txt file. I'm going to create one now..."
# 	pip freeze > requirements.txt
# fi

echo "creating new requirements.txt file"
pip freeze > requirements.txt
cat requirements.txt
pip bundle $PROJ_NAME.pybundle $(cat $TOP_DIR/requirements.txt)

cd -
