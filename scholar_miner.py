# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 21:18:26 2019

@author: Markus Borg
"""

from scholar import Scholar
from datetime import date
import time
import dblp

sci_list = ["IEEE Trans. Software Eng.", "Empirical Software Engineering", "ACM Trans. Softw. Eng. Methodol.", "Autom. Softw. Eng.", "Information & Software Technology", "Requir. Eng.", " Software and System Modeling", "Software Quality Journal", "Journal of Systems and Software", "Journal of Software: Evolution and Process", "Softw. Test., Verif. Reliab.", "Softw., Pract. Exper.", "IET Software", "International Journal of Software Engineering and Knowledge Engineering"]

class ScholarMiner:
    
    def __init__(self):
        self.output_file = open(str(date.today()) + "_output.txt","w+")
        self.scholars = {}
            
    def process_group(self, researchers):
        nbr_remaining = len(researchers)
        while nbr_remaining > 0:
            for scholar, processed in researchers.items():	
                if not processed: # only proceed if the scholar hasn't been processed already
                    try:
                        print("\n####### Processing scholar: " + scholar + " #######")
                        authors = dblp.search(scholar)
                        search_res = authors[0]
                    except:
                        print("ERROR: Invalid search result from DBLP. Waiting...")
                        time.sleep(5)
                        break
                    
                    current = Scholar(scholar)
                    self.scholars[scholar] = current
                                        
        			# initiate variables
                    nbr_publications = len(search_res.publications)
                    print("DBLP entries: ", nbr_publications)
                    top_papers = []
                    nbr_arxiv = 0
                    nbr_first_authorships = 0
                    nbr_first_top = 0
                    total_text = ""
        				
        			# traverse publications
                    for p in search_res.publications:
        				#temp.add_publication(p.title)
                        try:
                            time.sleep(0.5) # There appears to be some race condition in the dblp package	
                            print(p.title, " ", p.type, " ", p.journal)
                            co_authors = p.authors
        					# count SCI journals and how many as first author
                            if p.type == "article":
                                if p.journal == "CoRR": #skip ArXiv preprints
                                    nbr_arxiv += 1
                                    continue
                                elif p.journal in sci_list:
                                    #sci_journal = True
                                    top_papers.append(p.title)
                                    if (co_authors[0] == scholar):
                                        nbr_first_top += 1
                                        total_text += "-" + p.title + "\n"
                                if len(co_authors) > 0:
                                    if co_authors[0] == scholar:
                                        nbr_first_authorships += 1
        						#temp.publications.add(Publication(p.title, p.journal, sci_journal, len(co_authors))
        					    #print(co_authors) # used to find authors with a number, e.g., "Thomas Olsson 0001".
                        except:
                            print("ERROR. Processing one of the papers failed. Waiting...")
                            time.sleep(5)
                            break
                        self.scholars[scholar].add_publication(p)
                    nbr_publications -= nbr_arxiv
                    if nbr_publications > 0:
                        seed_ratio = nbr_first_authorships / nbr_publications
                        quality_ratio = len(top_papers) / nbr_publications
                    else:
                        seed_ratio = "N/A"
                        quality_ratio = "N/A"
                        
                    result_string = scholar + " (" + str(nbr_publications) + " publ., First-in-top: " + str(nbr_first_top) + ") \t\t ### Self-made ratio: " + str(seed_ratio) + " \t Quality ratio: " + str(quality_ratio) + "\n"
                    result_string += total_text
                    processed = True
                    print("Scholar processed: " + scholar)
                    nbr_remaining -= 1
                    self.output_file.write(result_string)
            
        self.output_file.close()
    
    def get_scholars(self):
        return self.scholars
    
    def print_scholars(self):
        tmp = open(str(date.today()) + "_ATTEMPT.txt","w+")
        for scholar in self.scholars.items():
            tmp.write(str(scholar) + "\n")
        tmp.close()