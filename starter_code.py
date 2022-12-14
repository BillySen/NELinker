import gzip
from html_process import *
from entity_extract_nltk import *
from candidate_selector import *
from candidate_ranking import *

#KEYNAME = "WARC-TREC-ID"
KEYNAME = "WARC-Record-ID"

# The goal of this function process the webpage and returns a list of labels -> entity ID
def find_labels():

    print("--Start Html Processing--")
    warc_src = reading("")
    warc_json = json.dumps(warc_src)
    print("--Finish Html Processing--")
    print("--Start Entity Extracting--")
    entity_frame_uniqueName = entity_extract_nltk(warc_json)
    entity_frame_uniqueName.to_json('entities_removeDuplicates_sorted.json',orient='records')
    print("--Finish Entity Extracting--")
    print(entity_frame_uniqueName)
    print("--Start Candidate Selecting--")
    with open('entities_removeDuplicates_sorted.json') as f:
        entity_list = json.load(f)
        candidate_selector(entity_list)
    print("--Finish Candidate Selecting--")
    print("--Start Candidate Ranking--")
    ranking()
    print("--Finish Candidate Ranking--")






    # Problem 2: Let's assume that we found a way to retrieve the text from a webpage. How can we recognize the
    # entities in the text?

    # Problem 3: We now have to disambiguate the entities in the text. For instance, let's assugme that we identified
    # the entity "Michael Jordan". Which entity in Wikidata is the one that is referred to in the text?

    # To tackle this problem, you have access to two tools that can be useful. The first is a SPARQL engine (Trident)
    # with a local copy of Wikidata. The file "test_sparql.py" shows how you can execute SPARQL queries to retrieve
    # valuable knowledge. Please be aware that a SPARQL engine is not the best tool in case you want to lookup for
    # some strings. For this task, you can use elasticsearch, which is also installed in the docker image.
    # The file start_elasticsearch_server.sh will start the elasticsearch server while the file
    # test_elasticsearch_server.py shows how you can query the engine.

    # A simple implementation would be to first query elasticsearch to retrieve all the entities with a label
    # that is similar to the text found in the web page. Then, you can access the SPARQL engine to retrieve valuable
    # knowledge that can help you to disambiguate the entity. For instance, if you know that the webpage refers to persons
    # then you can query the knowledge base to filter out all the entities that are not persons...

    # Obviously, more sophisticated implementations that the one suggested above are more than welcome :-)


    # For now, we are cheating. We are going to returthe labels that we stored in sample-labels-cheat.txt
    # Instead of doing that, you should process the text to identify the entities. Your implementation should return
    # the discovered disambiguated entities with the same format so that I can check the performance of your program.
    # cheats = dict((line.split('\t', 2) for line in open('data/sample-labels-cheat.txt').read().splitlines()))
    # for label, wikidata_id in cheats.items():
    #     if key and (label in payload):
    #         yield key, label, wikidata_id


def split_records(stream):
    payload = ''
    for line in stream:
        if line.strip() == "WARC/1.0":
            yield payload
            payload = ''
        else:
            payload += line
    yield payload

if __name__ == '__main__':
    import sys
    try:
        _, INPUT = sys.argv
    except Exception as e:
        print('Usage: python starter-code.py INPUT')
        sys.exit(0)
    find_labels()
    # with gzip.open(INPUT, 'rt', errors='ignore') as fo:
    #     for record in split_records(fo):
    #         for key, label, wikidata_id in find_labels(record):
    #             print(key + '\t' + label + '\t' + wikidata_id)
