# IOC Inspector / CLI replay

Released version: `v0.2.0`. Guided presentation of a real run on an owned fixture.

## 01 / FOLLOW THE CLUES

```text
One PDF. What is hiding inside?
Owned fixture / static analysis

$ python main.py \
  --file ../invoice.pdf \
  --report --json

[ok] process exited successfully
```

## 02 / READ THE FINDINGS

```text
3 UNIQUE URLs / 1 IP

hxxp://192[.]0[.]2[.]42/receipt

hxxps://example[.]org/help

hxxps://portal[.]example[.]com/invoice

Links defanged for display.
Source: generated JSON report.
```

## 03 / CLOSE THE CASE

```text
[ok] 3 URLs / 1 IP verified
[ok] 0 embedded / 0 JavaScript
[ok] JSON + Markdown written

Tool verdict: benign
Heuristic score: 0

Owned PDF. Reputation keys off.
A verdict is not a guarantee.

CASE VERIFIED
```

[Reproduce the run](../demos/README.md) · [Source provenance](./demo-provenance.json)
