# dap
The tool provides three commands:
* dap create
* dap clone

### Installation
* Install dependencies:
* * conda: https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html
* * direnv: `conda install -c conda-forge direnv`
* Get to dap base directory
* Run `pip install .`

Alternatively dap can be installed from Anaconda: https://anaconda.org/molinerislab/dap

### Help is provided by this command:
`dap --help`

## dap create
dap create creates a new project in the current working directory; it initiates a git repository and creates a conda environment.
### commands
`dap create [--usesnakemake --usemake --usebmake][--source_env=MyEnvironment] ProjectName ProjectVersion`
* ProjectName: the name of the project, which will correspond to the directory and the git repository created.
* ProjectVersion: initial version of the project; the directory dataset/{ProjectVersion} is created. ProjectVersion might specify subfolders to be put inside dataset; i.e. *humans/v1* will create the directory *dataset/humans/v1* and a version named *humans_v1*
* [--usesnakemake --usemake --usebmake]: creates the project with templates for Snakemake, Makefile and BMake. Many templates can be specified at the same time. **If no template is specified, Snakemake is used by default**.
* [--source_env=MyEnvironment]: optionally the user can specify an existing conda environment that is to be cloned when creating the project environment.
 
### Example of directory tree created with Snakemake template:
```
ProjectName
├── dataset
│   ├── V1
│   │   ├── Snakefile (symlink -->)
│   │   ├── config.yaml (symlink -->)
│   │   ├── Snakefile_versioned.sk (symlink -->)
├── local
│   ├── src
│   ├── bin
│   ├── env
│   ├── rules
│   │  ├── Snakefile
│   ├── config
│   │  ├── config_V1.mk
│   │  ├── Snakefile_versioned_V1.sk
│   ├── data
│   ├── modules
```

## dap update
dap update works similarly to dap create but, instead of creating the project from scratch, is to be executed inside the project directory and allows for the creation of new versions or the update of an existing version by adding different templates.
Two different use cases for dap update are:
* You want to add a different template to your project version - i.e. you may have created the project with the Snakefile template but want to add the Make template
* You want to create a new project version with empty version-specific rules.
**By running dap update, files already existing are never modified**

### commands
`dap update [--usesnakemake --usemake --usebmake] ProjectVersion`
* ProjectVersion: version of the project where the operation is to be applied; if the version does not exist, it is created.
* [--usesnakemake --usemake --usebmake]: adds the templates for Snakemake, Makefile and BMake. Many templates can be specified at the same time. **If no template is specified, Snakemake is used by default**.  **If one or more templates already exist, they are not changed**.


## dap clone
It creates a new version of the project, cloning an existing one.
It must be executed inside the project directory.
### commands
`dap clone SourceVersion NewVersion`
* SourceVersion: Name of the version to be cloned.
* NewVersion: Name of the new version.

The command creates a new directory  *PRJ_ROOT/dataset/{NewVersion}*. Here, for each link inside *PRJ_ROOT/dataset{SourceVersion}*:
* If the link refers to a non-version specific file: it copies the link.
* If the link refers to a version specific file: it creates a copy of the file and adds a link to the new one in the version directory.
**By convention, version specific files' names end with _{VersionName}.**

### Dap clone and sub-versions
SourceVersion and NewVersion might refer to subfolders inside the dataset/ directory, using the common '/' syntax. For example it's possible to have a version named *humans/v1*. In this case the following operations are allowed:
* dap clone humans/v1 humans/v2 --> simply clones the humans/v1 version into humans/v2.
* dap clone humans/v1 bald_monkeys/v1 --> clones the humans/v1 version into bald_monkeys/v1. If bald_monkey directory does not exist, it creates it.
* dap clone humans bald_monkeys --> clones the entire humans directory into the new directory. Any version inside the human directory will be cloned.
These operations are not allowed:
* dap clone humans humans/v3 --> cannot clone entire directory into a subdirectory of it.
* dap clone humans/v1 humans --> cannot clone directory into parent (or ancestor) directory.

## dap addmodule
**Currently not available**
It imports an external project inside the current project as a module, cloning it from a remote repository. 
The module is added as an sub-module in git.
### commands
`dap addmodule RepoUrl ProjectVersion ModuleVersion`
* RepoUrl: URL of the remote repository.
* ProjectVersion: path to the directory containing the project's version where you want to import the module, relative to PRJ_ROOT. In most cases it's a path structured as **dataset/{ProjectVersion}**
* ModuleVersion: name of the module's version we want to import.

ProjectVersion and ModuleVersion are optional. If not provided, dap will clone the project inside local/modules without creating version-specific symlinks.

### Compliance of the project
The project to be imported as a module must be compliant with the structure of the projects created with **dap**. It must contain the directory *INNER_PRJ_ROOT/dataset/{ModuleVersion}*.

The command, for each symbolic link inside the directory *INNER_PRJ_ROOT/dataset/{ModuleVersion}* creates a symbolic link in the directory *PRJ_ROOT/{ProjectVersion}/{ModuleName}* pointing to the same file.
