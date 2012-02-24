import sys
import os
from numpy import repeat

from pmcminer.Linnaeus.PyLinnaeus import LinnaeusDictBySubject

class SpeciesStats(object):
    """
        species stats  for different subjects
    """
    def __init__(self, sDict):
        self.spp = self.spp_number_dict(sDict)
        
    
    def article_number_dict(self, path):
        """
            Gets total number of articles in the subjects in a directory. 
            e.g. plos1_new/data/pure
        """
        sppNumDict = {}
        for subject in os.listdir(path):
            sppNumDict[subject] = len(os.listdir(os.path.join(path, subject)))
        return(sppNumDict)
        
    def spp_number_dict(self, LinnaeusDict):
        """returns number of species in a dictionary of linnaeuss output files"""
        speciesCounts = {}
        for subject in LinnaeusDict: 
            speciesCounts[subject] = [LinnaeusDict[subject][LinnaeusDict[subject].keys()[i]][4] for i in range(len(LinnaeusDict[subject]))]
        return(speciesCounts)
        
    def spp_tally(self, LinnaeusDict):
        """
            Build a dict of tallys of discrete species ids in articles.
            Ambiguous species ids are not delt with.
        """
        tallyDict = {}
        for subject in LinnaeusDict:
            tallyDict[subject] = {}
            for article in LinnaeusDict[subject]:
                for species in LinnaeusDict[subject][article][3]:
                    try:
                        tallyDict[subject][species] += 1
                    except KeyError:
                        tallyDict[subject][species] = 1
        return(tallyDict)
        
    def spp_tally2(self, LinnaeusDict):
        """
            Build a dict of tallys of discrete species ids in articles.
            Where the id is ambiguous, split the count between the n 
            potential species.
        """
        tallyDict = {}
        for subject in LinnaeusDict:
            tallyDict[subject] = {}
            for article in LinnaeusDict[subject]:
                for species in LinnaeusDict[subject][article][3]:
                    sppSplit = species.split("|")
                    if len(sppSplit) > 1:
                        inc = 1.0 / len(sppSplit)
                    else:
                        inc = 1
                    for spp in sppSplit:
                        try:
                            tallyDict[subject][spp] += inc
                        except KeyError:
                            tallyDict[subject][spp] = inc
        return(tallyDict)
        
    def spp_tally_unambig(self, LinnaeusDict):
        """
            Build a dict of tallys of discrete species ids in articles.
            Ambiguous species ids are not included.
        """
        tallyDict = {}
        for subject in LinnaeusDict:
            tallyDict[subject] = {}
            for article in LinnaeusDict[subject]:
                for species in LinnaeusDict[subject][article][3]:
                    if len(species.split("|")) == 1:
                        try:
                            tallyDict[subject][species] += 1
                        except KeyError:
                            tallyDict[subject][species] = 1
        return(tallyDict)
        
    def spp_names_to_tally(self, tallyDict, speciesDict):
        tallyNamesDict = {}
        for subject in tallyDict:
            tallyNamesDict[subject] = {}
            for species in tallyDict[subject]:
                sppSplit = species.split("|")
                speciesID = sppSplit[0]
                try:
                    speciesName = speciesDict[speciesID].split("|")
                except KeyError:
                    print speciesID, sppSplit
                if len(sppSplit) > 1:
                    tallyNamesDict[subject][speciesName[1]] = tallyDict[subject][species]
                else:
                    tallyNamesDict[subject][speciesName[0]] = tallyDict[subject][species]
        return(tallyNamesDict)
        
    def print_spp_counts(self, tallyNamesDict, outFile = False):
        if outFile:
            f = open(outFile, "w")
            f.write("subject\tspecies\tcount\n")            
            f.close()
        for subject in tallyNamesDict:
            items=tallyNamesDict[subject].items()
            backitems=[ [v[1],v[0]] for v in items]
            backitems.sort(reverse = True)
            if outFile:
                sys.stderr.write("writing %s species names to %s...\n" % (subject, outFile))
                f = open(outFile, "a")
                for i in backitems:
                    f.write("%s\t%s\t%d\n" % (subject, i[1], i[0]))
            else:
                sys.stdout.write("subject\tspecies\tcount\n")
                for i in backitems:
                    sys.stdout.write("%s\t%s\t%d\n" % (subject, i[1], i[0]))
    
    def make_spp_names_dict(self, pathToSpeciesDict):
        sys.stderr.write("Building species names dictionary...\n")
        f = open(pathToSpeciesDict, "r")
        sppDict = {}
        for line in f:
            lSplit = line.split("\t")
            sppDict[lSplit[0]] = lSplit[1].rstrip("\n")
        f.close()
        return(sppDict)

