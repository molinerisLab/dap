
#!/usr/bin/env python3
import os
import sys
from utils import *

def rename_directories(base_path):
    # 1. Rename PATH/dataset to PATH/results
    dataset_path = os.path.join(base_path, "dataset")
    results_path = os.path.join(base_path, "results")
    if os.path.exists(dataset_path):
        print(f"Renaming {dataset_path} to {results_path}")
        os.rename(dataset_path, results_path)
    else:
        print(f"Directory {dataset_path} does not exist.")

    if os.path.exists(os.path.join(base_path, "local")):
        run_command(base_path, f'mv {os.path.join(base_path, "local")} {os.path.join(base_path, "workflow")}')
    if os.path.exists(os.path.join(base_path, "workflow", "bin")):
        run_command(base_path, f'mv {os.path.join(base_path, "workflow", "bin")} {os.path.join(base_path, "workflow", "scripts")}')
    if os.path.exists(os.path.join(base_path, "workflow", "envs")):
        run_command(base_path, f'mv {os.path.join(base_path, "workflow", "envs")} {os.path.join(base_path, "workflow", "env")}')



def fix_symlinks(root_path):
    """
    Recursively traverse the given root_path.
    For each symbolic link, if its target contains 'dataset' or 'local',
    update the link so that 'dataset' becomes 'results' and 'local' becomes 'workflow'.
    """
    for dirpath, dirnames, filenames in os.walk(root_path, followlinks=False):
        for item in dirnames + filenames:
            full_path = os.path.join(dirpath, item)
            if os.path.islink(full_path):
                target = os.readlink(full_path)
                target_abs = os.path.abspath(os.path.join(full_path, target))
                target_abs = os.path.relpath(target_abs,root_path)
                if (target_abs.startswith("local")):
                    try:
                        new_target = target.replace("dataset", "results").replace("local/bin", "workflow/scripts").replace("local", "workflow")
                        if new_target != target:
                            os.remove(full_path)
                            os.symlink(new_target, full_path)
                            print(f"Updated symbolic link: {full_path} -> {new_target}")
                    except Exception as e:
                        print(f"Failed to update symlink {full_path}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python update_paths.py PATH")
        sys.exit(1)

    base_path = sys.argv[1]
    if not os.path.exists(base_path):
        print(f"Provided path {base_path} does not exist.")
        sys.exit(1)

    rename_directories(base_path)

    # Now fix symlinks under PATH/results
    results_dir = os.path.join(base_path, "results")
    if os.path.isdir(results_dir):
        print(f"Fixing symbolic links under {results_dir}")
        fix_symlinks(results_dir)
    else:
        print(f"Directory {results_dir} does not exist. Cannot fix symbolic links.")

if __name__ == "__main__":
    main()

def convertProject():
    base_path = os.getenv('PRJ_ROOT') 
    rename_directories(base_path)
    results_dir = os.path.join(base_path, "results")
    if os.path.isdir(results_dir):
        print(f"Fixing symbolic links under {results_dir}")
        fix_symlinks(results_dir)
    #Update envrc:
    with open(os.path.join(base_path, ".envrc"), "r") as f:
        lines = f.readlines()
    #fix path and fix conda activate
    lines = [l for l in lines if l.strip()!="PATH_add local/bin" and not l.strip().startswith("conda activate")]
    lines = lines + ["PATH_add workflow/scripts\n", 'conda activate workflow/env/env || echo "WARNING: Conda environment not loaded"\n'] 
    with open(os.path.join(base_path, ".envrc"), "w") as f:
        f.writelines(lines)
    
    #Update .gitignore
    with open(os.path.join(base_path, ".gitignore"), "a") as f:
        f.write("\nworkflow/env/env\nresults/*\n")