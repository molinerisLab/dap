#!/bin/bash

conda-build .
anaconda upload --user molinerislab $HOME/.conda/envs/mmasera_env/conda-bld/noarch/dap-0.6-py_0.tar.bz2

#conda convert --platform all $HOME/anaconda3/conda-bld/linux-64/dap-0.3-py_0.tar.bz2 -o outputdir/
#anaconda upload --user molinerislab outputdir/linux-32/dap-0.3-py_0.tar.bz2
#anaconda upload --user molinerislab outputdir/linux-32/dap-0.3-py_0.tar.bz2
#anaconda upload --user molinerislab outputdir/linux-aarch64/dap-0.3-py_0.tar.bz2
#anaconda upload --user molinerislab outputdir/linux-armv6l/dap-0.3-py_0.tar.bz2
#anaconda upload --user molinerislab outputdir/linux-armv7l/dap-0.3-py_0.tar.bz2
##anaconda upload --user molinerislab outputdir/linux-ppc64/dap-0.3-py_0.tar.bz2
#anaconda upload --user molinerislab outputdir/linux-ppc64le/dap-0.3-py_0.tar.bz2
#anaconda upload --user molinerislab outputdir/linux-s390x/dap-0.3-py_0.tar.bz2
#anaconda upload --user molinerislab outputdir/osx-64/dap-0.3-py_0.tar.bz2
#anaconda upload --user molinerislab outputdir/osx-arm64/dap-0.3-py_0.tar.bz2

