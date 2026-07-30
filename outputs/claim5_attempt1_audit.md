# Claim 5 Attempt 1 — source-faithful availability audit

## Verdict

**inconclusive_source_faithful_data_and_outputs_unavailable**. No proxy data or synthetic stream was used.

## Exact claim

On Reddit vaccine-sentiment daily embedding streams (d=20, January-May 2021), IDD alarms align with real news events such as the April 13 J&J pause, while Euclidean-summary and moment-based baselines produce monotonic drift or noise unrelated to shocks.

## Primary-source protocol evidence

- Paper documents daily batches, Sentence-BERT `all-MiniLM-L6-v2`, 384-D embeddings, PCA to 20 dimensions, and a qualitative-only evaluation: `{'daily_batches': True, 'minimum_30_comments': True, 'sbert_model': True, 'embedding_dimension_384': True, 'pca_dimension_20': True, 'phase_dates': True, 'jj_pause_date': True, 'qualitative_only': True}`.
- The pinned runner defaults to `sentiment3d`, with `embed_pca20` optional; its default cutoff is J&J EUA rather than the paper's revised phase dates: `{'default_representation_is_sentiment3d': True, 'pca20_is_optional': True, 'embedding_model_declared': True, 'daily_windows': True, 'default_cutoff_is_jj_eua': True, 'jj_pause_marked': True, 'all_phaseII_days_labeled_changed': True}`.
- The cited Harvard Dataverse metadata lists `SummaryResults_Covid_All.tab` as `fileAccessRequest=true`; the pinned author release has no raw Reddit input, precomputed embeddings, result/alarm CSV, or rendered Figure-4 artifact: `{'dataverse_released': True, 'target_file_name': 'SummaryResults_Covid_All.tab', 'target_file_access_request': True, 'target_file_md5': '25a3b3de956885ba52b221f7f50ed7c7', 'pinned_release_contains_reddit_raw_csv': False, 'pinned_release_contains_precomputed_embeddings': False, 'pinned_release_contains_paper_figure_outputs': False}`.

## Event evidence

The paper names April 13 as the J&J pause. The retained CDC MMWR page is an official contemporaneous J&J safety reference. This audit does **not** assert that any alarm aligns with the event because no source-faithful date/alarm series was available to compute that comparison.

## Reproducibility

- Source audit: `python3 src/claim5_attempt1_source_audit.py`
- Test: `.venv-claim1-attempt2/bin/python -m pytest -q tests/test_claim5_attempt1.py`
- Evidence hashes: `evidence/claim5_attempt1/SHA256SUMS`

## Limitation

This is an availability/protocol audit, not a data-level refutation or full CPU reproduction. A later attempt must obtain authorized raw data plus exact paper-era embedding, stream, and result protocol before evaluating claim-level alignment.
