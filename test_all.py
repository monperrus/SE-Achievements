# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:50:30 2019

@author: Markus Borg
"""

from scholar_miner import ScholarMiner

class TestClass:

    def setup_method(self, module):
        self.scholars = None
        self.test_scholar = {"David Notkin":False}
        self.miner = ScholarMiner()
        
    def test_david_notkin(self):
        self.miner.process_group(self.test_scholar)
        self.scholars = self.miner.get_scholars()
        dblp_search_res = self.scholars["David Notkin"]

        # TC1: Test that DBLP returns a result
        assert self.scholars != None
        
        # TC2: Test that David Notkin has 151 DBLP entries
        assert len(dblp_search_res.publications) == 151
        
        # TC3: Get David Notkin as an SEScholar
        scholars = self.miner.get_scholars()
        david = scholars["David Notkin"]
        assert david.name == "David Notkin"
        
        # TC4: Test that David Notkin has 151 publications after removing duplicates
        assert david.get_nbr_publications() == 151
        
        # TC5: Test that David Notkin has 35 publications in SCI-listed journals
        assert david.get_nbr_sci_publications() == 35
    