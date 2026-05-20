# Contributing to researchMethodsReports

Thank you for contributing! Please follow these guidelines to keep the repository clean and collaboration smooth.

---

## Branching Strategy

```
main          ← stable, reviewed, compiles cleanly
dev           ← integration branch (optional, for larger groups)
yourname/...  ← your personal feature/section branches
```

**Never commit directly to `main`.**

---

## Step-by-Step Contribution Workflow

### 1. Fork & clone (first time only)

If you are an **external contributor** (not a team member with write access):

```bash
# Fork on GitHub first, then clone YOUR fork
git clone https://github.com/<your-username>/researchMethodsReports.git
cd researchMethodsReports
git remote add upstream https://github.com/<your-org>/researchMethodsReports.git
```

If you are a **team member** with direct repo access, just clone the repo:

```bash
git clone https://github.com/<your-org>/researchMethodsReports.git
cd researchMethodsReports
```

### 2. Keep your local `main` up to date

Before starting any work, always pull the latest changes:

```bash
git checkout main
git pull origin main
```

### 3. Create a feature branch

Use the convention: `yourname/short-description`

```bash
git checkout -b alice/methodology-section
```

### 4. Make your changes

- Edit **only the section file(s) assigned to you** to minimise merge conflicts.
- Common assignments:

  | Section file | Assigned to |
  |---|---|
  | `sections/01_introduction.tex` | Team lead |
  | `sections/02_literature_review.tex` | Member A |
  | `sections/03_methodology.tex` | Member B |
  | `sections/04_results.tex` | Member C |
  | `sections/05_discussion.tex` | Member D |
  | `sections/06_conclusion.tex` | Team lead |

- If you need to add a new section, discuss with the team first and update `main.tex` together.

### 5. Test your build locally before pushing

```bash
cd reports/<your-report>
latexmk -pdf -interaction=nonstopmode main.tex
```

Fix all errors before pushing. A broken build blocks the entire team.

### 6. Stage and commit

Write clear, descriptive commit messages:

```bash
git add reports/report-01-sample/sections/03_methodology.tex
git commit -m "report-01: draft methodology section"
```

**Good commit messages:**
- `report-01: add results table in section 4`
- `shared: update preamble to add siunitx package`
- `ci: add report-02 to compile matrix`

**Bad commit messages:**
- `fix`
- `changes`
- `WIP`

### 7. Push your branch

```bash
git push origin alice/methodology-section
```

### 8. Open a Pull Request

1. Go to the repository on GitHub.
2. Click **"Compare & pull request"** for your branch.
3. Set the **base branch** to `main` (or `dev` if using it).
4. Fill in the PR template:
   - **What changed:** brief summary
   - **Report affected:** e.g. `report-01-sample`
   - **How to verify:** e.g. "compiles locally, PDF looks correct"
5. Assign at least one reviewer.
6. Submit.

### 9. Address review feedback

Push additional commits to the same branch — the PR updates automatically.

### 10. Merge

Once approved **and the CI check passes** (green tick), the reviewer or you can merge using **"Squash and merge"** to keep the history clean.

---

## Resolving Merge Conflicts in LaTeX

LaTeX merge conflicts are usually in `.tex` files. VS Code shows them inline:

```
<<<<<<< HEAD
Your current version of the paragraph.
=======
Incoming version from the other branch.
>>>>>>> feature/other-branch
```

1. Choose the correct version (or combine both).
2. Remove the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
3. Run `latexmk` locally to verify it still compiles.
4. Commit the resolved file.

---

## Code Style

- Use 2-space or 4-space indentation consistently within a file.
- One sentence per line in `.tex` files — this makes diffs much cleaner.
- Use `\label{sec:name}` on every `\section` and `\subsection`.
- Use `\cite{key}` for all references; never hardcode author names as plain text.
- Remove `\lipsum` placeholder text before marking your section as done.

---

## Pull Request Checklist

Before submitting your PR, confirm:

- [ ] Branch is up to date with `main` (`git pull origin main`)
- [ ] LaTeX compiles locally without errors (`latexmk -pdf main.tex`)
- [ ] No placeholder `\lipsum` text remains
- [ ] All new citations are added to `references.bib`
- [ ] Figures are placed in the `figures/` subfolder
- [ ] Build artifacts (`.aux`, `.log`, etc.) are NOT committed (check `.gitignore`)
- [ ] Commit messages are descriptive

---

## Questions?

Open a GitHub Issue or reach out to the repository maintainer.
