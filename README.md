<div align="center">

<a href="https://harsim.ca"><img src="./profile/mission-banner.svg" alt="Harsimran Sidhu — turning curiosity into automation. Cybersecurity, threat intelligence, and automation." width="100%" /></a>

**Cybersecurity analyst · Open-source builder · Homelab tinkerer**

<a href="https://harsim.ca"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&amp;weight=500&amp;size=20&amp;duration=2800&amp;pause=1500&amp;color=43E6C5&amp;center=true&amp;vCenter=true&amp;width=780&amp;height=38&amp;lines=Follow+the+evidence.;Automate+the+boring+bits.;Always+one+more+thing+to+build." alt="Follow the evidence. Automate the boring bits. Always one more thing to build." width="780" /></a>

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

### 💓 Project heartbeat

| Public project | Checks | Latest release |
| :--- | :--- | :--- |
| [SwiftIOC](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector) | [![SwiftIOC CI](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector/actions/workflows/ci.yml) | [![SwiftIOC release](https://img.shields.io/github/v/release/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector?label=release&color=A995FF)](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector/releases/latest) |
| [IOC Inspector](https://github.com/PKHarsimran/IOC-Inspector) | [![IOC Inspector CI](https://github.com/PKHarsimran/IOC-Inspector/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/PKHarsimran/IOC-Inspector/actions/workflows/ci.yml) | [![IOC Inspector release](https://img.shields.io/github/v/release/PKHarsimran/IOC-Inspector?label=release&color=A995FF)](https://github.com/PKHarsimran/IOC-Inspector/releases/latest) |
| [Website Downloader](https://github.com/PKHarsimran/website-downloader) | [![Website Downloader CI](https://github.com/PKHarsimran/website-downloader/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/PKHarsimran/website-downloader/actions/workflows/python-app.yml) | [![Website Downloader release](https://img.shields.io/github/v/release/PKHarsimran/website-downloader?label=release&color=A995FF)](https://github.com/PKHarsimran/website-downloader/releases/latest) |

<sub>Badges may be cached; open one for the underlying workflow or release.</sub>

### 01 / SwiftIOC

<a href="https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector"><img src="./profile/mission-swiftioc.svg" alt="SwiftIOC — follow the indicator, keep the evidence. Python threat intelligence and analyst workflows." width="100%" /></a>

**Threat intelligence you can trace back to the source.** A Python collector normalizes IOCs and vulnerability reports; the browser dashboard brings the evidence together for investigation and export.

[🛰️ Open dashboard ↗](https://harsim.ca/SwiftIOC-Automated-Threat-Intelligence-Collector/) · [Source ↗](https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector)

<details>
<summary><strong>🎬 Watch a 12-second evidence review</strong></summary>

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="./profile/swift-demo.png">
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

**Give suspicious documents a closer look.** Triage PDFs and Office files with static analysis, IOC extraction, and optional threat enrichment. Export findings in Markdown, JSON, or CSV for the next step of the investigation.

[Source ↗](https://github.com/PKHarsimran/IOC-Inspector)

### 03 / Website Downloader

<a href="https://github.com/PKHarsimran/website-downloader"><img src="./profile/mission-downloader.svg" alt="Website Downloader — take a little piece of the web offline. Python web archiving with optional Playwright rendering." width="100%" /></a>

**An offline copy you can actually browse.** Mirror websites you're authorized to archive, rewrite links and assets, and update existing copies. Optional Playwright rendering handles pages that need JavaScript.

[📖 Field guide ↗](https://github.com/PKHarsimran/website-downloader/wiki) · [Source ↗](https://github.com/PKHarsimran/website-downloader)

<details>
<summary><strong>🎬 Watch the CLI turn a site into an offline copy</strong></summary>

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="./profile/cli-demo.png">
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

I'm also turning what I've learned into a **modular Compose starter kit**, with guided setup and connected services so others can build their own home server.

**The fun part:** making the containers work together, then automating the bits in between. ⚙️

<details>
<summary><strong>🧠 Build story: a server, not just a list of containers</strong></summary>

- **Problem:** a collection of running services still leaves requests, downloads, imports, libraries, and troubleshooting disconnected.
- **Built:** a Compose-based home server connecting media workflows, photo and book libraries, custom dashboards, health checks, logs, and notifications.
- **Design takeaway:** the useful work is in the connections: storage paths, permissions, service handoffs, and understandable recovery. More containers alone don't make a better server.

</details>


## 🚧 Now building

<img src="./profile/mission-now.svg" alt="Now building: a modular Docker Compose home-server starter kit with guided setup and connected services. Next checkpoint: independent fresh-install validation using the documentation." width="100%" />

The next checkpoint is making the setup understandable to someone who wasn't there when it was built: follow the docs, choose service groups, and get a connected server running.

## 🧰 Toolkit

### 🐍 Code & scripts

<p>
<img src="https://img.shields.io/badge/Python-0D1117?style=for-the-badge&amp;logo=python&amp;logoColor=FFD43B" alt="Python" />
<img src="https://img.shields.io/badge/Bash-0D1117?style=for-the-badge&amp;logo=gnubash&amp;logoColor=00D4AA" alt="Bash" />
<img src="https://img.shields.io/badge/C++-0D1117?style=for-the-badge&amp;logo=cplusplus&amp;logoColor=659AD2" alt="C++" />
</p>

### 🛡️ Security & detection

<p>
<img src="https://img.shields.io/badge/Splunk-0D1117?style=for-the-badge&amp;logo=splunk&amp;logoColor=00D4AA" alt="Splunk" />
<img src="https://img.shields.io/badge/Cortex%20XDR-0D1117?style=for-the-badge&amp;logo=paloaltonetworks&amp;logoColor=F04E23" alt="Cortex XDR" />
<img src="https://img.shields.io/badge/Kibana-0D1117?style=for-the-badge&amp;logo=kibana&amp;logoColor=F04E98" alt="Kibana" />
<img src="https://img.shields.io/badge/F5%20BIG--IP-0D1117?style=for-the-badge&amp;logo=f5&amp;logoColor=E4002B" alt="F5 BIG-IP" />
</p>

### ⚙️ Automation & infrastructure

<p>
<img src="https://img.shields.io/badge/Docker-0D1117?style=for-the-badge&amp;logo=docker&amp;logoColor=2496ED" alt="Docker" />
<img src="https://img.shields.io/badge/Ansible-0D1117?style=for-the-badge&amp;logo=ansible&amp;logoColor=EE0000" alt="Ansible" />
<img src="https://img.shields.io/badge/Raspberry%20Pi-0D1117?style=for-the-badge&amp;logo=raspberrypi&amp;logoColor=A22846" alt="Raspberry Pi" />
</p>

### 📡 Observability

<p>
<img src="https://img.shields.io/badge/Grafana-0D1117?style=for-the-badge&amp;logo=grafana&amp;logoColor=F46800" alt="Grafana" />
<img src="https://img.shields.io/badge/InfluxDB-0D1117?style=for-the-badge&amp;logo=influxdb&amp;logoColor=22ADF6" alt="InfluxDB" />
<img src="https://img.shields.io/badge/MQTT-0D1117?style=for-the-badge&amp;logo=mqtt&amp;logoColor=B47BFF" alt="MQTT" />
</p>

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

---

<div align="center">

**Security workflows, useful tools, or a self-hosting rabbit hole? Let's talk.**

[Say hello on LinkedIn ↗](https://www.linkedin.com/in/harsimransidhu/) · [Explore harsim.ca ↗](https://harsim.ca)

<sub>Build with curiosity. Leave something useful behind.</sub>

</div>
