#creates pure sets of articles with no overlap between subjects

import os
import sys
import itertools
from collections import Counter
from control import settings
import codecs

from pmcminer.ProcessFiles import Articles
from pmcminer.ProcessFiles import Raw

def get_article_file_counts(root):
    """Count appearances of a file name across sub-directories in root"""
    article_counts = Counter()
    for article in Raw.generate_files(root):
        article_counts[os.path.basename(article)] += 1
    return(article_counts)

def write_tokenized_article(sentences, doi, article_name, dest_path):
    """Write a text file one sentence per line"""
    out_file = os.path.join(dest_path, 
                    os.path.basename(article_name).replace(".xml", ".txt"))
    f = codecs.open(out_file, "w", "utf-8")
    f.write(doi + "\n")
    f.writelines((sent + "\n" for sent in sentences if not sent.isspace()))
    f.close()
        
def purify_articles(data_dir, raw_dir, doi_lists, pure_articles_dir, updater = 500):
    """
        Read all files in raw_dir. If files only occur in one directory,
        tokenize and write to same directory structure in pure_articles_dir
    """
    article_counts = get_article_file_counts(os.path.join(data_dir, 
                                             raw_dir))
    corpora = ({ 
                    "articles": Raw.generate_files(os.path.join(data_dir, 
                                        raw_dir, subject)),
                    "subject": subject
                } for subject in doi_lists)
    for corpus in corpora:
        if not os.path.isdir(os.path.join(data_dir, 
                                          pure_articles_dir,
                                          corpus["subject"])):
            os.makedirs(os.path.join(data_dir, 
                                          pure_articles_dir,
                                          corpus["subject"]))
        for n, article in enumerate(corpus["articles"]):
            if article_counts[os.path.basename(article)] == 1:
                tree =  Articles.parse_XML_no_table(article)
                body = Articles.get_article_body_text(tree)
                sentences = Articles.tokenize_text(body)
                doi = list(Articles.extract_element(tree, "front/article-meta/article-id"))[-1]
                write_tokenized_article(sentences, doi, article, os.path.join(data_dir,
                                                                    pure_articles_dir,
                                                                    corpus["subject"]))
            if n % updater == 0:
                sys.stderr.write("%d articles purified in %s..." % (n, corpus["subject"]))
    sys.stderr.write("Done.\n")



                
                
