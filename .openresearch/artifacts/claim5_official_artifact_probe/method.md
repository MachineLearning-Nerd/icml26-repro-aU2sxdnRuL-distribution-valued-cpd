# Method

The fixed campaign command downloads three official representations with an explicit User-Agent, records SHA-256, MD5, byte length, response metadata, and a non-content 16-byte hexadecimal prefix. It independently probes comma and tab parsing and uses `csv.Sniffer`. Candidate date/text columns are selected only by column names, then the fixed paper windows and 30-comment rule are counted.

The preprocessed JSON representation is a negative control: it must not be accepted as a dated text stream. The verifier exits nonzero if any representation, checksum, parser comparison, or control is absent.
