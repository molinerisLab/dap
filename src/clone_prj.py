import os
from sys import exit
from utils import run_command, prj_root_not_found

projBasePath = ''

def getRelativePath(path, fromPath):
    fromPath = os.path.split(fromPath)[0]
    return os.path.relpath(path, start=fromPath)

def makeLink(sourcePath, destinationPath):
    os.makedirs(os.path.dirname(destinationPath), exist_ok=True)
    os.symlink(getRelativePath(sourcePath, destinationPath), destinationPath)
    #Adds to git bypassing gitignore
    executionDir = os.getcwd()
    os.chdir(projBasePath)
    os.system("git add -f {}".format(destinationPath))
    os.chdir(executionDir)

def copyFile(sourcePath, destinationPath):
    with open(sourcePath, 'r') as source:
        with open(destinationPath,'w') as dest:
            for line in source:
                dest.write(line)
    #Adds to git bypassing gitignore
    executionDir = os.getcwd()
    os.chdir(projBasePath)
    os.system("git add {}".format(destinationPath))
    os.chdir(executionDir)


def makeLinks(currentVPath, newVPath, destinationVersion, sourceVersion, make_all_links, copyFiles=False):
    #Generate a list of sys links to copy
    links = []
    files = []
    for file in os.listdir(currentVPath):
        file_path = os.path.join(currentVPath, file)
        #If is a link:
        if (os.path.islink(file_path)):
            #If makeLinks is false, check if the file linked belongs to workflow/*
            if (make_all_links or (os.path.relpath(os.path.realpath(file_path),projBasePath)).startswith('workflow')):
                links.append(file_path)
        #If it's a directory, recursively calls makeLinks on it, to clone its content        
        elif (os.path.isdir(file_path)):
            os.makedirs(os.path.join(newVPath, file), exist_ok=True)
            makeLinks(file_path, os.path.join(newVPath, file), destinationVersion, sourceVersion, make_all_links, copyFiles)
        elif (copyFiles):
            files.append((file_path, os.path.join(newVPath, file)))
        elif (make_all_links):
            links.append(os.path.join(currentVPath, file))

    for file_path, new_path in files:
        run_command(currentVPath, f"cp {file_path} {new_path}")
        
    for link in links:
        realPath =  os.path.realpath(link)
        fileName = os.path.basename(realPath)
        n = os.path.splitext(fileName)

        version_suffix = os.path.relpath(currentVPath, os.path.join(projBasePath, 'results')).replace('/','_')
        #Files in workflow/modules belongs to a sub-module of the project and behaves differently (see later)
        belongs_to_module = (os.path.relpath(realPath,projBasePath)).startswith(os.path.join('workflow', 'modules'))

        #Files not in workflow/modules and that ends in _{old_version_suffix}
        #are cloned, with the new version in the filename
        #(i.e. workflow/../file_v1.txt  =>  workflow/../file_v2.txt)
        if ((not belongs_to_module) and n[0].endswith("_"+version_suffix)):
            new_version_suffix = os.path.relpath(newVPath, os.path.join(projBasePath, 'results')).replace('/','_')
            if (new_version_suffix.startswith("..") or new_version_suffix.startswith("_..")):
                #it's a test
                new_version_suffix = os.path.relpath(newVPath, os.path.join(projBasePath, 'tests')).replace('/','_')
            if (n[0].endswith(version_suffix)):
                newFilename = n[0][:-len(version_suffix)] + new_version_suffix + n[1]
            else:
                newFilename = n[0] + "_" + new_version_suffix + n[1]
            newFilePath = os.path.join(os.path.dirname(realPath), newFilename)
            copyFile(realPath, newFilePath)
            makeLink(newFilePath, os.path.join(newVPath, os.path.basename(link)))
        #Other files, included modules, are not copied, only linked in the new version
        else :
            makeLink(realPath, os.path.join(newVPath, os.path.basename(link)))


#The two versions must not be one a subdirectory of the other
def prevent_infinite_recursion(source_dir, destination_dir):
    common_path = os.path.commonpath([source_dir, destination_dir])
    if (common_path == source_dir):
        exit(f"Error - {destination_dir} is a subversion of {source_dir}. Cannot clone it.")
    if (common_path == destination_dir):
        exit(f"Error - {source_dir} is a subversion of {destination_dir}. Cannot clone it.")


def cloneVersion(sourceVersion, destinationVersion, linkAllData):
    global projBasePath
    projBasePath = os.getenv('PRJ_ROOT') 

    if (projBasePath == None or len(projBasePath)==0):
        prj_root_not_found()

    #Defines PATHS to current version and new version
    newVPath = os.path.join(projBasePath, "results", destinationVersion)
    currentVPath = os.path.join(projBasePath, "results", sourceVersion)

    #Check: cannot generate a version into a sub-directory or parent directory of the current version
    prevent_infinite_recursion(sourceVersion, destinationVersion)

    if (os.path.isdir(newVPath)):
        exit(f"Error - Version {newVPath} already exists")
    if (not os.path.isdir(projBasePath)):
        exit(f"Error - Could not find project directory {projBasePath}.")
    if (not (os.path.isdir(os.path.join(projBasePath, "results")) and os.path.isdir(os.path.join(projBasePath, "workflow")))):
        exit(f"Error - Project directory {projBasePath} does not contain results or workflow subfolders.")
    if (not os.path.isdir(currentVPath)):
        exit(f"Error - Could not find  current version path {currentVPath}")

    #Generate directory for new version if not existing
    os.makedirs(newVPath, exist_ok = True)
    #Generate system links
    makeLinks(currentVPath, newVPath, destinationVersion, sourceVersion, linkAllData)    
    executionDir = os.getcwd()
    os.chdir(projBasePath)
    os.system("git commit -m \"Version {} created\"".format(destinationVersion))
    os.chdir(executionDir)

