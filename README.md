# dap
The tool provides three commands:
* dap create
* dap clone
* dap addmodule

Help is provided by this command:
`dap --help`

## dap create
dap create creates a new project in the current working directory; it initiates a git repository and creates a conda environment.
### commands
`dap create [--usesnakemake --usemake --usebmake] ProjectName ProjectVersion`
* ProjectName: the name of the project, which will correspond to the directory and the git repository created.
* ProjectVersion: initial version of the project; the directory dataset/{ProjectVersion} is created.
* [--usesnakemake --usemake --usebmake]: creates the project with templates for Snakemake, Makefile and BMake. Many templates can be specified at the same time. **If no template is specified, Snakemake is used by default**.
 
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

## dap addmodule
It imports an external project inside the current project as a module, cloning it from a remote repository. 
The module is added as an sub-module in git.
### commands
`dap addmodule RepoUrl ProjectVersion ModuleVersion`
* RepoUrl: URL of the remote repository.
* ProjectVersion: path to the directory containing the project's version where you want to import the module, relative to PRJ_ROOT. In most cases it's a path structured as **dataset/{ProjectVersion}**
* ModuleVersion: name of the module's version we want to import.

### Compliance of the project
The project to be imported as a module must be compliant with the structure of the projects created with **dap**. It must contain the directory *INNER_PRJ_ROOT/dataset/{ModuleVersion}*.

The command, for each symbolic link inside the directory *INNER_PRJ_ROOT/dataset/{ModuleVersion}* creates a symbolic link in the directory *PRJ_ROOT/{ProjectVersion}/{ModuleName}* pointing to the same file.
