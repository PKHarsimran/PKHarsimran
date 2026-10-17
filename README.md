<div align="center">

<a href="https://harsim.ca"><img src="./profile/mission-banner.svg" alt="Harsimran Sidhu — turning curiosity into automation. Cybersecurity, threat intelligence, and automation." width="100%" /></a>

**Cybersecurity analyst · Open-source builder · Homelab tinkerer**

<a href="https://harsim.ca"><img src="./profile/mission-typing.svg" alt="Follow the evidence. Automate the boring bits. Always one more thing to build." width="780" /></a>

[Website ↗](https://harsim.ca) · [LinkedIn ↗](https://www.linkedin.com/in/harsimransidhu/) · [Docker Hub ↗](https://hub.docker.com/u/pkvirus)

[👋 Operator](#-operator-profile) · [🚀 Projects](#-selected-builds) · [🏠 Homelab](#-inside-the-lab) · [🚧 Now building](#-now-building) · [🧰 Toolkit](#-toolkit) · [📊 Activity](#-activity-log)

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

### 📡 Public build radar

<a href="./profile/public-pulse.md"><img src="./profile/public-pulse.svg" alt="Daily public build radar: CI status, latest release, stars, and default-branch commit date for SwiftIOC, IOC Inspector, and Website Downloader." width="100%" /></a>

[Read the snapshot](./profile/public-pulse.md) · [Watch the generator run ↗](https://github.com/PKHarsimran/PKHarsimran/actions/workflows/profile-lab.yml)

<details>
<summary><strong>💓 Open live checks & release links</strong></summary>

| Public project | Checks | Latest release |
| :--- | :--- | :--- |
| [SwiftIOC](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector) | [![SwiftIOC CI](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector/actions/workflows/ci.yml) | [![SwiftIOC release](https://img.shields.io/github/v/release/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector?label=release&color=A995FF)](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector/releases/latest) |
| [IOC Inspector](https://github.com/PKHarsimran/IOC-Inspector) | [![IOC Inspector CI](https://github.com/PKHarsimran/IOC-Inspector/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/PKHarsimran/IOC-Inspector/actions/workflows/ci.yml) | [![IOC Inspector release](https://img.shields.io/github/v/release/PKHarsimran/IOC-Inspector?label=release&color=A995FF)](https://github.com/PKHarsimran/IOC-Inspector/releases/latest) |
| [Website Downloader](https://github.com/PKHarsimran/website-downloader) | [![Website Downloader CI](https://github.com/PKHarsimran/website-downloader/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/PKHarsimran/website-downloader/actions/workflows/python-app.yml) | [![Website Downloader release](https://img.shields.io/github/v/release/PKHarsimran/website-downloader?label=release&color=A995FF)](https://github.com/PKHarsimran/website-downloader/releases/latest) |

<sub>Badges may be cached; open one for the underlying workflow or release.</sub>

</details>

### 01 / SwiftIOC

<a href="https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector"><img src="./profile/mission-swiftioc.svg" alt="SwiftIOC — follow the indicator, keep the evidence. Python threat intelligence and analyst workflows." width="100%" /></a>

**Threat intelligence you can trace back to the source.** A Python collector normalizes IOCs and vulnerability reports; the browser dashboard brings the evidence together for investigation and export.

[🛰️ Open dashboard ↗](https://harsim.ca/SwiftIOC-Automated-Threat-Intelligence-Collector/) · [Source ↗](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector)

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

### 02 / IOC Inspector

<a href="https://github.com/PKHarsimran/IOC-Inspector"><img src="./profile/mission-inspector.svg" alt="IOC Inspector — suspicious documents, useful answers. Python static analysis and structured reports." width="100%" /></a>

**Suspicious documents, useful answers.** Triage PDFs and Office files with static analysis, IOC extraction, and optional threat enrichment. Export Markdown, JSON, or CSV for the next step of the investigation.

[Source ↗](https://github.com/PKHarsimran/IOC-Inspector)

### 03 / Website Downloader

<a href="https://github.com/PKHarsimran/website-downloader"><img src="./profile/mission-downloader.svg" alt="Website Downloader — take a little piece of the web offline. Python web archiving with optional Playwright rendering." width="100%" /></a>

**An offline copy you can actually browse.** Mirror websites you're authorized to archive, rewrite links and assets, and update existing copies. Optional Playwright rendering handles pages that need JavaScript.

[📖 Field guide ↗](https://github.com/PKHarsimran/website-downloader/wiki) · [Source ↗](https://github.com/PKHarsimran/website-downloader)

<details>
<summary><strong>🎬 Watch the CLI turn a site into an offline copy</strong></summary>

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="./profile/cli-demo.webp">
  <img src="./profile/cli-demo.gif" alt="Website Downloader walkthrough: recorded CLI output from an owned local demo site, followed by the generated offline mirror. Three HTML pages, CSS and an SVG asset; relative links verified." width="100%">
</picture>

<sub>A replay of real CLI output, followed by the generated mirror. Recorded October 17, 2026, using an owned local fixture; the localhost address is part of the demo.</sub>

</details>

## 🏠 Inside the lab

My **Zima homelab** brings media, photos, books, and everyday self-hosting together with **Docker Compose**. I've built the connections, dashboards, and automation around the services to make the whole stack easier to run.

<img src="./profile/mission-homelab.svg" alt="Zima homelab service map: Jellyfin and Jellyseerr with Radarr, Sonarr, Prowlarr and Bazarr; Transmission with Gluetun; PhotoPrism; Shelfmark and Audiobookshelf; Homepage, Portainer and custom flow dashboards; Uptime Kuma, Glances, Dozzle and ntfy. Connected using Docker Compose." width="100%" />

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

**The fun part:** teaching the containers to work together, then automating the bits in between. ⚙️

<details>
<summary><strong>🧠 Build story: a server, not just a list of containers</strong></summary>

- **Problem:** a collection of running services still leaves requests, downloads, imports, libraries, and troubleshooting disconnected.
- **Built:** a Compose-based home server connecting media workflows, photo and book libraries, custom dashboards, health checks, logs, and notifications.
- **Design takeaway:** the useful work is in the connections: storage paths, permissions, service handoffs, and understandable recovery. More containers alone don't make a better server.

</details>

## 🚧 Now building

<img src="./profile/mission-now.svg" alt="Now building: a modular Docker Compose home-server starter kit with guided setup and connected services. Next checkpoint: independent fresh-install validation using the documentation." width="100%" />

Turning lessons from the Zima lab into a **modular Compose starter kit**. The test: someone else can follow the docs, choose their services, and bring the stack online.

## 🧰 Toolkit

<picture>
  <source media="(max-width: 600px)" srcset="./profile/mission-toolkit-mobile.svg">
  <img src="./profile/mission-toolkit.svg" alt="Code: Python, Bash, C++. Security: Splunk, Cortex XDR, Kibana, F5 BIG-IP. Infrastructure: Docker, Ansible, Raspberry Pi. Observability: Grafana, InfluxDB, MQTT." width="100%">
</picture>

## 📊 Activity log

<div align="center">
  <img src="./profile/stats.svg" alt="Harsimran's GitHub activity statistics" width="54%" align="top" />
  <img src="./profile/top-langs.svg" alt="Most-used languages across Harsimran's GitHub repositories" width="39%" align="top" />
</div>

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

---

<div align="center">

**Security workflows, useful tools, or a self-hosting rabbit hole? Let's talk.**

[Say hello on LinkedIn ↗](https://www.linkedin.com/in/harsimransidhu/) · [Explore harsim.ca ↗](https://harsim.ca)

<sub>Build with curiosity. Leave something useful behind.</sub>

</div>
