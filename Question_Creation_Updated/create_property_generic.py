import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import random
import os
import shutil

#global vars
pFile=""
endpoint_url = "https://query.wikidata.org/sparql"
query_getelements = ""

#required  utils
def create_newAllPropFile(myList,pFile):
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
    if(len(sys.argv)<2):
        print("Number of argument required is 2. \nFormat: python3 <progname>.py <lang>")
        exit(1)
    LN = sys.argv[1]
    pFile = "ALL_"+LN+"_proplist.txt"

    query_getelements = """SELECT ?item ?itemLabel 
    WHERE 
    {
    ?item wdt:P31 wd:Q11344.
    SERVICE wikibase:label { bd:serviceParam wikibase:language"""+ """\"[AUTO_LANGUAGE],"""+LN+"""\". }
    }"""
    #print("Query to be fired: ", query_getelements)
    print("Create property-map program started for lang :", LN)
    all_elements=[]
    results = extract_results(endpoint_url, query_getelements)
    All_hn_dict={}
    for result in results["results"]["bindings"]:
        all_elements.append(result['item']['value'].split('/')[-1])

    for i in range(len(all_elements)):
        query_getproperty = """SELECT ?wdLabel {
	    VALUES (?element) {(wd:"""+str(all_elements[i])+""")}
	    ?element ?p ?statement .
	    ?wd wikibase:claim ?p.
	    SERVICE wikibase:label { bd:serviceParam wikibase:language \"""" + LN +""" \"}
	    } ORDER BY ?wd ?statement ?ps_"""
        #print("Elements Query to be fired: ", query_getproperty)
        propList = extract_results(endpoint_url, query_getproperty)
        for result in propList["results"]["bindings"]:
            All_hn_dict[result['wdLabel']['value']] = 1

    AllProSet =  list(All_hn_dict.keys())
    print("IN Number of UNIQUE properties in lang code - ",LN," : " , len(AllProSet))
    create_newAllPropFile(AllProSet,pFile)
    print("Successfully Created Property File:", pFile)

if __name__ == "__main__":
    main()


