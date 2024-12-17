
SHELL=/bin/bash -eo pipefail

.DELETE_ON_ERROR:

-include config.mk
#-include ignore che include if the file does not exists


ifneq (,$(wildcard ./bmakefile))
.bmake/makefile: bmakefile
	@echo bmakefile uptate detected, compling.
	mkdir -p .bmake
	bmake-filter -o --ignore-global-rules $(PWD) < $< > $@
	@echo bmake compiling done
endif
include .bmake/makefile
#-include ignore the include if the file does not exists


