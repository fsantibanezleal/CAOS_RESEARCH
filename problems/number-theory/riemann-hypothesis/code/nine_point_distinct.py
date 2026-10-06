"""Source-conditioned r-gap mixed-Gram assembly with exact input checks."""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from energy_envelope import envelope_bracket
from mixed_gram_parameters import ENERGY_GAIN, decimal_enclosure

PACKET_SHA256 = "9f113eb52fba9c3a1fd7d5f2714e925ef19d3104b8fdaa982661fa96794d0c0d"
HERE = Path(__file__).resolve().parents[1]/"experiments/EXP-018-nine-point-distinct-transfer"


def validate_packet(packet):
    assert packet["s"] == 9
    pairs = [tuple(x) for x in packet["pair_order"]]
    assert pairs == [(i,j) for i in range(9) for j in range(i+1,9)]
    assert len(packet["pair_weight_numerators"]) == 36
    den = packet["pair_weight_denominator"]
    assert den == 10**7
    weights = {ij:F(num,den) for ij,num in zip(pairs,packet["pair_weight_numerators"])}
    assert min(weights.values()) >= 0
    capacities = [sum(w for (i,j),w in weights.items() if j-i == r) for r in range(1,9)]
    assert capacities == [F(2)]*8
    assert packet["span_capacity_numerators"] == [2*den]*8
    assert all(weights[(i,j)] == weights[(8-j,8-i)] for i,j in pairs)
    pressure = F(packet["pressure"]["numerator"],packet["pressure"]["denominator"])
    delta = F(packet["target_epsilon"]["numerator"],packet["target_epsilon"]["denominator"])
    h0 = F(packet["certified_window_baseline"]["numerator"],packet["certified_window_baseline"]["denominator"])
    assert pressure == F(1,2500) and delta == F(15211,2500000) and h0 == ENERGY_GAIN
    assert packet["window_coefficient_denominator"] == 10**9
    assert packet["window_coefficient_numerators"] == [10**9,3322500,-7609135,1190194,-731476,-1680572,1141360]
    assert packet["interval_certificate_needed"] is True
    return weights, capacities, pressure, delta


def certificate(packet_path=None):
    path = Path(packet_path) if packet_path is not None else HERE/"artifacts/input/nine-point-final.json"
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PACKET_SHA256
    packet = json.loads(raw)
    weights, caps, p, delta = validate_packet(packet)
    m, r, tau, c = 958, 8, F(2409,1000), F(3409,1000)
    D = delta*(m-r)
    lo, hi = envelope_bracket(m,tau,D)
    assert lo == hi == D  # No square-root bracket needed for this candidate.
    a, beta = D/m, r*p*F(m-r,m)
    slacks = {"raw_energy_cutoff": tau*tau*F(m,m-1)-D,
              "unit_diagonal_threshold": c-1-tau,"double_diagonal_threshold": c-2-tau/2,
              "high_multiplicity_residual":6*c-7-c*c-a,
              "off_line_pair_residual":4*c-2-c*c-2*a}
    assert min(slacks.values()) >= 0
    q = (1+ENERGY_GAIN-beta)/(2-a)
    assert q > F(837,1000)
    return {"schema":"exp018-nine-point-distinct-transfer-v1","experiment":"EXP-018",
            "claim_status":"conditional on the explicit universal local inequality and source energy input",
            "packet_sha256":PACKET_SHA256,"capacities":[str(v) for v in caps],
            "weights":[[i,j,str(w)] for (i,j),w in weights.items()],
            "inputs":{"r":r,"delta":str(delta),"pressure":str(p),"energy_gain":str(ENERGY_GAIN)},
            "candidate":{"m":m,"tau":str(tau),"c":str(c),"D":str(D),"a":str(a),"beta":str(beta),
                         "q":str(q),"q_enclosure":decimal_enclosure(q),"slacks":{k:str(v) for k,v in slacks.items()}},
            "gain_over_exp017":str(q-F(2414226638567370500000000000000000000000000000000000,2884405070233731673605548076712427442954743117560789)),
            "provenance":{"source_candidate_verification_needed":True,"source_log_reports_verified":True,
                          "log_binds_candidate_hash":False,"full_interval_replay_performed_here":False},
            "not_established":["unconditional independent certificate","global parameter optimum","new onset","RH"]}
