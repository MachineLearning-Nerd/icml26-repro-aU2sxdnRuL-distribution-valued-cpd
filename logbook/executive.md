The six-claim contract was audited against the pinned paper source and [official code commit](https://github.com/yyzeng43/IDD-icml/tree/c5b1db4060e5081e5c487f91792dc18c17603fd0). Claim 6 is verified as a scoped theorem/numerical audit; Claims 2--4 are falsified as literally worded because their live wording conflicts with the source theorem, table arithmetic, or metric. Claim 5 is inconclusive: the source supports post-pause event alignment, but released artifacts do not permit an independent numeric rerun. Claim 1 has three retained toy mechanism audits but remains inconclusive because the source-faithful R/funcharts paper-scale route is unavailable. This CPU-only work used no Hugging Face Job or Bucket; all code and evidence are in the public [reproduction repository](https://github.com/MachineLearning-Nerd/icml26-repro-aU2sxdnRuL-distribution-valued-cpd).

## Scope & cost

| | This reproduction | Full replication |
| --- | --- | --- |
| Scope | Source-pinned theorem/table/provenance audits; small deterministic CPU transport checks | Source-scale mFPCA/OT, synthetic and real-data streams |
| Hardware | Local CPU only | Paper-scale CPU/R environment plus unreleased data artifacts |
| Compute time | Short deterministic CPU audits; no billed Job | Not reproducible from the pinned public release |
| Cost | $0 billed; no HF Job/Bucket used | Unknown |
| Outcome | 1 scoped verification, 3 literal-source falsifications, 2 inconclusive (Claim 1 has toy evidence) | Not established |
