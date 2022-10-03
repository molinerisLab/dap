
.bmake/config.mk: config_bmake.mk ; @bmake-filter -o --ignore-global-rules  < $< > $@
-include .bmake//config.mk 
#-include ignore che include if the file does not exists


.bmake/makefile: bmakefile ; @bmake-filter -o --ignore-global-rules  < $< > $@
-include .bmake/bmakefile.mk 
#-include ignore che include if the file does not exists


SHELL=/bin/bash -eo pipefail