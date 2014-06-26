#!/usr/bin/python2

import os

from  control import settings

"""
    Executable for PMCminer app for extracting species and ecological 
    interaction terms from PMCOASS XML files
"""

if settings.EXTRACT_RAW_ARTICLES_BY_DOI:
   from pmcminer.ProcessFiles import Raw
   Raw.extract_raw_articles(data_dir = settings.DATA_DIR, 
                            raw_dir = settings.RAW_ARTICLES_DIR, 
                            doi_lists = settings.DOI_LISTS, 
                            archive_dir = settings.ARCHIVE_DIR)
   
if settings.PURIFY_ARTICLE_SET:
    from pmcminer.ProcessFiles.Pure import PurifyArticleSet
    from pmcminer.ProcessFiles.Pure import ArticleScrubber
    PurifyArticleSet.purify_articles(settings.DATA_DIR, settings.RAW_ARTICLES_DIR,
                                     settings.DOI_LISTS, settings.PURE_ARTICLES_DIR)
    ArticleScrubber.scrub_articles_from_root(source_dir = os.path.join(settings.DATA_DIR,
                                                            settings.PURE_ARTICLES_DIR), 
                                                            stops = settings.STOPS)
if settings.TAG_SPECIES:
    from pmcminer.Linnaeus.PyLinnaeus import *
    for subject in range(len(settings.DOI_LISTS)):
        spp_tagger = Tagger(**lin_opts(0,subject))
        spp_tagger.check_directories()
        spp_tagger.run()


if settings.TAG_INTERACTIONS:
    from pmcminer.Linnaeus.PyLinnaeus import *
    for subject in range(len(settings.DOI_LISTS)):
        inter_tagger = Tagger(**lin_opts(1,subject))
        inter_tagger.check_directories()
        inter_tagger.run()


if settings.ANALYSE_INTERACTIONS:
    from pmcminer.Analysis import AnalyseInteractions, BuildInteractionsTable
    if not os.path.isdir(os.path.join(settings.DATA_DIR, settings.ANALYSIS_DIR)):
        os.makedirs(os.path.join(settings.DATA_DIR, settings.ANALYSIS_DIR))
    AnalyseInteractions.get_multispp_interactions(subjects = settings.DOI_LISTS, 
                tag_path = os.path.join(settings.DATA_DIR, settings.TAGS_DIR), 
                pure_path = os.path.join(settings.DATA_DIR, settings. PURE_ARTICLES_DIR),
                multi_file = os.path.join(settings.DATA_DIR, settings.ANALYSIS_DIR,
                                                        settings.MULTISPP_INTERACTIONS), 
                all_file = os.path.join(settings.DATA_DIR, settings.ANALYSIS_DIR,
                                                            settings.ALL_INTERACTIONS))
    BuildInteractionsTable.build_table(
                                       in_file = os.path.join(settings.DATA_DIR, 
                                                settings.ANALYSIS_DIR, 
                                                settings.MULTISPP_INTERACTIONS),
                                       out_file = os.path.join(settings.DATA_DIR, 
                                                settings.ANALYSIS_DIR, 
                                                settings.MULTISPP_INTERACTIONS_TABLE),
                                       pure_path = os.path.join(settings.DATA_DIR,
                                                              settings.PURE_ARTICLES_DIR),
                                       interaction_db = settings.INTERACTIONSDB
                                       )

if settings.ANALYSE_LINNAEUS_FILES:
    from pmcminer.Analysis import AnalyseLinnaeusFiles
    from pmcminer.ProcessFiles import CleanupFiles
    AnalyseLinnaeusFiles.get_linnaeus_stats(
                        data_dir  = settings.DATA_DIR, 
                        pure_dir = settings.PURE_ARTICLES_DIR,
                        tags_dir = settings.TAGS_DIR,
                        analysis_dir = settings.ANALYSIS_DIR,
                        spp_db = settings.SPECIESDB,
                        spp_per_article = settings.SPP_PER_ARTICLE_FILE, 
                        interactions_per_article = settings.INTERACTIONS_PER_ARTICLE_FILE,
                        species_numbers = settings.SPP_NUMBERS_FILE,
                        unambiguous_species_numbers = settings.UNAMBIG_SPP_NUMBERS_FILE,
                        ambiguous_species = settings.AMBIG_SPP_NUMBERS_FILE
                       )
    CleanupFiles.cleanup_spp_file(os.path.join(settings.DATA_DIR, 
                                                settings.ANALYSIS_DIR,
                                                settings.SPP_NUMBERS_FILE))
    CleanupFiles.cleanup_spp_file(os.path.join(settings.DATA_DIR, 
                                                settings.ANALYSIS_DIR,
                                                settings.UNAMBIG_SPP_NUMBERS_FILE))
    
if settings.SUMMARY_STATS:
    from pmcminer.Analysis import SummaryStats
    summary_table = SummaryStats.Summary(
                        data_dir = settings.DATA_DIR, 
                        raw_dir = settings.RAW_ARTICLES_DIR,
                        pure_path = settings.PURE_ARTICLES_DIR,
                        subjects = settings.DOI_LISTS,
                        speciesDb = settings.SPECIESDB,
                        species_tags_path = os.path.join(settings.DATA_DIR,
                                                settings.TAGS_DIR, "species"),
                        interactions_tags_path = os.path.join(settings.DATA_DIR,
                                                settings.TAGS_DIR, "interactions"),
                        species_numbers_file = os.path.join(settings.DATA_DIR,
                                            settings.ANALYSIS_DIR, settings.SPP_NUMBERS_FILE),
                        multispp_inter_file = os.path.join(settings.DATA_DIR,
                                        settings.ANALYSIS_DIR, settings.MULTISPP_INTERACTIONS), 
                        spp_per_article_file = os.path.join(settings.DATA_DIR,
                                        settings.ANALYSIS_DIR, settings.SPP_PER_ARTICLE_FILE),
                        interactions_per_article_file = os.path.join(settings.DATA_DIR,
                            settings.ANALYSIS_DIR, settings.INTERACTIONS_PER_ARTICLE_FILE)
                                        )
    summary_table.print_summary_stats(subjects = settings.SUMMARY_SUBJECT_ORDER,
                                    out_file = os.path.join(settings.DATA_DIR, 
                                        settings.ANALYSIS_DIR, 
                                        settings.SUMMARY_STATS_TABLE))
        
    
