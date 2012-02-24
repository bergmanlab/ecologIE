#!/usr/bin/python2

import sys
import os
import codecs


def build_multi_dict(in_file):
    """dictionary of interaction terms"""
    multiDict = {}
    df = codecs.open(in_file, "r", "utf-8")
    for line in df:
        line = line.split("\t")
        try:
            multiDict[line[0]]
        except KeyError:
            multiDict[line[0]] = {}
        try:
            multiDict[line[0]][line[1]]
        except KeyError:
            multiDict[line[0]][line[1]] = []
        multiDict[line[0]][line[1]].extend(line[5].split(","))
    return(multiDict)
            

def articlesInDirectorySet(path):
    """count of files in directories"""
    dirset = {}
    for f in os.listdir(path):
        dirset[f] = len(os.listdir(os.path.join(path, f)))
    return(dirset)

def getmultispeciesInteractions(inFile):
    articles = {}
    f = open(inFile, "r").readlines()
    for line in f:
        line = line.split("\t")
        try:
            articles[line[0]].append(line[1])
        except KeyError:
            articles[line[0]] = [line[1]]
    for subject in articles:
        articles[subject] = len(set(articles[subject]))
    return(articles)

def build_table(in_file, out_file, pure_path, interaction_db):
    """
        Makes a table of putative multi-species interactions.
        Each article is scored 0 or 1 for each interaction term.
    """
    sys.stderr.write("Building multispecies interaction table...\n")
    multiDict = build_multi_dict(in_file)
    totalArticles = articlesInDirectorySet(pure_path)
    multispp = getmultispeciesInteractions(in_file)
    
    interactions = [line.split("\t")[0] for line in open(interaction_db, "r")]
    zeroInteractions = ["0" for i in interactions]
    outDict = {}
    for subject in multiDict:
        outDict[subject] = {}
        for article in multiDict[subject]:
            articleInteractions = set(multiDict[subject][article])
            interactionScore = []
            for i in interactions:
                if i in articleInteractions:
                    interactionScore.append("1")
                else:
                    interactionScore.append("0")
            outDict[subject][article] = ",".join(interactionScore)
        for extra in range(totalArticles[subject] - multispp[subject]):
            article = subject + "NonIntArticle" + str(extra)
            outDict[subject][article] = ",".join(zeroInteractions)
    f = codecs.open(out_file, "w", "utf-8")
    f.write("subject,article," + ",".join(interactions)+"\n")
    for subject in outDict:
        for article in outDict[subject]:
            f.write(",".join([subject, article, outDict[subject][article]])+"\n")
    f.close()
    sys.stderr.write("Done.\n")
    

