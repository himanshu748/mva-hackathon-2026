# Rules and judging audit

Checked 7 September 2026 against the organizer's live source files: [rules](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/main/tabs/rules.py), [FAQ](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/main/tabs/faq.py), [Track 1 instructions](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/main/tabs/submit_track1.py), [Track 2 instructions](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/main/tabs/submit_track2.py), and the [processor clarification](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/2). The rules, FAQ and submission instructions match the earlier saved copies byte for byte. This audit records requirements and evidence; it is not an organizer certification of eligibility or compliance.

## Judging alignment

| Criterion | Weight | Concrete response | Remaining limitation |
|---|---:|---|---|
| Scientific rigor | 35% | Corrected chronology and mechanism; annotation-integrity tests; sensitivity results; supporting, null and adverse primary evidence; explicit outcome/analysis plan | No biological experiments; no held-out diagnostic validation |
| Potential impact | 25% | Tests whether tissue function can improve without sacrificing healthy cells; makes harmful or ineffective results useful to subsequent research | No demonstrated patient benefit or established therapeutic window |
| Innovation | 25% | Distinguishes clearance from corrected chromosome segregation; requires combination advantage and functional neural safety | No claim that D+Q for MVA is novel; novelty has not been established |
| Scalability | 15% | Reusable code, source ledger, control definitions and outcome records without redistribution of the genome | Other patients/genes require separate validation |

A perfect Track 1 score is foundational. The FAQ also requires a methods account for qualitative review, which is why the corrected report should be resubmitted even though the candidate pair is unchanged.

## Requirements and evidence

| Requirement | Implementation / status |
|---|---|
| Existing market-approved medicine for Track 2 | Dasatinib is the approved candidate. Quercetin is explicitly an experimental partner; D+Q is not described as approved for MVA. |
| Mechanism connecting variants to repurposing | Report separates predicted allele effects, checkpoint dysfunction, hypothesized senescent burden, and untested drug response. |
| Written report and GitHub repository | Both reports and reproducible code are present. The scientific strengthening revision was pushed as `8a262bf`; the final silent-media update follows separately. |
| Three-minute recorded pitch; YouTube or Vimeo URL | A silent, readable pitch is used at the participant’s request; the instructions do not explicitly require voice narration. It includes new evidence and the full acknowledgement. Verify its export under 180 seconds and obtain a hosted URL; upload is still pending. |
| Team/display name and filenames | Himanshu Kumar; report/CSV filenames retain HIMANSHUKUMARJHA. Use the same identity for revisions. |
| Submission limits | Track 1: six per participant; highest score displayed. Track 2: three per team; latest reviewed. Check quotas and success receipts when submitting. |
| AI provider, plan/tier and settings | Disclosure names Claude Code/consumer subscription, Codex Pro and Deepgram models. User confirmed training off for Codex and the original Claude work. Deepgram requests explicitly opt out. Historical retention and feedback handling are not independently audited. |
| Processor conditions | Training off is necessary but the organizer also limits other-purpose use and retention. Prior Deepgram request handling remains unverified and is disclosed; do not claim all historical service settings were certified. |
| Registration and eligibility | Existing HF sign-in and dataset access were observed. Participation requires age 18+ and individual registration/acceptance; no new legal attestation is made by this audit. |
| No recontact | No child, family or MVA Society contact. Future biological work is proposed through authorized research channels, not direct outreach. |
| No data redistribution | Gated inputs, genome-scale tables, caches and logs stay excluded. Candidate findings, HPO terms, code and reports fall within the organizer's clarified retainable categories. |
| Required acknowledgement | Full text in both reports, research plan, ledger and final pitch acknowledgement slide. Include it in the YouTube description and any subsequent public communication too. |
| CC BY and repository access | Findings/submissions are CC BY 4.0. The repository can remain private during the event but must be public after close, excluding prohibited data. |
| Dataset citation | For publication, the rules require the citation supplied on Synapse. The exact citation is not verified here; obtain it before any manuscript or publication that needs it. |
| Embargo | No dataset-derived peer-reviewed manuscript submission from close until the organizers' summary/preprint is public. Conference abstracts/posters require prior written approval. Code/results sharing does not authorize raw-data sharing. |
| Deletion and confirmation | Remove controlled genomic inputs, intermediates, relevant logs/caches within 30 days of close and email the specified organizer address confirming deletion. This is a future obligation, not completed. |
| Suspected unauthorized disclosure | Rules require reporting through Sage's Help Center. If a historical service configuration is found to have violated the processor conditions, use that route; this review does not assert a verified breach. |

The current timeline lists 24 October at 23:59 UTC as the submission deadline. Dates are subject to change. Its 25 November announcement date is more specific than the general two-to-three-month judging estimate elsewhere, so verify later rather than promising a fixed award date.

## Final submission gate

A report being ready, a Git push or a video upload is not a submission receipt. Upload the final report versions and video link, save the platform's success result and new quota counts for each track, and then update the status record. Track 1 replacement was accepted on 7 September as submission 2, with 100.0 rank points and F-max 1.000. Track 2 remains unsubmitted.

## Acknowledgement

> This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
