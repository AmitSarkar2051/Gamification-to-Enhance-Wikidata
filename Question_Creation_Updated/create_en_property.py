import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import random
import os
import shutil

#global vars
pFile="ALL_English_proplist.txt"
endpoint_url = "https://query.wikidata.org/sparql"
query_getelements = """SELECT ?item ?itemLabel 
WHERE 
{
  ?item wdt:P31 wd:Q11344.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}"""

#required  utils
def create_newAllPropFile(myList):
    print("Writing in the file:",pFile)
    print("Available Data size", len(myList))
    with open(pFile, 'w') as f:
        for item in myList:
            f.write("%s\n" % item)

def show(myList):
    for x in myList:
        print(x)

def extract_results(url,query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def main():
    print("English Create property-map program started . . .")
    all_elements=[]
    results = extract_results(endpoint_url, query_getelements)
    All_en_dict={}
    for result in results["results"]["bindings"]:
        all_elements.append(result['item']['value'].split('/')[-1])

    for i in range(len(all_elements)):
        query_getproperty = """SELECT ?wdLabel {
	    VALUES (?element) {(wd:"""+str(all_elements[i])+""")}
	    ?element ?p ?statement .
	    ?wd wikibase:claim ?p.
	    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
	    } ORDER BY ?wd ?statement ?ps_"""
        
        propList = extract_results(endpoint_url, query_getproperty)
        for result in propList["results"]["bindings"]:
            All_en_dict[result['wdLabel']['value']] = 1

    AllProSet =  list(All_en_dict.keys())
    print("IN ENGLISH Number of UNIQUE properties: ", len(AllProSet))
    create_newAllPropFile(AllProSet)
    print("Successfully Created Property File:", pFile)

if __name__ == "__main__":
    main()


