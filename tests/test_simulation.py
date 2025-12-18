

# Fix sys.path to ensure 'src' is importable regardless of test runner location
import sys
import os
import pytest # pyright: ignore[reportUnusedImport]

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)


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