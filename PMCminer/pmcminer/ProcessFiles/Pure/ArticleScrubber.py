import os
import sys
import codecs

from  control import settings
from pmcminer.ProcessFiles import Raw

def scrub_article(article_string, stops):
    """Remove artificial newlines left by tokenizer"""
    stops = ((i, i.rstrip("\n")+" ") for i in stops)
    for fragment in stops:
        article_string = article_string.replace(fragment[0], fragment[1])
    return(article_string)
    
def scrub_articles_from_root(source_dir, stops, updater = 500):
    """
        Runs through a whole directory, opens all files and removes newlines matching 
        stops.  Then saves back to the same file.
    """
    sys.stderr.write("Scrubbing extraneous newlines...\n")
    articles = Raw.generate_files(source_dir)
    article_strings = ({
                            "file": codecs.open(article, "r", "utf8").read(),
                            "path": article
                        } for article in articles)
    scrubbed_articles = ({
                            "file":scrub_article(a["file"], stops),
                            "path":a["path"]
                          } for a in article_strings)
    for n, scrubbed in enumerate(scrubbed_articles):
        fOut = codecs.open(scrubbed["path"], "w", "utf8")
        fOut.write(scrubbed["file"])
        fOut.close()
        if n % updater == 0:
            sys.stderr.write("%d articles scrubbed..." % n)
    sys.stderr.write("All scrubbed up.\n")
        
