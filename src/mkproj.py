import os
from sys import exit
import subprocess
from utils import copy_file, getRelativePath, run_command, version_path_ok



def get_files(version_name):
    version_name = version_path_ok(version_name)
    base_directories = [
        'workspaces/', f'workspaces/{version_name}',
        'workflow/scripts', 'workflow/env', 'workflow/rules',
        'workflow/config/', 
    ]

    #Files to be copied in the project. Destination is relative to PRJ_PATH; source files must be inside the model folder.
    files_to_copy = [
            ['.gitignore', '.gitignore'],
            ['.envrc', '.envrc'],
            ['Snakefile','workflow/rules/Snakefile'],
    ]

    files_to_create = [
        'workflow/config/config_general.yaml',
        'workflow/config/config.smk',
        f'workflow/config/config_{version_name}.yaml',
        f'workflow/rules/Snakefile_versioned_{version_name}.sk'
    ]

    dest = f"workspaces/{version_name}"
    filesToLink = [
            ['workflow/rules/Snakefile', dest+'/Snakefile'],
            ['workflow/config/config_general.yaml', dest+'/config_general.yaml'],
            ['workflow/config/config.smk', dest+'/config.smk'],
            [f'workflow/config/config_{version_name}.yaml', dest+'/config.yaml'],
            [f'workflow/rules/Snakefile_versioned_{version_name}.sk',dest+'/Snakefile_versioned.sk']
    ]
    return base_directories, files_to_copy, files_to_create, filesToLink

def make_directory(base_path, path):
    os.makedirs(os.path.join(base_path, path), exist_ok = True)

def make_file(base_path, path, exist_ok=True):
    if (exist_ok and os.path.isfile(os.path.join(base_path, path))):
        return
    with open(os.path.join(base_path, path), 'w') as f:
        f.write(' ')


def make_link(base_path, source_path, destination_path):
    source_path = os.path.join(base_path, source_path)
    destination_path = os.path.join(base_path, destination_path)

    os.symlink(getRelativePath(source_path, destination_path), destination_path)
    #Aggiunge a git nonostante gitignore
    run_command(base_path, "git add -f {}".format(destination_path))



#Initialize global variables and launches execute()
def createProject(project_name, project_version, source_env, remote_repo):
    base_path = os.path.join(os.getcwd(), project_name)
    if (source_env is not None):
        source_env = os.path.abspath(source_env)
    
    #Makes project directory
    if (os.path.isdir(base_path)):
        exit(f"Error - Target project directory {base_path} already exists.")
    os.makedirs(base_path, exist_ok=False)
    #Set up Git repository
    run_command(base_path, "git init")
    if (remote_repo is not None):
        run_command(base_path, f"git remote add origin {remote_repo}")
    
    base_directories, files_to_copy, files_to_create, filesToLink = get_files(project_version)

    #Create directory structure
    for directory in base_directories:
        make_directory(base_path, directory)
    #Copy files from model
    for file in files_to_copy:
        destination = os.path.join(base_path, file[1])
        copy_file(os.path.join(os.path.dirname(os.path.realpath(__file__)) ,file[0]), destination, True)
    for file in files_to_create:
        make_file(base_path, file)
    for file in filesToLink:
        make_link(base_path, file[0], file[1])

    #Create conda environment
    has_mamba = (run_command(base_path, "which mamba"))==0
    if (has_mamba):
        conda_or_mamba = "mamba"
    else:
        conda_or_mamba = "conda"
    command = f"CONDA_BASE=$({conda_or_mamba} info --base) && source $CONDA_BASE/etc/profile.d/conda.sh && cd {base_path} && "
    
    if (source_env is not None):
        import re
        target_env = os.path.join(base_path, "workflow", "env", "env.yaml")
        copy_file(source_env, target_env)
        # Add dependencies for dap
        with open(target_env, 'r') as file:
            lines = file.readlines()
        lines_to_add = [
               "colorama\n",
               "dap\n",
               "direnv\n",
               "pip\n",
               "python\n",
               "typer\n"
        ]
        for i, line in enumerate(lines):
            #Read lines[i+1] and get how many spaces it uses
            if line.strip() == "dependencies:":
                match = re.match(r"([\s-]*)(?=\S)", lines[i+1])
                header = "  - "
                if match:
                    header = match.group(1)
                # Insert empty line after "dependencies:"
                for l in lines_to_add:
                    lines.insert(i + 1, header+l)
                break
        
        # Write the modified content back to the file
        with open(target_env, 'w') as file:
            file.writelines(lines)

        source_env = target_env

    if (source_env == None):
        source_env = os.path.join(os.path.dirname(os.path.realpath(__file__)) ,'dapdefault.yml')
        copy_file(source_env, os.path.join(base_path, "workflow", "env", "env.yaml"))
    

    command += f"""{conda_or_mamba} env create -f {source_env} -p  {os.path.join(base_path, "workflow", "env","env")}"""
    subprocess.run(command, shell=True, check=True, executable='/bin/bash')
    
    #Git - final commit
    run_command(base_path, """git add . && git commit -m "created new project" """)
    

    



def main():
    print('Use dap create --help')

if __name__ == '__main__':
	main()
