import shutil
import os


def copy_file(source_path, destination_path, exist_ok=False):
    if (os.path.isfile(destination_path) and exist_ok):
        return 
    shutil.copy2(source_path, destination_path)

def getRelativePath(path, fromPath):
    fromPath = os.path.split(fromPath)[0]
    return os.path.relpath(path, start=fromPath)

def run_command(path, command):
    return os.system(f"cd {path} && {command}")

def version_path_ok(version_name):
    return version_name.replace('/','_')

def prj_root_not_found():
    exit("Error - PRJ_ROOT is not defined.\nMake sure you are inside a project directory and direnv is active. Try running direnv allow.")

def build_environment():
    import subprocess
    projBasePath = os.getenv('PRJ_ROOT')
    if (projBasePath == None or len(projBasePath)==0):
        prj_root_not_found()
    has_mamba = (run_command(projBasePath, "which mamba"))==0
    if (has_mamba):
        conda_or_mamba = "mamba"
    else:
        conda_or_mamba = "conda"

    #Check if env.yaml exists
    if not os.path.isfile(os.path.join(projBasePath, "workflow","env","env.yaml")):
        exit("env.yaml file not found in workflow/env")

    #Check if env exists
    if os.path.isdir(os.path.join(projBasePath, "workflow","env","env")):
        print("Local environment already exists. Do you want to re-create it?")
        response = input("y/n ")
        if (response.lower()=="y" or response.lower()=="yes"):
            p = os.path.join(projBasePath, "workflow","env", "env")
            run_command(p, f"rm -rf {p}")
        else:
            exit(0)
    base_path = projBasePath
    command = f"CONDA_BASE=$({conda_or_mamba} info --base) && source $CONDA_BASE/etc/profile.d/conda.sh && cd {base_path} && "
    command += f"""{conda_or_mamba} env create -f {os.path.join(base_path, "workflow", "env","env.yaml")} -p  {os.path.join(base_path, "workflow", "env","env")}"""
    subprocess.run(command, shell=True, check=True, executable='/bin/bash')

def export_environment():
    import subprocess
    projBasePath = os.getenv('PRJ_ROOT')
    if (projBasePath == None or len(projBasePath)==0):
        prj_root_not_found()
    has_mamba = (run_command(projBasePath, "which mamba"))==0
    if (has_mamba):
        conda_or_mamba = "mamba"
    else:
        conda_or_mamba = "conda"
    #Activate conda, enter PRJ_ROOT
    command = f"CONDA_BASE=$({conda_or_mamba} info --base) && source $CONDA_BASE/etc/profile.d/conda.sh && cd {projBasePath} && "
    #activate conda environment - just to make sure you're not exporting some other environment
    command += "conda activate workflow/env/env &&"
    #export env
    command += "conda env export --from-history"
    #Run
    result = subprocess.run(command, shell=True, check=False, executable='/bin/bash', capture_output=True, text=True)
    if (result.returncode!=0):
        print(result.stdout)
        print(result.stderr)
        exit("DAP: Error exporting the environment")
    output = result.stdout

    #Parse output:
    #1-Read current env, keep its channels
    #2-Add dap basics if they are missing
    def parse_minimal_yaml(yaml_string):
        result = {}
        current_key = None
        lines = yaml_string.strip().split('\n')
        for line in lines:
            if not line.strip():
                continue  
            # Check indentation
            indent = len(line) - len(line.lstrip())
            stripped_line = line.strip()
            
            if indent == 0 and ':' in stripped_line:
                key, value = [part.strip() for part in stripped_line.split(':', 1)]
                current_key = key
                if value:
                    result[key] = value
                else:
                    result[key] = []
            
            elif indent > 0 and stripped_line.startswith('-') and current_key:
                if current_key in result and isinstance(result[current_key], list):
                    item = stripped_line[1:].strip()
                    result[current_key].append(item)
        return result
    new_yaml = parse_minimal_yaml(output)
    with open(os.path.join(projBasePath, "workflow","env","env.yaml")) as f:
        old_yaml = parse_minimal_yaml(f.read())
    if ("name" in old_yaml):
        name = old_yaml["name"]
    else:
        name = "env"
    channels = set()
    if ("channels" in new_yaml):
        for v in new_yaml["channels"]:
            channels.add(v)
    if ("channels" in old_yaml):
        for v in old_yaml["channels"]:
            channels.add(v)
    dependencies = set()
    if ("dependencies" in new_yaml):
        for v in new_yaml["dependencies"]:
            dependencies.add(v)
    if ("dependencies" in old_yaml):
        for v in old_yaml["dependencies"]:
            dependencies.add(v)

    with open(os.path.join(projBasePath, "workflow","env","env.yaml"), "w") as f:
        f.write(f"name: {name}\n")
        f.write(f"channels:\n")
        for v in channels:
            f.write(f"  - {v}\n")
        f.write(f"dependencies:\n")
        for v in dependencies:
            f.write(f"  - {v}\n")
        if "prefix" in old_yaml:
            f.write(f"prefix: {old_yaml['prefix']}")
    print("Environment exported")


def check_if_older_project():
    prj_root = os.getenv('PRJ_ROOT') 
    if (prj_root == None or len(prj_root)==0):
        return 
    if (
        not os.path.isdir(os.path.join(prj_root, "workflow")) and
        not os.path.isdir(os.path.join(prj_root, "results")) and 
        os.path.isdir(os.path.join(prj_root, "local")) and 
        os.path.isdir(os.path.join(prj_root, "dataset"))
    ):
        print(f"> It seems this project was created with an older version of DAP.")
        print("> Run 'dap convert' to convert this project to the new DAP version.")
        exit()