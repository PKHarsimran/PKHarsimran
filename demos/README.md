# Reproducible profile exhibits

The daily `living-profile.yml` workflow reads SwiftIOC's public diagnostics and public GitHub release metadata. It renders repository-owned SVGs, source snapshots, a service-flow illustration and release patches.

The demo plan resolves the latest stable IOC Inspector and Website Downloader release tags to immutable commit SHAs. The recipe hash, release SHAs and ISO week determine whether reels need refreshing. Unchanged reels are reused; a new week rotates the owned PDF fixture. No private repositories are discovered or fetched.

Demo builds have read-only repository permission. A separate publishing job can write the verified artifacts, but does not run the downloaded project code. Neither demo receives reputation keys or write credentials.

- **IOC Inspector:** generates a harmless PDF using reserved example domains and documentation IPs, runs the released CLI, and checks its real JSON output. No macros, scripts, active payloads, or external reputation lookups. The case card and reveal panel come from those findings. A heuristic verdict is not a safety guarantee.
- **Website Downloader:** starts an owned three-page localhost fixture, invokes the released CLI, stops the source server, then verifies that every HTML link and asset reference resolves inside the generated mirror. The recording shows the runner invoking the real CLI and checking its output; it does not imitate a different application's interface.
- **VHS:** records guided terminal presentations around both executions. The three chapters show the real command, findings, and verified result. A spinner runs only while the actual subprocess is pending. Tool stdout is captured; the styled findings come from generated reports and the verified mirror. Commands show the isolated environment's Python as `python` and use the same relative paths and flags as the real invocation.
- **Playback:** desktop and 32-column mobile reels use the bundled ProfileMono font, a shared dark frame, and reading pauses. Each size has a lossless WebP of the completed result for reduced-motion preferences. Dimensions, duration, size, and GIF SHA-256 hashes are recorded in `profile/demo-provenance.json`; invalid, truncated, or oversized reels fail before publication.
- **Homelab:** `profile/lab-services.json` contains only curated public service labels. The diagram illustrates handoffs, not a network topology or live health check. Edit that manifest to regenerate both layouts.

To reproduce on Linux with Python 3.10+, Git and VHS 0.12.1:

```sh
python3 scripts/living_profile.py
python3 scripts/profile_demos.py prepare
vhs demos/inspector.tape
vhs demos/inspector-mobile.tape
vhs demos/downloader.tape
vhs demos/downloader-mobile.tape
.demo-work/inspector-env/bin/python scripts/profile_demos.py finish
```

Before recording, install `fonts/ibm-plex-mono-500.ttf` into the local fontconfig directory and run `fc-cache -f`. Plain `inspector` and `downloader` invocations verify immediately without animation or reading pauses. The tapes enable `--record`; `--compact` selects the mobile layout.

Network or validation failures leave the last published exhibits intact. Collection timestamps describe the SwiftIOC snapshot; README images and scheduled workflows can be delayed or cached.
