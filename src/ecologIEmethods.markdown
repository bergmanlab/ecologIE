﻿An exploration of mining species interaction data from the ecology literature.
==============================================================================
David Springate and Casey Bergman 2012 (Forthcoming)
----------------------------------------------------
###Materials and Methods

####Sourcing, extracting and tokenising articles:
1. The entire Open Access Subset from the [Pubmed Central repository FTP server](http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/) was downloaded on 29/09/2011.  The PLoS ONE directories in this archive comprised 40,015 full text articles as XML files.

2. The [PLoS API](http://api.plos.org/) allows for the downloading of article metadata from any of the PLoS journals based on a range of search terms.  Articles in PLoS ONE are  organised into different subject categories, each of which is effectively a mini-journal on that subject.  A Python script interfacing with the PLoS API was used to download DOI numbers corresponding to PLoS ONE articles in specific subject categoriese of Ecology, Molecular biology, Genetics/Genomics and Biochemistry.  The lists of DOIs were downloaded on 28/09/2011.

3. The downloaded DOIs were matched against the article-meta/article-id fields in the XML files from the PLoS ONE directories in the PMC OA subset. Text from the bodies (article text excluding abstracts, tables and references) of all articles in this set that had no subject overlap among the four categories were extracted. XML extraction and  processing was performed using the [lxml Python library](http://lxml.de/). The article bodies were tokenised into sentences using the punkt tokeniser from the python [nltk library](http://www.nltk.org/). Text from article bodies were stored in plain text files with one sentence per line in separate files for each article in separate directories for  each subject category. The article bodies were further post-processed to fix common problems of over-splitting by the tokeniser because of abbreviations that include full-stops as punctiation (e.g. “fig. 1”, “etc., “c.f.”).

4. Species and interactions were identified using a dictionary-based approach using the [Linnaeus system](http://linnaeus.sourceforge.net/).

5. A custom lexicon of community ecology terms (data/dict-community-ecology-interactions.tsv) was matched against full body text using Linnaeus (Case sensitive).  The resulting tags were stored in a separate file.

6. Linnaeus was also used to identify species names in the articles (Case insensitive).  Species name dictionaries were based on the combined [Catalogue of Life](http://www.catalogueoflife.org) 2009 and 2010 species names database, including scientific and common names.   .  Stopwords matching common words found in articles were removed from the dictionaries.

7. The frequency of unique species tags was recorded for all subject corpora.  Linnaeus cannot always resolve species to a unique tag.  For example, if ‘E. coli’ is mentioned in an article without the full species name, it could mean ‘Escherichia coli’ or ‘Entamoeba coli’.  Abbreviated names are tagged by Linnaeus as unambiguous names if a corresponding full name is used in the same article.  The percentage of ambiguous species tags for each subject corpora was recorded.  When calculating species numbers, the count for an ambiguously tagged species mention is divided equally between each of the putative species (Each species id accumulates  where n is the number of species ids in the ambiguous tag). We used standard diversity indices to analyse the richness and evenness of species tags in the different corpora.

8. The number of unique species and interaction tags in each article was calculated.

9. Species and interaction tags were combined to generate a table of sentences with more than 2 spp and at least 1 interaction term for all corpora (data/multispecies\_interactions.csv), based on the article body file coordinates in the output files from Linneaus.  For each sentence containing a putative multi-species interaction, the interaction type (according to our custom lexicon of community ecology terms) was scored.  Using this table, all articles were scored for presence or absence of each interaction term in a sentence  with at least 2 species.
