"""Independent packet, finite counting controls and symbolic assembly checks."""

import argparse
import hashlib
import json
from pathlib import Path
import time

import sympy as s

HERE=Path(__file__).resolve().parent


def audit(data, packet=None):
    started=time.monotonic()
    raw=(HERE/"artifacts/input/nine-point-final.json").read_bytes()
    packet=json.loads(raw) if packet is None else packet
    assert hashlib.sha256(raw).hexdigest()==data["packet_sha256"]=="9f113eb52fba9c3a1fd7d5f2714e925ef19d3104b8fdaa982661fa96794d0c0d"
    pairs=packet["pair_order"]
    weights=dict(zip(map(tuple,pairs),map(lambda v:s.Rational(v,packet["pair_weight_denominator"]),packet["pair_weight_numerators"])))
    assert len(weights)==36 and min(weights.values())>=0
    for r in range(1,9):
        assert sum(weights[(i,i+r)] for i in range(9-r))==2
    assert data["capacities"]==["2"]*8
    assert data["weights"]==[[i,j,str(weights[i,j])] for i,j in sorted(weights)]
    assert packet["interval_certificate_needed"] is True
    assert packet["target_epsilon"]=={"numerator":15211,"denominator":2500000}
    assert packet["pressure"]=={"numerator":1,"denominator":2500}
    assert packet["certified_window_baseline"]=={"numerator":3362285207,"denominator":5000000000}
    assert data["claim_status"]=="conditional on the explicit universal local inequality and source energy input"
    assert data["provenance"]=={"source_candidate_verification_needed":True,"source_log_reports_verified":True,
                               "log_binds_candidate_hash":False,"full_interval_replay_performed_here":False}
    # Independent counting controls: all finite block starts from all offsets.
    cases=0
    for mm in range(3,14):
        for rr in range(1,mm):
            length=4*mm+3
            blocks=[(offset+k*mm,offset+(k+1)*mm-1) for offset in range(mm)
                    for k in range(length//mm+1) if offset+(k+1)*mm<=length]
            assert len(blocks)>=length-2*mm
            for start in range(length-rr):
                inside=sum(left<=start and start+rr<=right for left,right in blocks)
                assert inside<=mm-rr
                if mm<=start and start+rr<length-mm:
                    assert inside==mm-rr
            for gap in range(length-1):
                hits=sum(start<=gap<start+rr for start in range(length-rr))
                assert hits<=rr
            cases+=1
    # Complete counting rearrangement, with no numerical substitutions.
    N,Nd,h,k,C,a,beta,rh,rk=s.symbols("N Nd h k C a beta rh rk")
    original=3*N-2*Nd+a*(Nd-h-2*k)-beta*N+rh*h+rk*k-C*N
    assembled=(3-C-beta)*N+(rh-a)*h+(rk-2*a)*k-(2-a)*Nd
    assert s.expand(original-assembled)==0
    row=data["candidate"]
    assert row["m"]==958 and data["inputs"]["r"]==8
    mm=958
    tau,c=s.Rational(2409,1000),s.Rational(3409,1000)
    delta,p,H=s.Rational(15211,2500000),s.Rational(1,2500),s.Rational(3362285207,5000000000)
    D=delta*(mm-8)
    aa,bb=D/mm,8*p*s.Rational(mm-8,mm)
    q=(1+H-bb)/(2-aa)
    assert 2-aa>0 and q>s.Rational(837,1000)
    for name,value in {"tau":tau,"c":c,"D":D,"a":aa,"beta":bb,"q":q}.items():
        assert s.Rational(row[name])==value
    slacks={"raw_energy_cutoff":tau*tau*s.Rational(mm,mm-1)-D,
            "unit_diagonal_threshold":c-1-tau,"double_diagonal_threshold":c-2-tau/2,
            "high_multiplicity_residual":6*c-7-c*c-aa,"off_line_pair_residual":4*c-2-c*c-2*aa}
    for name,value in slacks.items():
        assert value>=0 and s.Rational(row["slacks"][name])==value
    enc=row["q_enclosure"]
    assert s.Rational(enc["lower"])<=q<=s.Rational(enc["upper"])
    assert s.Rational(enc["upper"])-s.Rational(enc["lower"])==s.Rational(enc["width"])==s.Rational(1,10**50)
    old=s.Rational(2414226638567370500000000000000000000000000000000000,2884405070233731673605548076712427442954743117560789)
    assert q-old==s.Rational(data["gain_over_exp017"])>0
    assert data["inputs"]=={"r":8,"delta":str(delta),"pressure":str(p),"energy_gain":str(H)}
    if time.monotonic()-started>30:
        raise TimeoutError("audit budget exceeded")
    return {"schema":"exp018-independent-audit-v1","passed":True,"claim_status":"conditional",
            "q":str(q),"exact_partition_control_cases":cases,
            "route":"independent SymPy counting rearrangement and finite exact incidence controls",
            "local_inequality_independently_replayed":False}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--artifact",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    raw=args.artifact.read_bytes()
    data=json.loads(raw)
    root=HERE.parents[4]
    for path,expected in data["bindings"].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest()==expected
    result=audit(data)
    result["result_sha256"]=hashlib.sha256(raw).hexdigest()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes((json.dumps(result,indent=2,sort_keys=True)+"\n").encode())
    print("EXP-018 independent conditional audit passed",flush=True)


if __name__=="__main__":
    main()
