#!/usr/bin/python2

import sys

def tsv_to_dict(spp_tsv):
    """
        Convert a .tsv species names file to a Python dict with multiple IDs joined 
        to single lines.  Prints to stdout.
    """
    sys.stderr.write("Joining dictionary...\n")
    tsv = open(spp_tsv)
    spp_dict = {}
    for line in tsv:
        line = line.split("\t")
        try:
            spp_dict[line[0].split(":")[1]] = spp_dict[line[0].split(":")[1]] + "|" + line[1].rstrip("\n")
        except KeyError:
            spp_dict[line[0].split(":")[1]] = line[1].rstrip("\n")
    return(spp_dict)

def remove_redundancy(spp_dict):
    """reduces each line to the set of that line"""
    for key in spp_dict:
        line = set(spp_dict[key].split("|"))
        spp_dict[key] = "|".join(line)


def print_species_dict(spp_dict, outfile):
    """Prints a species dict to file or stdout if no outfile"""
    if outfile:
        f = open(outfile, "w")
        sys.stderr.write("Writing to file...\n")
    else:
        f = sys.stdout
    f.writelines((k + "\t" + v + "\n" for (k,v) in spp.iteritems()))
    if outfile:
        f.close()
        sys.stderr.write("New species dictionary written to %s\n" % outfile)


if __name__ == "__main__":
    species_dict = sys.argv[1]
    if len(sys.argv) > 2:
        new_dictionary = sys.argv[2]
    else:
        new_dictionary = ""
    spp = tsv_to_dict(species_dict)
    remove_redundancy(spp)
    print_species_dict(spp, new_dictionary)
