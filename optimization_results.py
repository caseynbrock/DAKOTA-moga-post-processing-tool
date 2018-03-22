# optimization_results.py
#
# reads output files from DAKOTA moga run and packages data into a class.
# The class can then be used by another script for plotting
# or further post processing
#
# WARNING: design point numbers 0-indexed in pandas database, but 
# eval_id column is the original 1-indexed value given by DAKOTA
#
# By default, looks for 'JEGAGlobal.log' and 'pp_moga.log' in current
# directory, but other files can be specified
# 
# 
#
# 
# The MIT License
# 
# Copyright (c) 2017 caseynbrock
# 
# Permission is hereby granted, free of charge, 
# to any person obtaining a copy of this software and 
# associated documentation files (the "Software"), to 
# deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, 
# merge, publish, distribute, sublicense, and/or sell # copies of the Software, and to permit persons to whom # the Software is furnished to do so, # subject to the following conditions: # 
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
import matplotlib.pyplot as plt


class MogaOptimizationResults(object):
    # panda database along with several other attributes of the results
    def __init__(self, global_log='JEGAGlobal.log', dakota_tabular_log='dakota_tabular.dat',
                 truncate=None):
        self.global_log = global_log
        self.dakota_tabular_log = dakota_tabular_log
        self.all_points = pd.read_csv(self.dakota_tabular_log, delimiter=r'\s+')
        if truncate != None:
            self._truncate_high_objectives(truncate[0], truncate[1])
        self.gen_size_list = self._get_gen_sizes()
        self._add_gen_numbers()
        self.pareto_front = self._get_pareto_fronts()
        
    def _get_gen_sizes(self):
        """ read generation sizes from JEGA log or DAKOTA's stdout """
        gens = []
        with open(self.global_log) as fin:
            for line in fin:
                if 'evaluations so far.' in line:
                    gens.append(int(line.split()[-4]) - sum(gens))
                if 'Global Log ' in line:
                    gens = []  # restart gen list if optimization was restarted
        return gens

    def _add_gen_numbers(self):
        """ add column for generation number in pandas database """
        gen_index_list = [] #labels each design point with its generation number
        for i, gen_size in enumerate(self.gen_size_list):
            gen_index_list += gen_size*[i]
        self.all_points['generation'] = gen_index_list

    def _get_pareto_fronts(self):
        """ find pareto front """
        pfront = pareto_frontier(self.all_points, 'obj_fn_1', 'obj_fn_2')
        return pfront

    def _truncate_high_objectives(self, obj1_thresh, obj2_thresh):
        """ sets design points with objectives above a threshhold
        as NaN.
        I added this because sometimes I return artificially high
        objectives to DAKOTA as error codes, and I don't need these
        for post-processing.
        """
        # don't completely remove the lines because that will mess up
        # processing based on generation sizes
        trunc_indices_1 = self.all_points[self.all_points['obj_fn_1']>obj1_thresh].index
        trunc_indices_2 = self.all_points[self.all_points['obj_fn_2']>obj2_thresh].index
        self.all_points = self.all_points.set_value(trunc_indices_1, ['obj_fn_1'], None)
        self.all_points = self.all_points.set_value(trunc_indices_2, ['obj_fn_2'], None)

    def plot_objective_space(self, legend_label=None):
        """ quick densty plot of design space and pareto front. 
        Not flexible yet 
        """
        xbins = 10**np.linspace(-3, 0, 200)
        ybins = 10**np.linspace(-2, 0, 200)
        counts, _, _ = np.histogram2d(self.all_points['obj_fn_1'], self.all_points['obj_fn_2'], 
                                      bins=(xbins, ybins))
        # needs to be rotated and flipped # also mask out 0s 
        counts = np.rot90(counts)
        counts = np.flipud(counts)
        counts = np.ma.masked_where(counts==0,counts)

        # design space        
        fig, ax = plt.subplots()
        #ax.pcolormesh(xbins, ybins, counts, cmap='hot')
        ax.pcolormesh(xbins, ybins, counts)
        ax.set_xscale('log')
        ax.set_yscale('log')

        # pareto front
        plt.plot(self.pareto_front['obj_fn_1'], self.pareto_front['obj_fn_2'], 'r-', 
                 label=legend_label)

        plt.xlabel('objective function 1')
        plt.ylabel('objective function 2')
        plt.grid(True, which="both")
        return fig, ax
        
    def plot_pareto_front(self):
        """ plot just the pareto front """
        plt.plot(self.pareto_front['obj_fn_1'], self.pareto_front['obj_fn_2'], 'r.-')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('objective function 1')
        plt.ylabel('objective function 2')
        plt.grid(True, which="both")


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
