#!/bin/bash

mkdir -p $PREFIX/bin/
cp dap.py $PREFIX/bin/dap
cp clone_prj.py $PREFIX/bin/clone_prj.py
cp mkproj.py $PREFIX/bin/mkproj.py
cp convert_prj.py $PREFIX/bin/convert_prj.py
cp utils.py  $PREFIX/bin/utils.py
chmod +x $PREFIX/bin/
cp -r dap_model $PREFIX/bin/dap_model
