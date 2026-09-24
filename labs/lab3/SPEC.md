# SPEC: Developer Portfolio Welcome Page

## 1. Purpose & Scope
- A personal portfolio welcome page for Kurt Schillinger, a software engineering student.
- Non-Goals: no multi-page routing; no backend; no contact forms.

## 2. Invariants & Negative Constraints
- All styling MUST reside in `./style.css` (no inline style="..." attributes).
- The page MUST NOT load external CSS frameworks or CDNs (no Bootstrap, no Tailwind).
- The avatar image MUST use the relative path `./assets/avatar.jpg`.
- The layout MUST collapse into a single vertical column on screens narrower than 768px.

## 3. UI Content & Interface Contract
- Hero header: my full name "Kurt Schillinger", the subtitle "Software Engineering Student", and this bio: "Passionate about software development and web applications. Currently building hands-on projects and exploring modern developer tools."
- Action link: a button labelled "See my projects" that links to `#projects`.
- Projects section with id="projects": lists these items:
  - Music Discovery App: A Tinder-style swipe interface for discovering songs and curating playlists.
  - Personal Portfolio: A responsive web portfolio built from a strict Markdown specification.
- Social link: GitHub (https://github.com/kschillinger28-source) MUST open in a new tab (target="_blank").

- The page background MUST be dark navy (#1b2a41) with white text.

## 4. Acceptance Checklist
- [x] Valid semantic HTML5: the page uses <header>, <main>, and <footer>.
- [x] The avatar image has width, height, and alt attributes.
- [x] No horizontal scrollbar when the browser is narrowed to 375px.
- [x] The GitHub link opens in a new tab and has rel="noopener".
- [x] No placeholder links: href="#" appears nowhere.

## 5. Audit Protocol
- Inspect the generated code line by line with `git diff --staged` before committing.