"""Independent equality, missing-premise and corrupted-certificate controls."""

from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROBLEM = ROOT/"problems/number-theory/riemann-hypothesis"
CODE = PROBLEM/"code"
HERE = PROBLEM/"experiments/EXP-016-trace-aware-clipping"
sys.path.insert(0,str(CODE))


def load(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PRODUCER = load("rh_trace_producer",CODE/"trace_clipping_parameters.py")
AUDITOR = load("rh_trace_auditor",HERE/"audit.py")


def test_independent_certificate_and_uniform_cap():
    data = PRODUCER.certificate()
    assert AUDITOR.audit(data)["passed"]
    assert all(value > 0 for value in PRODUCER.trace_boundary(1312))
    assert F(data["candidate"]["q"]) > PRODUCER.bound(1310)


@pytest.mark.parametrize("m,tau",[(2,F(1)),(7,F(12,5)),(20,F(3))])
def test_psd_equality_and_missing_trace_premise(m,tau):
    xs = [tau]+[-tau/F(m-1)]*(m-1)
    assert sum(xs) == 0 and min(1+x for x in xs) >= 0
    assert sum(PRODUCER.clipped(x,tau) for x in xs) == tau*tau*F(m,m-1)
    # Omitting the zero-sum premise leaves the high displacement alone.
    assert sum(PRODUCER.clipped(x,tau) for x in [tau]+[F()]*(m-1)) < tau*tau*F(m,m-1)


@pytest.mark.parametrize("field",["q","m","cap","trace","requirement","enclosure"])
def test_auditor_rejects_corruption(field):
    data = deepcopy(PRODUCER.certificate())
    if field == "q":
        data["candidate"]["q"] = "1"
    elif field == "m":
        data["candidate"]["m"] = 1312
    elif field == "cap":
        data["cap"]["maximum_integer_m"] = 1312
    elif field == "trace":
        data["sharp_control"]["displacements"][-1] = "0"
    elif field == "requirement":
        data["block_requirement"] = "unrestricted"
    else:
        data["candidate"]["q_enclosure"]["lower"] = "0.9"
    with pytest.raises(AssertionError):
        AUDITOR.audit(data)


def test_canonical_replay_and_complete_bindings(tmp_path):
    subprocess.run([sys.executable,str(HERE/"run.py"),"--output-dir",str(tmp_path)],check=True)
    raw = (HERE/"artifacts/canonical/result.json").read_bytes()
    assert (tmp_path/"result.json").read_bytes() == raw
    for path,expected in json.loads(raw)["bindings"].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected
