import os
import subprocess
import sys

from control import settings

def lin_opts(tags = 0, subject = 0):
    return {
                "platform": "java",
                "memory": "-Xmx%s" % settings.LINNAEUS_MEMORY,
                "type": "-jar",
                "path": settings.LINNAEUS_JAR,
                "properties": "--properties",
                "conf": settings.LINNAEUS_CONF[tags]["conf_file"],
                "in_type": "--textDir",
                "data_dir": os.path.join(settings.DATA_DIR, 
                                        settings.PURE_ARTICLES_DIR, 
                                        settings.DOI_LISTS.keys()[subject]),
                "output": "--out",
                "out_file": os.path.join(settings.DATA_DIR, settings.TAGS_DIR,
                                        settings.LINNAEUS_CONF[tags]["tags"],
                                        "".join((settings.DOI_LISTS.keys()[subject], "_",
                                        settings.LINNAEUS_CONF[tags]["tags"],".tsv")))
            }

class Tagger(object):
    """
        A wrapper for the Linnaeus entity tagger.
    """
    def __init__(self, **kwargs):
        self.options = kwargs
        self.run_string = " ".join((self.options["platform"], self.options["memory"], 
                                    self.options["type"], self.options["path"], 
                                    self.options["properties"], self.options["conf"],
                                    self.options["in_type"], self.options["data_dir"], 
                                    self.options["output"], self.options["out_file"]))
    def check_directories(self):
        """Make sure there is somewhere to write to."""
        if not os.path.isdir("/".join(self.options["out_file"].split("/")[0:-1])):
            os.makedirs("/".join(self.options["out_file"].split("/")[0:-1]))
            
    def __str__(self):
        return(self.run_string)
        
    def run(self):
        sys.stderr.write("Running Linnaeus.\n%s\n" % self.run_string)
        subprocess.call(self.run_string.split())
        if not os.path.isfile(self.options["out_file"]):
            sys.stderr.write("\nUnable to produce tag file %s...Aborting.\n\n" % self.options["out_file"])
            sys.exit(0)
        
def hash_linnaeus_file(linnaeus_file):
        """
            Build dictionaries from Linnaeus output files.
        """
        lin_dict = {}
        for line in open(linnaeus_file):
            line_split = line.split("\t")
            if not "#" in line_split[0]:
                try:
                    lin_dict[line_split[1]][0].append((int(line_split[2]), int(line_split[3])))
                    lin_dict[line_split[1]][1].append(line_split[0])
                    lin_dict[line_split[1]][2].append(line_split[4])
                except (KeyError, AttributeError):
                    lin_dict[line_split[1]] = [[(line_split[2], line_split[3])],
                                            [line_split[0]],
                                            [line_split[4]]]
        return lin_dict
            
class LinnaeusDictBySubject(object):
    def __init__(self, species_path, inters_path):
        self.species = {}
        self.interactions = {}
        self.populate(self.species, species_path)
        self.populate(self.interactions, inters_path)
        
    def add_linnaeus_file(self, linn_dict, linn_file):
        """
            Converts a Linnaeus output file to a dict.
            Includes counts of discrete spp. in an article
        """
        subject = os.path.basename(linn_file).split("_")[0]
        linn_dict[subject] = hash_linnaeus_file(linn_file)
        for article in linn_dict[subject]:
            linn_dict[subject][article].append(set(linn_dict[subject][article][1]))
            linn_dict[subject][article].append(len(linn_dict[subject][article][3]))
        sys.stderr.write("added %s to linn_dict.\n" % subject)
    
    
    def populate(self, linn_dict, path):
        linnaeus_dir = os.listdir(path)
        for l in linnaeus_dir:
            self.add_linnaeus_file(linn_dict, os.path.join(path, l))

#a = Tagger(**lin_opts(1,1))
#a.run()

#java -Xmx2G -jar $LINNAEUS/bin/linnaeus-1.5.jar --properties $DATA/species_tags/species.conf --textDir $DATAARCHIVE/pure/plos1Ecology --out $DATA/species_tags/tag_files/EcologySpecies.tsv

