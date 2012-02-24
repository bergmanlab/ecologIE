import math
import os

def hash_tag_file(tag):
    """
        Convert linnaeus output file to dictionary.
        keys are article names.
        Values are lists of species mentioned in articles.
    """
    t = open(tag)
    d = {}
    for line in t:
        line = line.split("\t")
        try:
            d[line[1]].append(line[0])
        except KeyError:
            d[line[1]] = [line[0]]
    for article in d:
        d[article] = list(set(d[article]))
    return(d)

def species_dict(hfile):
    """
        Dict of total species in corpus.
        Each species has a count.
        Ambiguous species have count split among them.
    """
    spp = {}
    for article in hfile:
        for species in hfile[article]:
            species = species.split("|")
            for each in species:
                try:
                    spp[each] += (1.0 / len(species))
                except KeyError:
                    spp[each] = (1.0 / len(species))
    return(spp)

def directory_species_dict(direc):
    """Get a dict of species_dicts for all linnaeus output files in a directory"""
    d = {}
    for f in os.listdir(direc):
        d[f] = species_dict(hash_tag_file(os.path.join(direc, f)) )
    return(d)



class Diversity:
    """Calculate diversity indices to output of directory_species_dict"""
    def __init__(self, sppDict):
        self.diversityDict = {}
        self.richnessDict = {}
        self.evennessDict = {}
        for subject in sppDict:
            self.calculateDiversity(sppDict[subject])
            self.diversityDict[subject] = self.shannon
            self.richnessDict[subject] = self.richness
            self.evennessDict[subject] = self.evenness

    def calculateDiversity(self, speciesDict):      
        """calculates Richness, evenness and Shannon index for a species_dict"""
        self.richness = len(speciesDict)
        N = 0
        for k, v in speciesDict.iteritems():
            N = N + v
        p = 0
        sum_p = 0
        for k, v in speciesDict.iteritems():
            p = float(v) / N
            sum_p += (p * math.log(p))
        self.shannon = round(-(sum_p ), 2)
        self.evenness = round(self.shannon / math.log(self.richness), 2)

def get_diversity(directory):
    """Wraps up the above functions for a directory of linnaeus output files"""
    return(Diversity(directory_species_dict(directory)))

    



