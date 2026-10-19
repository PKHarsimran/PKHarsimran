<a id="mission-control" name="mission-control"></a>

<div align="center">

<a href="https://harsim.ca">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/studio-orbit-hero-mobile.svg">
  <img src="./profile/studio-orbit-hero.svg" alt="Harsimran Sidhu. Security instincts. Builder energy. Cybersecurity, open source and self-hosting." width="100%" />
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
  <a href="#user-content-selected-builds"><img src="./profile/buttons/projects-tab.svg" alt="Projects" width="100" height="44" /></a>
  <a href="#user-content-homelab"><img src="./profile/buttons/homelab-tab.svg" alt="Homelab" width="102" height="44" /></a>
  <a href="#user-content-arcade"><img src="./profile/buttons/arcade-tab.svg" alt="Arcade" width="100" height="44" /></a>
</p>
<!-- buttons:navigation:end -->

</div>

I work in **cybersecurity** and build tools that make investigations clearer and repetitive work shorter. Off the clock, I connect the dots in my **Zima homelab**. The robot has other plans. 🛠️

<a name="selected-builds"></a>

## Selected builds

**Pick a side quest:** [Investigate threat feeds](#user-content-01--swiftioc) · [Inspect a document](#user-content-02--ioc-inspector) · [Save a site offline](#user-content-03--website-downloader)

### 01 / SwiftIOC

<a href="https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/studio-swiftioc-motion-mobile.svg">
  <img src="./profile/studio-swiftioc-motion.svg" alt="SwiftIOC — follow the indicator, keep the evidence. Animated feed documents flow into indicators and their evidence graph. Python threat intelligence and analyst workflows." width="100%" />
</picture>
</a>

**Follow an indicator back to its source.** A Python pipeline collects threat feeds and vulnerability reports; the dashboard keeps their evidence in view.

<!-- buttons:swift:start -->
<p align="left">
  <a href="https://harsim.ca/SwiftIOC-Automated-Threat-Intelligence-Collector/"><img src="./profile/buttons/dashboard.svg" alt="Open dashboard" width="166" height="44" /></a>
  <a href="https://github.com/PKHarsimran/SwiftIOC-Automated-Threat-Intelligence-Collector"><img src="./profile/buttons/source.svg" alt="View source" width="140" height="44" /></a>
</p>
<!-- buttons:swift:end -->

<details>
<summary><picture>
  <source media="(max-width: 600px)" srcset="./profile/drawers/evidence-mobile.svg">
  <img src="./profile/drawers/evidence.svg" alt="Evidence desk: Real feed snapshot + a 12-second walkthrough" width="94%" align="absmiddle">
</picture></summary>

<a href="./profile/intel-conveyor.md">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/intel-conveyor-mobile.svg">
  <img src="./profile/intel-conveyor.svg" alt="Workflow-generated SwiftIOC conveyor: collect, normalize, publish and investigate. Real retained observable and CVE counts, deduplication, last-interval changes and collection timestamp from the public diagnostics." width="100%">
</picture>
</a>

<sub>Real feed counts, illustrated from a saved collection snapshot. [Read the data](./profile/intel-conveyor.md).</sub>

**12 seconds at the evidence desk**

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="./profile/swift-demo.webp">
  <img src="./profile/swift-demo.gif" alt="SwiftIOC walkthrough: open the public dashboard, review a CVE, inspect CISA evidence, and compare NVD details." width="100%">
</picture>

<sub>Recorded October 17, 2026. Open the dashboard for current records.</sub>

</details>

<p align="center"><img src="./profile/studio-signal-divider.svg" alt="" width="100%" /></p>

### 02 / IOC Inspector

<a href="https://github.com/PKHarsimran/IOC-Inspector">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/studio-inspector-motion-mobile.svg">
  <img src="./profile/studio-inspector-motion.svg" alt="IOC Inspector — suspicious documents, useful answers. An illustrated document scan follows clues into a report. Python static analysis and structured reports." width="100%" />
</picture>
</a>

**Find the clues in a suspicious document.** Inspect PDFs and Office files, extract IOCs, and export a readable report. Optional threat enrichment adds context.

<!-- buttons:inspector:start -->
<p align="left">
  <a href="https://github.com/PKHarsimran/IOC-Inspector#-quick-start"><img src="./profile/buttons/quick-start.svg" alt="Quick start" width="150" height="44" /></a>
  <a href="https://github.com/PKHarsimran/IOC-Inspector"><img src="./profile/buttons/source-inspector.svg" alt="View source" width="140" height="44" /></a>
</p>
<!-- buttons:inspector:end -->

<details>
<summary><picture>
  <source media="(max-width: 600px)" srcset="./profile/drawers/case-mobile.svg">
  <img src="./profile/drawers/case.svg" alt="Case of the week: Spot the clues. Let the scanner check your theory." width="94%" align="absmiddle">
</picture></summary>

A harmless training PDF, a few hidden clues, and the real scanner. What can you spot?

<picture>
  <source media="(max-width: 600px)" srcset="./profile/case-file-mobile.svg">
  <img src="./profile/case-file.svg" alt="IOC Inspector case of the week: an owned, harmless PDF with a few clues. The released CLI generates the findings; expand the answer below." width="100%">
</picture>

<details>
<summary><strong>🔎 Open the evidence envelope</strong> <sub>· reveal the findings</sub></summary>

<img src="./profile/case-findings.svg" alt="Actual extracted URLs, IP count, heuristic verdict and score from the weekly harmless training PDF. External reputation lookups are disabled; a heuristic verdict is not a security guarantee." width="600">

[Read the report](./profile/case-report.md) · [See the extracted data](./profile/case-report.json)

</details>

<details>
<summary><strong>🎬 Replay the investigation</strong> <sub>· real CLI run</sub></summary>

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="./profile/inspector-demo.webp">
  <img src="./profile/inspector-demo.gif" alt="VHS recording of the demo runner invoking the released IOC Inspector CLI on the weekly owned PDF and verifying its actual JSON findings." width="100%">
</picture>

<sub>A real CLI run against an owned training file. [How it was recorded](./profile/demo-provenance.json).</sub>

</details>

</details>

<p align="center"><img src="./profile/studio-signal-divider.svg" alt="" width="100%" /></p>

### 03 / Website Downloader

<a href="https://github.com/PKHarsimran/website-downloader">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/studio-downloader-motion-mobile.svg">
  <img src="./profile/studio-downloader-motion.svg" alt="Website Downloader — take a little piece of the web offline. Animated page packets travel into an offline archive with connected files. Python web archiving with optional Playwright rendering." width="100%" />
</picture>
</a>

**Take a little piece of the web offline.** Save pages and assets with working local links. Add Playwright rendering when a page needs JavaScript.

<!-- buttons:downloader:start -->
<p align="left">
  <a href="https://github.com/PKHarsimran/website-downloader/wiki"><img src="./profile/buttons/field-guide.svg" alt="Field guide" width="150" height="44" /></a>
  <a href="https://github.com/PKHarsimran/website-downloader"><img src="./profile/buttons/source-downloader.svg" alt="View source" width="140" height="44" /></a>
</p>
<!-- buttons:downloader:end -->

<details>
<summary><picture>
  <source media="(max-width: 600px)" srcset="./profile/drawers/offline-mobile.svg">
  <img src="./profile/drawers/offline.svg" alt="Offline field trip: One site. No server. A real CLI demo." width="94%" align="absmiddle">
</picture></summary>

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="./profile/downloader-demo.webp">
  <img src="./profile/downloader-demo.gif" alt="VHS recording of the demo runner invoking the released Website Downloader CLI, stopping the owned local source server, and verifying all links and assets in the three-page offline mirror." width="100%">
</picture>

<sub>A real CLI run: save an owned test site, stop its server, then check the offline copy. [Run results](./profile/downloader-demo.json).</sub>

</details>

<a id="homelab" name="homelab"></a>

## Inside the lab

My **Zima homelab** is where side projects become everyday tools. **Docker Compose** connects media requests, libraries, photos, dashboards, and monitoring.

<picture>
  <source media="(max-width: 600px)" srcset="./profile/homelab-flow-motion-mobile.svg">
  <img src="./profile/homelab-flow-motion.svg" alt="Zima homelab flow theatre: Jellyseerr requests, Radarr/Sonarr/Prowlarr/Bazarr automation, Transmission with Gluetun, and Jellyfin playback. Photo and book libraries, operations and monitoring share the stack. Illustrated handoffs from a curated service manifest; no live telemetry." width="100%" />
</picture>

<sub>The real service cast, with illustrated handoffs. [Public service manifest](./profile/lab-services.json).</sub>

<details>
<summary><picture>
  <source media="(max-width: 600px)" srcset="./profile/drawers/crew-mobile.svg">
  <img src="./profile/drawers/crew.svg" alt="Meet the service crew: Media, libraries, dashboards &amp; monitoring" width="94%" align="absmiddle">
</picture></summary>

| Area | Services |
| :--- | :--- |
| Media & automation | Jellyfin, Jellyseerr, Radarr, Sonarr, Prowlarr, Bazarr |
| Downloads | Transmission, Gluetun |
| Photos | PhotoPrism |
| Books & audio | Shelfmark, Audiobookshelf |
| Operations | Homepage, Portainer, custom flow dashboards |
| Monitoring | Uptime Kuma, Glances, Dozzle, ntfy |

</details>

**Next checkpoint:** turn the lab lessons into a **modular Compose starter kit** that someone else can bring online by following the docs. ⚙️

## Toolkit

<picture>
  <source media="(max-width: 600px)" srcset="./profile/mission-toolkit-icons-mobile.svg">
  <img src="./profile/mission-toolkit-icons.svg" alt="Code: Python, Bash, C++. Security: Splunk, Cortex XDR, Kibana, F5 BIG-IP. Infrastructure: Docker, Ansible, Raspberry Pi. Observability: Grafana, InfluxDB, MQTT." width="100%">
</picture>

<!-- buttons:containers:start -->
<p align="left">
  <a href="https://hub.docker.com/u/pkvirus"><img src="./profile/buttons/docker.svg" alt="Container images" width="188" height="44" /></a>
</p>
<!-- buttons:containers:end -->

<a id="activity" name="activity"></a>
<a id="arcade" name="arcade"></a>

## After hours: the arcade

The tools do useful work. Pixel handles the side quests. Follow the bot, crack today’s code, or find the secret terminal.

<a href="https://harsim.ca/lab/">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/pixel-portal-mobile.svg">
  <img src="./profile/pixel-portal.svg" alt="Psst. There’s a secret terminal. Pixel previews help, party and patches with a wave and confetti. Click to enter the interactive lab: tiny cases, five mission patches and a creature badge to keep." width="100%">
</picture>
</a>

<!-- buttons:live-lab:start -->
<p align="left">
  <a href="https://harsim.ca/lab/"><img src="./profile/buttons/live-lab.svg" alt="Enter live lab" width="176" height="44" /></a>
</p>
<!-- buttons:live-lab:end -->

<sub>Step inside, press <code>/</code>, and ask Pixel for <code>help</code>. The terminal, saved progress, and collectible patches live in the lab.</sub>

<picture>
  <source media="(max-width: 600px)" srcset="./profile/contribution-evidence-run-mobile.svg">
  <img src="./profile/contribution-evidence-run.svg" alt="Contribution arcade: real GitHub calendar totals, active days and contributions in the last 30 displayed days. Below the calendar, a pixel bot hops over obstacles, collects clues, passes an inspection station and delivers a parcel through a portal. A bot message rotates daily. The phone layout splits the full calendar into two rows; reduced motion keeps it still." width="100%">
</picture>

<sub>Real GitHub activity; an illustrated bot adventure. Totals include automation and publicly shared private activity. [Daily snapshot](./profile/contribution-calendar.json).</sub>

<!-- arcade-lab:start -->
<details>
<summary><picture>
  <source media="(max-width: 600px)" srcset="./profile/drawers/heist-mobile.svg">
  <img src="./profile/drawers/heist.svg" alt="Today&#x27;s Signal Heist: Three clues. One code. A creature to uncover." width="94%" align="absmiddle">
</picture></summary>

<picture>
  <source media="(max-width: 600px)" srcset="./profile/arcade/heist-a8d845b69ffe7ca4-mobile.svg">
  <img src="./profile/arcade/heist-a8d845b69ffe7ca4.svg" alt="Signal Heist. Route: B, then A, then C. Gate A: Website Downloader, v2.6.1. Patch version: ones digit. Gate B: Days with activity, 346. Take the ones digit. Gate C: Stars / selected 3 projects, 233. Take the ones digit. Choose a three-digit code below." width="100%">
</picture>

**Three clues → one code → a tiny creature.** Take each gate’s digit, follow the printed route, and open a code hatch.

<details>
<summary><strong>🔐 Hatch 01</strong> · <code>750</code></summary>

↺ **Decoy hatch.** Check the ones digits and the route order. Another hatch awaits.

</details>

<details>
<summary><strong>🔐 Hatch 02</strong> · <code>613</code></summary>

🔓 **Signal recovered.** B → A → C gives **613**.

| Gate | Clue | Digit |
| --- | --- | ---: |
| A | Website Downloader: v2.6.1 | 1 |
| B | Days with activity: 346 | 6 |
| C | Stars / selected 3 projects: 233 | 3 |

**Next side quest:** [Explore Website Downloader](https://github.com/PKHarsimran/website-downloader) — the real tool behind gate A.

<img src="./profile/arcade/relic-a8d845b69ffe7ca4.svg" alt="Snapshot relic A8D845B6: Byte Moth, a symmetric pixel creature drawn from this public snapshot." width="600">

[Open your creature art](./profile/arcade/relic-a8d845b69ffe7ca4.svg)

</details>

<details>
<summary><strong>🔐 Hatch 03</strong> · <code>076</code></summary>

↺ **Decoy hatch.** Check the ones digits and the route order. Another hatch awaits.

</details>

<details>
<summary><strong>⏪ Checkpoint rewind</strong> <sub>· what changed since last time?</sub></summary>

Snapshots: **2026-10-18 19:57:06** → **2026-10-18 20:03:58** UTC. Comparing the three selected public projects.

**Quiet checkpoint.** No changes in releases, CI, stars, or latest commit times.

</details>

<sub>A fresh puzzle from public signals each day. [Snapshot & creature fingerprint](./profile/arcade-lab.json).</sub>

</details>
<!-- arcade-lab:end -->

<details>
<summary><picture>
  <source media="(max-width: 600px)" srcset="./profile/drawers/snake-mobile.svg">
  <img src="./profile/drawers/snake.svg" alt="Release the snake: A bonus lap around the contribution grid" width="94%" align="absmiddle">
</picture></summary>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/PKHarsimran/PKHarsimran/output/github-contribution-grid-snake-dark.svg">
  <img src="https://raw.githubusercontent.com/PKHarsimran/PKHarsimran/output/github-contribution-grid-snake.svg" alt="Animated snake tracing Harsimran's GitHub contribution grid" width="100%">
</picture>

</details>

<details>
<summary><picture>
  <source media="(max-width: 600px)" srcset="./profile/drawers/radar-mobile.svg">
  <img src="./profile/drawers/radar.svg" alt="Project radar: Build checks, releases &amp; collectible patches" width="94%" align="absmiddle">
</picture></summary>

<a href="./profile/public-pulse.md">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/public-pulse-mobile.svg">
  <img src="./profile/public-pulse.svg" alt="Daily public build radar: CI status, latest release, stars, and default-branch commit date for SwiftIOC, IOC Inspector, and Website Downloader." width="100%" />
</picture>
</a>

<!-- buttons:radar:start -->
<p align="left">
  <a href="./profile/public-pulse.md"><img src="./profile/buttons/snapshot.svg" alt="Read snapshot" width="160" height="44" /></a>
  <a href="https://github.com/PKHarsimran/PKHarsimran/actions/workflows/profile-lab.yml"><img src="./profile/buttons/workflow.svg" alt="Workflow" width="138" height="44" /></a>
</p>
<!-- buttons:radar:end -->

<details>
<summary><strong>🏅 Browse the patch cabinet</strong> <sub>· earned by real releases</sub></summary>

<a href="./profile/release-patches.md">
<picture>
  <source media="(max-width: 600px)" srcset="./profile/release-patches-mobile.svg">
  <img src="./profile/release-patches.svg" alt="Collectible mission patches generated from real public release versions and publication dates, showing up to two recent stable releases for each selected project." width="100%">
</picture>
</a>

[Open the release log](./profile/release-patches.md)

</details>

</details>

<details>
<summary><picture>
  <source media="(max-width: 600px)" srcset="./profile/drawers/backstage-mobile.svg">
  <img src="./profile/drawers/backstage.svg" alt="Behind the curtain: The workflows that keep this profile moving" width="94%" align="absmiddle">
</picture></summary>

GitHub Actions refresh the public project signals and daily puzzle. Case files and CLI demos refresh weekly or when their recipes change. The artwork keeps its source snapshots close.

[Arcade workflow](https://github.com/PKHarsimran/PKHarsimran/actions/workflows/profile-lab.yml) · [Demo workflow](https://github.com/PKHarsimran/PKHarsimran/actions/workflows/living-profile.yml) · [Make your own exhibits](./demos/README.md)

</details>

<!-- buttons:return:start -->
<p align="left">
  <a href="#user-content-mission-control"><img src="./profile/buttons/back-top-tab.svg" alt="Back to top" width="126" height="44" /></a>
</p>
<!-- buttons:return:end -->

<p align="center"><img src="./profile/studio-signal-divider.svg" alt="" width="100%" /></p>

<div align="center">

<!-- visitors:start -->
<picture>
  <source media="(max-width: 600px)" srcset="./profile/studio-guestbook-motion-mobile.svg" />
  <img src="./profile/studio-guestbook-motion.svg" alt="Still curious? A waving pixel mascot signs off from an animated orbital guestbook." width="100%" />
</picture>

<p align="center">
  <a href="https://hits.sh/github.com/PKHarsimran/"><img src="https://hits.sh/github.com/PKHarsimran.svg?style=for-the-badge&amp;label=LAB+PAGE+HITS&amp;color=a995ff&amp;labelColor=34445c" alt="Lab page hits — public profile view counter, not unique visitors" height="28" /></a>
</p>

<sub>Page hits, not unique visitors · <a href="https://github.com/silentsoft/hits#statistics">About the counter</a></sub>
<!-- visitors:end -->

<!-- buttons:footer:start -->
<p align="center">
  <a href="https://www.linkedin.com/in/harsimransidhu/"><img src="./profile/buttons/contact.svg" alt="Let&#x27;s connect" width="160" height="44" /></a>
</p>
<!-- buttons:footer:end -->

<sub>Build with curiosity. Leave something useful behind.</sub>

</div>
