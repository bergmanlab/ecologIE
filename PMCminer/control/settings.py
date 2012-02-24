##settings file for EcologIE PMCminer multi-species interactions extractor

from  nltk.data import load as NLTKload

#set directories
ARCHIVE_DIR = "/home/david/textmining/pubmedoa/allPLos_One/"
BIN = "pmcminer"

DATA_DIR = "/home/david/textmining/PMCdata"
RAW_ARTICLES_DIR = "raw_articles"
PURE_ARTICLES_DIR = "pure"
ANALYSIS_DIR = "analysis"

#locations of databases in .tsv format
SPECIESDB = "/home/david/textmining/linnaeus/species/col2009_2010ac_dict_join.tsv"
INTERACTIONSDB = "/home/david/textmining/linnaeus/interactions/dict-community-ecology-interactions.tsv"

#State the doi lists to be used for the analysis 
#DOI lists must be kept in DATA_DIR
#These names must be correct, even if you are not re-extracting the raw articles
#Downstream analysis relies on the  keys being correct
DOI_LISTS = {
        "Ecology": "DOI_lists/subjectEcology",
        "Molecular": "DOI_lists/subjectMolecular",
        "Genomics": "DOI_lists/subjectGenomics",
        "Biochemistry": "DOI_lists/subjectBiochemistry"
    }

#Match DOIs with articles in ANALYSIS_DIR and copy to DATA_DIR/raw_articles ?
EXTRACT_RAW_ARTICLES_BY_DOI = False

#copy processed article bodies to DATA_DIR/pure ?
PURIFY_ARTICLE_SET = False

TOKENIZER = NLTKload('tokenizers/punkt/english.pickle')

#Stopwords to be removed by ArticleScrubber:
STOPS = ["i.e.\n", "e.g.\n", "Refs.\n", " et al.\n", "Fig.\n", "cf.\n",
         "c.i.\n", " ca.\n", "spp.\n", " ver.\n", " ind.\n", " obs.\n"]
                
### LINNAEUS OPTIONS ###

#Run linnaeus tagger ?
TAG_SPECIES = False
TAG_INTERACTIONS = False

#linnaeus tags are stored relative to DATA_DIR
TAGS_DIR = "tags"

#path to Linnaeus jar file
LINNAEUS_JAR = "/home/david/textmining/linnaeus/bin/linnaeus-1.5.jar"

#How much RAM to allocate to Linnaeus? 
#Should be high enough to accommodate the loading of the entity dictionaries. 
#See guide-linneaus.txt for more details
LINNAEUS_MEMORY = "4G"

# Linnaeus conf files should be kept in  control directory
LINNAEUS_CONF = (
                    {
                        "tags": "species",
                        "conf_file": "control/species.conf"
                    },
                    {
                        "tags": "interactions",
                        "conf_file": "control/interactions.conf"
                    },
                 )

### ANALYSIS OPTIONS ###

ANALYSE_INTERACTIONS = False
MULTISPP_INTERACTIONS = "multispecies_interactions.csv"
ALL_INTERACTIONS = "all_interactions.csv"
MULTISPP_INTERACTIONS_TABLE = "multispp_interactions_table.csv"

ANALYSE_LINNAEUS_FILES = False
SPP_PER_ARTICLE_FILE = "spp_per_article.csv"
INTERACTIONS_PER_ARTICLE_FILE = "interactions_per_article.csv"
SPP_NUMBERS_FILE = "spp_numbers.csv"
UNAMBIG_SPP_NUMBERS_FILE = "spp_numbers_unambig.csv"
AMBIG_SPP_NUMBERS_FILE = "spp_numbers_ambig.csv"

SUMMARY_STATS = True
SUMMARY_SUBJECT_ORDER = ("Ecology", "Genomics", "Molecular", "Biochemistry")
SUMMARY_STATS_TABLE = "SummaryStats.csv"     


