<a name="mission-control"></a>

<div align="center">

<a href="https://harsim.ca">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/mission-banner-orbital-mobile.svg">
  <img src="./profile/mission-banner-orbital.svg" alt="Harsimran Sidhu — turning curiosity into automation. Cybersecurity, threat intelligence, and automation." width="100%" />
</picture>
</a>

**Cybersecurity analyst · Open-source builder · Homelab tinkerer**

<a href="https://harsim.ca">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/mission-typing-mobile.svg">
  <img src="./profile/mission-typing.svg" alt="Follow the evidence. Automate the boring bits. Always one more thing to build." width="780" />
</picture>
</a>

<!-- buttons:hero:start -->
<p align="center">
  <a href="https://harsim.ca"><img src="./profile/buttons/website.svg" alt="Visit website" width="150" height="44" /></a>
  <a href="https://www.linkedin.com/in/harsimransidhu/"><img src="./profile/buttons/linkedin.svg" alt="LinkedIn" width="150" height="44" /></a>
</p>
<!-- buttons:hero:end -->

<!-- buttons:navigation:start -->
<p align="center">
  <a href="#-selected-builds"><img src="./profile/buttons/projects.svg" alt="Projects" width="100" height="36" /></a>
  <a href="#-inside-the-lab"><img src="./profile/buttons/homelab.svg" alt="Homelab" width="102" height="36" /></a>
  <a href="#-activity-log"><img src="./profile/buttons/activity.svg" alt="Activity" width="100" height="36" /></a>
</p>
<!-- buttons:navigation:end -->

<!-- visitors:start -->
<picture>
  <source media="(max-width: 600px)" srcset="./profile/mission-visitors-mobile.svg" />
  <img src="./profile/mission-visitors.svg" alt="Hey, curious human. Welcome to the lab! A waving pixel visitor and an animated orbital arrival stamp." width="100%" />
</picture>

<p align="center">
  <a href="https://hits.sh/github.com/PKHarsimran/"><img src="https://hits.sh/github.com/PKHarsimran.svg?style=for-the-badge&amp;label=LAB+PAGE+HITS&amp;color=a995ff&amp;labelColor=34445c" alt="Lab page hits — public profile view counter, not unique visitors" height="28" /></a>
</p>

<sub>Thanks for dropping into my corner of the internet. ✨<br />Page hits, not unique visitors · <a href="https://github.com/silentsoft/hits#statistics">About the counter</a></sub>
<!-- visitors:end -->

</div>

## 👋 Operator profile

I'm **Harsimran Sidhu**. I work in cybersecurity and build tools that turn messy security data into something useful: clearer investigations, better dashboards, and fewer repetitive steps.

| Station | What I'm working on |
| :--- | :--- |
| 🛡️ **Defend** | WAF tuning, endpoint investigations, and detection engineering |
| 🔭 **Investigate** | Threat intelligence with **Splunk Enterprise**, exploring **OpenCTI** |
| 🏠 **Build** | A **Docker Compose** home server for media, photos, books, and monitoring |

> My favourite kind of side project? A repetitive task that doesn't need to be repetitive anymore.

## 🚀 Selected builds

Threat intelligence, document triage, and a little web archaeology.

