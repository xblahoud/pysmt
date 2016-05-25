#
# This file is part of pySMT.
#
#   Copyright 2014 Andrea Micheli and Marco Gario
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import os

from pysmt.test import SkipTest
from pysmt.shortcuts import get_env, reset_env
from pysmt.smtlib.parser import SmtLibParser
from pysmt.smtlib.script import check_sat_filter
from pysmt.logics import QF_LIA, QF_LRA, LRA, QF_UFLIRA, QF_UFBV, QF_BV
from pysmt.logics import QF_ALIA, QF_ABV, QF_AUFLIA, QF_AUFBV
from pysmt.exceptions import NoSolverAvailableError

SMTLIB_DIR = "pysmt/test/smtlib"
SMTLIB_TEST_FILES = [
    #
    # QF_LIA
    #
    (QF_LIA, "small_set/QF_LIA/prp-23-47.smt2", "unsat"),
    (QF_LIA, "small_set/QF_LIA/prp-20-46.smt2", "unsat"),
    (QF_LIA, "small_set/QF_LIA/prp-24-47.smt2", "unsat"),
    (QF_LIA, "small_set/QF_LIA/prp-24-46.smt2", "unsat"),
    (QF_LIA, "small_set/QF_LIA/prp-22-46.smt2", "unsat"),
    (QF_LIA, "small_set/QF_LIA/prp-25-49.smt2", "unsat"),
    (QF_LIA, "small_set/QF_LIA/prp-21-46.smt2", "unsat"),
    (QF_LIA, "small_set/QF_LIA/prp-23-46.smt2", "unsat"),
    (QF_LIA, "small_set/QF_LIA/prp-25-48.smt2", "unsat"),
    (QF_LIA, "small_set/QF_LIA/prp-25-47.smt2", "unsat"),
    (QF_LIA, "small_set/QF_LIA/prp-24-48.smt2", "unsat"),
    (QF_LIA, "small_set/QF_LIA/prp-25-46.smt2", "unsat"),
    (QF_LIA, "small_set/QF_LIA/issue_159.smt2", "sat"),
    #
    # QF_LRA
    #
    (QF_LRA, "small_set/QF_LRA/uart-8.induction.cvc.smt2", "sat"),
    (QF_LRA, "small_set/QF_LRA/uart-10.induction.cvc.smt2", "sat"),
    (QF_LRA, "small_set/QF_LRA/uart-18.induction.cvc.smt2", "sat"),
    (QF_LRA, "small_set/QF_LRA/uart-26.induction.cvc.smt2", "sat"),
    (QF_LRA, "small_set/QF_LRA/uart-11.induction.cvc.smt2", "sat"),
    (QF_LRA, "small_set/QF_LRA/uart-16.induction.cvc.smt2", "sat"),
    (QF_LRA, "small_set/QF_LRA/uart-6.induction.cvc.smt2", "sat"),
    (QF_LRA, "small_set/QF_LRA/uart-14.induction.cvc.smt2", "sat"),
    (QF_LRA, "small_set/QF_LRA/simple_startup_11nodes.abstract.base.smt2", "unsat"),
    (QF_LRA, "small_set/QF_LRA/simple_startup_8nodes.synchro.base.smt2", "unsat"),
    (QF_LRA, "small_set/QF_LRA/simple_startup_3nodes.bug.induct.smt2", "sat"),
    (QF_LRA, "small_set/QF_LRA/simple_startup_15nodes.abstract.base.smt2", "unsat"),
    (QF_LRA, "small_set/QF_LRA/simple_startup_12nodes.synchro.base.smt2", "unsat"),
    (QF_LRA, "small_set/QF_LRA/simple_startup_8nodes.missing.induct.smt2", "sat"),
    (QF_LRA, "small_set/QF_LRA/simple_startup_14nodes.abstract.base.smt2", "unsat"),
    (QF_LRA, "small_set/QF_LRA/simple_startup_9nodes.abstract.base.smt2", "unsat"),
    (QF_LRA, "small_set/QF_LRA/simple_startup_8nodes.synchro.induct.smt2", "unsat"),
    (QF_LRA, "small_set/QF_LRA/simple_startup_4nodes.synchro.base.smt2", "unsat"),
    (QF_LRA, "small_set/QF_LRA/simple_startup_14nodes.synchro.induct.smt2", "unsat"),
    #
    # LRA
    #
    (LRA, "small_set/LRA/water_tank-node21140.smt2", "unsat"),
    (LRA, "small_set/LRA/water_tank-node22228.smt2", "unsat"),
    (LRA, "small_set/LRA/water_tank-node9350.smt2", "unsat"),
    (LRA, "small_set/LRA/intersection-example-simple.proof-node679466.smt2", "unsat"),
    (LRA, "small_set/LRA/intersection-example-simple.proof-node394346.smt2", "unsat"),
    (LRA, "small_set/LRA/water_tank-node24658.smt2", "unsat"),
    #
    # QF_LIRA
    #
    (QF_UFLIRA, "small_set/QF_LIRA/lira1.smt2", "sat"),
    (QF_UFLIRA, "small_set/QF_LIRA/prp-20-46.smt2", "sat"),
    #
    # QF_UFBV
    #
    #(QF_UFBV, "small_set/QF_UFBV/btfnt_atlas_out.smt2", "unsat"),
    (QF_UFBV, "small_set/QF_UFBV/calc2_sec2_bmc10.smt2", "unsat"),
    (QF_BV, "small_set/QF_BV/bench_4631_simp.smt2", "sat"),
    (QF_BV, "small_set/QF_BV/bench_5200.smt2", "unsat"),
    (QF_BV, "small_set/QF_BV/bench_9457_simp.smt2", "sat"),
    #
    # Arrays
    (QF_ABV, "small_set/QF_ABV/a268test0002.smt2", "sat"),
#    (QF_ABV, "small_set/QF_ABV/com.galois.ecc.P384ECC64.group_add6.short.smt2", "unsat"),

    (QF_ALIA, "small_set/QF_ALIA/ios_t1_ios_np_sf_ai_00001_001.cvc.smt2", "unsat"),
    (QF_ALIA, "small_set/QF_ALIA/pointer-invalid-15.smt2", "sat"),

    (QF_AUFBV, "small_set/QF_AUFBV/com.galois.ecc.P384ECC64.mod_div10.short.smt2", "unsat"),

    (QF_AUFLIA, "small_set/QF_AUFLIA/array_incompleteness1.smt2", "unsat"),
    (QF_AUFLIA, "small_set/QF_AUFLIA/swap_invalid_t1_pp_nf_ai_00002_002.cvc.smt2", "sat"),
]

# We use test generation in order to be able to obtain a separate
# test for each file.
# This is a feature of nosetest. The correct way to invoke these
# tests is, e.g.,
#  $ nosetests pysmt/test/smtlib/test_parser_qf_lra.py
# The function 'execute_script_fname' is a generator that
# returns the correct arguments for the test
def execute_script_fname(smtfile, logic, expected_result):
    """Read and call a Solver to solve the instance"""

    reset_env()
    Solver = get_env().factory.Solver
    assert os.path.exists(smtfile), smtfile
    parser = SmtLibParser()
    script = parser.get_script_fname(smtfile)
    try:
        log = script.evaluate(Solver(logic=logic, incremental=False,
                                     generate_models=False))
    except NoSolverAvailableError:
        raise SkipTest("No solver for logic %s." % logic)

    res = check_sat_filter(log)
    if res:
        assert expected_result == "sat"
    else:
        assert expected_result == "unsat"
