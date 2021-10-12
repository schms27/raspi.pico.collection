import os
print(os.listdir())

deleteMain = True
deleteLibraries = False
deleteProjectFile = False
deleteEverythingElse = True

def removeFromArrayIfExists(array, element):
    try:
        array.remove(element)
    except ValueError:
        pass  # do nothing!


def rm(d):  # Remove file or tree
    try:
        if os.stat(d)[0] & 0x4000:  # Dir
            for f in os.ilistdir(d):
                if f[0] not in ('.', '..'):
                    rm("/".join((d, f[0])))  # File or Dir
            os.rmdir(d)
        else:  # File
            os.remove(d)
    except:
        print("rm of '%s' failed" % d)


if deleteMain:
    try:
        os.remove('main.py')
    except OSError:
        pass

if deleteLibraries:
    dir = 'lib'
    for f in os.listdir(dir):
        os.remove("{0}/{1}".format(dir,f))
        
if deleteProjectFile:
    try:
        os.remove('project.pico-go')
    except OSError:
        pass

if deleteEverythingElse:
    libdir = 'lib'
    itemsToRemove = os.listdir()
    removeFromArrayIfExists(itemsToRemove, libdir)
    
    if not deleteMain:
        removeFromArrayIfExists(itemsToRemove, 'main.py')
    if not deleteProjectFile:
        removeFromArrayIfExists(itemsToRemove, 'project.pico-go')
    if deleteLibraries:
        for f in os.listdir(libdir): 
            itemsToRemove.append("{0}/{1}".format(libdir,f))
    
    print("Items to remove: {0}".format(itemsToRemove))
    for f in itemsToRemove:     
        try:
            rm(f)
        except OSError as e:
            print("Error occured while removing items: {0}".format(e))
            pass
        

        
    