[01 / SwiftIOC](#01--swiftioc) · [02 / IOC Inspector](#02--ioc-inspector) · [03 / Website Downloader](#03--website-downloader)

### 01 / SwiftIOC

<a href="https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/mission-swiftioc-mobile.svg">
  <img src="./profile/mission-swiftioc.svg" alt="SwiftIOC — follow the indicator, keep the evidence. Python threat intelligence and analyst workflows." width="100%" />
</picture>
</a>

**Collect → normalize → investigate.** A Python pipeline turns IOC feeds and vulnerability reports into source-aware records. The browser dashboard brings the evidence together for review and export.

<!-- buttons:swift:start -->
<p align="left">
  <a href="https://harsim.ca/SwiftIOC-Automated-Threat-Intelligence-Collector/"><img src="./profile/buttons/dashboard.svg" alt="Open dashboard" width="166" height="44" /></a>
  <a href="https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector"><img src="./profile/buttons/source.svg" alt="View source" width="140" height="44" /></a>
</p>
<!-- buttons:swift:end -->

<a href="./profile/intel-conveyor.md">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/intel-conveyor-mobile.svg">
  <img src="./profile/intel-conveyor.svg" alt="Workflow-generated SwiftIOC conveyor: collect, normalize, publish and investigate. Real retained observable and CVE counts, deduplication, last-interval changes and collection timestamp from the public diagnostics." width="100%">
</picture>
</a>

<sub>Real collection data, illustrated. Counts describe the retained feed and one collection interval. [Open the snapshot](./profile/intel-conveyor.md).</sub>

<details>
<summary><strong>🎬 Watch a 12-second evidence review</strong></summary>

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="./profile/swift-demo.webp">
  <img src="./profile/swift-demo.gif" alt="SwiftIOC walkthrough: open the public dashboard, review a CVE, inspect CISA evidence, and compare NVD details." width="100%">
</picture>

<sub>Recorded from the public dashboard on October 17, 2026. The displayed records are a snapshot; use the live dashboard for current data.</sub>

</details>

<details>
<summary><strong>🧠 Build story: keep the evidence attached</strong></summary>

- **Problem:** scattered feeds make it hard to understand where an indicator came from or what a vulnerability report actually establishes.
- **Built:** a Python collection and normalization pipeline, source-aware records, downloadable feeds, and a browser workspace for investigation.
- **Design takeaway:** keep provenance visible and separate indicators from vulnerability evidence. A score helps order review; it doesn't establish compromise.

[Explore how SwiftIOC works ↗](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector#how-the-pieces-fit)

</details>

<p align="center"><img src="./profile/mission-orbit-divider.svg" alt="" width="100%" /></p>

### 02 / IOC Inspector

<a href="https://github.com/PKHarsimran/IOC-Inspector">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/mission-inspector-mobile.svg">
  <img src="./profile/mission-inspector.svg" alt="IOC Inspector — suspicious documents, useful answers. Python static analysis and structured reports." width="100%" />
</picture>
</a>

**Inspect → extract → report.** Triage PDFs and Office files with static analysis, IOC extraction, and optional threat enrichment. Export the findings as Markdown, JSON, or CSV.

<!-- buttons:inspector:start -->
<p align="left">
  <a href="https://github.com/PKHarsimran/IOC-Inspector#-quick-start"><img src="./profile/buttons/quick-start.svg" alt="Quick start" width="150" height="44" /></a>
  <a href="https://github.com/PKHarsimran/IOC-Inspector"><img src="./profile/buttons/source.svg" alt="View source" width="140" height="44" /></a>
</p>
<!-- buttons:inspector:end -->

<picture>
  <source media="(max-width: 600px)" srcset="./profile/case-file-mobile.svg">
  <img src="./profile/case-file.svg" alt="IOC Inspector case of the week: an owned, harmless PDF with a few clues. The released CLI generates the findings; expand the answer below." width="100%">
</picture>

<details>
<summary><strong>🕵️ Reveal the findings</strong></summary>

<img src="./profile/case-findings.svg" alt="Actual extracted URLs, IP count, heuristic verdict and score from the weekly harmless training PDF. External reputation lookups are disabled; a heuristic verdict is not a security guarantee." width="600">

[Read the case file](./profile/case-report.md) · [Raw tool findings](./profile/case-report.json) · [Fixture recipe](./demos/cases.json)

</details>

<details>
<summary><strong>🎬 Watch the released scanner work the case</strong></summary>

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="./profile/inspector-demo.webp">
  <img src="./profile/inspector-demo.gif" alt="VHS recording of the demo runner invoking the released IOC Inspector CLI on the weekly owned PDF and verifying its actual JSON findings." width="100%">
</picture>

<sub>The workflow records a real CLI execution. Reserved example domains and documentation IPs keep the fixture harmless. [Recording provenance](./profile/demo-provenance.json).</sub>

</details>

<p align="center"><img src="./profile/mission-orbit-divider.svg" alt="" width="100%" /></p>

### 03 / Website Downloader

<a href="https://github.com/PKHarsimran/website-downloader">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/mission-downloader-mobile.svg">
  <img src="./profile/mission-downloader.svg" alt="Website Downloader — take a little piece of the web offline. Python web archiving with optional Playwright rendering." width="100%" />
</picture>
</a>

**Capture → rewrite → browse offline.** Mirror websites, bring their assets along, and rewrite links for offline browsing. Update existing copies or use optional Playwright rendering for pages that need JavaScript.

<!-- buttons:downloader:start -->
<p align="left">
  <a href="https://github.com/PKHarsimran/website-downloader/wiki"><img src="./profile/buttons/field-guide.svg" alt="Field guide" width="150" height="44" /></a>
  <a href="https://github.com/PKHarsimran/website-downloader"><img src="./profile/buttons/source.svg" alt="View source" width="140" height="44" /></a>
</p>
<!-- buttons:downloader:end -->

<details>
<summary><strong>🎬 Watch the CLI turn a site into an offline copy</strong></summary>

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="./profile/downloader-demo.webp">
  <img src="./profile/downloader-demo.gif" alt="VHS recording of the demo runner invoking the released Website Downloader CLI, stopping the owned local source server, and verifying all links and assets in the three-page offline mirror." width="100%">
</picture>

<sub>Automatically recorded from the released CLI against an owned local site. The source server stops before the offline links are checked. [Run results](./profile/downloader-demo.json) · [Recording provenance](./profile/demo-provenance.json).</sub>

</details>

<!-- buttons:return:start -->
<p align="left">
  <a href="#mission-control"><img src="./profile/buttons/back-top.svg" alt="Back to top" width="126" height="36" /></a>
</p>
<!-- buttons:return:end -->

## 🏠 Inside the lab

My **Zima homelab** runs on **Docker Compose**. Media, photos, books, dashboards, and monitoring share a home; I build the workflows and automation that connect them.

<picture>
  <source media="(max-width: 600px)" srcset="./profile/homelab-flow-mobile.svg">
  <img src="./profile/homelab-flow.svg" alt="Zima homelab flow theatre: Jellyseerr requests, Radarr/Sonarr/Prowlarr/Bazarr automation, Transmission with Gluetun, and Jellyfin playback. Photo and book libraries, operations and monitoring share the stack. Illustrated handoffs from a curated service manifest; no live telemetry." width="100%" />
</picture>

<sub>Animated from the [public service manifest](./profile/lab-services.json). Illustrated handoffs; the service inventory below has the full cast.</sub>

- 🎬 **Connect the workflow:** requests → library automation → VPN-routed downloads → Jellyfin playback.
- 🖼️ **Bring the libraries together:** photo management, books, and audiobooks in one self-hosted stack.
- 🧭 **See what's happening:** custom Homepage and flow dashboards, health checks, logs, and notifications.

<details>
<summary><strong>🧩 Open the service inventory</strong></summary>

| Area | Services |
| :--- | :--- |
| Media & automation | Jellyfin, Jellyseerr, Radarr, Sonarr, Prowlarr, Bazarr |
| Downloads | Transmission, Gluetun |
| Photos | PhotoPrism |
| Books & audio | Shelfmark, Audiobookshelf |
| Operations | Homepage, Portainer, custom flow dashboards |
| Monitoring | Uptime Kuma, Glances, Dozzle, ntfy |

</details>

**Current side quest:** make the stack easier to run, recover, and eventually share. ⚙️

<details>
<summary><strong>🧠 Build story: a server, not just a list of containers</strong></summary>

- **Problem:** a collection of running services still leaves requests, downloads, imports, libraries, and troubleshooting disconnected.
- **Built:** a Compose-based home server connecting media workflows, photo and book libraries, custom dashboards, health checks, logs, and notifications.
- **Design takeaway:** the useful work is in the connections: storage paths, permissions, service handoffs, and understandable recovery. More containers alone don't make a better server.

</details>

<!-- buttons:return:start -->
<p align="left">
  <a href="#mission-control"><img src="./profile/buttons/back-top.svg" alt="Back to top" width="126" height="36" /></a>
</p>
<!-- buttons:return:end -->

## 🚧 Now building

<picture>
  <source media="(max-width: 600px)" srcset="./profile/mission-now-mobile.svg" />
  <img src="./profile/mission-now.svg" alt="Now building: a modular Docker Compose home-server starter kit with guided setup and connected services. Next checkpoint: independent fresh-install validation using the documentation." width="100%" />
</picture>

Turning lessons from the Zima lab into a **modular Compose starter kit**. The test: someone else can follow the docs, choose their services, and bring the stack online.

## 🧰 Toolkit

<picture>
  <source media="(max-width: 600px)" srcset="./profile/mission-toolkit-icons-mobile.svg">
  <img src="./profile/mission-toolkit-icons.svg" alt="Code: Python, Bash, C++. Security: Splunk, Cortex XDR, Kibana, F5 BIG-IP. Infrastructure: Docker, Ansible, Raspberry Pi. Observability: Grafana, InfluxDB, MQTT." width="100%">
</picture>

<!-- buttons:containers:start -->
<p align="left">
  <a href="https://hub.docker.com/u/pkvirus"><img src="./profile/buttons/docker.svg" alt="Container images" width="188" height="44" /></a>
</p>
<!-- buttons:containers:end -->

## 📊 Activity log

### 📡 Public build radar

<a href="./profile/public-pulse.md"><img src="./profile/public-pulse.svg" alt="Daily public build radar: CI status, latest release, stars, and default-branch commit date for SwiftIOC, IOC Inspector, and Website Downloader." width="100%" /></a>

<!-- buttons:radar:start -->
<p align="left">
  <a href="./profile/public-pulse.md"><img src="./profile/buttons/snapshot.svg" alt="Read snapshot" width="160" height="44" /></a>
  <a href="https://github.com/PKHarsimran/PKHarsimran/actions/workflows/profile-lab.yml"><img src="./profile/buttons/workflow.svg" alt="Workflow" width="138" height="44" /></a>
</p>
<!-- buttons:radar:end -->

<details>
<summary><strong>💓 Open live checks & release links</strong></summary>

| Public project | Checks | Latest release |
| :--- | :--- | :--- |
| [SwiftIOC](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector) | [![SwiftIOC CI](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector/actions/workflows/ci.yml) | [![SwiftIOC release](https://img.shields.io/github/v/release/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector?label=release&color=A995FF)](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector/releases/latest) |
| [IOC Inspector](https://github.com/PKHarsimran/IOC-Inspector) | [![IOC Inspector CI](https://github.com/PKHarsimran/IOC-Inspector/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/PKHarsimran/IOC-Inspector/actions/workflows/ci.yml) | [![IOC Inspector release](https://img.shields.io/github/v/release/PKHarsimran/IOC-Inspector?label=release&color=A995FF)](https://github.com/PKHarsimran/IOC-Inspector/releases/latest) |
| [Website Downloader](https://github.com/PKHarsimran/website-downloader) | [![Website Downloader CI](https://github.com/PKHarsimran/website-downloader/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/PKHarsimran/website-downloader/actions/workflows/python-app.yml) | [![Website Downloader release](https://img.shields.io/github/v/release/PKHarsimran/website-downloader?label=release&color=A995FF)](https://github.com/PKHarsimran/website-downloader/releases/latest) |

<sub>Badges may be cached; open one for the underlying workflow or release.</sub>

</details>

<details>
<summary><strong>🏅 Open the release mission-patch cabinet</strong></summary>

<a href="./profile/release-patches.md">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/release-patches-mobile.svg">
  <img src="./profile/release-patches.svg" alt="Collectible mission patches generated from real public release versions and publication dates, showing up to two recent stable releases for each selected project." width="100%">
</picture>
</a>

[Open the release log](./profile/release-patches.md)

</details>

<picture>
  <source media="(max-width: 600px)" srcset="./profile/activity-summary-mobile.svg">
  <img src="./profile/activity-summary.svg" alt="GitHub activity statistics and repository language mix. The cards stack vertically on smaller screens." width="100%">
</picture>

### 🐍 Even the snake has a backlog

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/PKHarsimran/PKHarsimran/output/github-contribution-grid-snake-dark.svg">
  <img src="https://raw.githubusercontent.com/PKHarsimran/PKHarsimran/output/github-contribution-grid-snake.svg" alt="Animated snake tracing Harsimran's GitHub contribution grid" width="100%">
</picture>

<details>
<summary><strong>🚀 Launch contribution patrol</strong></summary>

<img src="./profile/contribution-patrol.svg" alt="A pixel ship patrols active days from Harsimran's public GitHub contribution calendar. Every square is a real calendar day; colours are GitHub activity levels. Animation respects reduced-motion preferences." width="100%" />

<sub>Every square is a day; colour is GitHub's activity level. Generated daily from the [public calendar](https://github.com/PKHarsimran). [Read the calendar snapshot](./profile/contribution-patrol.json).</sub>

</details>

<details>
<summary><strong>⚙️ How the profile builds itself</strong></summary>

- **Daily:** read public SwiftIOC diagnostics and public release metadata; regenerate the conveyor, homelab flow and release patches.
- **Weekly, or when releases/recipes change:** rotate the harmless case, run the released CLIs, verify their output, and record fresh demo reels.
- **Every build:** keep collection timestamps and source provenance, support reduced motion, and publish only after the checks pass.

[Watch the workflow ↗](https://github.com/PKHarsimran/PKHarsimran/actions/workflows/living-profile.yml) · [Reproduce the exhibits](./demos/README.md)

</details>

<!-- buttons:return:start -->
<p align="left">
  <a href="#mission-control"><img src="./profile/buttons/back-top.svg" alt="Back to top" width="126" height="36" /></a>
</p>
<!-- buttons:return:end -->

<p align="center"><img src="./profile/mission-orbit-divider.svg" alt="" width="100%" /></p>

<div align="center">

**Security workflows, useful tools, or a self-hosting rabbit hole? Let's talk.**

<!-- buttons:footer:start -->
<p align="center">
  <a href="https://www.linkedin.com/in/harsimransidhu/"><img src="./profile/buttons/contact.svg" alt="Let&#x27;s connect" width="160" height="44" /></a>
</p>
<!-- buttons:footer:end -->

<sub>Build with curiosity. Leave something useful behind.</sub>

</div>
