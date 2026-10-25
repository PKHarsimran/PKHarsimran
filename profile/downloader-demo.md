# Website Downloader / CLI replay

Released version: `v2.7.0`. Guided presentation of a real run on an owned fixture.

## 01 / PACK A PIECE OF THE WEB

```text
Three pages. Take them offline.
Owned localhost fixture

$ base=http://127.0.0.1:41329
$ python -m website_downloader \
  --url "$base/index.html" \
  --destination mirror/3800 \
  --max-pages 3 --respect-robots

[ok] process exited successfully
```

## 02 / PULL THE PLUG

```text
SOURCE SERVER: OFF

The mirror has to stand alone.
No server to fall back on.

index.html / guide.html
about.html / CSS / SVG
```

## 03 / THE OFFLINE PROOF

```text
[ok] 3 HTML pages saved
[ok] CSS + SVG stored locally
[ok] 15 local references resolve

SOURCE SERVER: STILL OFF
Every link stays in the mirror.

A little web, ready to travel.

OFFLINE MIRROR VERIFIED
```

[Reproduce the run](../demos/README.md) · [Source provenance](./demo-provenance.json)
