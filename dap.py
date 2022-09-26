import typer
from mkproj import createProject
from clone_prj import cloneVersion
from add_module import add_module
app = typer.Typer()




@app.command()
def create(projectname: str = typer.Argument(..., help="The name of the project to be created"),
           projectversion: str = typer.Argument(..., help="The current version of the project - es. V1"),
           usesnakemake: bool = True,
           usemake: bool = False, usebmake: bool = False):
    createProject(projectname, projectversion, usesnakemake, usemake, usebmake)

@app.command()
def clone(sourceversion: str = typer.Argument(..., help="Version of the project to be cloned"),
        newversion: str = typer.Argument(..., help="Version of the project to be generated")):
    cloneVersion(sourceversion, newversion)

@app.command()
def addmodule(repo_url: str = typer.Argument(..., help="URL to remote repository"),
        project_version: str = typer.Argument(..., help="Version of the project where you want to include the module - relative to project root - es. dataset/V1"),
        module_version: str = typer.Argument(..., help="Version of the module that you want to include - es. V1")):
	add_module(repo_url, project_version, module_version)

if __name__ == "__main__":
    app()
