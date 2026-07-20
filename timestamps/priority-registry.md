# TLM Priority Timestamp Registry

This file records SHA-256 digests of TLM research artifacts that are **not yet
public**, published here to establish authorship-at-date without disclosing their
contents. Committing this file to the public `TLM-Research/TLM` repository — and,
optionally, anchoring it with OpenTimestamps — provides a verifiable public record
that the named documents existed, in exactly the hashed form, at the commit date.

**How to verify (once a document is released):** obtain the named file, run
`sha256sum <file>`, and confirm the digest matches the entry below. Any change to
the file — even one byte — changes the digest, so a match proves the released
document is byte-identical to the one hashed here at the recorded date.

---

## Entries

### RN-005 — Temporal Liquidity Reserve (Feasibility Sketch), v0.1

- **File:** `RN-005_Temporal_Liquidity_Reserve_Feasibility_Sketch_v0.1.md` (held privately)
- **SHA-256:** `39959e014bd987bd886f132dbcb8ea0f461ceed7cde0be2ffa58e9ec2ac96601`
- **Size:** 9294 bytes
- **Author:** Duanyang (Dan) Guo <danguo01@gmail.com>
- **Recorded (UTC):** 2026-07-20T03:17:42Z
- **Note:** Private feasibility sketch (candidate mechanism / existence proof). Content withheld pending public release; only the digest is disclosed here.

---

## Optional: strengthen with OpenTimestamps (Bitcoin anchor)

A public git commit already gives a strong, witnessed timestamp. To add a
trustless cryptographic anchor that does not depend on GitHub:

```bash
# install once:  pip install opentimestamps-client
ots stamp priority-registry.md          # creates priority-registry.md.ots
# commit BOTH priority-registry.md and priority-registry.md.ots

# later, to verify:
ots verify priority-registry.md.ots
```

The `.ots` proof anchors this file's hash into the Bitcoin blockchain, letting
anyone verify the date without trusting any single party.