class InteractionStats(SpeciesStats):
    """
        For getting mean interaction numbers...
    """
    def __init__(self, iDict):
        self.inter = self.spp_number_dict(iDict)
        
    def interaction_articles(self, path):
        """
            Gets total number of articles in the subjects in a directory. 
            e.g. plos1_new/data/pure
        """
        intNumDict = {}
        for subject in os.listdir(path):
            intNumDict[subject] = len(os.listdir(os.path.join(path, subject)))
        return(intNumDict)

def write_spp_numbers(nDict, totalDict,  outFile = False):
    if outFile:
        f = open(outFile, "w")
        f.write("subject\tin_article\n")
    for subject in nDict:
        theNumbers = nDict[subject] + list(repeat(0, totalDict[subject] - len(nDict[subject])))
        if outFile:
            sys.stderr.write("writing %s to %s\n" % (subject, os.path.basename(outFile)))
            f.writelines(["%s\t%d\n" % (subject, i) for i in theNumbers])
        else:
            sys.stdout.writelines(["%s\t%d\n" % (subject, i) for i in theNumbers])

def write_spp_dict(sppDict,  outFile = False):
    if outFile:
        f = open(outFile, "w")
        f.write("subject\tspecies\tcount\n")
    for subject in sppDict.keys():
        items = sppDict[subject].items()
        backitems=[ [v[1],v[0]] for v in items]
        backitems.sort(reverse = True)
        if outFile:
            sys.stderr.write("writing %s to %s\n" % (subject, os.path.basename(outFile)))
            f.writelines(["%s\t%s\t%f\n" % (subject, i[1], i[0]) for i in backitems])
        else:
            sys.stdout.writelines(["%s\t%s\t%f\n" % (subject, i[1], i[0]) for i in backitems])
   
def get_ambig_spp(tallyDict):
    """
        returns a dict of subjects with total number species and total 
        number of ambiguous species ids. 
    """
    tallyNamesDict = {}
    for subject in tallyDict:
        tallyNamesDict[subject] = {}
        ambiguousSpecies = 0
        for species in tallyDict[subject]:
            sppSplit = species.split("|")
            if len(sppSplit) > 1:
                ambiguousSpecies += 1
        tallyNamesDict[subject]["totalSpecies"] = len(tallyDict[subject].keys())
        tallyNamesDict[subject]["ambiguousSpecies"] = ambiguousSpecies
        tallyNamesDict[subject]["percentAmbiguous"] = 100 * (tallyNamesDict[subject]["ambiguousSpecies"] / float(tallyNamesDict[subject]["totalSpecies"])) 
    return(tallyNamesDict)

def write_ambig_dict(sppDict,  outFile = False):
    if outFile:
        f = open(outFile, "w")
        f.write("subject\ttotal species\tambiguous species\tpercent ambiguous\n")
    for subject in sppDict:
        if outFile:
            sys.stderr.write("writing %s to %s\n" % (subject, os.path.basename(outFile)))
            f.writelines("%s\t%d\t%d\t%f\n" % (subject, sppDict[subject]["totalSpecies"],
                                                sppDict[subject]["ambiguousSpecies"],
                                                sppDict[subject]["percentAmbiguous"]))
        else:
            sys.stdout.writelines("%s\t%d\t%d\t%f\n" % (subject, sppDict[subject]["totalSpecies"],
                                                sppDict[subject]["ambiguousSpecies"],
                                                sppDict[subject]["percentAmbiguous"]))

def get_linnaeus_stats(data_dir, pure_dir, tags_dir, analysis_dir,
                        spp_db,
                        spp_per_article, interactions_per_article,
                        species_numbers, unambiguous_species_numbers,
                        ambiguous_species):
    L = LinnaeusDictBySubject(species_path = os.path.join(data_dir, tags_dir, "species"),
                            inters_path = os.path.join(data_dir, tags_dir, "interactions"))
    S = SpeciesStats(L.species)
    S.totalArticles = S.article_number_dict(os.path.join(data_dir, pure_dir))
    
    td = S.spp_tally2(L.species)
    sppDict = S.make_spp_names_dict(spp_db)
    names = S.spp_names_to_tally(td, sppDict)
    
    I = InteractionStats(L.interactions)
    I.totalArticles = I.interaction_articles(os.path.join(data_dir, pure_dir))
    
    ambig = S.spp_tally(L.species)
    ambigDict = get_ambig_spp(ambig)
    
    unambig = S.spp_tally_unambig(L.species)
    unambigNames = S.spp_names_to_tally(unambig, sppDict)
    
    
    #output analysis datafiles:
    write_spp_numbers(S.spp, S.totalArticles, os.path.join(data_dir, analysis_dir, spp_per_article))
    write_spp_numbers(I.inter, I.totalArticles, os.path.join(data_dir, analysis_dir, interactions_per_article))
    write_spp_dict(names, os.path.join(data_dir, analysis_dir, species_numbers))
    write_spp_dict(unambigNames, os.path.join(data_dir, analysis_dir, unambiguous_species_numbers))
    write_ambig_dict(ambigDict, os.path.join(data_dir, analysis_dir, ambiguous_species))
    
    

