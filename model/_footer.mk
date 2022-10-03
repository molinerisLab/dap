
.bmake/prj_rules.mk: prj_rules.mk ; @bmake-filter -o --ignore-global-rules  < $< > $@
-include .bmake/epigen/prj_rules.mk 
#-include ignore dhe include if the file does not exists