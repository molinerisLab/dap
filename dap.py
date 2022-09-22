import typer
from mkproj import createProject
app = typer.Typer()




@app.command()
def create(projectName: str, projectVersion: str, useSnakemake: bool = True,
            useMake: bool = False, useBMake: bool = False):
    createProject(projectName, projectVersion, useSnakemake, useMake, useBMake)



if __name__ == "__main__":
    app()