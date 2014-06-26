#!/usr/bin/python2


import os
import codecs
import sys
import numpy

from pmcminer.Analysis.AnalyseInteractions import ProcessedArticle
from pmcminer.Linnaeus.PyLinnaeus import hash_linnaeus_file

class ProcessInteractions(object):
    """
        Locates interaction terms from a linnaeus output file
        in an article.
    """
    def __init__(self, data_path, pure_path, subjects, inter_tag_path):
        #self.pure_path = pure_path
        #self.tagsPath = tagsPath
        self.inter_totals = self.processDirectory(data_path, pure_path, subjects, inter_tag_path)
        self.inter_sentence_stats(self.inter_totals)
        #self.interDict = self.hashLinnaeusFile(open(interactionsFile).readlines())
        #self.totals = self.process(self.interDict, directoryPath, "plos1Ecology")
    
    def process(self, inter_dict, data_path, pure_path, subject):
        totalsDict = {}
        for article in inter_dict:
            interSentences = {}
            sys.stderr.write("processing article %s\n" % article) 
            articleFileName = os.path.join(data_path, pure_path, subject, article + ".txt")
            sys.stderr.write(articleFileName + "\n")
            ###
            sentences = ProcessedArticle(articleFileName)
            for interaction in inter_dict[article][0]: #coordinates of interaction terms tagged by linnaeus
                interactionLocation = int(interaction[0])
                #print "interactionLocation %d" % interactionLocation
                for line in range(len(sentences.coordinates)):
                    #print "coordinates %d" % sentences.coordinates[line][1][0]
                    if  interactionLocation > sentences.coordinates[line][1][0] and \
                    interactionLocation < sentences.coordinates[line][1][1]:
                        try:
                            interSentences[[line][0]] += 1
                        except KeyError:
                            interSentences[[line][0]] = 1
            totalsDict[article] = interSentences.keys()
        return(totalsDict)
    
    def processDirectory(self, data_path, pure_path, subjects, inter_tag_path):
        """ Apply process to a directory of interaction tagfiles"""
        processDict = {}
        for subject in subjects:
            sys.stderr.write("Locating %s interaction terms...\n" % subject)
            interDict = hash_linnaeus_file(os.path.join(inter_tag_path, 
                                            subject + "_interactions.tsv"))
            processDict[subject] = self.process(interDict, data_path, pure_path, subject)
        return(processDict)
        
    def inter_sentence_stats(self, interactionTotalDict):
        """
            total articles with interactions in corpus,
            total sentences with interactions in corpus,
            median sentences with interactions per article in corpus.
        """
        self.totalInteractionArticles = dict(zip(interactionTotalDict.keys(),
                [len(interactionTotalDict[i]) for i in interactionTotalDict.keys()]))
        self.totalInteractionSentences = dict(zip(interactionTotalDict.keys(),
        [sum([len(interactionTotalDict[i][j]) for j in interactionTotalDict[i].keys()]) \
                for i in interactionTotalDict.keys()]))
        self.medianInteractionSentences = dict(zip(interactionTotalDict.keys(),
        [numpy.median([len(interactionTotalDict[i][j]) for j in interactionTotalDict[i].keys()]) \
                for i in interactionTotalDict.keys()]))
        
    
   
