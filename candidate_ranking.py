import json
import numpy as np
import time
from timeit import default_timer as timer
from multiprocessing import Pool, cpu_count
# from textwiser import TextWiser, Embedding, Transformation, WordOptions, PoolOptions
from text2vec import *

def ranking():
    page_id = []
    entity_name = []
    with open('entities_removeDuplicates_sorted.json') as f:
        entity_list = json.load(f)
    for entity_dict in entity_list:
        page_id.append(entity_dict['PageId'])
        entity_name.append(entity_dict['EntityName'])
    print(len(page_id))

    start = timer()
    print(f'starting computations on {cpu_count()} cores')

    tfidf_entity_uri = []
    score = []
    with open('result.json') as f:
        entity_list = json.load(f)

    for entity_dict in entity_list:
        corpus = []
        schema = []
        corpus.append(entity_dict)
        print("Input:{}".format(entity_dict))
        candidate_dict = entity_list[entity_dict]
        for entity, labels in candidate_dict.items():
            schema.append(labels['schema_name'])
            corpus.append(labels['schema_name'])
            corpus.append(labels['schema_description'])
        if len(schema) > 0:
            # Features
            try:
                t2v = text2vec(corpus)
                vecs = t2v.get_lsi()
                #             emb = TextWiser(Embedding.TfIdf(min_df=1))
                #             vecs = emb.fit_transform(corpus)
                last_sim = 0
                last_index = 0
                for i in range(0, len(schema)):
                    sc1 = simical(vecs[0], vecs[2 * i + 1])
                    sc2 = simical(vecs[0], vecs[2 * i + 2])
                    sim = 0.9 * sc1.Cosine() + 0.1 * sc2.Cosine()
                    if sim > last_sim:
                        last_sim = sim
                        last_index = i
                print("Output:{}".format(schema[last_index]))
                tfidf_entity_uri.append(list(candidate_dict.keys())[last_index])
                score.append(last_sim)
                print(list(candidate_dict.keys())[last_index])
            except:
                tfidf_entity_uri.append("")
                score.append("")
        else:
            print("Exception")
            tfidf_entity_uri.append("")
            score.append("")

    end = timer()
    print(f'elapsed time: {end - start}')

    output = []
    for i in range(len(page_id)):
        if tfidf_entity_uri[i] != "" and score[i] > 0.5:
            output.append("{0}\t{1}\t{2}".format(page_id[i], entity_name[i], tfidf_entity_uri[i]))
    print(len(output))
    with open(r'result.tsv', 'w') as f:
        for line in output:
            f.write(line+'\n')
        f.close()