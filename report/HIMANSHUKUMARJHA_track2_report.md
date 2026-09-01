# Track 2 Report: Drug Repurposing

**MVA Hackathon 2026, "Rare Disease, Real Kid"**
Team: Himanshu Kumar (HIMANSHUKUMARJHA)
Proband: PROBAND01, *BUB1B* compound heterozygous
Date: 1 September 2026

> This report proposes a research hypothesis for preclinical investigation. It is not a treatment recommendation, not medical advice, and not a suggestion that any named medicine should be given to this child or any other. Nothing here should reach a clinical decision without the validation programme set out in section 7.

---

## 1. The proposal in one paragraph

The causal genotype is a *BUB1B* null allele in trans with a hypomorph (Track 1). The single best-characterised animal model of that exact genotype, the **BubR1 hypomorphic mouse**, is a progeroid model in which **senescent cells accumulate and are causally responsible for the pathology**: genetically clearing p16^Ink4a-positive cells in these mice delays the disease. Senescent-cell burden is therefore not a side effect of the *BUB1B* defect but a validated, druggable node downstream of it. We propose the **senolytic combination dasatinib plus quercetin (D+Q)** as the candidate for investigation. Dasatinib is FDA-approved in children with established weight-based dosing, quercetin is a widely available flavonoid, the combination has first-in-human safety and target-engagement data, and it is given intermittently rather than continuously. To our knowledge senolytics have never been proposed or tested in mosaic variegated aneuploidy.

---

## 2. Mechanism characterisation

### 2.1 From genotype to protein

| Allele | Variant | Protein effect | Predicted outcome |
|---|---|---|---|
| 1 | c.2210T>G | p.Leu737Ter, exon 17 of 23 | PTC well upstream of the final exon-exon junction, triggers nonsense mediated decay, **true null** |
| 2 | c.3006T>G | p.Asn1002Lys, exon 23 of 23 | last exon, escapes NMD, full-length protein in the kinase domain, **hypomorph** |

Total BUBR1 activity is therefore roughly one attenuated allele's worth. This is the defining feature of viable MVA1: complete biallelic loss of *BUB1B* is embryonic lethal, and every surviving patient retains partial function through a hypomorphic allele. Our proband's genotype is the textbook instance of that constraint.

### 2.2 From protein to cell

BUBR1 is the core effector of the **spindle assembly checkpoint (SAC)**. With securin and BUB3 it forms the mitotic checkpoint complex, which sequesters CDC20 and restrains the anaphase-promoting complex (APC/C) until every kinetochore is correctly attached to the spindle. Reduced BUBR1 dosage weakens that restraint, anaphase begins before attachment is complete, and whole chromosomes missegregate.

Repeated over many divisions this produces the **variegated pattern of gains and losses across different chromosomes in different cells** that names the disease. It is a per-division stochastic process, which is why the aneuploidy is mosaic and tissue-variable rather than constitutional.

### 2.3 From cell to disease, and where the drug target is

The step that matters therapeutically is what happens to an aneuploid cell. It does not simply carry on. Aneuploidy imposes acute proteotoxic, metabolic and replicative stress, and it generates DNA damage. The dominant cell fate is **cellular senescence**: a stable arrest accompanied by the senescence-associated secretory phenotype (SASP), a programme of inflammatory cytokines, chemokines and proteases exported into the tissue.

This is the crux of the argument, and it is not speculation. The BubR1 hypomorphic mouse carries a hypomorphic *Bub1b* mutation, has high levels of constitutive DNA damage, and shows a markedly shortened lifespan with sarcopenia, cataracts, fat loss, arterial stiffening, impaired wound healing and infertility. In that model, **genetic inactivation of p16^Ink4a, or inducible clearance of p16^Ink4a-positive cells using the INK-ATTAC system, slows the functional decline of tissues**, establishing a causal link between senescent-cell accumulation and functional impairment rather than a correlative one.

So the chain is:

```
BUB1B null / hypomorph
      -> reduced BUBR1 dosage
      -> weakened spindle assembly checkpoint
      -> whole-chromosome missegregation (mosaic variegated aneuploidy)
      -> aneuploidy-induced stress and DNA damage
      -> senescent cell accumulation + SASP        <-- DRUGGABLE NODE
      -> tissue dysfunction, growth failure, and a pro-tumorigenic microenvironment
```

