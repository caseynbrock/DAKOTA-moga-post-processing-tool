# main.py
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

import optimization_results as optr

def main():
    a4 = optr.MogaOptimizationResults('.')
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
