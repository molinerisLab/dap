#!/bin/bash

mkdir -p $PREFIX/bin/
cp dap.py $PREFIX/bin/dap
cp add_module.py $PREFIX/bin/add_module.py
cp clone_prj.py $PREFIX/bin/clone_prj.py
cp mkproj.py $PREFIX/bin/mkproj.py
cp convert_prj.py $PREFIX/bin/convert_prj.py
chmod +x $PREFIX/bin/

cp model/dapdefault.yml $PREFIX/bin/dapdefault.yml
cp model/.envrc  $PREFIX/bin/.envrc
cp model/.gitignore  $PREFIX/bin/.gitignore
cp model/Snakefile $PREFIX/bin/Snakefile
