import sys
import os
import pytest # pyright: ignore[reportUnusedImport]

# Ensure src directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, '..', 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from simulation import classify_node, effective_env

def test_classify_node():
    assert classify_node("CTCF_TAG@1") == "ANCHOR"
    assert classify_node("SMC_RING@2") == "HUB"
    assert classify_node("lncRNA_BRIDGE@3") == "RNA"

def test_effective_env_decay():
    assert effective_env(0) < effective_env(50)

import unittest

class TestSimulation(unittest.TestCase):
    def test_placeholder(self):
        # Replace this with real tests for your simulation module
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()