Building the species dictionaries
=================================


The species dictionary used for the analysis is a combination of the [Catalogue of Life](http://www.catalogueoflife.org) dictionaries for 2009 and 2010.
Various stopwords have been filtered out.
######The original dictionaries are hosted here:
- 2009 : path
- 2010 : path

######to combine and remove stopwords:
    cat col2009ac_dict.tsv col2010ac_dict.tsv > full_col.tsv
    species_dict_x_years_join.py full_col.tsv
    col_dict_stopwords.py   # ensure the filepaths are correct


