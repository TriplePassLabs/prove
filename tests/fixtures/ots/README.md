Historical header bytes are the first 80 bytes of the first serialized Bitcoin
block in python-opentimestamps 0.5.0, opentimestamps/tests/test_bitcoin.py,
Test_make_timestamp_from_block.test. Upstream labels that vector “genesis block!”;
its previous-block field points to the genesis block. Tests assign height 1.
These historical public block bytes are factual test data, not copied source code.
Pinned distribution: https://pypi.org/project/opentimestamps/0.5.0/
Upstream source: https://github.com/opentimestamps/python-opentimestamps
Upstream distribution identifies its source license as LGPL-3.0-or-later.

All other headers, detached proofs, cache tips and witness branches in these tests
are synthetic and generated with upstream serializers. A proof starting at a
historical merkle root tests commitment matching, without claiming a file preimage.
No fixture supplies independently validated node evidence or current freshness.
