import typer
from mkproj import createProject
from clone_prj import cloneVersion
app = typer.Typer()




@app.command()
def create(projectname: str, projectversion: str, usesnakemake: bool = True,
            usemake: bool = False, usebmake: bool = False):
    createProject(projectname, projectversion, usesnakemake, usemake, usebmake)

@app.command()
def clone(sourceversion: str, newversion: str):
    cloneVersion(sourceversion, newversion)

if __name__ == "__main__":
    app()