#Checks if the directory contains links to things outside of project
#and if there are big files
def validate_version_for_test(path, projBasePath):
    bad_links = []
    files = []

    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if (os.path.islink(file_path)):
            if not (os.path.relpath(os.path.realpath(file_path),projBasePath)).startswith('workflow'):
                bad_links.append((file_path, os.path.realpath(file_path)))

        elif (os.path.isdir(file_path)):
            #recursion
            bad_links_, files_ = validate_version_for_test(file_path, projBasePath)
            bad_links += bad_links_; files += files_
        else:
            size = os.path.getsize(file_path)
            files.append((file_path, size / 1024))#kb

    return bad_links, files


def dap_prune(only_version, skip_confirmation=False):
    prj_root = os.getenv('PRJ_ROOT') 
    if (prj_root == None or len(prj_root)==0):
        prj_root_not_found()

    def get_all_workflow_version_files(directory_path, only_version):
        all_files = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                filename = os.path.basename(file)
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory_path)
                if (rel_path.startswith("env")):
                    continue
                #Remove format syntax
                
                if f"_{only_version}" in filename:
                    all_files.append(file_path)
        return all_files 
    
    to_delete = get_all_workflow_version_files(os.path.join(prj_root, "workflow"), only_version.replace("/","_"))
    if os.path.isdir(os.path.join(prj_root, "results", only_version)):
        to_delete.append(os.path.join(prj_root, "results", only_version))
    
    if (not skip_confirmation):
        if (len(to_delete)==0):
            print(">Nothing to remove")
            exit()
        print(f">DAP prune - the following files are going to be deleted:")
        for f in to_delete:
            print(f"\t- {f}")
        print(f">Do you want to proceed?")
        response = input("y/n ")
        if not(response.lower()=="y" or response.lower()=="yes"):
            exit(0)

    for f in to_delete:
        run_command(prj_root, f"rm -rf {f}")



def makeTest(sourceVersion, test_name):
    global projBasePath
    projBasePath = os.getenv('PRJ_ROOT') 

    if (projBasePath == None or len(projBasePath)==0):
        prj_root_not_found()

    #Defines PATHS to current version and new version
    newVPath = os.path.join(projBasePath, "tests", test_name)
    currentVPath = os.path.join(projBasePath, "results", sourceVersion)


    if (os.path.isdir(newVPath)):
        exit(f"Error - Test {newVPath} already exists")
    if (not os.path.isdir(projBasePath)):
        exit(f"Error - Could not find project directory {projBasePath}.")
    if (not (os.path.isdir(os.path.join(projBasePath, "results")) and os.path.isdir(os.path.join(projBasePath, "workflow")))):
        exit(f"Error - Project directory {projBasePath} does not contain results or workflow subfolders.")
    if (not os.path.isdir(currentVPath)):
        exit(f"Error - Could not find  version path {currentVPath}")

    bad_links, files = validate_version_for_test(currentVPath, projBasePath)
    if (len(bad_links)>0):
        for link_name, link_path in bad_links:
            print(f"Error: link {bad_links} refers to file {link_path}")
        exit("Symbolic links in tests must point to data in workflow. This is needed to guarantee the tests work in newly cloned repositories.")
    files = [f for f in files if f[1]>= 10*1024]
    if (len(files)>0):
        print("Some files are large:")
        for f, s in files:
            print(f"File {f}: {s} KB.")
        print("Input files for tests are added to the git repository. You might want to generate a test version with smaller files.")
        print("Do you want to proceed anyway?")
        response = input("y/n ")
        if not(response.lower()=="y" or response.lower()=="yes"):
            exit(0)

    #Generate directory for new version if not existing
    os.makedirs(newVPath, exist_ok = True)
    #Generate system links
    makeLinks(currentVPath, newVPath, test_name, sourceVersion, True, True)    

    #Ask user to delete the sourceVersion
    print(f"\n>Test {test_name} successfully created from template {sourceVersion}")
    print(f">Do you want to remove the template version {sourceVersion}?")
    print(f">Removing the template version results in the deletion of directory: {currentVPath} and all version-specific files in workflow/")
    response = input("y/n ")
    if not(response.lower()=="y" or response.lower()=="yes"):
        return 
    run_command(currentVPath, f"rm -rf {currentVPath}")
    dap_prune(sourceVersion, True)


def main():
    print("Clone prj")

if __name__ == '__main__':
	main()