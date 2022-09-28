------------------------------------------------------------------------------------------------------------------------
Packages which need to install before running the file:
pip install elasticsearch_dsl
pip install spacy
pip intsall gensim
python -m spacy download en_core_web_sm
------------------------------------------------------------------------------------------------------------------------
How to start and run our code to generate the result?
As we have generated the code into one main file - starter_code.py 
------------------------------------------------------------------------------------------------------------------------
The first step is to start the elasticsearch server by using shell command: 
sh start_elasticsearch_server.sh
------------------------------------------------------------------------------------------------------------------------
Since the search engine is started, the following step is to use this command: 
python starter_code.py .\data\sample_warc.gz
------------------------------------------------------------------------------------------------------------------------
The program will come up with a final result file: result.tsv under current work path
------------------------------------------------------------------------------------------------------------------------
As for testing the final score, please directly execute this command: 
python score.py data\sample_annotations.tsv result.tsv
------------------------------------------------------------------------------------------------------------------------
The output will be demonstrated in the command line terminal for examine. 
------------------------------------------------------------------------------------------------------------------------