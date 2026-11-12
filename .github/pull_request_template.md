# Flow task contract

<!-- FLOW-CONTRACT:START -->
```toml
contract_schema_version = 1
task_id = ""
base_sha = ""
# standard or elevated. flow/classify.py decides from the changed paths and the
# flow-classify job overwrites the label on every push. Do not edit by hand.
level = "standard"
# What "done" means. Copied from the KRYTERIUM field of Norbert's email.
criterion = ""
allowed_paths = []
# Permalink of Norbert's comment with the line `ACCEPT <task_id>`
# (`ACCEPT <task_id> GOVERNANCE` when the level is elevated). Empty until he accepts.
product_owner_accept_reference = ""
# Permalink of the Independent QC comment with `verdict: PASS`. Empty until QC runs.
qc_reference = ""
```
<!-- FLOW-CONTRACT:END -->

## What changed

<!-- Required. One paragraph, plain language. -->

## How to check it

<!-- Required and observable: what to run, open or click, and what should happen. -->

## What this must not change

<!-- Required. Scope exclusions. -->
