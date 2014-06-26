"""
    Checks for DOIs matching multiple filenames in raw articles.
    Worth checking if there are more files than DOIs 
"""
import sys
import os

from pmcminer.ProcessFiles import Raw, Articles
from  control import settings

def check_DOI_by_dict(DOI_dict, article_ID, data_dir, raw_article_dir):
    """generate subject, DOI and filename for PMC XML file"""
    for subject in DOI_dict:
        for item in article_ID[0]:
            if item in DOI_dict[subject]:
                yield (subject, item, article_ID[1])
                

DOIs = Raw.get_DOI_list(settings.DOI_LISTS)

archived_articles = Raw.generate_files(settings.ARCHIVE_DIR)
article_trees = ((Articles.parse_XML(article), article) for article in archived_articles)
article_IDs = ((list(Articles.extract_element(tree[0],
                "front/article-meta/article-id")), tree[1]) for tree in article_trees)

check_dict = dict(((key, {}) for key in settings.DOI_LISTS.keys()))

#for ID in article_IDs:
for n, ID in enumerate(article_IDs):
    checker = check_DOI_by_dict(DOIs, ID, settings.DATA_DIR, settings.RAW_ARTICLES_DIR)
    for i in checker:
        try:
            check_dict[i[0]][i[1]].append(i[2])
        except KeyError:
            check_dict[i[0]][i[1]] = [i[2]]
    if n % 500 == 0:
        sys.stderr.write( "%d files processed...\n" % n)
 
#are there dois which are in mulitple files in the directory?
multiple_files_for_DOIs = dict((k,v) for (k, v) in check_dict["Ecology"].items() if len(v) > 1)
#list of multiple files for a doi that have different file size (in kb).
# Essesntially, are they the same file?
[(x, y) for (x,y) in multiple_files_for_DOIs.values() if os.path.getsize(x)/1024 != os.path.getsize(y)/1024 ]

 
 
