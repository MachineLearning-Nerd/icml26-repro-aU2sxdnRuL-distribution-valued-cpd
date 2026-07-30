# Claim 5 Attempt 1 — source-faithful availability audit

## Verdict

**inconclusive_source_faithful_data_and_outputs_unavailable**. No proxy or synthetic stream was used.

## Exact claim

On Reddit vaccine-sentiment daily embedding streams (d=20, January-May 2021), IDD alarms align with real news events such as the April 13 J&J pause, while Euclidean-summary and moment-based baselines produce monotonic drift or noise unrelated to shocks.

## Input and protocol evidence

- The Harvard Dataverse file `SummaryResults_Covid_All.tab` was retrieved; its MD5 matches the dataset metadata. It contains `12915` rows from `2020-04-24` to `2021-05-06`, including `11713` rows on `105` Jan--May 2021 days.
- The paper documents daily batches, Sentence-BERT `all-MiniLM-L6-v2`, 384-D embeddings, PCA to 20 dimensions, and qualitative-only evaluation: `{'daily_batches': True, 'minimum_30_comments': True, 'sbert_model': True, 'embedding_dimension_384': True, 'pca_dimension_20': True, 'phase_dates': True, 'jj_pause_date': True, 'qualitative_only': True}`.
- The pinned runner defaults to `sentiment3d`, makes `embed_pca20` optional, and defaults to a J&J-EUA cutoff rather than the paper's revised phase dates: `{'default_representation_is_sentiment3d': True, 'pca20_is_optional': True, 'embedding_model_declared': True, 'daily_windows': True, 'default_cutoff_is_jj_eua': True, 'jj_pause_marked': True, 'all_phaseII_days_labeled_changed': True}`.
- A source-faithful runner invocation against the checksum-matched input fails before processing because the pinned code imports the absent `simulation` package. The release also has no paper-era embedding cache, dated alarm/result series, or Figure-4 output.

## Event evidence

The paper names April 13 as the J&J pause. The retained CDC MMWR page is an official contemporaneous J&J safety reference. This audit does **not** assert that an alarm aligns with that event because no source-faithful dated alarm series was produced.

## Reproducibility

- Audit: `python3 src/claim5_attempt1_source_audit.py`
- Source runner (expected failure retained): `DIDO_REDDIT_CSV=... DIDO_REDDIT_DATADIR=... .venv-claim1-attempt2/bin/python upstream/IDD-icml/case_study/run_reddit_vax.py`
- Test: `.venv-claim1-attempt2/bin/python -m pytest -q tests/test_claim5_attempt1.py`
- Evidence hashes: `evidence/claim5_attempt1/SHA256SUMS`

## Limitation

A later attempt needs a runnable paper-era OT/mFPCA dependency path plus an exact d=20 configuration and baseline/alarm series. This result neither verifies nor refutes the underlying qualitative Reddit observation.
