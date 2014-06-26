#!/usr/bin/python2

import sys
import os
import codecs


def generate_files(top_level):
    """generate paths to all files under top level"""
    for path, dirlist, filelist in os.walk(top_level):
        for name in filelist:
            yield os.path.join(path, name)
            
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
            


def build_table(in_file, out_file, pure_path, interaction_db, doi_list):
    """
        Makes a table of putative multi-species interactions.
        Each article is scored 0 or 1 for each interaction term.
    """
    sys.stderr.write("Building multispecies interaction table...\n")
    multi_dict = build_multi_dict(in_file)
    interactions = [line.split("\t")[0] for line in open(interaction_db, "r")]
    zeroInteractions = ["0" for i in interactions]
    outDict = {}
    
    for subject in doi_list:
        outDict[subject] = {}
        articles = generate_files(os.path.join(pure_path, subject))
        ids = ({"filename": os.path.basename(article)[:-len(".txt")],
                "doi": open(article).next().rstrip("\n")} for article in articles) # doi is in first line of file
        for text in ids:
            if text["filename"] in multi_dict[subject]:
                articleInteractions = set(multi_dict[subject][text["filename"]])
                interactionScore = []
                for i in interactions:
                    if i in articleInteractions:
                        interactionScore.append("1")
                    else:
                        interactionScore.append("0")
                outDict[subject][text["filename"]] = "\t".join([text["doi"]]+interactionScore)
            else:
                outDict[subject][text["filename"]] = "\t".join([text["doi"]]+zeroInteractions)
    f = codecs.open(out_file, "w", "utf-8")
    f.write("subject\tarticle\tdoi\t" + "\t".join(interactions)+"\n")
    for subject in outDict:
        for article in outDict[subject]:
            f.write("\t".join([subject, article, outDict[subject][article]])+"\n")
    f.close()
    sys.stderr.write("Done.\n")
                
 
             
