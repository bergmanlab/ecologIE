##settings file for EcologIE PMCminer multi-species interactions extractor

from  nltk.data import load as NLTKload

#set directories for your own system...
ARCHIVE_DIR = "/home/david/Avidastuff/mining/pubmedoa/allPLos_One/"     # Your archive of PMC .xml files
BIN = "pmcminer"  

DATA_DIR = "/home/david/textmining/PMCdata"   # where you want to put your data

# These are below your DATA_DIR
RAW_ARTICLES_DIR = "raw_articles"
PURE_ARTICLES_DIR = "pure"
ANALYSIS_DIR = "analysis_fc"

#locations of databases in .tsv format
SPECIESDB = "/home/david/Avidastuff/mining/linnaeus/species/full_col_final.tsv"
INTERACTIONSDB = "/home/david/Avidastuff/mining/linnaeus/interactions/dict-community-ecology-interactions.tsv"

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
EXTRACT_RAW_ARTICLES_BY_DOI = True 

#copy processed article bodies to DATA_DIR/pure ?
PURIFY_ARTICLE_SET = True

TOKENIZER = NLTKload('tokenizers/punkt/english.pickle')

#Stopword linefeeds to be removed by ArticleScrubber:
STOPS = ["i.e.\n", "e.g.\n", "Refs.\n", " et al.\n", "Fig.\n", "cf.\n",
         "c.i.\n", " ca.\n", "spp.\n", " ver.\n", " ind.\n", " obs.\n"]
                
### LINNAEUS OPTIONS ###

#Run linnaeus tagger ?
TAG_SPECIES = True
TAG_INTERACTIONS = True

#linnaeus tags are stored relative to DATA_DIR
TAGS_DIR = "tags_fc"

#path to Linnaeus jar file
LINNAEUS_JAR = "/home/david/Avidastuff/mining/linnaeus/bin/linnaeus-1.5.jar"

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
#all files go to ANALYSIS_DIR

ANALYSE_INTERACTIONS = True
MULTISPP_INTERACTIONS = "multispecies_interactions.tsv"
ALL_INTERACTIONS = "all_interactions.tsv"
MULTISPP_INTERACTIONS_TABLE = "multispecies_interactions_table.tsv"

ANALYSE_LINNAEUS_FILES = True
SPP_PER_ARTICLE_FILE = "species_per_article.tsv"
INTERACTIONS_PER_ARTICLE_FILE = "interactions_per_article.tsv"
SPP_NUMBERS_FILE = "species_numbers.tsv"
UNAMBIG_SPP_NUMBERS_FILE = "species_numbers_unambig.tsv"
AMBIG_SPP_NUMBERS_FILE = "species_numbers_ambig.tsv"

SUMMARY_STATS = True
SUMMARY_SUBJECT_ORDER = ("Ecology", "Genomics", "Molecular", "Biochemistry")
SUMMARY_STATS_TABLE = "SummaryStats.tsv"     


