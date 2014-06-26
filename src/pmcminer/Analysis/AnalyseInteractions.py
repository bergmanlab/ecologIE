import codecs
import os
import sys

from control import settings
from pmcminer.Linnaeus.PyLinnaeus import hash_linnaeus_file

class ProcessedArticle(object):
    """
        If input is a sentence-split text file, this gives file as a raw string (self.raw),
        list of sentences (self.sentences) and a numbered list of tuples with start and end 
        coordinates for each sentence (self.coordinates).
        
        If input is a list of sentences, just the coordinates are returned.
    """
    def __init__(self, text):
        if type(text) == list:
            self.coordinates = self.line_coordinates(text)
        else:
            try:
                self.raw = codecs.open(text,"r", "utf8").read()
                self.sentences = codecs.open(text,"r", "utf8").readlines()
                self.doi = self.sentences[0].rstrip("\n")
                self.coordinates = self.line_coordinates(self.sentences)
                self.file_name = os.path.basename(text.rstrip(".txt"))
            except IOError:
                sys.stderr.write("input must be a list of sentences or a text file\n")
                sys.exit(0)

    def cumulative_sum(self, values, start=0):
        """
            Yields cumulative sum of elements in a list.
        """
        for v in values:
            start += v
            yield start
    
    def line_coordinates(self, text):
        """
            returns a numbered list of tuples of start and end of line coordinates
        """
        line_lengths = (len(i) for i in text)
        end_of_lines = list(self.cumulative_sum(line_lengths))
        start_of_lines = []
        for i in range(len(end_of_lines)):
            if i == 0:
                start_of_lines.append(0)
            else:
                start_of_lines.append(end_of_lines[i-1] + 1)
        return(list(enumerate(zip(start_of_lines, end_of_lines))))

class MultiSppDirectory(object):
    """
        Find all putative multispecies interactions in articles in a subjcet directory
    """
    def __init__(self, source, dest, species, interactions, subject, 
                                            min_spp, min_ints):
        species_dict = hash_linnaeus_file(species)
        interacts_dict = hash_linnaeus_file(interactions)
        #subject = os.path.basename(source)
        sys.stderr.write("writing output from %s to %s...\n" % (source, dest))
        f = codecs.open(dest, "a", "utf8")
        for article in os.listdir(source):
            p = ProcessedArticle(os.path.join(source, article))
            out = ArticleInteractions(p, species_dict, interacts_dict, min_spp, min_ints)
            if out.tagged_sentences:
                sys.stderr.write("...writing %s..." % p.file_name)
                f.writelines([subject + "\t" + line for line in out.flat_output])
        f.close()
        sys.stderr.write("\nDone.\n")

class ArticleInteractions(object):            
    def __init__(self, processed_article, species, interacts, 
                        min_spp, min_ints):
        """
            Gives all information about multi species interactions above min_spp species
            and min_ints ecological interactions.
        """
        try:
            self.species = species[processed_article.file_name]
            self.interactions = interacts[processed_article.file_name]
            self.extract_interactions(processed_article, min_spp, min_ints)
            self.flat_output = self.write()
        except KeyError:
            self.tagged_sentences = None
            
    def extract_interactions(self, processed_article, min_spp, min_ints):
        """checks every sentence against spp and interaction dictionaries"""
        self.min_spp = min_spp
        self.tagged_sentences = []
        self.species_IDs = []
        self.species_names = []
        self.interaction_IDs = []
        self.interaction_names = []
        self.article_name = processed_article.file_name
        self.doi = processed_article.doi
                
        for sentence in processed_article.coordinates:
            spp_count = 0
            ints_count = 0
            sentence_spp = [] 
            sentence_ints = []
            for occurence in range(len(self.species[0])):
                if self.species[0][occurence][0] >= sentence[1][0] and \
                self.species[0][occurence][1] <= sentence[1][1]:
                    spp_count += 1
                    sentence_spp.append((self.species[1][occurence],
                                            self.species[2][occurence]))
                    
            for interaction in range(len(self.interactions[0])):
                if self.interactions[0][interaction][0] >= sentence[1][0] and \
                self.interactions[0][interaction][1] <= sentence[1][1]:
                    ints_count += 1
                    sentence_ints.append((self.interactions[1][interaction],
                                                 self.interactions[2][interaction]))
            if spp_count >= self.min_spp and ints_count >= min_ints:
                self.species_IDs.append([i[0] for i in sentence_spp])
                self.species_names.append([i[1] for i in sentence_spp])
                self.interaction_IDs.append([i[0] for i in sentence_ints])
                self.interaction_names.append([i[1] for i in sentence_ints])
                self.tagged_sentences.append(processed_article.sentences[sentence[0]])
    
    def write(self):
        assert len(self.species_IDs) == len(self.species_names) == \
        len(self.interaction_IDs) == len(self.interaction_names) == len(self.tagged_sentences)
        
        return(["\t".join([self.article_name, self.doi, ",".join(self.species_IDs[i]), 
                    ",".join(self.species_names[i]), ",".join(self.interaction_IDs[i]),
                    ",".join(self.interaction_names[i]), self.tagged_sentences[i]]) \
        for i in range(len(self.species_IDs)) if len(set(self.species_IDs[i])) >= self.min_spp])
   
  
def get_multispp_interactions(subjects, tag_path, pure_path, multi_file, all_file,
                                                            min_spp = 2, min_ints = 1):
    """
        Outputs csv files for all putative multispecies interactions
        and for all interactions (Irrespective of species).
    """
    subs = (
                {
                    "datapath": os.path.join(pure_path, subj),
                    "species_tags": os.path.join(tag_path,"species",subj+"_species.tsv"),
                    "interaction_tags": os.path.join(tag_path,"interactions",subj+"_interactions.tsv"),
                    "subject": subj
                } for subj in subjects
            )
    
    for subj in subs:
        multispp = MultiSppDirectory(source = subj["datapath"], dest = multi_file, 
                                        species = subj["species_tags"],
                                        subject = subj["subject"], 
                                        interactions = subj["interaction_tags"],
                                        min_spp = min_spp, min_ints = min_ints)
        allinteractions = MultiSppDirectory(source = subj["datapath"], dest = all_file, 
                                        species = subj["species_tags"],
                                        subject = subj["subject"], 
                                        interactions = subj["interaction_tags"],
                                        min_spp = 0, min_ints = min_ints)
    













