import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import random
import os
import shutil

#global vars
dataFolder="chem_folder/"
endpoint_url = "https://query.wikidata.org/sparql"
query_getelements = """SELECT ?item ?itemLabel 
WHERE 
{
  ?item wdt:P31 wd:Q11344.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],hi". }
}"""

#required  utils
def create_newPropFile(myList):
    with open('tmp_proplist.txt', 'w') as f:
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
    print("Create property-map program started . . .")
    all_elements=[]
    tmplist=[]
    results = extract_results(endpoint_url, query_getelements)
    for result in results["results"]["bindings"]:
        all_elements.append(result['item']['value'].split('/')[-1])

    for i in range(len(all_elements)):
        query_getproperty = """SELECT ?wdLabel {
	    VALUES (?element) {(wd:"""+str(all_elements[i])+""")}
	    ?element ?p ?statement .
	    ?wd wikibase:claim ?p.
	    SERVICE wikibase:label { bd:serviceParam wikibase:language "hi" }
	    } ORDER BY ?wd ?statement ?ps_"""
        
        propList = extract_results(endpoint_url, query_getproperty)
        for result in propList["results"]["bindings"]:
            if result['wdLabel']['value'][0] == 'P':
                tmplist.append(result['wdLabel']['value'])

    tmplist.sort()
    propSet=set(tmplist)
    print("Number of unnamed properties: ", len(propSet))
    create_newPropFile(propSet)
    print("Temp file generated for unnamed properties: "+"tmp_proplist.txt")
    #print(propSet)

if __name__ == "__main__":
    main()


