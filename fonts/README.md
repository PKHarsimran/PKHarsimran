# Profile type assets

Space Grotesk 700 supplies display headings; a smaller 600 subset supplies button labels. IBM Plex Mono 500 supplies terminal text and compact metadata. Body prose follows GitHub's native typography.

All three subsets cover the printable ASCII alphabet and the profile’s typographic punctuation. Button coverage is not restricted to an old list of labels, so new calls to action retain the same typeface.

The font subsets are embedded as data URLs inside repository-owned SVGs. Browsers need no font installation, Google Fonts request or external font service. Font faces, source revision and SHA-256 hashes are recorded in `sources.json`; the upstream SIL Open Font Licenses are included alongside the subsets.

The modified subsets use the internal names ProfileDisplay, ProfileButton and ProfileMono; upstream copyright and license records are preserved.

The optional preparation command requires `fonttools` and `brotli`:

```sh
python scripts/subset_profile_fonts.py
```

Normal profile generators use the committed WOFF2 files with Python's standard library. Regenerate static panels with `python scripts/build_profile_style.py`, and buttons with `python scripts/build_profile_design.py`. Project motion is decorative, and reduced-motion preferences keep the illustrations static.
