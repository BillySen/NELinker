import nltk
import pandas as pd
import re
import json

#parse and tokenize the text/doucument
def text_handler(text):
    text = re.sub('\n', '', text)
    if isinstance(text, str):
        text = text
    else:
        raise ValueError('text is not string!')

    text = text.strip()
    #phrase or sentences
    phrases = nltk.sent_tokenize(text)
    phrases = [sentence.strip() for sentence in phrases]

    return phrases
def entity_extract_nltk(warc_json):

    data_list = json.loads(warc_json)
    df = pd.json_normalize(data_list)
    length= df.shape[0]
    #text="your name is Amsterdam "

    #Row Operation
    entities_Named = []
    for i in range(length):
        text_content = (" ".join(i for i in df.iat[i,1]))
        #print("text_content:",text_content)
        print("pageid:",df.iat[i,0])
        #  tokenize sentence
        sentences = text_handler(text_content)
        tokenized_phrases = [nltk.word_tokenize(sentence) for sentence in sentences]

        #  tag sentences and use nltk's Named Entity Chunk
        tagged_phrases = [nltk.pos_tag(phrase) for phrase in tokenized_phrases]
        neChunked_phrase = [nltk.ne_chunk(tagged_phrase) for tagged_phrase in tagged_phrases]

        #  find all named entities
        for neTagged_phrase in neChunked_phrase:
            for tagged_tree in neTagged_phrase:
                #  maintain only chunks with Named Entity labels
                if hasattr(tagged_tree, 'label'):
                    pageid = df.iat[i,0]
                    entity_name = ' '.join(c[0] for c in tagged_tree.leaves())
                    entity_type = tagged_tree.label()  # entity category
                    entities_Named.append((pageid,entity_name, entity_type))
                    #  Remove Duplicates using set()
                    entities_Named = list(set(entities_Named))

    #  store named entities
    entity_frame = pd.DataFrame(entities_Named, columns=['PageId','EntityName', 'EntityType'])
    # remove duplicates and keep the first occurred one
    entity_frame_uniqueName = entity_frame.drop_duplicates(subset='EntityName', keep='first')
    # entity_frame_uniqueName.PageId=entity_frame_uniqueName['PageId'].sort_values(ascending=True)
    entity_frame_uniqueName = entity_frame_uniqueName.sort_values(['PageId'], ascending=True)
    return entity_frame_uniqueName
# print(entity_frame_uniqueName)
# store
# entity_frame_uniqueName.to_json('entities_removeDuplicates.json',orient='records')
