




# Ensure 'src' is importable regardless of test runner location
import sys
import os
try:
    base_dir = os.path.dirname(__file__)
except NameError:
    base_dir = os.getcwd()
src_path = os.path.abspath(os.path.join(base_dir, '..', 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

import pytest # pyright: ignore[reportUnusedImport]


import simulation

def test_classify_node():
    assert simulation.classify_node("CTCF_TAG@1") == "ANCHOR"
    assert simulation.classify_node("SMC_RING@2") == "HUB"
    assert simulation.classify_node("lncRNA_BRIDGE@3") == "RNA"

def test_effective_env_decay():
    assert simulation.effective_env(0) < simulation.effective_env(50)

import unittest

class TestSimulation(unittest.TestCase):
    def test_placeholder(self):
        # Replace this with real tests for your simulation module
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()