The upstream steps are not druggable. You cannot restore a missing allele, and a drug that stabilised the checkpoint would have to act in every dividing cell continuously and would carry unacceptable mitotic toxicity. The senescence node is different: it is downstream, it is where the damage is actually cashed out into pathology, it accumulates rather than acting instantaneously, and it has approved drugs pointed at it.

### 2.4 Why this explains the specific patient

Each of the proband's features maps onto this chain rather than requiring separate explanation.

| Clinical feature | Mechanistic account |
|---|---|
| Rhabdomyosarcoma (HP:0002859) | chromosomal instability generates oncogenic karyotypes; SASP supplies a pro-tumorigenic, inflammatory microenvironment |
| Small for gestational age, short stature (HP:0001518, HP:0004322) | reduced effective proliferative capacity; senescent cells occupy niches without dividing |
| Failure to thrive, skeletal muscle atrophy (HP:0001508, HP:0003202) | direct parallel to the sarcopenia of the BubR1 hypomorphic mouse |
| Nephrocalcinosis (HP:0000121) | tissue-level dysfunction and inflammatory remodelling |
| Premature birth (HP:0001622) | placental and fetal proliferative compromise |
| Parental recurrent miscarriage (HP:0200067) | aneuploid conceptions from carrier parents |

The muscle phenotype deserves emphasis. **Sarcopenia is the signature phenotype of the BubR1 hypomorphic mouse**, and this child presents with documented skeletal muscle atrophy and failure to thrive. The correspondence between the model organism's cardinal phenotype and the patient's is unusually tight for a rare disease, and it is what makes the senescence hypothesis worth testing rather than merely plausible.

---

## 3. The candidate: dasatinib plus quercetin

Senescent cells resist apoptosis through senescent-cell anti-apoptotic pathways (SCAPs). Different senescent cell types depend on different SCAPs, which is why the founding senolytic regimen is a **combination**: dasatinib, a tyrosine kinase inhibitor, and quercetin, a flavonoid, together cover a broader range of senescent cell types than either alone.

**Why this combination and not another senolytic:**

- **Dasatinib is already approved in children.** The FDA granted regular approval for pediatric Ph+ CML in November 2017 and extended it to pediatric Ph+ ALL in 2019, with established weight-based dosing (10 to <20 kg: 40 mg; 20 to <30 kg: 60 mg; 30 to <45 kg: 75 mg; 45 kg and above: 100 mg). For a pediatric rare-disease hypothesis this removes the single largest translational obstacle: there is real pediatric pharmacokinetic and safety experience, not an extrapolation from adults.
- **There is human senolytic data.** D+Q has been through a first-in-human open-label pilot in idiopathic pulmonary fibrosis (Justice et al., 2019) and a trial in diabetic kidney disease that demonstrated **target engagement in humans**, an actual reduction in senescent-cell burden, not merely a clinical endpoint.
- **Dosing is intermittent, not continuous.** Senolytics are "hit and run": the published human regimen is three consecutive days per week for three weeks, nine doses total. This matters enormously here and is developed in section 5.
- **Quercetin is low-risk.** A widely available flavonoid with a benign tolerability profile.

**Why not navitoclax**, the other well-known senolytic: it causes dose-limiting thrombocytopenia and neutropenia. In a child with a cancer-predisposition syndrome who may require cytotoxic chemotherapy, adding a marrow-suppressive agent is the wrong trade. We rejected it on that basis.

**Possible secondary benefit, flagged as speculative.** Dasatinib inhibits SRC-family kinases, which have been investigated in sarcoma biology. We are deliberately not building any part of the argument on this. It is a hypothesis-generating observation, not a second indication.

---

## 4. What makes this different from a database query

The obvious computational approach to Track 2 is to query a drug-target database for *BUB1B* and return whatever binds it. That produces mitotic inhibitors, which is precisely backwards: this patient's problem is too little checkpoint function, and the drugs that appear are ones that perturb mitosis further.

The reasoning here runs through the **disease mechanism rather than the gene product**. The target is not BUBR1. The target is the senescent-cell population that a lifetime of BUBR1 insufficiency produces. That reframing is what surfaces an approved pediatric drug with human target-engagement data, and it is not reachable by target-based querying.

The supporting evidence chain is also unusually direct for a rare disease. Most repurposing hypotheses connect a human genotype to a drug through several inferential hops. Here the model organism carries **a hypomorphic mutation in the same gene**, and the intervention has been demonstrated causally **in that model**. The inference is from BubR1 hypomorph to BUB1B hypomorph, not across a pathway analogy.

