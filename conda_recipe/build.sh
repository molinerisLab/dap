#!/bin/bash

mkdir -p $PREFIX/bin/
cp dap.py $PREFIX/bin/dap
cp clone_prj.py $PREFIX/bin/clone_prj.py
cp mkproj.py $PREFIX/bin/mkproj.py
cp convert_prj.py $PREFIX/bin/convert_prj.py
cp utils.py  $PREFIX/bin/utils.py
chmod +x $PREFIX/bin/
cp dap_model/.gitignore $PREFIX/bin
cp dap_model/.envrc $PREFIX/bin
cp dap_model/Snakefile $PREFIX/bin
cp dap_model/config_general.yaml $PREFIX/bin
cp dap_model/config.yaml $PREFIX/bin
cp dap_model/readme.md $PREFIX/bin
cp dap_model/dapdefault.yml $PREFIX/bin
