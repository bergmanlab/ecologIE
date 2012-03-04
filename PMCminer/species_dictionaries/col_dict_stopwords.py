#!/usr/bin/python2

import sys

species_file = "linnaeus/species/col2009_2010ac_dict_join.bak"
outfile = "linnaeus/species/col2009_2010ac_dict_join.tsv"

def remove_stopwords(line, stopdict):
    line = line.split("\t")
    species = "|".join((species for species in line[1].split("|") if species.lower() not in stopdict))
    return("\t".join((line[0], species)))

stopwords = ("black","white","pink","bung","near", "var", "red", "reds", "blacks", "whites", "pinks"
             "bars", "bar", "x", "clines", "box", "cline", "knife", "knifes",
             "drill", "cock-up", "glass", "million", "pilot", "roman", "romans", "banana", "bananas", "rocker", "rockers",
             "bleak", "puller", "pullers", "rainbow", "rainbows", "lumpy", "visitor", "visitors", "pop", "split", 
             "splits", "spring", "spot", "spots", "whitney", "john", "moon", "scavenger", "rock", "rubbish", "spanish", "king",
             "rough","kit", "xs", "xi", "lookup", "available", "fisher", "permit", "e", "es", "lizard", "lizards")

stopdict = dict(((word, None) for word in stopwords))
species = (remove_stopwords(line, stopdict) for line in open(species_file))

if outfile:
    f = open(outfile, "w")
else:
    f = sys.stdout.write
sys.stderr.write("Writing species dict to %s...\n" % outfile)
for i in species:
    f.write(i)

if outfile:
    f.close()
sys.stderr.write("Done\n")


