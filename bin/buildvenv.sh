#!/bin/bash

# source the settings and activate the virtualenv
THIS_DIR=$(readlink -f $(dirname $BASH_SOURCE))
source $THIS_DIR/../.settings.sh

if [[ ! -f  "$TOP_DIR/$PROJ_NAME.pybundle" ]]; then
	$TOP_DIR/bin/bundle.sh
else
	buildenv
fi

vactivate
cd -
