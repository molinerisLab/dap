import os
from sys import exit
from utils import prj_root_not_found

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


def makeLinks(currentVPath, newVPath, destinationVersion, sourceVersion, make_all_links):
    #Generate a list of sys links to copy
    links = []
    for file in os.listdir(currentVPath):
        file_path = os.path.join(currentVPath, file)
        #If is a link:
        if (os.path.islink(file_path)):
            #If makeLinks is false, check if the file linked belongs to workflow/*
            if (make_all_links or (os.path.relpath(os.path.realpath(file_path),projBasePath)).startswith('workflow')):
                links.append(file_path)
        #If it's a directory, recursively calls makeLinks on it, to clone its content        
        elif (os.path.isdir(file_path)):
            makeLinks(file_path, os.path.join(newVPath, file), destinationVersion, sourceVersion,make_all_links)
        elif (make_all_links):
            links.append(os.path.join(currentVPath, file))

        
    for link in links:
        realPath =  os.path.realpath(link)
        fileName = os.path.basename(realPath)
        n = os.path.splitext(fileName)

        version_suffix = os.path.relpath(currentVPath, os.path.join(projBasePath, 'workspaces')).replace('/','_')
        #Files in workflow/modules belongs to a sub-module of the project and behaves differently (see later)
        belongs_to_module = (os.path.relpath(realPath,projBasePath)).startswith(os.path.join('workflow', 'modules'))

        #Files not in workflow/modules and that ends in _{old_version_suffix}
        #are cloned, with the new version in the filename
        #(i.e. workflow/../file_v1.txt  =>  workflow/../file_v2.txt)
        if ((not belongs_to_module) and n[0].endswith("_"+version_suffix)):
            new_version_suffix = os.path.relpath(newVPath, os.path.join(projBasePath, 'workspaces')).replace('/','_')
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
    newVPath = os.path.join(projBasePath, "workspaces", destinationVersion)
    currentVPath = os.path.join(projBasePath, "workspaces", sourceVersion)

    #Check: cannot generate a version into a sub-directory or parent directory of the current version
    prevent_infinite_recursion(sourceVersion, destinationVersion)

    if (os.path.isdir(newVPath)):
        exit(f"Error - Version {newVPath} already exists")
    if (not os.path.isdir(projBasePath)):
        exit(f"Error - Could not find project directory {projBasePath}.")
    if (not (os.path.isdir(os.path.join(projBasePath, "workspaces")) and os.path.isdir(os.path.join(projBasePath, "workflow")))):
        exit(f"Error - Project directory {projBasePath} does not contain workspaces or workflow subfolders.")
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

def main():
    print("Clone prj")

if __name__ == '__main__':
	main()