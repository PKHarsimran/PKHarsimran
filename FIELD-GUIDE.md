# Field guide / choose your route

A short, motion-free way into the projects, their working demos, and the Zima homelab.

[Back to the animated profile](./README.md) · [Visit the website](https://harsim.ca) · [Meet Pixel](https://harsim.ca/lab/)

## Find the right tool

**A threat indicator needs context → [SwiftIOC](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector).** Collect public threat feeds and vulnerability records, then follow the source evidence in the dashboard.

**A document needs inspecting → [IOC Inspector](https://github.com/PKHarsimran/IOC-Inspector).** Extract indicators from PDFs and Office files, inspect static findings, and write readable reports.

**A useful page needs preserving → [Website Downloader](https://github.com/PKHarsimran/website-downloader).** Keep pages and their assets together in an offline mirror with local links.

## See the tools work

- **SwiftIOC:** [Live dashboard](https://harsim.ca/SwiftIOC-Automated-Threat-Intelligence-Collector/) · [Saved feed snapshot](./profile/intel-conveyor.md)
- **IOC Inspector:** [CLI replay](./profile/inspector-demo.gif) · [Transcript](./profile/inspector-demo.md) · [Case report](./profile/case-report.md)
- **Website Downloader:** [CLI replay](./profile/downloader-demo.gif) · [Transcript](./profile/downloader-demo.md) · [Offline checks](./profile/downloader-demo.json)

The CLI replays use released tools and owned fixtures. The transcripts let you read every chapter at your own pace. [Recording recipe and source provenance](./demos/README.md).

## Bring a terminal

- [IOC Inspector quick start](https://github.com/PKHarsimran/IOC-Inspector#-quick-start)
- [Website Downloader field guide](https://github.com/PKHarsimran/website-downloader/wiki)
- [SwiftIOC source and setup](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector)
- [Container images](https://hub.docker.com/u/pkvirus)

## Take the self-hosting route

The **Zima homelab** connects media requests, libraries, photos, dashboards, and monitoring with Docker Compose. The profile illustrates how those services hand work to each other.

[Meet the service crew](./README.md#user-content-homelab) · [Curated public inventory](./profile/lab-services.json)

The next checkpoint is a modular Compose starter kit, documented so someone else can bring it online.

## Take the scenic route

- [Enter the live lab](https://harsim.ca/lab/): meet Pixel, solve tiny cases, and collect mission patches. Press <kbd>/</kbd> to open Pixel's terminal.
- [Spin pocket Pixel](./profile/pixel-pocket.stl): a small voxel keepsake in GitHub's 3D viewer. Drag to rotate and scroll to zoom.
- [Check the project radar](./profile/public-pulse.md): real public build checks and releases, with timestamps.
- [Open the patch cabinet](./profile/release-patches.md): the releases behind the collectible artwork.

## Look behind the curtain

[Daily profile workflow](./.github/workflows/profile-lab.yml) · [Demo workflow](./.github/workflows/living-profile.yml) · [Rebuild the illustrations](./scripts/build_readme_art.py) · [Pocket Pixel recipe](./scripts/build_pixel_collectible.py)

Build with curiosity. Leave something useful behind.
