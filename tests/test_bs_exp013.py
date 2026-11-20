"""Gate G3 of EXP-013 (boij-soderberg-realizability): the substitution on monomials against hand-written products for A3,
phi(u v) = phi(u) phi(v) on twenty random pairs of forms of degree at most 3 for A3 and B4, the scaling of a table, and the
comparison routine on a case built to differ."""
import random
import sys
from pathlib import Path

EXPS = (Path(__file__).resolve().parents[1] / "problems" / "commutative-algebra" / "boij-soderberg-realizability"
        / "experiments")
sys.path.insert(0, str(EXPS / "EXP-013-pull-back-scaling"))

import exp013_routine as R  # noqa: E402


def test_a3_images_of_the_generators():
    phi = R.endo_phi("A3")
    assert phi["x"] == {(3, 0, 0): 1, (0, 1, 1): 1}
    assert phi["y"] == {(0, 3, 0): 1, (1, 0, 1): 1}
    # [x^3 + y z, y^3 + x z] = [y z, x z] = z^2 [y, x] = - z^3 = 2 z^3 over GF(3) (x^3 and y^3 are central there)
    assert phi["z"] == {(0, 0, 3): 2}


def test_a3_substitution_on_monomials_against_hand_written_products():
    phi = R.endo_phi("A3")
    assert R.phi_mono(phi, (0, 0, 0)) == {(0, 0, 0): 1}
    assert R.phi_mono(phi, (1, 0, 0)) == phi["x"]
    # phi(x y) = (x^3 + y z)(y^3 + x z) = x^3 y^3 + x^4 z + y^4 z + y x z^2, and y x z^2 = x y z^2 - z^3
    assert R.phi_mono(phi, (1, 1, 0)) == {(3, 3, 0): 1, (4, 0, 1): 1, (0, 4, 1): 1, (1, 1, 2): 1, (0, 0, 3): 2}
    # phi(x^2) = (x^3 + y z)^2 = x^6 + x^3 y z + y z x^3 + y^2 z^2, and y x^3 = x^3 y - 3 x^2 z = x^3 y over GF(3)
    assert R.phi_mono(phi, (2, 0, 0)) == {(6, 0, 0): 1, (3, 1, 1): 2, (0, 2, 2): 1}
    # phi(z) = 2 z^3, so phi(z^2) = 4 z^6 = z^6
    assert R.phi_mono(phi, (0, 0, 2)) == {(0, 0, 6): 1}
    # phi(x z) = (x^3 + y z) (2 z^3) = 2 x^3 z^3 + 2 y z^4
    assert R.phi_mono(phi, (1, 0, 1)) == {(3, 0, 3): 2, (0, 1, 4): 2}


def _random_form(rng, p, maxdeg):
    poly = {}
    for _ in range(rng.randint(1, 6)):
        m = (rng.randint(0, 3), rng.randint(0, 3), rng.randint(0, 2))
        if 0 < R.A.deg(m) <= maxdeg:
            poly[m] = rng.randint(1, p - 1)
    return poly or {(1, 0, 0): 1}


def _multiplicative(name, seed):
    phi = R.endo_phi(name)
    p = phi["p"]
    rng = random.Random(seed)
    for _ in range(20):
        u, v = _random_form(rng, p, 3), _random_form(rng, p, 3)
        assert R.phi_poly(phi, R.mul(u, v, p)) == R.mul(R.phi_poly(phi, u), R.phi_poly(phi, v), p)


def test_phi_is_multiplicative_on_twenty_random_pairs_a3():
    _multiplicative("A3", 13)


def test_phi_is_multiplicative_on_twenty_random_pairs_b4():
    _multiplicative("B4", 14)


def test_phi_z_is_computed_not_typed():
    phi = R.endo_phi("B4")
    p = phi["p"]
    assert phi["z"] == R.sub(R.mul(phi["x"], phi["y"], p), R.mul(phi["y"], phi["x"], p), p)


def test_module_generators_are_in_the_pbw_basis():
    # Q3 over GF(3): x^2 + y^2 + y x = x^2 + y^2 + x y - z and x^2 + y x - z = x^2 + x y - 2 z = x^2 + x y + z
    g1, g2 = R.mod_gens("Q3")
    assert g1 == {(2, 0, 0): 1, (0, 2, 0): 1, (1, 1, 0): 1, (0, 0, 1): 2}
    assert g2 == {(2, 0, 0): 1, (1, 1, 0): 1, (0, 0, 1): 1}


def test_scaling_of_a_table():
    t = {(0, 0): 1, (1, 2): 2, (2, 6): 2, (3, 8): 1}
    assert R.scale_table(t, 4) == {(0, 0): 1, (1, 8): 2, (2, 24): 2, (3, 32): 1}
    assert R.scale_table(t, 1) == t


def test_compare_on_a_case_built_to_differ():
    base = {(0, 0): 1, (1, 2): 2, (2, 6): 2, (3, 8): 1}
    good = R.scale_table(base, 3)
    assert R.compare(good, 27 * 8, base, 8, 3) == {"table_is_scaled_table": True, "length_is_d3_times": True}
    bad = dict(good)
    bad[(2, 18)] = 3
    assert R.compare(bad, 27 * 8, base, 8, 3)["table_is_scaled_table"] is False
    assert R.compare(good, 27 * 8 + 1, base, 8, 3)["length_is_d3_times"] is False
    assert R.compare(None, None, base, 8, 3) == {"table_is_scaled_table": None, "length_is_d3_times": None}


def test_phi_of_the_image_pair_gives_the_pair_of_the_hypothesis_s1():
    s, phi, gens, imgs = R.case_setup("S1")
    # the image of the stored generators, nothing else: two generators of degree 6
    assert len(imgs) == len(gens) == 2
    assert all(max(R.A.deg(m) for m in g) == 6 for g in imgs)
    assert imgs[0] == R.phi_poly(phi, gens[0])
