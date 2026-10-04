"""Conditional transfer, packet tampering and source-premise boundaries."""

from copy import deepcopy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
PROBLEM=ROOT/"problems/number-theory/riemann-hypothesis"
CODE=PROBLEM/"code"
HERE=PROBLEM/"experiments/EXP-018-nine-point-distinct-transfer"
sys.path.insert(0,str(CODE))


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PRODUCER=load("rh_nine_transfer",CODE/"nine_point_distinct.py")
AUDITOR=load("rh_nine_audit",HERE/"audit.py")


def test_conditional_result_and_independent_assembly():
    data=PRODUCER.certificate()
    report=AUDITOR.audit(data)
    assert report["passed"] and report["claim_status"]=="conditional"
    assert F(data["candidate"]["q"])==F(3997934614153,4775549550000)>F(837,1000)
    assert report["local_inequality_independently_replayed"] is False


@pytest.mark.parametrize("field",["weight","delta","pressure","window","pending"])
def test_packet_mutations_fail_closed(field):
    packet=json.loads((HERE/"artifacts/input/nine-point-final.json").read_bytes())
    if field=="weight":
        packet["pair_weight_numerators"][0]+=1
    elif field=="delta":
        packet["target_epsilon"]["numerator"]+=1
    elif field=="pressure":
        packet["pressure"]["denominator"]+=1
    elif field=="window":
        packet["window_coefficient_numerators"][1]+=1
    else:
        packet["interval_certificate_needed"]=False
    with pytest.raises(AssertionError):
        PRODUCER.validate_packet(packet)


@pytest.mark.parametrize("field",["q","a","m","capacity","packet_hash","conditional","replay"])
def test_independent_auditor_rejects_corruption(field):
    data=deepcopy(PRODUCER.certificate())
    if field in {"q","a"}:
        data["candidate"][field]="1"
    elif field=="m":
        data["candidate"]["m"]+=1
    elif field=="capacity":
        data["capacities"][0]="3"
    elif field=="packet_hash":
        data["packet_sha256"]="0"*64
    elif field=="conditional":
        data["claim_status"]="unconditional"
    else:
        data["provenance"]["full_interval_replay_performed_here"]=True
    with pytest.raises(AssertionError):
        AUDITOR.audit(data)


def test_tampered_input_file_rejected(tmp_path):
    target=tmp_path/"input.json"
    target.write_bytes((HERE/"artifacts/input/nine-point-final.json").read_bytes()+b" ")
    with pytest.raises(AssertionError):
        PRODUCER.certificate(target)


def test_byte_replay_and_complete_bindings(tmp_path):
    subprocess.run([sys.executable,str(HERE/"run.py"),"--output-dir",str(tmp_path)],check=True)
    raw=(HERE/"artifacts/canonical/result.json").read_bytes()
    assert (tmp_path/"result.json").read_bytes()==raw
    for path,expected in json.loads(raw)["bindings"].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected


def test_manifest_schema_and_input_source_binding():
    data=json.loads((PROBLEM/"context/source-manifest-exp018.json").read_bytes())
    assert data["repositories"]==[] and len(data["documents"])==15
    row=next(x for x in data["documents"] if x["filename"]=="data/candidate-nine-point-final.json")
    assert row["sha256"]==PRODUCER.PACKET_SHA256 and row["license"]["status"]=="MIT"
    assert "1610b97b7895ff34982260f8dcaf04a0f7b82cf7" in row["source_url"]
