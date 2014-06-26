import nltk.data
import lxml.etree
import re
import numpy
import math
import os
import sys
import cPickle as pickle

from control import settings

def parse_XML(XML_file):
    """parses xml file using lxml."""
    return(lxml.etree.parse(open(XML_file,'r')))

def extract_element(XML_tree, element):
    """Extracts a given element from a parsed XML object"""
    return((i.text for i in XML_tree.findall(element)))

def parse_XML_no_table(XML_file):
    """
        Parses xml file with lxml.
        Removes all article tables.
    """
    doc = lxml.etree.parse(open(XML_file,'r'))
    elems = [i for i in doc.xpath("body/sec/table-wrap")]
    elems.extend([i for i in doc.xpath("body/sec/sec/table-wrap")])
    elems.extend([i for i in doc.xpath("body/sec/sec/sec/table-wrap")])
    for elem in elems:
        parent = elem.getparent()
        parent.remove(elem)
    return(doc)   

def get_article_body_text(xmlTree):
    """gets all raw text from the article body"""
    doc = xmlTree.findall("body")[0]
    doc_out = u" ".join([i for i in doc.itertext()])
    doc_out = doc_out.replace("\n","")
    return(doc_out)
    
def tokenize_text(raw_text):
    """Sentence tokenize by punctuation"""
    return(settings.TOKENIZER.tokenize(raw_text))
        
            
class ProcessedArticle(object):
    # merge these two classes to ProcessedArticle
    # include all article processing methods after parsing
    # inpiut either with or without tables (based on a parameter in __init__)
    def __init__(self, article, remove_tables = True):
        self.tree = parse_XML(article)
        self.raw = get_article_body_text(self.tree)
        self.paras = self.tokenize_text(self.raw)
                
    def get_article_body_text(self, xmlTree):
        """gets all raw text from the article body"""
        doc = xmlTree.findall("body")[0]
        doc_out = u" ".join([i for i in doc.itertext()])
        doc_out = doc_out.replace("\n","")
        return(doc_out)
    
    def get_article_abstract_text(self, XML_tree):
        """gets all raw text from the article body"""
        try:
            doc = XML_tree.findall("front/article-meta/abstract")[0]
            return(u" ".join([i for i in doc.itertext()]))
        except IndexError:
            return(0)

    def tokenize_text(self, raw_text):
        """Sentence tokenize by punctuation"""
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        return(tokenizer.tokenize(raw_text))


class ExtractArticleBody(ProcessedArticle):
    def __init__(self, source_file):
        self.article = source_file
        self.tree = parse_XML(self.article)
        self.body = self.get_article_body_text(self.tree)
        self.sentences = self.tokenize_text(self.body)
        self.doi = extract_element(self.tree, "front/article-meta/article-id")
    
    def write(self, dest_path):
        """
            Writes article body to dest_path directory.  
            One line per sentence.  
        """
        self.out_file = os.path.join(dest_path, 
                            os.path.split(self.article)[-1].replace(".xml", ".txt"))
        f = codecs.open(self.out_file, "w", "utf-8")
        f.write(self.doi[-1] + "\n")
        f.writelines((sent + "\n" for sent in self.sentences if not sent.isspace()))
        f.close()
        sys.stderr.write("%s --->>> %s\n" % (os.path.split(self.article)[-1], self.out_file))
        
