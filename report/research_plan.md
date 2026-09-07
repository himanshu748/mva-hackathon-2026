# Research plan: selective clearance with preserved tissue function

Prepared 7 September 2026. This is a proposed preclinical plan, not a registered protocol, completed experiment or treatment recommendation. The next decisions require a qualified laboratory and clinical research team; no contact with the child or family is proposed.

## Question and present decision

Does dasatinib, alone or with quercetin, selectively reduce an excess senescent-cell population in a BUB1B disease model while preserving healthy developing-cell function and avoiding increased chromosome instability among survivors?

Retain D+Q as a conditional research candidate. Do not advance it toward administration on the evidence assembled here. Dasatinib is the approved drug selected for repurposing; quercetin remains an experimental partner. The combination has to earn its place by comparison with each component.

The original proposal joined genetic mouse evidence to adult drug studies. That bridge leaves three uncertainties: whether this patient's cells have the target, whether the drugs act selectively in relevant cell types, and whether the overall tissue effect is beneficial. The 2026 oligodendrocyte study makes the third question especially important because dysfunction occurred without apparent cell death.

## Models and controls

| Comparison | What it can resolve | What it cannot establish |
|---|---|---|
| Patient-background cells versus an independently verified corrected control | Whether a cellular phenotype tracks the candidate genotype in that background | Effects in other patients; clone-specific effects without additional controls |
| Unrelated non-MVA controls | Baseline variation and toxicity in another background | A substitute for an isogenic comparison |
| Multiple independently derived clones/culture preparations | Reproducibility within the selected model and sensitivity to clone/batch effects | Between-patient replication when all clones come from one patient |
| Induced-senescence assay control | Whether the assay can detect a known positive state and drug response | The presence of disease-driven senescence in MVA |
| Cell types relevant to muscle function and neural development | Tissue-specific activity and off-target function | A complete organism-level therapeutic window |

Any patient-derived material would require appropriate consent and institutional authorization. Model availability is not established. Select the model and feasibility criteria before promising an experimental schedule or cost.

## Intervention comparisons

Run vehicle, dasatinib, quercetin and D+Q under matched conditions. Include untreated assay controls where vehicle effects are uncertain. Use the same time points and blinded outcome scoring. Set concentrations and exposure schedules through a pharmacology feasibility review, rather than translating an adult oral dose into a cell experiment or a pediatric regimen.

A favorable D+Q-versus-vehicle result alone does not establish combination advantage. Compare with both components. If dasatinib alone provides comparable benefit with less harm, the experiment should remove the partner rather than preserve the preferred story. A synergy claim would require a prespecified interaction model, adequate dose-response data and uncertainty estimates; no synergy is claimed here.

Genotype correction is a mechanistic control, not a repurposed medication. The SIRT2/BubR1 stabilization literature provides a separate upstream hypothesis, but does not establish an approved drug that repairs these specific variants. Avoid selecting a checkpoint inhibitor merely because its target list contains BUB1B: inhibition in a cancer model is a different therapeutic objective from preserving checkpoint function in non-tumor tissue.

## Outcomes and reasons to stop

| Domain | Required observation | Misleading shortcut to avoid | Consequence for the proposal |
|---|---|---|---|
| Target presence | Reproducible baseline excess using complementary arrest, senescence and secretory readouts | One positive p16 or SA-beta-gal marker defines the target | Absent target prevents progression of this mechanism in that model |
| Preferential clearance | Absolute counts, death markers and fate of senescent versus non-senescent populations | Reduced marker expression alone proves cell removal | Nonspecific killing rejects the claimed selectivity |
| Function | Prespecified tissue-relevant functional readout after exposure and washout | Normal viability implies normal differentiation or tissue function | Functional harm stops progression even if senescence markers fall |
| Neural safety | Oligodendrocyte differentiation/myelin-related functional measurements in an appropriate model | Healthy-looking surviving cells establish safety | Reproduced neural dysfunction is a blocking result at the tested exposure |
| Ongoing chromosome instability | Segregation errors per observed division and micronuclei/aneuploidy measures in survivors | Lower aneuploid fraction proves restored chromosome segregation | Worsened errors stop progression; compositional selection is reported separately |
| Persistence | Recovery, replenishment of senescent cells and function after washout | A favorable immediate endpoint implies durable benefit | Rapid recurrence constrains the proposed benefit and exposure rationale |
| Cancer context | Parallel assessment of non-tumor tissue and relevant tumor behavior | Killing damaged cells proves reduced lifetime cancer risk | Adverse tumor behavior blocks translation; clinical oncology interactions remain separate |

Preservation of a harmful clone and loss of healthy cells are both possible selection effects. Record total cell yield and population proportions together so a denominator change cannot masquerade as repair.

## Analysis before outcomes are known

The independent unit is the biological culture preparation or other justified experimental unit, not each cell or each image. Aggregate technical wells within their unit. Report the number of donors, clones, preparations, wells and scored cells separately. Multiple clones from one patient remain one patient background; a confidence interval across those clones does not describe population-level clinical response.

Randomize treatment allocation within batches and balance batches across conditions. Blind image analysis and endpoint adjudication. Prespecify exclusions, missing-data handling and the primary endpoint. Record all groups and all planned endpoints, including null and adverse outcomes.

The primary analysis should estimate a treatment contrast for a tissue-relevant functional endpoint, with uncertainty at the biological-unit level. Target engagement, selective clearance and harm outcomes are complementary requirements; they should not be averaged into a single score that allows a large biomarker change to compensate for neural injury. Use explicit noninferiority/equivalence margins for preservation of healthy function when justified. A nonsignificant harm test does not demonstrate safety.

The laboratory team must set meaningful effect-size and harm margins, exposure feasibility, follow-up duration, multiplicity handling and a replication plan before confirmatory data collection. Use a separate feasibility stage to estimate variability and inform sample size. These values remain undecided; this document does not invent numerical cutoffs or claim adequate statistical power.

## Research value if the drug fails

A well-controlled null or adverse result would still distinguish an unsupported treatment from a plausible target. Publish a source-linked record of the model, exposure, controls and outcomes, subject to consent and data-use restrictions. Other teams could reuse the evidence structure and endpoint definitions without receiving the child's genomic dataset. Reuse across CEP57 or TRIP13 disease would require fresh target and safety evidence.

Patient benefit should eventually be assessed with outcomes meaningful to affected families, such as function and treatment burden, through authorized research channels. No patient preference, consultation or clinical improvement is claimed in this entry.

## Targeted literature search record

Searches were run on 7 September 2026 through web search, followed by primary-source inspection. This was a targeted challenge of the proposal, not a systematic review. Queries covered BUB1B/BubR1 rescue and drug repurposing; D+Q discovery and cell-type specificity; D+Q randomized trials and primary endpoints; D+Q oligodendrocyte dysfunction and demyelination; and SIRT2/BubR1 stabilization. Searches for the exact missense and stop protein names did not establish variant-specific functional evidence. Absence of a search result is not evidence of novelty or benignity.

Include a study if it directly informs disease mechanism, the selected drug's activity, a relevant negative result, safety, or the distinction between genetic and pharmacologic intervention. Do not combine heterogeneous studies into a pooled efficacy estimate. Regulatory status comes from labeling, not a paper's casual description of a compound as approved. Reviews and social posts were used only to locate primary work.

The structured source register is `evidence_ledger.json`. It records what each study supports and what it cannot establish. No patient-derived drug-response measurement appears in that ledger.

## Acknowledgement

> This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
