# Terminal Profile Design System

This document outlines the strict visual language, typography, color palette, dimensions, and animation principles required to generate the SVGs for the premium Linux terminal GitHub Profile. Every generator must adhere to these rules to maintain a cohesive, high-quality aesthetic.

---

## 1. Core Visual Language

The profile mimics a real Linux terminal window. The design must feel authentic, minimalist, and highly structured, avoiding cluttered layouts. It relies strictly on typography, precise spacing, and subtle motion to convey a premium "developer" feel.

### Terminal Window Anatomy
- **Background**: Solid color (no gradients).
- **Window Chrome (Header)**: Minimalist MacOS/Linux style.
  - Height: `32px`
  - Controls: Three circular dots (Close, Minimize, Maximize) aligned to the top-left.
    - Radius: `6px`
    - Spacing: `8px` between dots.
- **Border**: A subtle 1px border surrounds the terminal window to separate it from the GitHub background.
- **Border Radius**: `8px` for all terminal SVG canvases.

---

## 2. Color Palette (GitHub Dark)

The system enforces a strict implementation of the GitHub Dark color palette.

| Token | Hex Code | Usage |
| :--- | :--- | :--- |
| `background_default` | `#0d1117` | Main terminal background. |
| `background_header` | `#161b22` | Terminal window top header bar. |
| `border_subtle` | `#30363d` | 1px borders around SVGs, dividers, or panels. |
| `text_primary` | `#c9d1d9` | Standard text, stdout, file contents. |
| `text_secondary` | `#8b949e` | Timestamps, comments, inactive elements. |
| `accent_blue` | `#58a6ff` | Links, primary highlights, directory names. |
| `accent_green` | `#3fb950` | Success messages, strings, additions. |
| `accent_red` | `#f85149` | Window close button, errors, deletions. |
| `accent_yellow` | `#d29922` | Window minimize button, warnings. |
| `accent_purple` | `#bc8cff` | Keywords, special variables. |

*(The Maximize button in the header should use `#3fb950` or `#2ea043`)*

---

## 3. Typography System

The exclusive typeface for the entire project is **JetBrains Mono**. It provides an authentic coding environment aesthetic with excellent legibility.

- **Font Family**: `'JetBrains Mono', monospace`
- **Base Font Size**: `14px`
- **Line Height**: `1.5` (21px)
- **Weights**:
  - `Regular (400)`: Body text, standard output.
  - `Bold (700)`: Terminal prompts, headings, key metrics.

---

## 4. Spatial System

The design utilizes a strict **8pt grid system** to ensure mathematical rhythm and consistency across all generators.

| Variable | Value | Usage |
| :--- | :--- | :--- |
| `spacing_xs` | `4px` | Inner-element spacing (e.g., gap between prompt and cursor). |
| `spacing_sm` | `8px` | Small gaps, list items. |
| `spacing_md` | `16px` | Standard margin between paragraphs/blocks. |
| `spacing_lg` | `24px` | Padding inside terminal panels. |
| `spacing_xl` | `32px` | Vertical spacing between major sections. |

**Standard Padding**: All terminal windows have a standard inner padding of `24px` (`spacing_lg`) on the left, right, and bottom. The top padding must account for the `32px` window header.

---

## 5. Standardized Dimensions

To ensure SVGs align perfectly on a GitHub profile, their dimensions are strictly standardized. 

| Component | Width (px) | Height (px) | Description |
| :--- | :--- | :--- | :--- |
| **ASCII Portrait** | `400` | `320` | Left-aligned, displays the animated face. |
| **Fastfetch Card** | `400` | `320` | Right-aligned, displays system/user specs. |
| **Skills Panel** | `820` | `280` | Full width, categorizes the tech stack. |
| **Contribution Graph** | `820` | `220` | Full width, GitHub-style heatmap rendering. |
| **Project Cards** | `820` | `400` | Full width, displays featured repositories. |

*(Note: Widths of 820px allow for side-by-side 400px SVGs with a 20px gap in the Markdown file.)*

---

## 6. Terminal Prompts

To simulate a real developer environment, every profile section is introduced via a terminal prompt command. The syntax highlights the user context (`om@github`).

- **Prompt Color Coding**:
  - `om@github`: `accent_green` (`#3fb950`)
  - `:`: `text_primary` (`#c9d1d9`)
  - `~$`: `accent_blue` (`#58a6ff`)
  - `[Command]`: `text_primary` (`#c9d1d9`)

**Section Commands**:
1. **Boot/Init**: `om@github:~$ ./boot.sh`
2. **System Info**: `om@github:~$ fastfetch`
3. **Projects**: `om@github:~$ ls projects/`
4. **Skills**: `om@github:~$ cat skills.json`
5. **Achievements**: `om@github:~$ achievements`
6. **Contact**: `om@github:~$ contact --all`

---

## 7. Animation Principles

Animations bring the terminal to life but must remain subtle and professional. Over-animation looks chaotic; motion must feel mechanical, snappy, and intentional.

- **Easing**: `cubic-bezier(0.4, 0.0, 0.2, 1)` (Standard ease-in-out)
- **Base Duration**: `300ms` for standard fades/slides.

### Core Effects:
1. **Typing Effect (`typing`)**: 
   - Used for the terminal prompts.
   - Text is revealed character by character using `stroke-dashoffset` or discrete CSS steps.
   - Speed: `~50ms` per character.
2. **Blinking Cursor (`cursor`)**:
   - A solid block (`█`) appended to the current active line.
   - Animation: `opacity 1 -> 0 -> 1`
   - Duration: `1000ms` infinite loop.
3. **Fade In (`fade`)**:
   - Used for standard output (stdout) appearing after a command is typed.
   - Duration: `400ms`.
4. **Slide Up & Fade (`slide`)**:
   - Used for lists, project cards, and skill items to create a cascading entrance.
   - Transform: `translateY(10px) -> translateY(0)`
   - Duration: `400ms`.
5. **Staggered Delays (`stagger`)**:
   - Items in a list (e.g., skills, projects) must not appear simultaneously.
   - Delay multiplier: `100ms` per index item.

### Orchestration Timing
1. `0ms - 1500ms`: Type the prompt command.
2. `1500ms - 1700ms`: Pause (simulating enter key press).
3. `1700ms +`: Fade/Slide in the command output.
4. `(End of render)`: Leave the blinking cursor on a new empty prompt line.

---

## 8. Icon Usage

- Use **Nerd Fonts** / Devicons representations where possible (e.g., Python logo, React logo).
- Icons should generally adopt the color of their respective brand, but desaturated slightly to fit the GitHub Dark aesthetic, OR be monochromatic (`text_secondary`).
- Icon size: `16px` by `16px`, vertically aligned with text.

---

### End of Document
*This design system guarantees that all modular SVGs will assemble into a cohesive, high-end profile.*