---

## 5. Safety, stated honestly

This is where an enthusiastic report would stop and a serious one continues. There is a direct and serious tension in this proposal.

**The central concern: dasatinib affects growth and development in children.** The prescribing information carries explicit warnings on effects on growth and development in pediatric patients, and requires that bone growth and development be monitored. This proband already presents with **short stature, small for gestational age and failure to thrive**. A drug that impairs growth is being proposed for a child whose growth is already the presenting problem. That tension has to be resolved before anything else is discussed, and it is the first thing we would want a reviewer to interrogate.

**Why the tension may be resolvable, and why that is a hypothesis rather than an answer:**

The pediatric growth data derive from **continuous daily dosing** in CML and ALL, sustained over months to years. The senolytic regimen is categorically different: three days per week for three weeks, then stop. Total exposure is roughly an order of magnitude lower and is not sustained. Senolytics work by killing a persistent cell population, so the effect outlasts the drug and the drug does not need to be present chronically. Whether that difference in exposure is sufficient to avoid the growth signal is **an empirical question that has not been answered**, and it is the single most important thing the preclinical programme in section 7 must resolve.

**Other warnings requiring monitoring:** myelosuppression and bleeding, fluid retention, cardiovascular toxicity, pulmonary arterial hypertension, QT prolongation, severe dermatologic reactions, tumor lysis syndrome and hepatotoxicity.

**Cancer-context interaction.** The proband has had rhabdomyosarcoma. Any intervention must be evaluated against active or planned oncological therapy, and myelosuppression risk during chemotherapy is a specific contraindication to concurrent use.

**A theoretical risk that argues against the proposal, stated because it is real.** Senescence is a tumour-suppressive mechanism. It exists to arrest cells that have sustained damage. In a patient whose cells are continuously generating aneuploidy, removing senescent cells could in principle release damaged cells that senescence had safely contained, in a child who already has a cancer predisposition. The counter-argument is that the SASP is itself pro-tumorigenic and that senescent-cell clearance reduced cancer incidence in mouse studies. **We do not think this is settled**, and we regard it as the most important biological objection to the entire hypothesis. It must be addressed with tumour-incidence endpoints in the model before any clinical consideration, not hand-waved.

---

## 6. Alternatives considered

| Candidate | Rationale | Why not primary |
|---|---|---|
| **Navitoclax** | potent senolytic | thrombocytopenia and neutropenia; wrong risk profile in a cancer-predisposed child |
| **Metformin** | AMPK activation, aneuploidy tolerance, mild senomorphic effect | very weak effect size; does not clear senescent cells, only dampens SASP |
| **HSP90 inhibitors** | aneuploid cells carry proteotoxic stress and are HSP90-dependent | no approved agent with an acceptable pediatric profile; narrow therapeutic window |
| **Fisetin** | flavonoid senolytic, excellent safety | weaker human evidence than D+Q; a reasonable lower-risk alternative if dasatinib is excluded on growth grounds, and we would advance it in that case |
| **Antioxidants (NAC etc.)** | oxidative stress in BubR1 mice | addresses a consequence, not the accumulating cell population; unlikely to alter trajectory |

Fisetin is the designated fallback. If the growth-toxicity question in section 5 resolves against dasatinib, the hypothesis survives with fisetin substituted, because the argument is about the **senescence node**, not about dasatinib specifically. That is a deliberate design property: the proposal degrades gracefully rather than collapsing.

---

## 7. Validation plan, and what would falsify this

A hypothesis that cannot be killed is not worth proposing. In order:

1. **Establish senescent-cell burden in patient-derived cells.** Fibroblasts from the proband, assayed for SA-beta-gal, p16^Ink4a and p21 expression, and SASP cytokine profile, against age-matched controls. **Falsification: if senescent-cell burden is not elevated, the hypothesis is dead.** This is the cheapest and fastest experiment and it should be done first.
2. **Confirm the alleles are in trans.** Parental carrier testing or long-read phasing. This is the outstanding gap from Track 1 and it conditions everything downstream.
3. **Functional confirmation of the hypomorph.** Checkpoint activity assay in patient cells, confirming p.Asn1002Lys is attenuating rather than merely predicted damaging.
4. **Senolytic response in vitro.** D+Q on patient-derived fibroblasts; does senescent-cell burden fall, and are proliferating cells spared?
5. **The growth question, in vivo.** Intermittent D+Q in BubR1 hypomorphic mice, with **bone growth and body composition as primary endpoints**, not as safety afterthoughts. This is the experiment that decides whether the proposal is viable in a child.
6. **Tumour incidence endpoints** in the same model, addressing the objection in section 5.
7. Only then, and only through a formal regulatory pathway with the treating clinical team, does any of this approach a patient.

