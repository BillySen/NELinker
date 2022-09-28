import requests
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import time
from timeit import default_timer as timer
from multiprocessing import Pool, cpu_count


def search(query):
    e = Elasticsearch()
    p = {"query": {"query_string": {"query": query}}}
    response = e.search(index="wikidata_en", body=json.dumps(p))
    id_labels = {}
    if response:
        for hit in response['hits']['hits']:
            label = hit['_source']['schema_name']
            id = hit['_id']
            id_labels.setdefault(id, set()).add(label)
    return id_labels


def search_rank(query):
    print(query)
    time.sleep(3)
    e = Elasticsearch()
    try:
        s = Search(using=e, index="wikidata_en").query("query_string", query=query)
        response = s[0:20].execute()
    except:
        print("Exception********************************")
        time.sleep(3)
        try:
            s = Search(using=e, index="wikidata_en").query("query_string", query=query)
            response = s[0:20].execute()
        except:
            print("null*********************************")
            return {}
    query_list = query.split(" ")
    id_labels = {}
    if response:
        for hit in response:
            try:
                schema_name = hit.schema_name
            except:
                schema_name = ""

            try:
                schema_description = hit.schema_description
            except:
                schema_description = ""
            my_dict = {}
            my_dict["schema_name"] = schema_name
            my_dict["schema_description"] = schema_description
            my_dict["score"] = hit.meta.score
            id_labels.setdefault(hit.meta.id, set())
            id_labels[hit.meta.id] = my_dict
            # else:
            # return {}
    else:
        return {}
    return id_labels


def candidate_selector(entity_list):
    '''
    import sys
    entity_list = []
    try:
        _, QUERY = sys.argv
    except Exception as e:
        with open('entities_00092_removeDuplicates_sorted.json') as f:
            entity_list = json.load(f)'''

    start = timer()
    print(f'starting computations on {cpu_count()} cores')
    result_dict = {}
    query_list = []
    entity_name = []
    for entity_dict in entity_list:
        QUERY = entity_dict['EntityName']
        temp = tuple()
        temp = QUERY,
        query_list.append(temp)
        entity_name.append(QUERY)
    print(len(query_list))

    with Pool() as pool:
        result = pool.starmap(search_rank, query_list)
        # result = search_rank(QUERY)
        # for entity, labels in result.items():
        #    print(entity, labels)
        for i in range(len(result)):
            result_dict[entity_name[i]] = result[i]
    result_json = json.dumps(result_dict)
    with open(r'result.json', 'w') as jf:
        jf.write(result_json)
    end = timer()
    print(f'elapsed time: {end - start}')


if __name__ == '__main__':
    print('START!')
    with open('entities_removeDuplicates_sorted.json') as f:
        entity_list = json.load(f)
        candidate_selector(entity_list)
    print('FINISH! You can test the score')
