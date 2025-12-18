import pytest
from src.simulation import classify_node, effective_env

def test_classify_node():
    assert classify_node("CTCF_TAG@1") == "ANCHOR"
    assert classify_node("SMC_RING@2") == "HUB"
    assert classify_node("lncRNA_BRIDGE@3") == "RNA"

def test_effective_env_decay():
    assert effective_env(0) < effective_env(50)
