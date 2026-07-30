# Claim 4 — Attempt 1: source/release audit

## Live claim

> On the FlowCAP-II flow cytometry dataset (7-dimensional), IDD detects abnormal AML cell populations with F1 approximately 0.75 and ARL_1 approximately 1, versus Hotelling's T² F1 below 0.4.

## Source pins

- Paper source: `https://export.arxiv.org/e-print/2602.07252`
- Pinned code: `https://github.com/yyzeng43/IDD-icml@c5b1db4060e5081e5c487f91792dc18c17603fd0`
- Retained source excerpt: `evidence/claim4_attempt1/main0.tex`
- Hashes: `evidence/claim4_attempt1/SHA256SUMS`

## Protocol found in paper source

The paper source specifies a 7-D FlowCAP-II setting: 2,000 cells per measurement; 300 healthy calibration samples; a 300-sample monitoring stream; and 80% injected AML-positive measurements. It says F1 is a batch-level labeling metric and ARL_1 is first-detection delay.

## Source/release audit result

The pinned repository has no tracked FlowCAP, AML, or cytometry data, loader, preprocessing code, labels, stream-construction script, or FlowCAP runner. Its documented real-data case study is Reddit only. Therefore the public release does not provide an executable source-faithful CPU route for the claimed FlowCAP-II table/figure result, and no synthetic replacement was run.

The literal live claim also conflates/misstates source metrics:

- main text reports IDD F1 about 0.75 and ARL_1 about 1;
- appendix says IDD ARL_1 is approximately 2--3;
- the main text describes Hotelling's T² **precision** below 0.4, not F1 below 0.4.

## Verdict

**Falsified for literal source scope.** This is a source-contract audit, not a claim that the dataset-level result is false. The public source/release cannot substantiate the live claim as written, and the claim's Hotelling F1 wording is unsupported by the pinned paper text.

## Control and validation

`src/claim4_attempt1_source_audit.py` asserts every stated FlowCAP protocol fragment and verifies that no FlowCAP/AML/cytometry path exists in the pinned source tree. `tests/test_claim4_source_audit.py` encodes the same checks. The local environment lacks `pytest`; direct Python assertions against the generated JSON passed.

## Next step

Attempt 2 may only proceed if an authoritative public FlowCAP-II data source supplies the exact files, labels, and preprocessing/stream protocol needed to reproduce the result. Otherwise retain this source-scope result; do not call a substituted dataset a full reproduction.
