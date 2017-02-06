# optimization_results.py
#
# reads output files from DAKOTA moga run and packages data into a class.
# The class can then be used by another script for plotting
# or further post processing
#
# WARNING: design point numbers 0-indexed in pandas database, but 
# eval_id column is the original 1-indexed value given by DAKOTA
#
#
# 
# The MIT License
# 
# Copyright (c) 2011 Dominic Tarr
# 
# Permission is hereby granted, free of charge, 
# to any person obtaining a copy of this software and 
# associated documentation files (the "Software"), to 
# deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom 
# the Software is furnished to do so, 
# subject to the following conditions:
# 
# The above copyright notice and this permission notice 
# shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR 
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import numpy as np
import pandas as pd

### USER PARAMETERS
logfile_name = 'pp_moga.log'
dakota_tabular_filename = 'dakota_tabular.dat'
###################

class MogaOptimizationResults(object):
    # panda database along with several other attributes of the results
    def __init__(self, output_files_directory):
        self.all_design_points_db = pd.read_csv(dakota_tabular_filename, 
                                                delim_whitespace=True)
        self.gen_size_list = self._get_gen_sizes()
        self._add_gen_numbers()
        self.pareto_front = self._get_pareto_fronts()
        
    def _get_gen_sizes(self):
        gens = []
        with open(logfile_name) as fin:
            for line in fin:
                if 'evaluations so far.' in line:
                    gens.append(int(line.split()[-4]) - sum(gens))
        return gens

    def _add_gen_numbers(self):
        """ add column for generation number in pandas database """
        gen_index_list = [] #labels each design point with its generation number
        for i, gen_size in enumerate(self.gen_size_list):
            gen_index_list += gen_size*[i]
        self.all_design_points_db['generation'] = gen_index_list

    def _get_pareto_fronts(self):
        """ find pareto front """
        pfront = pareto_frontier(self.all_design_points_db, 'obj_fn_1', 'obj_fn_2')
        return pfront


def pareto_frontier(df, obj1='obj_fn_1', obj2='obj_fn_2'):
    """ 
    Finds a 2D pareto front of obj1 and obj2, which are objectives in a
    two objective optimization,
    This assumes that lower objectives are better.
    points can be pulled from the all points database.
    returns pareto front as a pandas database where the indices are 
    retained from the all points data frame.
    This could be optimized a lot better.
    """
    sorted_df = df.sort_values([obj1, obj2])
    pareto_front = sorted_df.iloc[[0]].copy()  # initialize pareto front
    for i in sorted_df.index[1:]:
        if sorted_df.loc[i].obj_fn_2 < pareto_front.iloc[-1].obj_fn_2:
            pareto_front = pareto_front.append(sorted_df.loc[[i]].copy()) 
    return pareto_front
