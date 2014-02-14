#!/bin/bash

pkill -f 'pyhueapi/presets'
Returned=$?
if [ $Returned -eq 0 ]; then
	echo "OK"
else:
	echo "FAIL"
fi