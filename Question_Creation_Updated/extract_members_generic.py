import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import random
import os
import shutil

#global vars
propMapFile=""
stopListFile="stoplist.txt"
X=4
dataFolder=""
endpoint_url = "https://query.wikidata.org/sparql"
query_getelements = ""

#required  utils

def loadStopListProp(stopListFile):
    sl=set()
    with open(stopListFile, 'r') as f:
        for line in f:
            line=line.strip().strip('\n')
            sl.add(line)
    print("StopWord Property Loaded Successfully from ", stopListFile, " of size:", len(sl))
    #print(sl)
    return sl

def inStopList(stopWordSet, prop):
    if prop in stopWordSet:
        return True
    else:
        return False

def load_unamedprop(propMapFile):
    propDict={}
    with open(propMapFile, 'r') as f:
        for line in f:
            line=line.strip()
            tmp=line.split(',')
            if(len(tmp)<2):
                continue
            if(len(tmp)==X):
                continue
            propDict[tmp[0].strip()]=tmp[1].strip()
            #print(tmp[1])
    return propDict

def show(myList):
    for x in myList:
        print(x)

def folder_creation(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory Created Successfully: ",directory)
    else:
        print("Directory Already present: ",directory)

def extract_results(url,query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def main():
    if(len(sys.argv)<2):
        print("Number of argument required is 2. \nFormat: python3 <progname>.py <lang>")
        exit(1)
    LN = sys.argv[1]

    propMapFile = "map_proplist_"+LN+".txt"
    dataFolder="chem_folder_"+LN+"/"
    query_getelements = """SELECT ?item ?itemLabel 
    WHERE 
    {
    ?item wdt:P31 wd:Q11344.
    SERVICE wikibase:label { bd:serviceParam wikibase:language"""+ """\"[AUTO_LANGUAGE],"""+LN+"""\". }
    }"""

    print("Extraction program started . . .")
    folder_creation(dataFolder)
    propDict = load_unamedprop(propMapFile)
    all_elements=[]
    names=[]
    stopWordSet = loadStopListProp(stopListFile)

    results = extract_results(endpoint_url, query_getelements)
    for result in results["results"]["bindings"]:
        all_elements.append(result['item']['value'].split('/')[-1])
        names.append(result['itemLabel']['value'])
    #show(names)

    for i in range(len(all_elements)):
        query_getproperty = """SELECT ?wdLabel {
	    VALUES (?element) {(wd:"""+str(all_elements[i])+""")}
	    ?element ?p ?statement .
	    ?wd wikibase:claim ?p.
	    SERVICE wikibase:label { bd:serviceParam wikibase:language\"""" + LN +""" \"}
	    } ORDER BY ?wd ?statement ?ps_"""
        
        path=dataFolder+names[i]
        file=open(path,'w')
        propList = extract_results(endpoint_url, query_getproperty)
        for result in propList["results"]["bindings"]:
            if(inStopList(stopWordSet, result['wdLabel']['value'])):
                #print("Property Excluded: present in Stop Word Property - ", result['wdLabel']['value'])
                continue
            if result['wdLabel']['value'][0] != 'P':
                file.write(str(result['wdLabel']['value'])+'\n')
            if result['wdLabel']['value'][0] == 'P':
                oldprop = result['wdLabel']['value']
                newprop = ""
                if oldprop in propDict.keys():
                    newprop = propDict[oldprop.strip()]
                    newprop2 = newprop.split('(')[0]
                    file.write(str(newprop2)+'\n')
                    #print(" old prop: " + oldprop + " new prop: "+ newprop2)
    #print(propSet)

if __name__ == "__main__":
    main()
    print("Property Folder Creation Completed. Please Check: ",dataFolder)


