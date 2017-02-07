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
    assert a4.gen_size_list == [100, 94, 48, 45, 45, 46, 62, 85, 102, 108, 131, 130, 134, 119, 
                                127, 128, 155, 124, 124, 130, 128, 123, 137, 135, 149, 165, 154, 
                                164, 169, 177, 205, 196, 215, 185, 205, 190, 162, 158, 154, 159, 
                                163, 183, 175, 183, 186, 188, 188, 186, 201, 213, 222]

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
