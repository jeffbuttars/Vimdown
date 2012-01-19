#!/bin/bash

set -e

# source the settings and activate the virtualenv
THIS_DIR=$(readlink -f $(dirname $BASH_SOURCE))
. $THIS_DIR/../.settings.sh

buildenv

cd $TOP_DIR
if [[ ! -f requirements.txt ]]; then
	echo "generating requirements.txt..."
	pip freeze > requirements.txt
fi

echo "updating the packages listed in requirements.txt"
for pkg in $(cat requirements.txt)
do
	pkg=$(echo $pkg | awk -F '==' '{print $1}')
	echo $pkg
	pip install -U $pkg
done

cd -
