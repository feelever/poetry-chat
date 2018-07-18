# -*- coding: UTF-8 -*- 
import os
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema,TEXT,ID
from jieba.analyse import ChineseAnalyzer
import json
import glob
analyzer = ChineseAnalyzer()
indexdir = r'./indexdir'
schema = Schema(strains=TEXT(stored=True, analyzer=analyzer), author=TEXT(stored=True,analyzer=analyzer),
                paragraphs=TEXT(stored=True, analyzer=analyzer),title=TEXT(stored=True,analyzer=analyzer))
def index():
    # 存储schema信息至'indexdir'目录下    
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)
    writer = ix.writer()
    poems = glob.glob(r'./poetry/*.json')
    for poem in poems:
        with open(poem,'rb') as f:
            pms=json.load(f)
            for pm in pms:
                writer.add_document(strains=pm['strains'],author=pm['author'],paragraphs=pm['paragraphs'],title=pm['title'])
        print(poem)    
    writer.commit()
   
def search():
    idx = open_dir(indexdir) 
    searcher = idx.searcher()    
    results = searcher.find("", "杨万里")
    firstdoc = results[0].fields()
    jsondoc = json.dumps(firstdoc, ensure_ascii=False)
    #print(jsondoc)  # 高亮标题中的检索词
    print(results[0])  # bm25分数
index()
#search()