# read_log.m
#
# reads output files from a moga run.
# the created arrays can then be used by another script for plot 
# or further post processing
#
# design_var_names: array of design variable names 
# design_vars: design variable values for all design points (size n by n_vars)
# accu: accuracy objectives of all design points
# work: work objectives of all design points
# n: number of design points 
# 
# vars_final: design variable values for pareto front (size n_final x n_vars)
# accu_final: accuracy objectives of all pareto points
# work_final: work objectives of all pareto points
# n_final: number of pareto points
#
# gens: generation number of each design point (array size nx1)
# the design points are grouped into generations

# edit to include atan AND work objectives
# generation numbers start at 0
# WARNING: design point numbers 0 indexed in pandas database, but 1st column is the original 1 indexed value given by DAKOTA

import numpy as np
import pandas as pd

### USER PARAMETERS
logfile_name = 'pp_moga.log'
dakota_tabular_filename = 'dakota_tabular.dat'
###################

class JegaOptimizationResults(object):
    # panda database along with several other attributes of the results
    def __init__(self, output_files_directory):
        self.all_design_points_db = pd.read_csv(dakota_tabular_filename, 
                                                delim_whitespace=True)
        self.gen_size_list = self._get_gen_sizes()
        self._add_gen_numbers()
        self._get_pareto_fronts()
        
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
        # find pareto front at each generation        
        pf = pareto_frontier(self.all_design_points_db, 'obj_fn_1', 'obj_fn_2')



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
 

def main():
    a4 = JegaOptimizationResults('.')
    #print a4.all_design_points_db.iloc[0]
    #print a4.all_design_points_db
    print a4.gen_size_list
    print 'calculating pareto front'
    print a4.pareto_front
    print 'done'
    #print a4.pareto_front
    # all pareto fronts (list or what?)
    # all generations (list or what?)

    # # read pareto front data
    # A2 = load('finaldata1.dat');
    # # Ga_rc_final = A2(:,1);
    # # As_rc_final = A2(:,2);
    # # Ga_ed_final = A2(:,3);
    # # As_ed_final = A2(:,4);
    # vars_final  = A2(:,1:n_vars);
    # accu_final  = A2(:,5);
    # work_final  = A2(:,6);
    # n_final=length(work_final);
     
    # # read force and atan accuracy objectives from 
    # # all_accuracy_objectives.dat
    # A3 = load('all_accuracy_objectives.dat');
    # completed_points = A3(:,1);
    # force_objs = A3(:,2);
    # atan_objs = A3(:,3);
    # n3 = length(A3(:,1));
     
     


if __name__=='__main__':
    main()
