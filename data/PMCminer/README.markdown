Data from Springate ... & Bergman (2012) An exploration of mining species interaction data from the ecological literature (forthcoming).
-----------------------------------------------------------------------------

This directory contains:

* *dict-community-ecology-interactions.tsv* - a dictionary of terms describing types of interactions in community ecololgy used to tag articles.

* *DOI\_lists*
    Files listing DOIs of articles in PLoS One downloaded using the PLoS API (28/9/2011) for the following subject categories:
    - Ecology
    - Molecular biology
    - Genomics
    - Biochemistry

* *analysis*:
    Output files from a run of ecologIE/PMCminer system based on a complete archive of PLoS One articles downloaded via FTP from the PMC Open Access subset (29/9/2011), including:
    - all\_interactions.tsv - a tab separated value text file of every putative ecological interaction term found by the Linnaeus tagger in all subject corpora. Columns include subject category, PMC article file name, DOI, species id list, species name list, interaction type id (from dict-community-ecology-interactions.tsv), interaction term trigger (as found in the article), and the sentence in which the interaction term was found.
    - interactions\_per\_article.tsv - a tab separated value text file of counts of the number of interactions found in all articles in each corpus. Columns include subject category, PMC article file name, DOI, and the number of interactions.
    - multispecies\_interactions.tsv - a tab separated value text file of all putative multispecies interactions found in all corpora. Putative multispecies interactions are classified as a tagged ecological interaction term in the same sentence as two different tagged species. Columns include subject category, PMC article file name, DOI, species id list, species name list, interaction id, interaction name, sentence.
    - multispecies\_interactions\_table.tsv - a tab separated value text file with presence/absence of multispecies interaction type for all articles in all corpora. Columns include subject category, PMC article file name, DOI, and presence (1) or absence (0) for each multispecies interaction type.
    - species\_per\_article.tsv - a tab separated value text file of the number of unique species tags in each article in each subject corpus. Columns include subject category, PMC article file name, DOI, and the number of species.
    - SummaryStats.tsv - a tab separated value text file of subject category summary statistics.


######Additional files
- [Species dictionary](http://bergman.smith.man.ac.uk/data/ecologie/full_col_final.tsv)
- [Archive of PLoS One PMC XML files](http://bergman.smith.man.ac.uk/data/ecologie/raw.tgz)
- [Full text of article bodies](http://bergman.smith.man.ac.uk/data/ecologie/pure.tgz)
- [Linnaeus output files](http://bergman.smith.man.ac.uk/data/ecologie/tags.tgz)


######Contact 
- david dot springate at postgrad dot manchester dot ac dot uk
- casey dot bergman at manchester dot ac dot uk

