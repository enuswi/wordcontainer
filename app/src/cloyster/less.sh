#!/bin/bash

if test -e static/less/layout.less; then
    lessc static/less/layout.less static/css/layout.css
    echo 'Success Compile LESS!'
else
    echo 'Not Success Compile LESS.'
fi