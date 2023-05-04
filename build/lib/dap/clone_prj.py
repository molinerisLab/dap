import os
from sys import exit

projBasePath = ''

def getRelativePath(path, fromPath):
    fromPath = os.path.split(fromPath)[0]
    return os.path.relpath(path, start=fromPath)

def makeLink(sourcePath, destinationPath):
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


def makeLinks(currentVPath, newVPath, destinationVersion, sourceVersion):
    links = []
    for link in os.listdir(currentVPath):
        link_ = os.path.join(currentVPath, link)
        if (os.path.islink(link_)):
            links.append(link_)
        elif (os.path.isdir(link_)):
            os.makedirs(os.path.join(newVPath, link) , exist_ok = True)
            makeLinks(link_, os.path.join(newVPath, link), destinationVersion, sourceVersion)
        
    for link in links:
        realPath =  os.path.realpath(link)
        fileName = os.path.basename(realPath)
        n = os.path.splitext(fileName)

        version_suffix = os.path.relpath(currentVPath, os.path.join(projBasePath, 'dataset')).replace('/','_')
        belongs_to_module = (os.path.relpath(realPath,projBasePath)).startswith(os.path.join('local', 'modules'))

        if ((not belongs_to_module) and n[0].endswith("_"+version_suffix)):
        
            new_version_suffix = os.path.relpath(newVPath, os.path.join(projBasePath, 'dataset')).replace('/','_')

            newFilename = n[0].removesuffix(version_suffix) + new_version_suffix + n[1]
            newFilePath = os.path.join(os.path.dirname(realPath), newFilename)
            copyFile(realPath, newFilePath)
            makeLink(newFilePath, os.path.join(newVPath, os.path.basename(link)))
        else :
            makeLink(realPath, os.path.join(newVPath, os.path.basename(link)))


#The two versions must not be one a subdirectory of the other
def prevent_infinite_recursion(source_dir, destination_dir):
    common_path = os.path.commonpath([source_dir, destination_dir])
    if (common_path == source_dir):
        exit(f"Error - {destination_dir} is a subversion of {source_dir}. Cannot clone it.")
    if (common_path == destination_dir):
        exit(f"Error - {source_dir} is a subversion of {destination_dir}. Cannot clone it.")


def cloneVersion(sourceVersion, destinationVersion):
    global projBasePath
    projBasePath = os.getenv('PRJ_ROOT') 

    if (projBasePath == None or len(projBasePath)==0):
        exit("Error - PRJ_ROOT is not defined. Make sure you are inside a project directory and direnv is active.")

    newVPath = os.path.join(projBasePath, "dataset", destinationVersion)
    currentVPath = os.path.join(projBasePath, "dataset", sourceVersion)

    prevent_infinite_recursion(sourceVersion, destinationVersion)
    if (os.path.isdir(newVPath)):
        exit(f"Error - Version {newVPath} already exists")
    if (not os.path.isdir(projBasePath)):
        exit(f"Error - Could not find project directory {projBasePath}.")
    if (not (os.path.isdir(os.path.join(projBasePath, "dataset")) and os.path.isdir(os.path.join(projBasePath, "local")))):
        exit(f"Error - Project directory {projBasePath} does not contain dataset or local subfolders.")
    if (not os.path.isdir(currentVPath)):
        exit(f"Error - Could not find  current version path {currentVPath}")


    os.makedirs(newVPath, exist_ok = True)
    makeLinks(currentVPath, newVPath, destinationVersion, sourceVersion)    
    executionDir = os.getcwd()
    os.chdir(projBasePath)
    os.system("git commit -m \"Version {} created\"".format(destinationVersion))
    os.chdir(executionDir)

def main():
    print("Clone prj")

if __name__ == '__main__':
	main()