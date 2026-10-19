# IOC Inspector / CLI replay

Released version: `v0.1.0`. Guided presentation of a real run on an owned fixture.

## 01 / FOLLOW THE CLUES

```text
One PDF. What is hiding inside?
Owned fixture / static analysis

$ python main.py \
  --file ../delivery.pdf \
  --report --json

[ok] process exited successfully
```

## 02 / READ THE FINDINGS

```text
2 UNIQUE URLs / 1 IP

hxxp://198[.]51[.]100[.]23/tracking

hxxps://example[.]com/parcel

Links defanged for display.
Source: generated JSON report.
```

## 03 / CLOSE THE CASE

```text
[ok] 2 URLs / 1 IP verified
[ok] 0 embedded / 0 JavaScript
[ok] JSON + Markdown written

Tool verdict: benign
Heuristic score: 0

Owned PDF. Reputation keys off.
A verdict is not a guarantee.

CASE VERIFIED
```

[Reproduce the run](../demos/README.md) · [Source provenance](./demo-provenance.json)
