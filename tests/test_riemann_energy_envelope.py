"""Sharp PSD controls, missing premises, rational brackets and artifact integrity."""

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
HERE = PROBLEM/"experiments/EXP-017-sharp-energy-envelope"
sys.path.insert(0,str(CODE))


def load(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PRODUCER = load("rh_energy_envelope",CODE/"energy_envelope.py")
AUDITOR = load("rh_energy_audit",HERE/"audit.py")


def test_independent_scalar_minorant_and_candidate():
    data = PRODUCER.certificate()
    assert AUDITOR.audit(data)["passed"]
    assert F(data["candidate"]["q"]) > PRODUCER.EXP016_Q
    assert data["search"]["global_optimality_claimed"] is False


@pytest.mark.parametrize("m,tau,s",[(2,F(1),F(1,2)),(7,F(1),F(1)),
                                  (7,F(1),F(6)),(50,F(12,5),F(49))])
def test_psd_equicorrelation_extrema(m,tau,s):
    xs = [s]+[-s/F(m-1)]*(m-1)
    E = sum(x*x for x in xs)
    lo, hi = PRODUCER.envelope_bracket(m,tau,E)
    assert lo == hi == sum(PRODUCER.clipped(x,tau) for x in xs)
    assert min(1+x for x in xs) >= 0


def test_multiple_clipped_entries_and_pressure_endpoints():
    xs = [F(3,2)]*10+[F(-1)]*15
    E = sum(x*x for x in xs)
    lo,hi = PRODUCER.envelope_bracket(25,F(1),E)
    assert sum(xs) == 0
    assert sum(PRODUCER.clipped(x,F(1)) for x in xs) > hi >= lo
    # E=0 requires the nonnegative pressure to carry all of D.
    D, p = F(8), F(1,7)
    lo,hi = PRODUCER.envelope_bracket(2,F(1),D)
    assert lo == hi == 7 and p*(D/p) == D >= hi
    # E<D, with exact equality in the premise; clipping loses one unit.
    assert PRODUCER.envelope_bracket(2,F(1),F(2)) == (F(2),F(2))
    assert 2+(D-2) >= hi


@pytest.mark.parametrize("m,tau,energy",[(1,F(1),F(1)),(True,F(1),F(1)),
                                       (7,F(0),F(1)),(7,F(-1),F(1)),(7,F(1),F(-1))])
def test_invalid_premises_rejected(m,tau,energy):
    with pytest.raises(ValueError):
        PRODUCER.envelope_bracket(m,tau,energy)


@pytest.mark.parametrize("field",["q","a","envelope_lower","tau","delta","optimum","trace"])
def test_independent_auditor_rejects_corruption(field):
    data = deepcopy(PRODUCER.certificate())
    if field in {"q","a","envelope_lower","tau"}:
        data["candidate"][field] = "1"
    elif field == "delta":
        data["source_inputs"]["delta"] = "1"
    elif field == "optimum":
        data["search"]["global_optimality_claimed"] = True
    else:
        data["sharp_controls"][0]["displacements"][-1] = "0"
    with pytest.raises(AssertionError):
        AUDITOR.audit(data)


def test_byte_replay_and_complete_bindings(tmp_path):
    subprocess.run([sys.executable,str(HERE/"run.py"),"--output-dir",str(tmp_path)],check=True)
    raw = (HERE/"artifacts/canonical/result.json").read_bytes()
    assert (tmp_path/"result.json").read_bytes() == raw
    for path,expected in json.loads(raw)["bindings"].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected
