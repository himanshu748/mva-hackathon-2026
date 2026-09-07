"""Exploratory lookup in a historical configured secondary-gene set.
Not a complete/current ACMG clinical secondary-findings screen. Filtering and
transcript selection upstream can exclude actionable variants.
"""
import os, sys as _s; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))  # run from repo root
import json

# Historical configured gene set; not asserted to be a complete ACMG release.
ACMG = set("""ACTA2 ACTC1 ACVRL1 APC APOB ATP7B BAG3 BMPR1A BRCA1 BRCA2 BTD CACNA1S CALM1
CALM2 CALM3 CASQ2 COL3A1 DES DSC2 DSG2 DSP ENG FBN1 FLNC GAA GLA HFE HNF1A KCNH2 KCNQ1
LDLR LMNA MAX MEN1 MLH1 MSH2 MSH6 MUTYH MYBPC3 MYH11 MYH7 MYL2 MYL3 NF2 OTC PALB2 PCSK9
PKP2 PMS2 PRKAG2 PTEN RB1 RET RPE65 RYR1 RYR2 SCN5A SDHAF2 SDHB SDHC SDHD SMAD3 SMAD4
STK11 TGFBR1 TGFBR2 TMEM43 TNNI3 TNNT2 TP53 TPM1 TRDN TSC1 TSC2 TTN TTR VHL WT1""".split())

recs = json.load(open("out/ranked_top200.json"))
hits = [r for r in recs if r["gene"] in ACMG]

print(f"ranked variants screened: {len(recs)}")
print(f"variants in configured secondary-gene set: {len(hits)}\n")
if not hits:
    print("No candidates in this limited lookup; not a negative clinical finding.")
for r in hits:
    af = "absent" if r["af"] is None else f"{r['af']:.1e}"
    print(f"  {r['gene']:<9} {r['input'].split(' . ')[0]:<20} {r['cons']:<28} "
          f"gnomAD={af:<9} GT={r['gt']} AD={r['ad']}")
    print(f"            {r['hgvsp']}")
print("\nEach hit requires manual assessment against gene-specific ACMG reporting")
print("criteria before it is reported. See section 7 of the Track 1 report.")
