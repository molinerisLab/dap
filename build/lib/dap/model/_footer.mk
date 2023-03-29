
ifneq (,$(wildcard ./bmakefile_versioned.mk))
.bmake/makefile_versioned.mk: bmakefile_versioned.mk
	@echo bmakefile_versioned.mk uptate detected, compling.
	mkdir -p .bmake
	bmake-filter -o --ignore-global-rules $(PWD) < $< > $@
	@echo bmake compiling done
endif
-include .bmake/epigen/makefile_versioned.mk 
-include makefile_versioned.mk
#-include ignore the include if the file does not exists
