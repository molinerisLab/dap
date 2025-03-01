#!/usr/bin/env python3

import sys
import os
script_dir = os.path.dirname(os.path.realpath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
import typer
from typing import Optional
from typing_extensions import Annotated
from mkproj import createProject
from clone_prj import cloneVersion, makeTest, prune
from convert_prj import convertProject
from utils import export_environment, build_environment

app = typer.Typer()

def hello(extra=""):
    intro = """

      _______    ______   _______  
      |       \\  /      \\ |       \\
      | ▒▒▒▒▒▒▒\\|  ▒▒▒▒▒▒\\| ▒▒▒▒▒▒▒\\
      | ▒▒  | ▒▒| ▒▒__| ▒▒| ▒▒__/ ▒▒      
      | ▒▒  | ▒▒| ▒▒    ▒▒| ▒▒    ▒▒
      | ▒▒  | ▒▒| ▒▒▒▒▒▒▒▒| ▒▒▒▒▒▒▒ 
      | ▒▒__/ ▒▒| ▒▒  | ▒▒| ▒▒      
      | ▒▒    ▒▒| ▒▒  | ▒▒| ▒▒      
       \\▒▒▒▒▒▒▒  \\▒▒   \\▒▒ \\▒▒      
____________________________________________
::::::Data Analysis Project Management::::::

    """
    print(intro)
    print(extra)

@app.command()
def create(
    projectname: str = typer.Argument(..., help="The name of the project"),
           projectversion: str = typer.Argument(..., help="The base version of the project - es. V1"),
           remote_git_repo: str = typer.Option(None, "--remote_repo", help="Optional: specifiy a remote git repo URL and initialize the project inside it"),
           source_environment: str = typer.Option(None, "--source_env", help="Optional: specify a conda yaml file to populate the project environment - the environment will be cloned")):
    """
    Create a new dap project.
    """
    hello(f">Creating a new DAP project - {projectname}.\n")
    createProject(projectname, projectversion, source_environment, remote_git_repo)


@app.command()
def clone(sourceversion: str = typer.Argument(..., help="Version of the project to be cloned"),
        newversion: str = typer.Argument(..., help="Version of the project to be generated"),
        link_All_Data: bool = False):
    """
    Create a new version of the project by cloning an existing one.
    """
    hello(f">Cloning version {sourceversion} into {newversion}.\n")
    cloneVersion(sourceversion, newversion, link_All_Data)

@app.command()
def make_test(templateVersion: str = typer.Argument(..., help="Version of the project to be used as test template"),
        test_name: str = typer.Argument(..., help="Name of the test")):
    """
    Create a test using a version as a template. Files inside the template version will be copied and added to git - it is recommended to create tests with minimal input data.
    """
    hello(f">Creating test {test_name} from template {templateVersion}.\n")
    makeTest(templateVersion, test_name)

@app.command()
def convert():
    """
    Convert old dap project into new structure.
    """
    hello(">Converting project from old DAP version.\n")
    convertProject()

@app.command()
def export_env():
    """
    Update the project environment .yaml file. Useful if new packages are installed.
    """
    hello(">Updating project environment .yaml file.\n")
    export_environment()

@app.command()
def build_env():
    """
    Build the project conda environment from the env.yaml file. Useful if the project has just been cloned from a git repository.
    """
    hello("Build project environment.\n")
    build_environment()

@app.command()
def prune():
    """
    Clean workflow directories, remove files connected to versions no longer existing.
    """
    hello("Cleaning workflow directories.\n")
    prune()

def run_dap():
    app()

if __name__ == "__main__":
    app()
