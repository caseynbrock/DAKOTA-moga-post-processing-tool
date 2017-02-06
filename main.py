# main.py
#
# currently just an example script I use to test my optimization_results module
#
# WARNING: design point numbers 0-indexed in pandas database, but 
# eval_id column is the original 1-indexed value given by DAKOTA

import optimization_results as optr

def main():
    a4 = optr.MogaOptimizationResults()
    print a4.gen_size_list
    print a4.pareto_front

    ### OLD MATLAB CODE I NEED TO REWORK ### 
    # # read force and atan accuracy objectives from 
    # # all_accuracy_objectives.dat
    # A3 = load('all_accuracy_objectives.dat');
    # completed_points = A3(:,1);
    # force_objs = A3(:,2);
    # atan_objs = A3(:,3);
    # n3 = length(A3(:,1));


if __name__=='__main__':
    main()
