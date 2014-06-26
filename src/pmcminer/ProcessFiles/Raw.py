import os
import sys
import shutil

import lxml.etree

from  control import settings
from pmcminer.ProcessFiles import Articles

def create_directories(names_dict, root):
    """Build directory structure in root according to names_dict"""
    for directory in names_dict:
        new_dir = os.path.join(root, directory)
        if not os.path.isdir(new_dir):
            os.makedirs(new_dir)

    
def generate_files(top_level):
    """generate paths to all files under top level"""
    for path, dirlist, filelist in os.walk(top_level):
        for name in filelist:
            yield os.path.join(path, name)

def get_DOI_list(DOI_dict):
    """Builds a dict of dicts of DOIs from a dict e.g. from settings.DOI_LISTS"""
    DOIs = {}
    for subject in DOI_dict:
        try:
            DOIs[subject] = dict((line.rstrip("\n"), None) for line in open(os.path.join(settings.DATA_DIR,
                                                            DOI_dict[subject]), "r"))
        except IOError, err:
            sys.stderr.write("Not a DOI list.\n%s" % err)
            sys.exit(0)
    return(DOIs)

def check_and_copy_DOI(DOI_dict, article_ID, data_dir, raw_article_dir, found_dict):
    """Copies article to subject dir if article_ID from XML article-meta in DOI_lists"""
    #print article_ID[0]
    for subject in DOI_dict:
        checker = False
        for item in article_ID[0]:
            if item in DOI_dict[subject] and item not in found_dict[subject]:
                checker = True
        if checker:
            shutil.copyfile(article_ID[1], 
                            os.path.join(data_dir, raw_article_dir, subject,
                            os.path.basename(article_ID[1])))
            found_dict[subject][item] = 1
    return (found_dict)
                
def collect_files_by_DOI(DOI_dict, archive_dir, data_dir, raw_article_dir, updater = 200):
    """
        iterates over all archived articles and copies files to subject dirs
        if article DOIs are in the DOI list.  
    """  
    archived_articles = generate_files(archive_dir)
    article_trees = ((Articles.parse_XML(article), article) for article in archived_articles)
    article_IDs = ((list(Articles.extract_element(tree[0],
                "front/article-meta/article-id")), tree[1]) for tree in article_trees)
    found_DOIs = dict(((key, {}) for key in settings.DOI_LISTS.keys()))
    for n, ID in enumerate(article_IDs):
        found_DOIs = check_and_copy_DOI(DOI_dict, ID, data_dir, raw_article_dir, found_DOIs)
        if n % updater == 0:
            sys.stderr.write( "%d files processed...\n" % n)

def extract_raw_articles(data_dir, raw_dir, doi_lists, archive_dir):
    """
        Main control function: This runs from pmcminer.py.
        Extracts files from archive according to doi list.
        puts in raw_dir.  Creates directories as needed.
    """
    raw_articles = os.path.join(data_dir, raw_dir)
    if not os.path.isdir(raw_articles):
        os.makedirs(raw_articles)
    create_directories(doi_lists, raw_articles)
    DOIs = get_DOI_list(doi_lists)
    collect_files_by_DOI(DOIs, 
                         archive_dir,
                         data_dir,
                         raw_dir,
                         updater = 500)

    
