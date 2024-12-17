#!/bin/bash

mkdir -p $PREFIX/bin/
cp dap.py $PREFIX/bin/dap
cp add_module.py $PREFIX/bin/add_module.py
cp clone_prj.py $PREFIX/bin/clone_prj.py
cp mkproj.py $PREFIX/bin/mkproj.py
chmod +x $PREFIX/bin/

cp model/dapdefault.yml $PREFIX/bin/dapdefault.yml
cp model/.envrc  $PREFIX/bin/.envrc
cp model/_footer.mk  $PREFIX/bin/_footer.mk
cp model/.gitignore  $PREFIX/bin/.gitignore
cp model/_header.mk  $PREFIX/bin/_header.mk
cp model/makefile  $PREFIX/bin/makefile
cp model/Snakefile $PREFIX/bin/Snakefile
