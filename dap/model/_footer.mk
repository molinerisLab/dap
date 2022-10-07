
.bmake/makefile_versioned.mk: bmakefile_versioned.mk ; @bmake-filter -o --ignore-global-rules  < $< > $@
-include .bmake/epigen/makefile_versioned.mk 
-include makefile_versioned.mk
#-include ignore dhe include if the file does not exists