---

## 8. Scalability

The reasoning generalises well beyond this child, which is the point of doing it this way.

**Same gene, other patients.** MVA1 is defined by *BUB1B* hypomorphism. Every MVA1 patient sits on the same mechanistic chain, so the hypothesis is a disease-level hypothesis, not a patient-level one. MVA affects fewer than 50 people worldwide, and a mechanism-level hypothesis is the only kind that can serve a population that small.

**Same node, other diseases.** The generalisable claim is that **chromosomal instability disorders converge on senescent-cell burden as a shared, druggable node**. That reaches the other MVA genes (*CEP57*, *TRIP13*), and more broadly the chromosome-instability and DNA-repair disorders in which senescence accumulates. Any monogenic disease whose mouse model is progeroid is a candidate for the same reasoning.

**The method is a reusable procedure**, not a one-off insight: characterise the allele series precisely (null versus hypomorph, with NMD prediction), identify the model organism carrying the same class of lesion, ask what intervention has been shown causal in that model, then ask whether an approved drug hits that node with acceptable pediatric exposure. The Track 1 pipeline supplies the first step for any proband from a VCF plus an HPO list in about 30 minutes on a laptop.

---

## 9. Limitations

**Phasing is unproven.** Carried forward from Track 1 and repeated here because it is load-bearing: the trans configuration is inferred from phenotype, not demonstrated.

**No patient-derived cells were available.** Every statement about senescent-cell burden in this specific child is an inference from the genotype and from the mouse model. Experiment 1 in section 7 exists precisely because this is currently unmeasured.

**The mouse-to-human inference is real but not free.** BubR1^H/H mice carry a hypomorphic allele; our proband carries a null plus a hypomorph. These are related but not identical genetic architectures, and the mouse is not a model of rhabdomyosarcoma predisposition.

**The growth-toxicity question is open**, and it is the most likely reason this proposal fails.

**Senolytic clearance of a tumour-suppressive mechanism in a cancer-predisposed child is a genuine theoretical hazard**, not a formality.

**Our own aneuploidy analysis was inconclusive.** The Track 1 screen flagged chromosomes 20, 21 and 22 on two concordant axes, but with a single sample and no matched control we could not separate that from GC and mappability bias. We have not demonstrated the aneuploidy in this child from the data supplied, only inferred it from the diagnosis.

---

## 10. Methods description form, Track 2

**Team name:** Himanshu Kumar

**Please describe your approach in detail (how you went from variant/mechanism to candidate medication(s)).**
See sections 2 and 3. Briefly: we characterised the allele series from Track 1 (NMD-triggering null plus last-exon hypomorph), traced the mechanistic chain from BUBR1 dosage through spindle assembly checkpoint failure to aneuploidy-induced senescence, then searched for the point in that chain where an intervention has been shown **causal** rather than correlative in a model organism carrying a lesion in the same gene. That identified senescent-cell clearance in the BubR1 hypomorphic mouse. We then asked which approved drugs act at that node with acceptable pediatric exposure, which selected dasatinib plus quercetin, and rejected alternatives on risk grounds specific to this patient's cancer predisposition.

**(required) Generative AI disclosure.**

> **Provider:** Anthropic. **Model:** Claude Opus 5, accessed through Claude Code. **Plan or tier:** consumer Claude subscription (not the Anthropic API and not an Enterprise agreement). **Data-handling setting:** model training on conversation content is disabled; no data is shared for training.

The assistant was used for literature search, reasoning and drafting. Every factual claim about drug approval status, dosing, trial results and mouse-model findings was verified against primary or authoritative sources listed below, and citations are to those sources rather than to model output. No genomic or clinical data was uploaded to any commercial generative AI provider. Challenge data handling is as described in the Track 1 report.

