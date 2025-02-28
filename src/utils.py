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

def export_environment():
    import subprocess
    projBasePath = os.getenv('PRJ_ROOT')
    if (projBasePath == None or len(projBasePath)==0):
        prj_root_not_found()
    #Activate conda, enter PRJ_ROOT
    command = f"CONDA_BASE=$({conda_or_mamba} info --base) && source $CONDA_BASE/etc/profile.d/conda.sh && cd {PRJ_ROOT} && "
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
    with open(os.path.join(PRJ_ROOT, "workflow","env","env.yaml")) as f:
        old_yaml = f.read()
    if ("name" in old_yaml):
        name = old_yaml["name"]
    else:
        name = "env"
    channels = set()
    if ("channels" in new_yaml):
        for v in new_yaml["channels"]:
            channels.add(v)
    if ("channels" in old_yaml):
        for v in new_yaml["channels"]:
            channels.add(v)
    
    channels = set()
    if ("channels" in new_yaml):
        for v in new_yaml["channels"]:
            channels.add(v)
    if ("channels" in old_yaml):
        for v in new_yaml["channels"]:
            channels.add(v)
    dependencies = set()
    if ("dependencies" in new_yaml):
        for v in new_yaml["dependencies"]:
            dependencies.add(v)
    if ("dependencies" in old_yaml):
        for v in new_yaml["dependencies"]:
            dependencies.add(v)

    with open(os.path.join(PRJ_ROOT, "workflow","env","env.yaml"), "w") as f:
        f.write(f"name: {name}\n")
        f.write(f"channels:\n")
        for v in channels:
            f.write(f"  - {v}\n")
        f.write(f"dependencies:\n")
        for v in dependencies:
            f.write(f"  - {v}\n")
        if "prefix" in old_yaml:
            f.write(f"prefix: {old_yaml['prefix']}")