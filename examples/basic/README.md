# Generic artifact receipt example

This example represents outputs from any evaluation program. It needs no model, API account, hosted service or research-project checkout. The fixed manifest nonce is a conformance fixture, not a recommendation for real registrations.

The source files and installed copies under `prove/data/examples/basic` are byte-identical. Access installed copies with `importlib.resources.files("prove").joinpath("data/examples/basic")`. The primary quickstart generates its own inputs and needs no example files.

After copying these files into a fresh working directory:

```sh
prove pre-register manifest.json --receipt receipt
prove seal receipt --artifacts outputs
prove verify receipt --offline --policy integrity-only
prove proof create receipt --index 0 --out inclusion.json --without-proofs
prove verify --inclusion inclusion.json --offline --policy integrity-only
```

No score is inferred from metrics.json: without explicit selection scoring is unavailable. To record the supplied metric, use a fresh receipt and `--score-path metrics.json --aggregate aggregate.json`, where aggregate.json contains `{"numerator":3,"denominator":4}`. This remains recorded-only, without a claim that its math or observations are correct. Passing a receipt check does not establish honest execution or model identity.

Generate a fresh manifest with `prove init`, edit evidence/budgets, then use this generic workflow for real output directories. `prove verify receipt` defaults to anchored verification and returns insufficient evidence until qualifying timestamp proofs and independently selected chain evidence are supplied. Calendar submission is not completed anchoring.
