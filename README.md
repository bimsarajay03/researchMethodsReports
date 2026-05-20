# researchMethodsReports

Collaborative LaTeX report repository for the Research Methods module.
All reports are written in LaTeX, version-controlled on GitHub, and automatically compiled to PDF by GitHub Actions on every push.

---

## Table of Contents

1. [Repository Structure](#repository-structure)
2. [Setup Guide](#1-setup-guide)
3. [Creating a New Report](#2-creating-a-new-report)
4. [Creating a Page (Section) in a Report](#3-creating-a-page-section-in-a-report)
5. [How to Contribute](#4-how-to-contribute)
6. [Compiling Locally & Getting a PDF](#5-compiling-locally--getting-a-pdf)
7. [Automated CI Compilation](#6-automated-ci-compilation)

---

## Repository Structure

```
researchMethodsReports/
├── .devcontainer/
│   └── devcontainer.json        ← VS Code Dev Container (full TeX Live)
├── .github/
│   └── workflows/
│       └── compile-latex.yml    ← GitHub Actions: auto-compile on push
├── reports/
│   ├── template/                ← Copy this to start a new report
│   │   ├── main.tex
│   │   ├── references.bib
│   │   └── sections/
│   │       ├── 01_introduction.tex
│   │       ├── 02_literature_review.tex
│   │       ├── 03_methodology.tex
│   │       ├── 04_results.tex
│   │       ├── 05_discussion.tex
│   │       └── 06_conclusion.tex
│   └── report-01-sample/        ← Example completed report
│       ├── main.tex
│       ├── references.bib
│       └── sections/
├── shared/
│   ├── preamble.tex             ← Common packages & styles (edit once, applies everywhere)
│   └── title_page.tex           ← Reusable title page
├── .gitignore
├── CONTRIBUTING.md
└── README.md
```

---

## 1. Setup Guide

### Option A — VS Code Dev Container (Recommended, zero local install)

> Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) and the
> [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-org>/researchMethodsReports.git
   cd researchMethodsReports
   ```

2. **Open in VS Code**
   ```bash
   code .
   ```

3. When prompted **"Reopen in Container"** — click it (or run **Dev Containers: Reopen in Container** from the Command Palette).

4. VS Code will pull a full TeX Live image and install all recommended extensions automatically. This takes a few minutes the first time.

5. You are ready. The LaTeX Workshop extension auto-compiles on save.

---

### Option B — Local macOS Setup

1. **Install TeX Live (full)**
   ```bash
   brew install --cask mactex
   ```
   > This installs MacTeX (~5 GB) which includes `pdflatex`, `lualatex`, `biber`, and `latexmk`.

2. **Reload your shell** (or open a new terminal) so `pdflatex` is on your `PATH`.

3. **Install VS Code extensions** (optional but strongly recommended):
   - [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
   - [LTeX – Grammar/spell check](https://marketplace.visualstudio.com/items?itemName=valentjn.vscode-ltex)
   - [GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)

4. **Clone the repository**
   ```bash
   git clone https://github.com/<your-org>/researchMethodsReports.git
   cd researchMethodsReports
   code .
   ```

---

### Option C — Local Ubuntu/Debian Setup

```bash
sudo apt-get update
sudo apt-get install -y texlive-full biber latexmk
```

---

## 2. Creating a New Report

1. **Copy the template folder** and rename it following the convention `report-NN-short-slug`:
   ```bash
   cp -r reports/template reports/report-02-my-topic
   ```

2. **Edit the metadata** in `reports/report-02-my-topic/main.tex`:
   ```latex
   \newcommand{\ReportTitle}{Your Report Title}
   \newcommand{\ReportSubtitle}{Your Subtitle}
   \newcommand{\ReportAuthors}{Alice \and Bob \and Carol}
   \newcommand{\ReportDate}{June 2026}
   ```

3. **Register the report in CI** — open `.github/workflows/compile-latex.yml` and add the folder name to the matrix:
   ```yaml
   matrix:
     report:
       - report-01-sample
       - report-02-my-topic    # ← add this line
   ```

4. **Commit and push** — GitHub Actions will compile it automatically.

---

## 3. Creating a Page (Section) in a Report

Each section of a report lives in its own `.tex` file inside the `sections/` folder of that report. This keeps individual contributions small and merge conflicts rare.

### Add a new section

1. Create a new file, e.g. `sections/07_appendix.tex`:
   ```latex
   \section{Appendix}
   \label{sec:appendix}

   Your content here.
   ```

2. Include it in `main.tex` **in the correct order**:
   ```latex
   \input{sections/06_conclusion}
   \input{sections/07_appendix}   % ← add this line
   ```

3. Save, commit, and push.

### Section file conventions

| File | Section |
|------|---------|
| `01_introduction.tex` | Introduction |
| `02_literature_review.tex` | Literature Review |
| `03_methodology.tex` | Methodology |
| `04_results.tex` | Results |
| `05_discussion.tex` | Discussion |
| `06_conclusion.tex` | Conclusion |

### Adding a figure

Place images inside `reports/report-NN/figures/` and reference them:

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/my-chart.png}
  \caption{Description of the figure.}
  \label{fig:my-chart}
\end{figure}
```

### Adding a citation

1. Add the BibTeX entry to `references.bib` in your report folder.
2. Cite it with `\cite{key}` in the text.

---

## 4. How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. Quick summary:

1. **Never push directly to `main`.**
2. Create a feature branch: `git checkout -b yourname/section-name`
3. Make changes — each contributor should normally edit only their assigned section file.
4. Push and open a Pull Request targeting `main`.
5. At least one other team member must review and approve before merging.
6. The CI pipeline compiles LaTeX and fails the PR if there are errors — fix them before merging.

---

## 5. Compiling Locally & Getting a PDF

### Using VS Code + LaTeX Workshop (Dev Container or local)

- Open `main.tex` of the report you want to compile.
- Press **Ctrl+Alt+B** (macOS: **Cmd+Option+B**) to build, or simply **save the file** (auto-build is enabled).
- Click the **PDF preview** button (top-right of the editor) to open the PDF side by side.

### Using the command line

```bash
cd reports/report-01-sample

# Full build (PDF + bibliography)
latexmk -pdf -interaction=nonstopmode main.tex

# Clean auxiliary files
latexmk -c

# The output PDF is: reports/report-01-sample/main.pdf
```

### Troubleshooting

| Problem | Fix |
|---------|-----|
| `biber` not found | Install via `brew install biber` or `apt install biber` |
| Missing package | Run `tlmgr install <package>` (TeX Live) |
| Bibliography not updating | Run `latexmk` (it reruns biber automatically) |
| Font errors | Make sure you have a full TeX Live install, not a minimal one |

---

## 6. Automated CI Compilation

Every push to `main` or `dev` that touches `reports/` or `shared/` triggers the GitHub Actions workflow:

- Each registered report is compiled with `latexmk`.
- The compiled PDF is uploaded as a **build artifact** (downloadable from the Actions tab for 30 days).
- Merges to `main` additionally push PDFs to the `compiled-pdfs` branch.

To download a compiled PDF:
1. Go to the **Actions** tab on GitHub.
2. Click the most recent **Compile LaTeX Reports** run.
3. Scroll to **Artifacts** and download the PDF for your report.
