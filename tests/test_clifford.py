# -*- coding: utf-8 -*-

# Copyright 2019, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""
Test Clifford functions:
- Generating Clifford tables on 1 and 2 qubits: rb.clifford1_table and rb.clifford2_table
- Generating a pseudo-random Clifford (using the tables or "on the fly"): rb.random_clifford
- Inverting a Clifford: rb.find_inverse_clifford_circuit
"""

# import config
import os
import unittest
import filecmp
import random
import numpy as np

# Import the clifford_utils functions
import verification.randomized_benchmarking.standard_rb.clifford_utils as clutils

class TestClifford(unittest.TestCase):
    """
        Test Clifford functions
    """
    def setUp(self):
        """
            setUp and global parameters
        """
        self.number_of_tests = 20  # number of pseudo-random seeds
        self.max_nq = 10  # maximal number of qubits to check

    def test_tables(self):
        """
            test: generating the tables for 1 and 2 qubits
        """
        test_tables_file = open('test_tables_results.txt', 'w')  # new file with the test results
        test_tables_file.write("test: generating the clifford group table for 1 qubit:\n")
        clifford1 = clutils.clifford1_table()
        test_tables_file.write(str(len(clifford1)))
        test_tables_file.write("\n")
        test_tables_file.write(str(sorted(clifford1.values())))
        test_tables_file.write("\n")
        test_tables_file.write("-------------------------------------------------------\n")

        test_tables_file.write("test: generating the clifford group table for 2 qubits:\n")
        clifford2 = clutils.clifford2_table()
        test_tables_file.write(str(len(clifford2)))
        test_tables_file.write("\n")
        test_tables_file.write(str(sorted(clifford2.values())))
        test_tables_file.write("\n")

        # test (to do): generating the tables for 3 and 4 qubits (dat files)
        # need to verify that the dat files (generated using the C++ code) are the same

        # verify that the dat tables for 3 and 4 qubits exist - otherwise raise an error:
        for nq in range(3, 5):
            if not os.path.exists(os.path.join(os.path.dirname(__file__), 'src',
                                               'qubits_%d_cnots_0.dat'%(nq))):
                raise ValueError("Please run 'ex %d' to generate the .dat tables"%(nq))

        test_tables_file.close()
        self.assertTrue(filecmp.cmp('test_tables_results.txt', 'test_tables_expected.txt'),
                        "Error: tables on 1 and 2 qubits are not the same")

    def test_random_and_inverse(self):
        """
            test: generating a pseudo-random Clifford using tables
            (either using the tables or "on-the-fly")
            and computing its inverse
        """
        clifford_tables = [[]]*self.max_nq
        clifford_tables[0] = clutils.clifford1_table()
        clifford_tables[1] = clutils.clifford2_table()
        test_random_file = open('test_random_results.txt', 'w')  # new file with the test results

        # test: generating a pseudo-random Clifford using tables - 1,2,3,4 qubits
        # and computing its inverse
        for nq in range(1, 5):
            for i in range(0, self.number_of_tests):
                my_seed = i
                np.random.seed(my_seed)
                random.seed(my_seed)
                test_random_file.write("test: generating a pseudo-random clifford using the tables "
                                       "- %d qubit - seed=%d:\n" %(nq, my_seed))
                cliff_nq = clutils.random_clifford(nq)
                test_random_file.write(str(cliff_nq.circuit))
                test_random_file.write("\n")
                test_random_file.write("test: inverting a pseudo-random clifford using the tables "
                                       "- %d qubit - seed=%d:\n" %(nq, my_seed))
                inv_cliff_nq = clutils.find_inverse_clifford_circuit(cliff_nq,
                                                                     clifford_tables[nq-1])
                test_random_file.write(str(inv_cliff_nq))
                test_random_file.write("\n")
                test_random_file.write("-------------------------------------------------------\n")

        # test: generating a pseudo-random Clifford using "on the fly" method -
        # 1,2,...,max_nq qubits, and computing its inverse
        for nq in range(1, self.max_nq+1):
            for i in range(0, self.number_of_tests):
                my_seed = i
                np.random.seed(my_seed)
                random.seed(my_seed)
                test_random_file.write("test: generating a pseudo-random clifford using "
                                       "on the fly method - %d qubit - seed=%d:\n" %(nq, my_seed))
                cliff_nq = clutils.random_clifford(nq, True)
                test_random_file.write(str(cliff_nq.circuit))
                test_random_file.write("\n")
                test_random_file.write("test: inverting a pseudo-random clifford using "
                                       "on the fly method - %d qubit - seed=%d:\n" %(nq, my_seed))
                inv_cliff_nq = clutils.find_inverse_clifford_circuit(cliff_nq, None, True)
                test_random_file.write(str(inv_cliff_nq))
                test_random_file.write("\n")
                test_random_file.write("-------------------------------------------------------\n")

        test_random_file.close()
        self.assertTrue(filecmp.cmp('test_random_results.txt', 'test_random_expected.txt'),
                        "Error: random and/or inverse cliffords are not the same")


if __name__ == '__main__':
    unittest.main()