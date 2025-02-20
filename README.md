# DAP

DAP (Data Analisys Project) is a template and a project management tool, suited for bioinformatics or data anaysis project in general.

DAP encapsulates some conventions on how to organize projects and offers tools to manage them.

DAP conventions aim to:
* Facilitate project versioning
   * Creation, editing of versions, isolation of version-specific logic and configuration.
* Push toward sustainable use of conda environments.
   * one project <--> one conda environment
   * environment stored locally inside the project tree.
   * environment automatically activated upon user entering the project directory.

# Usage
## Installation

Linux and Mac OSX are supported.

Python >= 3 required.

### Install dap with conda

Dap can be installed from Anaconda: https://anaconda.org/molinerislab/dap with the following command

```
conda install -c molinerislab dap
```

we advise to install it in the `base` environment or in a specific one. This environment will be needed to create new projects.

## The DAP tree
The directory structure of a DAP project is made of two main components in its root:
* The **Workflow** directory, containing the entire project's logic and configuration, both global and version-specific.
   * The Workflow directory is **not** where the user stores the input files, results and it's not where the user works.
* The **Workspaces** directory is where versions are kept and where the user running the workflow works. 

![alt text](.img/dap_tree_workflow.png)
![alt text](.img/dap_tree_workspaces.png)

The **workflow** directory has sub-directories for the configuration files, environment, rules and scripts.

The **workspaces** directory has sub-directories for all the versions created. Inside each version:
* **Snakefile** is a symbolic link to *workflows/rules/Snakefile*
* **Snakefile_versioned.sk**  is a symbolic link to *workflows/rules/Snakefile_versioned_{VERSION_NAME}*
* **config_global.yaml** is a symbolic link to *workflows/config/config_global.yaml*
* **config.yaml** is a symbolic link to *workflows/config/config_{VERSION_NAME}.yaml*.


Basically, for rules and configuration, the user finds both global and version-specific files inside its version's directory. These files are links to files stored in the **workflow** directory, and the original files are managed by DAP.

Version-specific rules and configurations always override global ones.

## Create a new project
The command `dap create` creates a new project in the current working directory; it initiates a git repository and creates a conda environment.

```dap create [--source_env=MyEnvironment.yaml] [--remote-git-repo=https://..] ProjectName ProjectVersion```

* **ProjectName**: the name of the project, which will correspond to the directory and the git repository created.
* **ProjectVersion**: initial version of the project; the directory dataset/{ProjectVersion} is created. ProjectVersion might specify subfolders to be put inside dataset; i.e. *humans/v1* will create the directory *dataset/humans/v1* and a version named *humans_v1*
* [--source_env=MyEnvironment]: optionally the user can specify the yaml of an existing conda environment that will be cloned. If not specified, a new, empty project environment will be created.
* [--remote-git-repo=https://..]: optionally the user can connect the newly created git repository to a remote one.

## Work inside a project
Once the project is created with `dap create`, it is already set up with a git repository and a *.gitignore* file, a conda environment and a *direnv* file that automatize some bash context set-up.

Upon first entering the project directory, the user needs to authorize direnv with `direnv allow`. Once direnv is authorized, the conda environment and some environmental variables will be automatically set up upon entering the project. This includes:
* **PRJ_ROOT** will point to the root of the project.
* **The system PATH** will include *PRJ_ROOT/workflow/scripts*.

The user can work in its current version in *workspaces/version_name*, modify and run the Snakefile.

## Create new version
`dap clone` clones a project's version creating a new one. It needs to be executed inside the project directory.

`dap clone SourceVersion NewVersion`
* SourceVersion: Name of the version to be cloned.
* NewVersion: Name of the new version.

The command creates a new directory  *worspaces/{NewVersion}*. Here, for each link inside *worspaces/{OldVersion}*:
* If the link refers to a non-version specific file: the link is copied, the original file is not changed.
* If the link refers to a version specific file: the version-specific file is copied, with updated name, and a link to the new file is created.
**By convention, version specific files' names end with _{VersionName}.**

### Dap clone and sub-versions
SourceVersion and NewVersion might refer to subfolders inside the dataset/ directory, using the common '/' syntax. For example it's possible to have a version named *humans/v1*. In this case the following operations are allowed:
* dap clone humans/v1 humans/v2 --> simply clones the humans/v1 version into humans/v2.
* dap clone humans/v1 bald_monkeys/v1 --> clones the humans/v1 version into bald_monkeys/v1. If bald_monkey directory does not exist, it creates it.
* dap clone humans bald_monkeys --> clones the entire humans directory into the new directory. Any version inside the human directory will be cloned.
These operations are not allowed:
* dap clone humans humans/v3 --> cannot clone entire directory into a subdirectory of it.
* dap clone humans/v1 humans --> cannot clone directory into parent (or ancestor) directory.



