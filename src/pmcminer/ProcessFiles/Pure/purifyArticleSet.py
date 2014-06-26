#!/usr/bin/python2
#creates pure sets of articles with no overlap between subjects
#ensure that there are only the article directories in the inPath...

import os
import sys
import itertools

from control import settings

from pmcminer.ProcessFiles import Articles
from pmcminer.ProcessFiles import Raw






articles = ({ "articles": Raw.generate_files(os.path.join(settings.DATA_DIR, 
                                    settings.RAW_ARTICLES_DIR, 
                                    subject)),
               "subject": subject} for subject in settings.DOI_LISTS)

class Purify(Articles.ExtractArticleBody):
    """
        builds an article set for article subjects that are non-overlapping.
        put a tuple or list in dirSet to specify directories within inPath.
    """
    def __init__(self, inPath, outPath, dirSet = False):
        if dirSet:
            self.subjects = dirSet
        else:
            self.subjects = [subject for subject in os.listdir(inPath) if 
                               os.path.isdir(os.path.join(inPath, subject))]
        self.subjectCount = [len(os.listdir(os.path.join(inPath, subject))) for subject in self.subjects]
        
        self.inPath = inPath
        self.outPath = outPath
        self.sortSubjects() 
        
        self.check_for_purity()
            
    def sort_subjects(self):
        subjectsAndCounts = zip(self.subjectCount, self.subjects)
        subjectsAndCounts.sort(reverse = True)
        self.subjectCount, self.subjects = zip(*subjectsAndCounts)
    
    def check_for_purity(self):
        self.articlesInPath = len(list(itertools.chain.from_iterable([os.listdir(
                                    os.path.join(self.inPath, sub)) 
                                    for sub in self.subjects])))
        self.expungedArticles = 0
        for subject in self.subjects:
            inGroup = os.listdir(os.path.join(self.inPath, subject))
            outGroup  = self.freqTable(list(itertools.chain.from_iterable([os.listdir(
                                    os.path.join(self.inPath, sub)) 
                                    for sub in self.subjects 
                                    if sub != subject])))
            for article in inGroup:
                try:
                    outGroup[article] += 1
                    sys.stderr.write("%s is not pure... not adding to %s...\n" % (article, subject))
                    self.expungedArticles += 1
                except KeyError:
                    sys.stderr.write("processing %s in %s\n" % (article, subject))
                    if article == ".directory":
                        continue
                    self.outputPureArticle(article, subject)
    
    def freqTable(self, myList):
        freqdist = {}
        for item in myList:
            try:
                freqdist[item] += 1
            except KeyError:
                freqdist[item] = 1
        return(freqdist)
    
    def output_pure_article(self, article, subject):
        self.article = os.path.join(self.inPath, subject, article)
        self.tree = Articles.parse_XML_no_Table(self.article)
        self.body = self.get_article_body_text(self.tree)
        self.sentences = self.tokenize_text(self.body)
        self.doi = Articles.extract_element(self.tree, "front/article-meta/article-id")
        if not os.path.exists(os.path.join(self.outPath, subject)):
            sys.stderr.write("creating directory %s\n" % os.path.join(self.outPath, subject))
            os.mkdir(os.path.join(self.outPath, subject))
        
        self.write(os.path.join(self.outPath, subject))

    
if __name__ == "__main__":
    rawArticles = sys.argv[1]
    pureArticles = sys.argv[2]
    a = Purify(rawArticles,pureArticles)
    
                
                
