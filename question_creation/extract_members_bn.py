import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import random
import os
import shutil

#global vars
propMapFile='map_proplist.txt'
X=4
dataFolder="chem_folder/"
endpoint_url = "https://query.wikidata.org/sparql"
query_getelements = """SELECT ?item ?itemLabel 
WHERE 
{
  ?item wdt:P31 wd:Q11344.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],hi". }
}"""

#required  utils

def load_unamedprop():
    propDict={}
    with open(propMapFile, 'r') as f:
        for line in f:
           #print(line)
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

def folder_creation():
	shutil.rmtree("chem_folder" )
	os.mkdir("chem_folder")

def extract_results(url,query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def main():
    print("Extraction program started . . .")
    folder_creation()
    propDict = load_unamedprop()
    print(propDict)
    #exit(1)
    all_elements=[]
    names=[]
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
	    SERVICE wikibase:label { bd:serviceParam wikibase:language "hi" }
	    } ORDER BY ?wd ?statement ?ps_"""
        
        path=dataFolder+names[i]
        file=open(path,'w')
        propList = extract_results(endpoint_url, query_getproperty)
        for result in propList["results"]["bindings"]:
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


