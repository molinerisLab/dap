
SHELL=/bin/bash -eo pipefail

.DELETE_ON_ERROR:

.bmake/config.mk: config_bmake.mk ; @bmake-filter -o --ignore-global-rules  < $< > $@
-include .bmake/config.mk 
-include config.mk
#-include ignore che include if the file does not exists


.bmake/makefile: bmakefile ; @bmake-filter -o --ignore-global-rules  < $< > $@
-include .bmake/makefile
#-include ignore che include if the file does not exists


