Data from Springate and Bergman 2012 (forthcoming):
---------------------------------------------------
An exploration of mining species interaction data from the ecology literature.
-----------------------------------------------------------------------------

This directory contains:

* *dict-community-ecology-interactions.tsv* - dictionary of ecological interaction terms used to tag articles.

* *DOI\_lists*
    files containing a list of doi codes downloaded from the PLoS API.
    They reference all articles in PLoS One for the following subject categories:
    - ecology
    - Molecular biology
    - Genomics
    - Biochemistry
    The lists of dois were downloaded on 28/9/2011

* *analysis*:
    The output files from a run of ecologIE/PCminer, based on a complete archive of PLoS One articles downloaded via FTP from the PMC OASS on 29/9/2011.
    includes:
    - all\_interactions.csv - a flatfile of every putative  ecological interaction termfound by the Linnaeus tagger in all  subject corpora.  Includes subject, article file name, doi, interaction id (from interaction dictionary), interaction term (as found in the article), the sentence in which the term was found.
    - interactions\_per\_article.csv - Counts of the number of interactions found in all articles
    in each corpus.
    - multispecies\_interactions.csv - flatfile of all putative multispecies interactions found in all corpora. Putative multispecies interactions are classified as a tagged ecological interaction term in the same sentence as two different tagged species. Includes subject, article file name, doi, species id (from database), species name, interaction id, interaction name, sentence.
    - multispp\_interactions\_table.csv - table of 0/1 (absence/presence) of multispp-interactions of each category for all articles in all corpora
     - spp\_per\_article.csv - number of unique species tags in each article in each
     subject corpus.
     - SummaryStats.csv - Some per subject summary stats

Not included (lots of files/big files):
- archived PLoS One article files
- corpora of article bodies for each subject
- species dictionary
- Linnaeus output files

David dot springate at postgrad dot manchester dot ac dot uk