**Was candidate identification automated or primarily manual literature review and expert curation?**
Primarily manual, mechanism-led literature review, deliberately so. We did not run a drug-target database query against *BUB1B*, because that approach returns mitotic inhibitors, which are contraindicated by the mechanism: the defect is insufficient checkpoint function and such drugs would perturb it further. Candidate identification was driven by reasoning about the disease mechanism and then constrained by pediatric approval status and by this patient's specific risk profile.

**Please describe any manual literature review or expert curation in detail.**
Targeted searches on the BubR1 hypomorphic mouse as a progeroid model and senescent-cell clearance in it; on senolytic first-in-human trials and demonstrated target engagement; and on dasatinib pediatric approval, dosing and its warnings. Each candidate was then filtered against this proband's context: pediatric approval, marrow-suppression risk given cancer predisposition, and growth effects given the presenting short stature and failure to thrive. Alternatives were recorded with reasons for rejection (section 6) rather than discarded silently.

**Did you rely solely on publicly available drug/target databases and literature?**
Yes, exclusively. No proprietary data sources were used.

**Please describe the public data sources used in detail.**
Peer-reviewed literature accessed via PubMed Central, Nature, Cell Reports, PLOS Genetics and EBioMedicine (specific sources in section 12). FDA pediatric approval and prescribing information for dasatinib as reported by AACR *Cancer Discovery*, the ASCO Post, OncLive and the Drugs.com professional monograph. Pharos and the IUPHAR/BPS Guide to Pharmacology for MVA1 target annotation. ClinVar and OMIM for variant and disease context. Ensembl VEP, gnomAD, GENCODE and the Human Phenotype Ontology as described in the Track 1 report.

**Please describe any proprietary data sources used in detail.**
None.

**How did you characterize the variant's mechanism?**
**Loss of function**, specifically a compound heterozygous null-plus-hypomorph configuration rather than complete loss, which is the architecture compatible with survival. p.Leu737Ter sits in exon 17 of 23, well upstream of the final exon-exon junction and therefore within the window that triggers nonsense mediated decay, making it a true null. p.Asn1002Lys sits in the terminal exon within the kinase domain, escapes decay, and yields full-length protein with impaired function. **Pathway disrupted:** the spindle assembly checkpoint, through the mitotic checkpoint complex that sequesters CDC20 and restrains the APC/C. **Downstream biological consequence:** premature anaphase onset, whole-chromosome missegregation producing mosaic variegated aneuploidy, aneuploidy-induced stress and DNA damage, and consequent accumulation of senescent cells with a pro-inflammatory SASP, which is the proposed point of therapeutic intervention.

**Please provide an estimate of time or effort spent on this analysis.**
Approximately one working day for Track 1 and Track 2 combined, including pipeline development, verification and both reports. Computational cost zero: public APIs and one laptop.

**Method abstract (up to 500 words).**

We propose senolytic therapy, specifically the dasatinib plus quercetin combination, as a drug repurposing hypothesis for *BUB1B*-associated mosaic variegated aneuploidy, and we propose it as a candidate for preclinical investigation rather than as a treatment.

The reasoning is mechanism-led rather than target-led. Track 1 established a compound heterozygous genotype: c.2210T>G p.Leu737Ter in exon 17 of 23, upstream of the final exon-exon junction and therefore NMD-triggering, hence a true null; in trans with c.3006T>G p.Asn1002Lys in the terminal exon within the kinase domain, escaping decay and yielding a hypomorphic full-length protein. Reduced BUBR1 dosage weakens the spindle assembly checkpoint, permitting anaphase onset before all kinetochores are attached. The resulting whole-chromosome missegregation produces the variegated aneuploidy that names the disease.

The therapeutically relevant step is the fate of aneuploid cells. Aneuploidy imposes proteotoxic and replicative stress and generates DNA damage, driving cells into senescence with a pro-inflammatory secretory phenotype. Critically, this is not inference: the BubR1 hypomorphic mouse, carrying a hypomorphic mutation in the same gene, is a progeroid model in which genetic inactivation of p16^Ink4a or inducible clearance of p16^Ink4a-positive cells slows tissue functional decline, establishing senescent-cell accumulation as causal rather than correlative. Senescent-cell burden is therefore a validated, druggable node downstream of an undruggable lesion. The mouse's cardinal phenotype, sarcopenia, corresponds directly to this child's documented skeletal muscle atrophy and failure to thrive.

