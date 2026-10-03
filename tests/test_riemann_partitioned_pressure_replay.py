"""Changed-pressure preflight: exact transfer and real checkpoint/resume smoke."""

import importlib
from fractions import Fraction as Q
from pathlib import Path
import sys

from flint import fmpq
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"problems/number-theory/riemann-hypothesis/code"))
replay = importlib.import_module("partitioned_pressure_replay")
core = importlib.import_module("rh019_vendor.quadratic_partitioned")
kernel = importlib.import_module("rh019_vendor.kernel")


@pytest.mark.parametrize("size", [1, 2, 3, 4, 5, 17, 48864])
def test_exact_quarter_cover_no_missing_or_duplicate_cell(size):
    result = core._quarter_components([(100, 100+size-1)])
    cells = [n for lo, hi in result for n in range(lo, hi+1)]
    assert cells == list(range(100, 100+size))
    assert len(result) == min(4, size)


def test_only_core_change_is_initial_cover_refinement():
    original = Path(core.__file__).with_name("quadratic_general.py").read_text()
    changed = Path(core.__file__).read_text()
    begin = changed.index("def _quarter_components(components):")
    end = changed.index("def cutoff_cell_count", begin)
    restored = changed[:begin]+changed[end:]
    restored = restored.replace("    coordinate_components = [_quarter_components(parts) for parts in coordinate_components]\n", "")
    assert restored == original


def test_exact_changed_pressure_transfer():
    delta, p, m = Q(52231, 5000000), Q(1, 1250), 562
    tau, c = Q(1203, 500), Q(1703, 500)
    d = delta*(m-8)
    a, beta = d/m, 8*p*(m-8)/m
    assert tau*tau >= d
    assert c >= 1+tau and c >= 2+tau/2
    assert 6*c-7-c*c >= a and 4*c-2-c*c >= 2*a
    assert 2-a > 0
    result = (1+Q(3362285207, 5000000000)-beta)/(2-a)
    assert result == Q(2340938143167, 2795532013000)
    # The declared value gate compares actual exact proposed consequences.
    q20 = (1+Q(3362285207, 5000000000)-8*Q(1, 2500)*950/958)/(2-Q(3051, 500000)*950/958)
    assert result-q20 > Q(1, 10000)


def test_compound_rounding_all_changed_pressure_indices():
    result = replay.pressure_audit()
    assert result["passed"] and result["cutoff_indices"] == 52232
    assert result["checked_indices"] == 8*52231+1
    assert replay.spec().capacity_ok()


def test_actual_worker_emits_checkpoint_and_resumes(tmp_path, monkeypatch, capsys):
    # Synthetic conservative tables force the real verifier to split; no
    # scientific claim is made from this infrastructure smoke instance.
    toy = core.CertificateSpec(kernel=kernel.KernelSpec(coeffs=(fmpq(1),), omega_pi_multiples=()),
                               q=2, pressure=fmpq(1), target=fmpq(1, 10),
                               weights={(0, 1): fmpq(1), (1, 2): fmpq(1), (0, 2): fmpq(2)},
                               grid=16, precision=128, use_tangent=False)
    import struct
    monkeypatch.setattr(replay, "spec", lambda: toy)
    monkeypatch.setattr(replay, "binding", lambda: {"smoke": True})
    tables = ([0.1, 0., 0.1, 0.1], [-100.]*4)
    table_dir = tmp_path/"tables"
    table_dir.mkdir()
    hashes = {}
    for name, values in zip(["w.bin", "w-second.bin"], tables):
        raw = struct.pack(">4d", *values)
        (table_dir/name).write_bytes(raw)
        hashes[name] = replay.digest(raw)
    bound = {"smoke": True, "tables": hashes, "cells": 4}
    original_write = replay.atomic_json

    class Interrupted(Exception):
        pass

    def interrupt_after_write(path, value):
        original_write(path, value)
        if "checkpoints" in str(path):
            raise Interrupted

    monkeypatch.setattr(replay, "atomic_json", interrupt_after_write)
    with pytest.raises(Interrupted):
        replay.worker((0, str(tmp_path), bound))
    checkpoint = tmp_path/"checkpoints/shard-000.json"
    saved = replay.read_state(checkpoint, bound, 0)
    assert saved["stack"]
    assert "pressure shard=0/96 nodes=0 pending=" in capsys.readouterr().out
    monkeypatch.setattr(replay, "atomic_json", original_write)
    result = replay.worker((0, str(tmp_path), bound))
    direct = core.verify_general(toy, shard=0, shard_count=96, tables=tables)
    assert result["report"]["verified"] and result["report"]["nodes"] == direct.nodes
    assert direct.nodes > 0
    assert not replay.read_state(checkpoint, bound, 0)["stack"]
    assert (tmp_path/"reports/shard-000.json").is_file()
    assert not list(tmp_path.rglob("*.tmp"))
