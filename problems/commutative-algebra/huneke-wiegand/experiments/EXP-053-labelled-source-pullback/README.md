# EXP-053 labelled source pullback

This experiment pulls the sparse EXP-052 relative cycle back through the transformed-HNF kernel
basis to the original labelled chain domain. The hypothesis is committed before extraction.

Run the training phase with:

```powershell
python extract_training.py --budget-seconds 600 --memory-gib 10
```

Do not inspect `p=11` source labels until a candidate has been frozen from `p=8,9,10`.
