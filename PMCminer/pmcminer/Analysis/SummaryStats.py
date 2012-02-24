#!/usr/bin/python2
#build table of summary stats for plos1 data

import sys
import os
import math
import numpy
from scipy.stats import scoreatpercentile as percentile

from pmcminer.Linnaeus.PyLinnaeus import hash_linnaeus_file, LinnaeusDictBySubject
from pmcminer.Analysis.AnalyseLinnaeusFiles import InteractionStats, SpeciesStats
from pmcminer.Analysis import Checkdiversity
from pmcminer.Analysis.LocateInteractions import ProcessInteractions

class Summary(LinnaeusDictBySubject, SpeciesStats):
    def __init__(self, data_dir, raw_dir, pure_path, subjects, speciesDb, 
                        species_tags_path, interactions_tags_path, 
                        species_numbers_file, multispp_inter_file, 
                        spp_per_article_file, interactions_per_article_file):
        self.species = {}
        self.interactions = {}
        self.D = Checkdiversity.get_diversity(species_tags_path)
        self.populate(self.species, species_tags_path) # from LinnaeusDictBySubject
        self.populate(self.interactions, interactions_tags_path)
        print "interactions sentences..."
        self.interactionSentences = ProcessInteractions(data_dir, pure_path, subjects,
                                                    interactions_tags_path)
        
        print "self.spp"
        self.spp = self.spp_number_dict(self.species) # from SpeciesStats
        self.totalArticles = self.article_number_dict(os.path.join(data_dir, pure_path)) ##
        self.td = self.spp_tally2(self.species)    ##
        self.sppDict = self.make_spp_names_dict(speciesDb)
        self.sppNames = self.speciesDictFromFile(species_numbers_file)
        self.inter = self.spp_number_dict(self.interactions)
        self.inPlos1 = self.articlesInplos1(data_dir, subjects)
        self.inOASS = self.articlesInDirectorySet(os.path.join(data_dir, raw_dir), subjects)
        self.pureArticles = self.articlesInDirectorySet(os.path.join(data_dir, pure_path), subjects)
        self.articleswithSpp = self.articlesInDictionary(self.species)
        self.articleswith2Spp = self.getarticleswith2Spp(self.species)
        self.articleswithInteractions = self.articlesInDictionary(self.interactions)
        self.multispeciesInteractions = self.getmultispeciesInteractions(multispp_inter_file)
        self.lengths = self.getMeanarticleLengths(os.path.join(data_dir, pure_path), subjects)
        self.totalSentences = self.getTotalSubjectSentences(os.path.join(data_dir, pure_path), subjects)
        self.meanSentences = self.getMeanSentencesperCorpus(os.path.join(data_dir, pure_path), subjects)
        self.medianSpecies = Medians(spp_per_article_file)
        self.medianInteractions = Medians(interactions_per_article_file)

        
    def print_summary_stats(self, subjects, out_file = False):
        if out_file:
            writer = open(out_file, "w")
        else:
            writer = sys.stdout
        writer.write(" ," + ",".join(subjects) + "\n")
        writer.write(",".join(["Articles in PLoS API"] + [str(self.inPlos1[i]) for i in subjects])+"\n")
        writer.write(",".join(["Articles in OASS (%ge in PloS)"] + [self.pc(self.inOASS[i], self.inPlos1[i]) for i in subjects])+"\n")
        writer.write(",".join(["Pure article corpus (%ge in OASS)"] + [self.pc(self.pureArticles[i], self.inOASS[i]) for i in subjects])+"\n")
        writer.write(",".join(["Articles containing species (%ge in pure)"] + [self.pc(self.articleswithSpp[i], self.pureArticles[i]) for i in subjects])+"\n")
        writer.write(",".join(["Articles containing 2+ species (%ge in pure)"] + [self.pc(self.articleswith2Spp[i], self.pureArticles[i]) for i in subjects])+"\n")
        writer.write(",".join(["Articles containing interaction terms (%ge in pure)"] + [self.pc(self.articleswithInteractions[i], self.pureArticles[i]) for i in subjects])+"\n")
        writer.write(",".join(["Articles containing multispecies interactions (%ge in pure)"] + [self.pc(self.multispeciesInteractions[i], self.pureArticles[i]) for i in subjects])+"\n")
        writer.write(",".join(["Total sentences in corpus"] + ["%d" % self.totalSentences[i] for i in subjects])+"\n")
        writer.write(",".join(["Mean sentences/article (sd)"] + ["%d (%d)" % self.meanSentences[i] for i in subjects])+"\n")
        writer.write(",".join(["Total sentences with interactions in corpus"] + ["%d" % self.interactionSentences.totalInteractionSentences[i] for i in subjects])+"\n")
        writer.write(",".join(["Median sentences with interactions/article"] + ["%d" % self.interactionSentences.medianInteractionSentences[i] for i in subjects])+"\n")
        writer.write(",".join(["Median species/article (25th-; 75th percentile)"] + ["%d (%d; %d)" % self.medianSpecies.median[i] for i in subjects])+"\n")
        writer.write(",".join(["Median interactions/article (25th-; 75th percentile)"] + ["%d (%d; %d)" % self.medianInteractions.median[i] for i in subjects])+"\n")
        writer.write(",".join(["Species richness / articles in corpus"] + [str(round(float(self.D.richnessDict[i+"_species.tsv"]) / self.pureArticles[i], 1)) for i in subjects])+"\n")
        writer.write(",".join(["Species evenness"] + [str(self.D.evennessDict[i+"_species.tsv"]) for i in subjects])+"\n")
        writer.write(",".join(["Shannon diversity index"] + [str(self.D.diversityDict[i+"_species.tsv"]) for i in subjects])+"\n")

        if out_file:
            writer.close()
        
    def pc(self, num, denom):
        """
            Gives (num, percentage numerator of denominator)
        """
        return("%d (%d%s)" % (num, round(float(num) / denom * 100, 1), "%"))
        
        
        
    def articlesInplos1(self, data_dir, doi_lists):
        """Total number of DOIs in plos1 API download"""
        doi = {}
        for f in doi_lists:
            doi[f] = sum(1 for line in open(os.path.join(data_dir, doi_lists[f])))
        return(doi)
        
    def articlesInDirectorySet(self, pure_path, subjects):
        """count of files in directories"""
        dirset = {}
        for f in subjects:
            dirset[f] = len(os.listdir(os.path.join(pure_path, f)))
        return(dirset)
        
    def articlesInDictionary(self, sppDict):
        articles = {}
        for subject in sppDict:
            articles[subject] = len(sppDict[subject])
        return(articles)
    
    
    def getarticleswith2Spp(self, sppDict):
        articles = {}
        for subject in sppDict:
            articles[subject] = len([1 for article in sppDict[subject] if sppDict[subject][article][4] > 1])
        return(articles)
        
    def getmultispeciesInteractions(self, inFile):
        articles = {}
        f = open(inFile, "r")
        for line in f:
            line = line.split("\t")
            try:
                articles[line[0]].append(line[1])
            except KeyError:
                articles[line[0]] = [line[1]]
        for subject in articles:
            articles[subject] = len(set(articles[subject]))
        return(articles)
     
    def speciesDictFromFile(self, sppFile):
        f = open(sppFile, "r").readlines()
        speciesdict = {}
        for line in f[1:]:
            lineSplit = line.split("\t")
            try:
                speciesdict[lineSplit[0]][lineSplit[1]] = float(lineSplit[2])
            except KeyError:
                speciesdict[lineSplit[0]] = {}
                speciesdict[lineSplit[0]][lineSplit[1]] = float(lineSplit[2])
        return(speciesdict)
        
    def getMeanarticleLengths(self, pure_path, subjects):
        """Mean/sd sentences per article in each subject"""
        dirset = {}
        for subject in subjects:
            lengths = []
            for article in os.listdir(os.path.join(pure_path, subject)):
                lengths.append(sum(1 for line in open(os.path.join(pure_path, subject, article))))
            dirset[subject] = (numpy.mean(lengths), numpy.std(lengths)) 
        return(dirset)        
    
    def getTotalSubjectSentences(self, pure_path, subjects):
        """Total sentences in each subject corpus"""
        dirset = {}
        for subject in subjects:
            lengths = []
            for article in os.listdir(os.path.join(pure_path, subject)):
                lengths.append(sum(1 for line in open(os.path.join(pure_path, subject, article))))
            dirset[subject] = sum(lengths) 
        return(dirset)
        
    def getMeanSentencesperCorpus(self, pure_path, subjects):
        """Total sentences / total articles and"""
        dirset = {}
        for subject in subjects:
            lengths = []
            for article in os.listdir(os.path.join(pure_path, subject)):
                lengths.append(sum(1 for line in open(os.path.join(pure_path, subject, article))))
            dirset[subject] = (round(numpy.mean(lengths),2), round(numpy.std(lengths), 2))
        return(dirset)
    
        
class Medians(object):
    def __init__(self, inArticleFile):
        self.inArticleDict = self.readFile(inArticleFile)
        self.median = self.getMedian(self.inArticleDict)

    def readFile(self, inArticleFile):
        """puts xxx_per_article file into a dict_"""
        inArticleDict = {}
        inArticles = open(inArticleFile).readlines()[1:]
        for article in inArticles:
            article = article.split("\t")
            try:
                inArticleDict[article[0]].append(int(article[1].rstrip("\n")))
            except KeyError:
                inArticleDict[article[0]] = [int(article[1].rstrip("\n"))]
        return(inArticleDict)

    def getMedian(self, inArticleDict):
        """returns dict of medians for subjects"""
        medDict = {}
        for subject in inArticleDict:
            medDict[subject] = (round(numpy.median(self.inArticleDict[subject])),
                                round(percentile(self.inArticleDict[subject],25)),
                                round(percentile(self.inArticleDict[subject],75)))
        return(medDict)

    def getPercentile(self, inArticleDict, percent):
        """returns dict of percentiles for subjects"""
        medDict = {}
        for subject in inArticleDict:
            medDict[subject] = percentile(self.inArticleDict[subject], percent)
        return(medDict)

