import typer
from mkproj import createProject
from clone_prj import cloneVersion
app = typer.Typer()




@app.command()
def create(projectName: str, projectVersion: str, useSnakemake: bool = True,
            useMake: bool = False, useBMake: bool = False):
    createProject(projectName, projectVersion, useSnakemake, useMake, useBMake)

@app.command()
def clone(sourceVersion: str, newVersion: str):
    cloneVersion(sourceVersion, newVersion)

if __name__ == "__main__":
    app()