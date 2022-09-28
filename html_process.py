import gzip
from warcio.archiveiterator import ArchiveIterator
import json
import bs4
import re
import lxml

WARC_ID = "WARC-Record-ID"


# WARC text
def filtering(text, str_starter=""):
    # removing non-english text
    res1 = re.compile(u"([^.,';\s\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])")
    text_filtered = res1.sub(str_starter, text)
    # Remove leading and trailing spaces or line breaks from strings
    return text_filtered.strip()

def html_to_text(html):
    soup = bs4.BeautifulSoup(html, "lxml")
    # delete white space and repeated text
    text = list(set([filtering(text) for text in soup.stripped_strings]))
    text = list(filter(None, text))
    return text #html text

def reading(path):
    if path == '':
        path = "data/sample.warc.gz"
    warc_src = []

    with gzip.open(path, 'rb') as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == 'response':
                if record.http_headers != None:
                    # WARC Record ID
                    record_id = record.rec_headers.get_header('WARC-TREC-ID')
                    html = record.content_stream().read()
                    page_content = {}
                    page_content['id'] = record_id
                    page_content['text'] = html_to_text(html)
                    warc_src.append(page_content)
    return warc_src


if __name__ == '__main__':
    with open("Text_of_HTML.json", "w") as f:
        warc_src = reading("")
        json.dump(warc_src, f)
    print("HTML processing finished")
