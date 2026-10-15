# Project 8: post-training dataset manifest

**Job-post test:** Can SFT, preference, and RL data share basic quality, provenance, and versioning checks?

`python3 build_dataset.py` validates six invented records and prints a stable content hash, schema version, and counts by training-data type. `python3 -m unittest test_build_dataset.py` checks deterministic hashing and rejection of duplicate IDs, missing provenance, and invalid preference pairs.

This is a small schema/quality demonstration. It does not prove distributed processing, real annotator agreement, privacy controls, dataset lineage across systems, or model improvements.
