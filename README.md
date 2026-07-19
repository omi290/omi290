<!-- README.md -->
<div align="center">
  <img src="assets/generated/ascii/portrait.svg" alt="Terminal Portrait" />
  <img src="assets/generated/ascii/fastfetch.svg" alt="System Info" />
</div>

<br />

<div align="center">
  <img src="assets/generated/skills/skills.svg" alt="Tech Stack" />
</div>

<br />

<div align="center">
  <img src="assets/generated/heatmap/heatmap.svg" alt="Contribution Heatmap" />
</div>

<br />

<div align="center">
  <img src="assets/generated/projects/projects.svg" alt="Top Projects" />
</div>

---

### Project Vision
This repository is a production-quality GitHub Profile Generator built for a Software Engineer specializing in AI-powered applications. It treats the GitHub profile as a dynamic software product, moving beyond simple static markdown files. Everything is modular, scalable, and data-driven.

### Architecture
The project strictly separates generated assets from static resources. A central `config.py` manages sizing and timings, while a robust Theme abstraction (with `GitHubDark` as default) handles styling. Generators do not hardcode personal data; instead, they retrieve their information from a unified `profile.json` source of truth.

### Folder Structure
- `assets/generated/`: Contains dynamic SVG outputs, categorized into subdirectories (`ascii`, `cards`, `heatmap`, `skills`, `projects`).
- `assets/static/`: Houses static materials like photos, icons, fonts, and backgrounds.
- `src/`: Contains the core application code, including the orchestrator, modular generators, and shared SVG utilities.
- `tests/`: Ensure system reliability.

### Generator Pipeline
The orchestrator reads configurations and the active theme, parses the central data JSON, and dynamically dispatches tasks to independent generators. Each generator has a single responsibility and utilizes shared, reusable utility modules to render optimized, stateless SVGs directly to their respective asset directories.

### Development Workflow
Developers can modify the `profile.json` structure or add new themes without touching the core generator logic. New profile sections can be added by creating a new generator class that interfaces with the base generator, fetching data from APIs and rendering isolated SVGs using unified utilities.

### GitHub Actions Workflow
The workflow is designed to run non-interactively on a scheduled basis (e.g., daily). It checks out the repository, bootstraps the Python environment, executes the generator orchestrator locally, and commits any newly generated animated SVGs back to the `main` branch to update the public profile in real-time.
