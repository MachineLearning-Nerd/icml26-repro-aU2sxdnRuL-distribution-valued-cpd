# Source audit

Paper 2602.07252 describes daily Reddit vaccine-comment distributions, discards days with fewer than 30 comments, and reports 50 Phase-I and 50 Phase-II distributions spanning 2020-12-02 through 2021-05-05. The official Dataverse datafile is `6430672`.

Dataverse's Data Access API documentation states that the default representation of an ingested tabular file is archival TSV, while `format=original` requests the saved uploaded file. This route audits both plus `format=prep` rather than assuming the first served representation has the paper-required schema.

Paper source archive SHA-256: `6d4af865d403a1c4f72ed3ef8057069212ac1633aa79410b4607b04a8b9edb87`.
