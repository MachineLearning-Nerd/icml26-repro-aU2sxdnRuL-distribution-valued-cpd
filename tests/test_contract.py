import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContractTest(unittest.TestCase):
    def test_live_contract_has_six_nonempty_claims(self):
        claims = json.loads((ROOT / "contract" / "live_claims.json").read_text())
        self.assertEqual(len(claims), 6)
        self.assertTrue(all(claim["text"].strip() for claim in claims))

    def test_manifest_matches_target_id_and_score_ceiling(self):
        manifest = json.loads((ROOT / "contract" / "contract_manifest.json").read_text())
        self.assertEqual(manifest["openreview_id"], "aU2sxdnRuL")
        self.assertEqual(manifest["max_points"], 12)


if __name__ == "__main__":
    unittest.main()
