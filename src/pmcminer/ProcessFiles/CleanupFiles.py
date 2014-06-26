import fileinput
import sys

def cleanup_spp_file(spp_file):
    for line in fileinput.input(spp_file, inplace = True):
        line=line.replace("'","")
        #sys.stdout is redirected to the file
        sys.stdout.write(line)

