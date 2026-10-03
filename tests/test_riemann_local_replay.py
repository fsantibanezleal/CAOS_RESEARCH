"""Proof-state and adversarial controls; smoke is not a nine-point proof."""

import copy
import importlib
import json
from pathlib import Path
import sys

import pytest
from flint import fmpq

CODE = Path(__file__).resolve().parents[1]/"problems/number-theory/riemann-hypothesis/code"
sys.path.insert(0, str(CODE))
replay = importlib.import_module("local_replay")
original = importlib.import_module("rh019_vendor.verify_general")


def toy():
    spec = replay.CertificateSpec(kernel=replay.KernelSpec(coeffs=(fmpq(1),), omega_pi_multiples=()),
                                  q=2, pressure=fmpq(1), target=fmpq(1, 10),
                                  weights={(0, 1): fmpq(1), (1, 2): fmpq(1), (0, 2): fmpq(2)},
                                  grid=16, precision=128, use_tangent=False)
    # A synthetic conservative table for constant w=1/10; forces splitting.
    return spec, ([0.1, 0., 0.1, 0.1], [-100.]*4)


def test_pressure_entire_relevant_range():
    audit = replay.pressure_audit()
    assert audit["passed"] and audit["checked_indices"] == 60845
    assert audit["invalid_indices"] == []


def test_resume_equivalent_to_frozen_original(tmp_path):
    spec, tables = toy()
    expected = original.verify_general(spec, tables=tables)
    assert expected.splits > 0
    checkpoint = tmp_path/"checkpoint.json"
    binding = {"smoke": True}

    class Interrupted(Exception):
        pass

    def callback(state, force):
        replay.validate_state(state, spec)
        data = {"schema": "exp019-checkpoint-v1", "binding": binding,
                "shard": 0, "shard_count": 1, "state": state, "complete": not state["stack"]}
        replay.atomic_json(checkpoint, {"data": data, "sha256": replay.digest(replay.encoded(data))})
        print(f"smoke nodes={state['nodes']} pending={len(state['stack'])}", flush=True)
        if state["nodes"] >= 1:
            raise Interrupted

    with pytest.raises(Interrupted):
        replay.verify_general(spec, tables=tables, state_callback=callback, state_every=1)
    saved = replay.read_checkpoint(checkpoint, binding, 0, 1, spec)
    assert not saved["complete"]
    resumed = replay.verify_general(spec, tables=tables, resume_state=saved["state"])
    for name in ["verified", "nodes", "pruned", "splits", "maximum_depth", "initial_boxes", "details"]:
        assert getattr(resumed, name) == getattr(expected, name)
    assert not list(tmp_path.glob("*.tmp"))


@pytest.mark.parametrize("mutation", ["checksum", "binding", "shard", "complete", "counter", "box", "cover"])
def test_checkpoint_rejects_corruption(tmp_path, mutation):
    spec, tables = toy()
    states = []
    replay.verify_general(spec, tables=tables, state_callback=lambda s, f: states.append(copy.deepcopy(s)), state_every=1)
    data = {"schema": "exp019-checkpoint-v1", "binding": {"toy": 1}, "shard": 0,
            "shard_count": 1, "state": states[0], "complete": False}
    if mutation == "binding":
        data["binding"]["toy"] = 2
    elif mutation == "shard":
        data["shard"] = 1
    elif mutation == "complete":
        data["complete"] = True
    elif mutation == "counter":
        data["state"]["nodes"] = 2
    elif mutation == "box":
        data["state"]["stack"][0] = (((-1, 1), (0, 1)), 0)
    elif mutation == "cover":
        data["state"]["initial_sha256"] = "bad"
    obj = {"data": data, "sha256": replay.digest(replay.encoded(data))}
    if mutation == "checksum":
        obj["sha256"] = "bad"
    path = tmp_path/"checkpoint.json"
    replay.atomic_json(path, obj)
    if mutation == "cover":
        saved = replay.read_checkpoint(path, {"toy": 1}, 0, 1, spec)
        with pytest.raises(ValueError, match="initial cover"):
            replay.verify_general(spec, tables=tables, resume_state=saved["state"])
    else:
        with pytest.raises(ValueError):
            replay.read_checkpoint(path, {"toy": 1}, 0, 1, spec)


def test_terminal_unresolved_fails_closed():
    spec, tables = toy()
    with pytest.raises(RuntimeError, match="terminal cell"):
        replay.verify_general(spec, tables=([0.]*4, tables[1]))


def test_missing_and_duplicate_shards(tmp_path):
    (tmp_path/"reports").mkdir()
    with pytest.raises(ValueError, match="incomplete"):
        replay.aggregate(tmp_path, {}, 2)
    for name in ["shard-000.json", "shard-001.json"]:
        (tmp_path/"reports"/name).write_text(json.dumps({"shard": -1, "report": {}}))
    with pytest.raises(ValueError, match="invalid shard"):
        replay.aggregate(tmp_path, {}, 2)


def test_table_binding_rejection(tmp_path):
    replay.atomic_json(tmp_path/"tables.json", {"binding": {"other": 1}})
    with pytest.raises(ValueError, match="binding"):
        replay.load_tables(tmp_path, {"packet": 2})
