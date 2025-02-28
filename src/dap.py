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
from clone_prj import cloneVersion
from convert_prj import convertProject

app = typer.Typer()

def hello(extra=""):
    intro = """

      _______    ______   _______  
      |       \  /      \ |       \ 
      | ▒▒▒▒▒▒▒\|  ▒▒▒▒▒▒\| ▒▒▒▒▒▒▒\
      | ▒▒  | ▒▒| ▒▒__| ▒▒| ▒▒__/ ▒▒      
      | ▒▒  | ▒▒| ▒▒    ▒▒| ▒▒    ▒▒
      | ▒▒  | ▒▒| ▒▒▒▒▒▒▒▒| ▒▒▒▒▒▒▒ 
      | ▒▒__/ ▒▒| ▒▒  | ▒▒| ▒▒      
      | ▒▒    ▒▒| ▒▒  | ▒▒| ▒▒      
       \▒▒▒▒▒▒▒  \▒▒   \▒▒ \▒▒      
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
    hello(f"\t>Creating a new DAP project - {projectname}.")
    createProject(projectname, projectversion, source_environment, remote_git_repo)


@app.command()
def clone(sourceversion: str = typer.Argument(..., help="Version of the project to be cloned"),
        newversion: str = typer.Argument(..., help="Version of the project to be generated"),
        link_All_Data: Annotated[bool, typer.Option(help="Copy symbolic links to data outside of the project's workflow too")] = False,):
    """
    Create a new version of the project by cloning an existing one.
    """
    hello(f"\t>Cloning version {sourceversion} into {newversion}.")
    cloneVersion(sourceversion, newversion, link_All_Data)

@app.command()
def convert():
    """
    Convert old dap project into new structure.
    """
    hello("\t>Converting project from old DAP version.")
    convertProject()

@app.command()
def export_env():
    """
    Update the project environment .yaml file. Useful if new packages are installed.
    """
    hello("\t>Updating project environment .yaml file.")
    pass

def run_dap():
    app()

if __name__ == "__main__":
    app()
