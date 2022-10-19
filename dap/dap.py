import typer
from typing import Optional
from .mkproj import createProject, updateProject
from .clone_prj import cloneVersion
from .add_module import add_module, add_module_no_symlink
app = typer.Typer()

#Opt per non creare env -> o no env o env 
#Derivare env da un altro env
#Create version

@app.command()
def create(
    projectname: str = typer.Argument(..., help="The name of the project to be created"),
           projectversion: str = typer.Argument(..., help="The current version of the project - es. V1"),
           usesnakemake: bool = False,
           usemake: bool = False, 
           usebmake: bool = False,
           source_environment: str = typer.Option(None, "--source_env", help="Optional: specify a conda env to clone")):
    if (not (usebmake or usemake)):
        usesnakemake = True
    createProject(projectname, projectversion, usesnakemake, usemake, usebmake, source_environment)

@app.command()
def update(
           projectversion: str = typer.Argument(..., help="The version of the project to be created or updated - es. V1"),
           usesnakemake: bool = False,
           usemake: bool = False, 
           usebmake: bool = False):
    if (not (usebmake or usemake)):
        usesnakemake = True
    updateProject(projectversion, usesnakemake, usemake, usebmake)

@app.command()
def clone(sourceversion: str = typer.Argument(..., help="Version of the project to be cloned"),
        newversion: str = typer.Argument(..., help="Version of the project to be generated")):
    cloneVersion(sourceversion, newversion)

#name: Optional[str] = typer.Argument(None)
@app.command()
def addmodule(repo_url: str = typer.Argument(..., help="URL to remote repository"),
        project_version: Optional[str] = typer.Argument(None, help="Version of the project where you want to include the module - relative to project root - es. dataset/V1"),
        module_version: Optional[str] = typer.Argument(None, help="Version of the module that you want to include - es. V1")):

        if (project_version is None or module_version is None):
            add_module_no_symlink(repo_url)
        else:
            add_module(repo_url, project_version, module_version)

def run_dap():
    app()

if __name__ == "__main__":
    app()
