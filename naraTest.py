import requests
import os
from bs4 import BeautifulSoup
import wget
import re


# To-do: rename images, pack .exe, check how wget works with .exe


# 0 - node, 1 - image, 2 - dead end
def typeChecker(naID):
    jsonCheck = requests.get('https://catalog.archives.gov/OpaAPI/iapi/v1/id/%d?searchTerm=' % int(naID)).json()
    bsObj = BeautifulSoup(jsonCheck["opaResponse"]["content"]["description"], features="html.parser")
    if bsObj.find(class_='btn btn-primary details'):
        return 0
    if jsonCheck['opaResponse']['content']['objects'] is not None:
        return 1
    return 2


# main function, chooses a procession method based on type of page based on naID
def processID(naID, spread, level=6, path=os.getcwd()):
    nodeType = typeChecker(naID)
    if nodeType == 0:
        generateDir(naID, spread, path, level - 1)
    elif nodeType == 1:
        downloadImage(naID)
    else:
        generateDeadEnd(naID)


# generates directory for nodes
def generateDir(naID, spread, path=os.getcwd(), level=5):
    template = 'https://catalog.archives.gov/OpaAPI/iapi/v1'
    payload = {'action': 'searchWithin',
               'f.ancestorNaIds': naID,
               'facet': 'true',
               'facet.fields': 'oldScope,level,materialsType,fileFormat,locationIds,ancestorNaIds,dateRangeFacet',
               'highlight': 'true',
               'offset': 0,
               'q': "*:*",
               'rows': spread,
               'sort': 'naIdSort asc',
               'tabType': 'all'}
    getJson = requests.get(template, params=payload).json()
    # get name for directory
    pathNew = os.path.join(path, '%d %s' % (naID, getJson['opaResponse']['searchWithin'][0]['title']))
    try:
        os.mkdir(pathNew)
    except OSError:
        raise NameError('Wrong Directory')
    else:
        if level == 0:
            return
        else:
            os.chdir(pathNew)
            toProcess = getJson['opaResponse']['results']['result']
            # processing each child of current node
            for i in toProcess:
                processID(int(i['naId']), level - 1, spread, pathNew)
    os.chdir(path)
    return


# generates text file for dead ends
def generateDeadEnd(naID):
    base = 'https://catalog.archives.gov/OpaAPI/iapi/v1/id/%d?searchTerm=' % naID
    jsonFile = requests.get(base).json()
    with open(jsonFile['opaResponse']['@title'] + '.txt', 'w') as file:
        file.write('No images or nodes found for %d' % naID)
    return


# to-do: implement renaming of images
# downloads image in current node's directory
def downloadImage(naID):
    template = 'https://catalog.archives.gov/OpaAPI/iapi/v1/id/%d?searchTerm=' % naID
    toDownload = requests.get(template).json()
    # different cases for pdf/jpg and jpg-only architectures
    try:
        address = toDownload['opaResponse']['content']['objects']['objects']['object'][0]['file']['@url']
        name = toDownload['opaResponse']['@title'].replace(' ', '_')
        name = re.sub(r'\W+', '', name)
        image = wget.download(address, str(naID) + '.jpg')
    except KeyError:
        address = toDownload['opaResponse']['content']['objects']['objects']['object']['file']['@url']
        name = toDownload['opaResponse']['@title'].replace(' ', '_')
        name = re.sub(r'\W+', '', name)
        image = wget.download(address, str(naID) + '.jpg')
    with open(str(naID) + ' ' + name + '.txt', 'w') as file:
        file.write('Image for %s downloaded as %d.jpg' % (name, naID))
    return


if __name__ == "__main__":
    processID(naID=int(input('Input start ID: ')), spread=int(input('Input node spread: ')))
