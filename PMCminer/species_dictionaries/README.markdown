Building the species dictionaries
=================================


The species dictionary used for the analysis is a combination of the [Catalogue of Life](http://www.catalogueoflife.org) dictionaries for 2009 and 2010.
Various stopwords have been filtered out.
######The original distionaries are hosted here:
- 2009 : path
- 2010 : path

######to combine and remove stopwords:
    cat col2009ac\_dict.tsv col2010ac\_dict.tsv > full\_col.tsv
    species\_dict\_x\_years\_join.py full\_col.tsv
    col\_dict\_stopwords.py   # ensure the filepaths are correct


