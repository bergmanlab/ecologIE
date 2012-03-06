EcologIE PMCMiner  - Tools for extracting putative multispecies interaction data from articles in the Pubmed Open Access Subset.
================================================================================================================================
V.0.1 (22/Feb/2012)
------------------

###David A. Springate and Casey Bergman, Faculty of Life Sciences, University of Manchester

Includes a Python wrapper for the [Linnaeus entity recognition tool](http://linnaeus.sourceforge.net/).

The pmcminer.py file is the main executable to replicate the analyses in **An exploration of mining species interaction data from the ecology literature**, Springate and Bergman 2012 (forthcoming).

#####To do this you need...
- A directory containing the PLoSONE XML archive
- A set of DOIs from the PLoS API
- A working copy of Linnaeus
- Species names dictionary
- Ecological Interaction terms dictionary 
- Python 2.7 (It may work on earlier versions but is untested)

#####...and the following Python libraries:
- lxml
- nltk with punkt tokeniser from nltk.data
- numpy
- scipy
 
 Running *pmcminer.py*  should find articles matching DOIs,  extract and tokenise article bodies,  match species and interaction terms using Linnaeus, build tables of sentences containing putative multispecies interactions and various other summary tables presented in the paper.

The tools are designed to be modular and pluggable to facilitate use in other projects. 
All directory and path logic is in settings.py in the control folder.


For questions, suggestions or bug reports, please contact David Springate:
david dot springate at postgrad dot manchester dot ac dot uk
####To do:
* Upload script for downloading DOIs from PLoS API
* Upload species and ecological interactions databases
* Upload R analysis scripts for Springate and Bergman 2012 paper.
* Fix the horrible hack that allows the diversity function to work.
