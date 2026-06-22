"""
update_silhouettes_manifest.py
-------------------------------
Scans game/silhouettes/ and game/reveals/ for GIFs named {player_id}.gif
and writes the list of IDs that have BOTH files to game/data/silhouettes.json.

Run this any time you add a new silhouette/reveal pair:
    python scripts/update_silhouettes_manifest.py
"""

import json
import pathlib

REPO_ROOT    = pathlib.Path(__file__).parent.parent
SIL_DIR      = REPO_ROOT / "game" / "silhouettes"
REVEAL_DIR   = REPO_ROOT / "game" / "reveals"
MANIFEST_OUT = REPO_ROOT / "game" / "data" / "silhouettes.json"

SIL_DIR.mkdir(parents=True, exist_ok=True)
REVEAL_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST_OUT.parent.mkdir(parents=True, exist_ok=True)

silhouette_ids = {int(f.stem) for f in SIL_DIR.glob("*.mp4") if f.stem.isdigit()}
reveal_ids     = {int(f.stem) for f in REVEAL_DIR.glob("*.mp4") if f.stem.isdigit()}

# Only include players that have BOTH a silhouette and a reveal clip
ready_ids = sorted(silhouette_ids & reveal_ids)

missing_reveal     = silhouette_ids - reveal_ids
missing_silhouette = reveal_ids - silhouette_ids

if missing_reveal:
    print(f"⚠ Have silhouette but no reveal for IDs: {sorted(missing_reveal)}")
if missing_silhouette:
    print(f"⚠ Have reveal but no silhouette for IDs: {sorted(missing_silhouette)}")

with open(MANIFEST_OUT, "w") as f:
    json.dump(ready_ids, f)

print(f"\n{len(ready_ids)} player(s) ready: {ready_ids}")
print(f"Wrote manifest to {MANIFEST_OUT}")
