#!/bin/bash

conda-build .
conda convert --platform all $HOME/anaconda3/conda-bld/linux-64/dap-0.2-py39_0.tar.bz2 -o outputdir/
anaconda upload --user molinerislab outputdir/linux-32/dap-0.2-py39_0.tar.bz2

anaconda upload --user molinerislab outputdir/linux-32/dap-0.2-py39_0.tar.bz2
anaconda upload --user molinerislab outputdir/linux-aarch64/dap-0.2-py39_0.tar.bz2
anaconda upload --user molinerislab outputdir/linux-armv6l/dap-0.2-py39_0.tar.bz2
anaconda upload --user molinerislab outputdir/linux-armv7l/dap-0.2-py39_0.tar.bz2
anaconda upload --user molinerislab outputdir/linux-ppc64/dap-0.2-py39_0.tar.bz2
anaconda upload --user molinerislab outputdir/linux-ppc64le/dap-0.2-py39_0.tar.bz2
anaconda upload --user molinerislab outputdir/linux-s390x/dap-0.2-py39_0.tar.bz2
anaconda upload --user molinerislab outputdir/osx-64/dap-0.2-py39_0.tar.bz2
anaconda upload --user molinerislab outputdir/osx-arm64/dap-0.2-py39_0.tar.bz2