Dasatinib plus quercetin was selected over other senolytics on grounds specific to this patient. Dasatinib holds FDA approval in children with established weight-based dosing, removing the usual pediatric extrapolation problem. D+Q has first-in-human trial data including demonstrated reduction of senescent-cell burden in humans. Dosing is intermittent rather than continuous, which materially changes the exposure profile. Navitoclax was rejected for marrow suppression in a cancer-predisposed child; fisetin is retained as a graceful fallback, since the argument concerns the senescence node rather than dasatinib specifically.

Strengths. The evidence chain is unusually short for a rare disease: the model organism carries a lesion in the same gene and the intervention was demonstrated causal in that model, rather than inferred across a pathway analogy. The candidate is an approved pediatric drug. The mechanism accounts for every element of the presenting phenotype. The reasoning generalises to all MVA1 patients, to *CEP57* and *TRIP13*, and to chromosomal instability disorders broadly.

Limitations, and they are substantial. Dasatinib carries explicit warnings on growth and development in children, and this child's presenting problem is growth failure; whether intermittent senolytic dosing avoids that signal is unresolved and is the most likely failure mode. Senescence is tumour-suppressive, so clearing senescent cells in a cancer-predisposed child is a genuine theoretical hazard requiring tumour-incidence endpoints before clinical consideration. Phasing remains unproven. No patient-derived cells were available, so senescent-cell burden in this child is inferred, not measured. The falsifying experiment is first in the validation plan for that reason.

---

## 11. What we would want a judge to press us on

We would rather name our weakest points than have them found.

1. **The growth-toxicity tension in section 5.** We think intermittent dosing resolves it. We have not shown that.
2. **Removing a tumour suppressor mechanism in a tumour-prone child.** The strongest biological objection to the whole proposal.
3. **Mouse hypomorph versus human null-plus-hypomorph.** Related architectures, not identical.
4. **We measured nothing in this patient.** The entire senescence claim rests on genotype and model-organism inference.

---

## 12. Key sources

- Baker DJ, Wijshake T, Tchkonia T, et al. Clearance of p16Ink4a-positive senescent cells delays ageing-associated disorders. *Nature* 479:232-236 (2011). [PDF](https://static1.squarespace.com/static/5a2069c3ccc5c5325fd05b02/t/5a475049f9619ae3bb34ac41/1514623052249/2011_baker.pdf)
- [Reduced Life- and Healthspan in Mice Carrying a Mono-Allelic BubR1 MVA Mutation. *PLOS Genetics*](https://journals.plos.org/plosgenetics/article?id=10.1371%2Fjournal.pgen.1003138)
- [p21 Both Attenuates and Drives Senescence and Aging in BubR1 Progeroid Mice. *Cell Reports*](https://www.cell.com/cell-reports/fulltext/S2211-1247(13)00135-6)
- [A novel in vitro model of sarcopenia using BubR1 hypomorphic C2C12 myoblasts. *Cytotechnology*](https://link.springer.com/article/10.1007/s10616-015-9920-7)
- [Hickson LJ, et al. Senolytics decrease senescent cells in humans: preliminary report from a clinical trial of dasatinib plus quercetin in individuals with diabetic kidney disease. *EBioMedicine*](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6796530/)
- [First-in-human trial of senolytic drugs (Justice et al., idiopathic pulmonary fibrosis)](https://www.sciencedaily.com/releases/2019/01/190107112944.htm)
- [Dasatinib Approved for Pediatric CML. *Cancer Discovery*, AACR](https://aacrjournals.org/cancerdiscovery/article/8/1/OF2/112595/Dasatinib-Approved-for-Pediatric-CMLDasatinib)
- [FDA Approves Dasatinib for Pediatric Ph+ ALL. OncLive](https://www.onclive.com/view/fda-approves-dasatinib-for-pediatric-ph-all)
- [Dasatinib monograph for professionals. Drugs.com](https://www.drugs.com/monograph/dasatinib.html)
- [Pharos: mosaic variegated aneuploidy syndrome 1](https://pharos.nih.gov/diseases/mosaic%20variegated%20aneuploidy%20syndrome%201)
- [Mosaic variegated aneuploidy syndrome 1; MVA1. IUPHAR/BPS Guide to Pharmacology](https://www.guidetopharmacology.org/GRAC/DiseaseDisplayForward?diseaseId=638)
- [Pathogenic correlation between mosaic variegated aneuploidy 1 (MVA1) and a novel BUB1B variant. PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9616775/)

---

## 13. Acknowledgement

> "This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible."
