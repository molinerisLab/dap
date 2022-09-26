import typer
from mkproj import createProject
from clone_prj import cloneVersion
from add_module import add_module
app = typer.Typer()




@app.command()
def create(projectname: str, projectversion: str, usesnakemake: bool = True,
            usemake: bool = False, usebmake: bool = False):
    createProject(projectname, projectversion, usesnakemake, usemake, usebmake)

@app.command()
def clone(sourceversion: str, newversion: str):
    cloneVersion(sourceversion, newversion)

@app.command()
def addmodule(project_root: str, repo_url: str, project_version, module_version):
	add_module(project_root, repo_url, project_version, module_version)

if __name__ == "__main__":
    app()
