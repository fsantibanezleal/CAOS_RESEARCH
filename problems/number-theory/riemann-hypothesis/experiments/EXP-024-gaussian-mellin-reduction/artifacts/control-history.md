# Control history

The first enclosed-kernel launch failed on an unsupported arb.inv() API;
setup-failure.txt retains it. Division corrected that API error before the
eight independent integral controls and 32 explicit remainder checks passed.

The first full-moment control passed, including the wrong-residue-sign
negative control, but Ruff reported an unused math import. Its receipt and
exact runtime source are preserved as initial-full-moment-control.json and
initial-full-moment-control-source.txt. The latter matches the original
code hash in that historical receipt. Remove the unused import and an
unused overwritten residue assignment, then rerun the complete control.
Neither cleanup changes any used mathematical expression. The current
receipt binds the cleaned runtime source. Both runs retain explicit tails.
