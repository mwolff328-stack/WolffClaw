# SurvivorPulse Shared Design Token Specification
**Extracted from:** Back Tester (`/private/tmp/BackTesting-Prototype`)  
**Target:** Main App (`/tmp/SurvivorPulse`) + all future SurvivorPulse surfaces  
**Design System Version:** 1.0.0  
**Author:** Deb (Task 2.1 — Design Token Extraction)  
**Date:** 2026-04-28

---

## Overview

The Back Tester prototype has a fully implemented, production-quality design system (DESIGN.md + tailwind.config.ts + index.css). It is the canonical SurvivorPulse design system. The main app currently uses a divergent theme (lime-green `#AECC41` brand, light + dark modes, minimal token set). This document extracts all Back Tester tokens into a shared specification so the main app can be migrated to match.

**Design System Pillars:**
- Dark-mode-native only (`#08090a` canvas, luminance-stepped elevation)
- Inter Variable (UI) + JetBrains Mono (numeric data)
- Indigo-violet brand palette (replaces lime-green `#AECC41`)
- IBM Carbon status tokens (danger / success / warning / info)
- Semi-transparent white borders (no opaque dark borders)

---

## 1. Shared Tailwind Theme Extension

Drop this into any SurvivorPulse app's `tailwind.config.ts` under `theme.extend`. This is the single source of truth for all design tokens.

```typescript
// survivorpulse-theme.ts — import and spread into tailwind.config.ts theme.extend
// Usage: import { survivorpulseTheme } from './survivorpulse-theme'
// Then: theme: { extend: { ...survivorpulseTheme } }

export const survivorpulseTheme = {

  // ============================================================
  // FONT FAMILIES
  // Inter Variable (UI) + JetBrains Mono (numeric data)
  // OpenType features "cv01","ss03" applied globally in CSS
  // ============================================================
  fontFamily: {
    sans: [
      'Inter',
      'SF Pro Display',
      '-apple-system',
      'system-ui',
      'Segoe UI',
      'Roboto',
      'Helvetica Neue',
      'sans-serif',
    ],
    mono: [
      'JetBrains Mono',
      'ui-monospace',
      'SF Mono',
      'Menlo',
      'Monaco',
      'Consolas',
      'Liberation Mono',
      'monospace',
    ],
  },

  // ============================================================
  // FONT WEIGHTS
  // Linear discipline: 510 default emphasis, 590 max, never 700+
  // ============================================================
  fontWeight: {
    light:    '300',
    normal:   '400',
    ui:       '510',   // Linear signature weight — default emphasis
    medium:   '510',
    semibold: '590',   // Max weight — never exceed this
    bold:     '590',   // Alias — maps to semibold
  },

  // ============================================================
  // LETTER SPACING
  // Uppercase structural labels: positive tracking (Sentry pattern)
  // Display text: negative tracking (Linear pattern)
  // ============================================================
  letterSpacing: {
    structural: '0.08em',    // Column headers, section labels — UPPERCASE always
    label:      '0.04em',    // Pool tags, minor labels
    loose:      '0.06em',    // Week selector label, matrix headers
    tightest:   '-1.584px',  // 72px display
    tighter:    '-1.408px',  // 64px display
    tight:      '-1.056px',  // 48px display
    snug:       '-0.704px',  // 32px heading
    normal:     '0',
  },

  // ============================================================
  // COLORS
  // Canonical SurvivorPulse palette
  // ============================================================
  colors: {
    // --- shadcn semantic tokens (mapped to SP palette) ---
    // These bridge shadcn components to SP design without per-component overrides.
    // Values are HSL strings because shadcn components construct them with opacity modifiers.
    background: 'hsl(var(--background))',
    foreground: 'hsl(var(--foreground))',
    border:     'hsl(var(--border))',
    input:      'hsl(var(--input))',
    ring:       'hsl(var(--ring))',

    primary: {
      DEFAULT:    'hsl(var(--primary))',
      foreground: 'hsl(var(--primary-foreground))',
    },
    secondary: {
      DEFAULT:    'hsl(var(--secondary))',
      foreground: 'hsl(var(--secondary-foreground))',
    },
    muted: {
      DEFAULT:    'hsl(var(--muted))',
      foreground: 'hsl(var(--muted-foreground))',
    },
    accent: {
      DEFAULT:    'hsl(var(--accent))',
      foreground: 'hsl(var(--accent-foreground))',
    },
    destructive: {
      DEFAULT:    'hsl(var(--destructive))',
      foreground: 'hsl(var(--destructive-foreground))',
    },
    card: {
      DEFAULT:    'hsl(var(--card))',
      foreground: 'hsl(var(--card-foreground))',
    },
    popover: {
      DEFAULT:    'hsl(var(--popover))',
      foreground: 'hsl(var(--popover-foreground))',
    },

    // --- Canvas & surface elevation (Linear luminance model) ---
    canvas:   '#08090a',   // Deepest background — page canvas
    panel:    '#0f1011',   // Sidebar, nav panel, secondary areas
    elevated: '#191a1b',   // Cards, dropdowns, list containers

    surface: {
      overlay:   'rgba(255,255,255,0.02)',  // Card fill over dark bg
      hover:     'rgba(255,255,255,0.04)',  // Hover state fill
      active:    'rgba(255,255,255,0.05)',  // Active / selected fill
      secondary: '#28282c',                 // Lightest surface
    },

    // --- Text palette ---
    text: {
      primary:    '#f7f8f8',   // Headings, critical data — NOT pure white
      secondary:  '#d0d6e0',   // Body text, descriptions, standard cells
      tertiary:   '#8a8f98',   // Metadata, placeholders, de-emphasized
      quaternary: '#62666d',   // Timestamps, disabled, subtle labels
      inverse:    '#08090a',   // Text on light / colored backgrounds
    },

    // --- Brand: Linear indigo-violet ---
    brand: {
      DEFAULT: '#5e6ad2',   // Primary CTA backgrounds, brand marks
      accent:  '#7170ff',   // Interactive accents, links, active states
      hover:   '#828fff',   // Hover on accent elements
      muted:   '#7a7fad',   // Secondary brand, subtle elements
    },

    // --- Status colors: IBM Carbon naming ---
    // ONLY for entry health and risk communication — never for brand decoration.
    danger: {
      DEFAULT: '#da1e28',              // Carbon Red 60 — eliminated, critical
      subtle:  'rgba(218,30,40,0.15)', // Badge background
      border:  'rgba(218,30,40,0.3)',
      text:    '#ff8389',              // Carbon Red 30 — text on dark surface
    },
    success: {
      DEFAULT: '#24a148',              // Carbon Green 50 — safe, confirmed
      subtle:  'rgba(36,161,72,0.15)',
      border:  'rgba(36,161,72,0.3)',
      text:    '#6fdc8c',              // Carbon Green 30 — text on dark surface
    },
    warning: {
      DEFAULT: '#f1c21b',              // Carbon Yellow 30 — at-risk, deadline
      subtle:  'rgba(241,194,27,0.15)',
      border:  'rgba(241,194,27,0.3)',
      text:    '#f1c21b',              // Same hue — sufficient contrast on dark
    },
    info: {
      DEFAULT: '#0f62fe',              // Carbon Blue 60 — pool metadata, neutral
      subtle:  'rgba(15,98,254,0.15)',
      border:  'rgba(15,98,254,0.3)',
      text:    '#78a9ff',              // Carbon Blue 40 — text on dark surface
    },

    // --- Borders ---
    'border-subtle':   'rgba(255,255,255,0.05)',  // Whisper-thin, card edges
    'border-standard': 'rgba(255,255,255,0.08)',  // Standard cards, inputs
    'border-emphasis': '#23252a',                  // Prominent separations
    'border-strong':   '#34343a',                  // High-contrast separators
  },

  // ============================================================
  // BORDER RADIUS
  // ============================================================
  borderRadius: {
    xs:      '2px',
    sm:      '4px',
    DEFAULT: '6px',
    md:      '6px',
    lg:      'var(--radius)',   // 8px via CSS variable
    xl:      '12px',
    full:    '9999px',
  },

  // ============================================================
  // SPACING (8px base)
  // Named tokens alongside standard Tailwind scale
  // ============================================================
  spacing: {
    'sp-1':  '4px',    // Micro gaps, icon-to-text
    'sp-2':  '8px',    // Base unit — tight component spacing
    'sp-3':  '12px',   // Compact padding
    'sp-4':  '16px',   // Standard padding (cards, panels)
    'sp-5':  '20px',   // Comfortable section spacing
    'sp-6':  '24px',   // Panel padding, generous spacing
    'sp-8':  '32px',   // Section breaks
    'sp-10': '40px',   // Major section separation
    'sp-12': '48px',   // Large section padding
  },

  // ============================================================
  // BOX SHADOW (dark surface model)
  // Luminance-based elevation, not shadow depth
  // ============================================================
  boxShadow: {
    'sp-xs':     'rgba(0,0,0,0.03) 0px 1.2px 0px',                        // Micro-elevation (toolbar)
    'sp-sm':     'rgba(0,0,0,0.2) 0px 0px 0px 1px',                       // Standard card
    'sp-inset':  'rgba(0,0,0,0.2) 0px 0px 12px 0px inset',                // Sunken panel
    'sp-md':     'rgba(0,0,0,0.4) 0px 2px 4px',                           // Floating elements
    'sp-dialog': 'rgba(0,0,0,0.4) 0px 8px 32px, rgba(0,0,0,0.2) 0px 2px 8px, rgba(0,0,0,0.08) 0px 0px 1px', // Dialog/modal/command palette
    'sp-focus':  'rgba(0,0,0,0.1) 0px 4px 12px, 0 0 0 2px rgba(94,106,210,0.5)', // Focus ring
  },

  // ============================================================
  // MOTION
  // Fast, subtle. No bounce or spring.
  // ============================================================
  transitionDuration: {
    '75':  '75ms',
    '150': '150ms',
    '200': '200ms',
  },
  transitionTimingFunction: {
    'ui': 'cubic-bezier(0.16, 1, 0.3, 1)',   // Ease-out snappy — all UI transitions
  },
}
```

---

## 2. CSS Custom Properties (Non-Tailwind Fallback)

For contexts that don't use Tailwind (email templates, third-party embeds, server-rendered pages), paste this `<style>` block. All tokens are prefixed `--sp-` to avoid collisions.

```css
/* SurvivorPulse Design Tokens v1.0.0 — CSS Custom Properties */
/* Dark-mode-native. No light theme variables defined. */
/* Prefix: --sp- */

:root {
  /* =============================================
     CANVAS & SURFACE ELEVATION
     Linear luminance model — elevation via lightness steps, not shadow
     ============================================= */
  --sp-canvas:            #08090a;                  /* Page background */
  --sp-panel:             #0f1011;                  /* Sidebar, nav */
  --sp-elevated:          #191a1b;                  /* Cards, dropdowns */
  --sp-surface-overlay:   rgba(255,255,255,0.02);   /* Card fill */
  --sp-surface-hover:     rgba(255,255,255,0.04);   /* Hover fill */
  --sp-surface-active:    rgba(255,255,255,0.05);   /* Selected fill */
  --sp-surface-secondary: #28282c;                  /* Lightest surface */

  /* =============================================
     TEXT
     ============================================= */
  --sp-text-primary:    #f7f8f8;   /* Headings, critical data */
  --sp-text-secondary:  #d0d6e0;   /* Body, descriptions, cells */
  --sp-text-tertiary:   #8a8f98;   /* Metadata, placeholders */
  --sp-text-quaternary: #62666d;   /* Timestamps, disabled */
  --sp-text-inverse:    #08090a;   /* Text on colored backgrounds */

  /* =============================================
     BRAND (Linear indigo-violet)
     ============================================= */
  --sp-brand-primary: #5e6ad2;   /* CTA backgrounds */
  --sp-brand-accent:  #7170ff;   /* Links, interactive, active */
  --sp-brand-hover:   #828fff;   /* Hover on accent elements */
  --sp-brand-muted:   #7a7fad;   /* Secondary brand elements */

  /* =============================================
     STATUS — IBM Carbon naming
     danger / success / warning / info
     NEVER use for brand decoration
     ============================================= */
  --sp-danger:          #da1e28;            /* Carbon Red 60 */
  --sp-danger-subtle:   rgba(218,30,40,0.15);
  --sp-danger-border:   rgba(218,30,40,0.3);
  --sp-danger-text:     #ff8389;            /* Carbon Red 30 */

  --sp-success:         #24a148;            /* Carbon Green 50 */
  --sp-success-subtle:  rgba(36,161,72,0.15);
  --sp-success-border:  rgba(36,161,72,0.3);
  --sp-success-text:    #6fdc8c;            /* Carbon Green 30 */

  --sp-warning:         #f1c21b;            /* Carbon Yellow 30 */
  --sp-warning-subtle:  rgba(241,194,27,0.15);
  --sp-warning-border:  rgba(241,194,27,0.3);
  --sp-warning-text:    #f1c21b;

  --sp-info:            #0f62fe;            /* Carbon Blue 60 */
  --sp-info-subtle:     rgba(15,98,254,0.15);
  --sp-info-border:     rgba(15,98,254,0.3);
  --sp-info-text:       #78a9ff;            /* Carbon Blue 40 */

  /* =============================================
     BORDERS & DIVIDERS
     Semi-transparent white — never opaque dark borders
     ============================================= */
  --sp-border-subtle:    rgba(255,255,255,0.05);   /* Whisper-thin */
  --sp-border-standard:  rgba(255,255,255,0.08);   /* Cards, inputs */
  --sp-border-emphasis:  #23252a;                   /* Prominent separations */
  --sp-border-strong:    #34343a;                   /* High contrast */

  /* =============================================
     OVERLAYS
     ============================================= */
  --sp-overlay-modal:   rgba(0,0,0,0.85);   /* Dialog backdrop */
  --sp-overlay-tooltip: rgba(0,0,0,0.95);   /* Tooltip background */

  /* =============================================
     SPACING (8px base)
     ============================================= */
  --sp-space-1:  4px;
  --sp-space-2:  8px;
  --sp-space-3:  12px;
  --sp-space-4:  16px;
  --sp-space-5:  20px;
  --sp-space-6:  24px;
  --sp-space-8:  32px;
  --sp-space-10: 40px;
  --sp-space-12: 48px;

  /* =============================================
     BORDER RADIUS
     ============================================= */
  --sp-radius-xs:   2px;     /* Inline badges, toolbar buttons */
  --sp-radius-sm:   4px;     /* Small containers */
  --sp-radius-md:   6px;     /* Buttons, inputs */
  --sp-radius-lg:   8px;     /* Cards, dropdowns */
  --sp-radius-xl:   12px;    /* Featured panels, modals */
  --sp-radius-full: 9999px;  /* Status badges, filter chips */

  /* =============================================
     SHADCN BRIDGE VARIABLES (HSL)
     Maps SP palette to shadcn's expected variable names.
     shadcn constructs colors as: hsl(var(--background) / <alpha>)
     ============================================= */
  --background: 240 12% 4%;             /* #08090a */
  --foreground: 210 14% 97%;            /* #f7f8f8 */
  --card: 240 8% 7%;                    /* ~#0f1011 */
  --card-foreground: 213 22% 88%;       /* #d0d6e0 */
  --popover: 240 6% 11%;               /* #191a1b */
  --popover-foreground: 213 22% 88%;
  --primary: 233 47% 58%;              /* #5e6ad2 */
  --primary-foreground: 0 0% 100%;
  --secondary: 240 5% 16%;             /* #28282c */
  --secondary-foreground: 213 22% 88%;
  --muted: 240 5% 16%;
  --muted-foreground: 220 5% 56%;      /* #8a8f98 */
  --accent: 240 100% 72%;              /* #7170ff */
  --accent-foreground: 0 0% 100%;
  --destructive: 355 75% 47%;          /* #da1e28 */
  --destructive-foreground: 0 82% 76%; /* #ff8389 */
  --border: 228 7% 15%;                /* ~#23252a solid fallback */
  --input: 240 6% 11%;                 /* #191a1b */
  --ring: 237 60% 57%;                 /* #5e6ad2 focus ring */
  --radius: 0.5rem;                    /* 8px = --sp-radius-lg */
}
```

---

## 3. Typography Scale

### Font Families

| Role | Font | Fallbacks |
|------|------|-----------|
| UI / Reading | Inter Variable | SF Pro Display, -apple-system, system-ui, Segoe UI, Roboto, Helvetica Neue |
| Numeric / Data | JetBrains Mono | ui-monospace, SF Mono, Menlo, Monaco, Consolas |

**Critical:** Both fonts must load. Without JetBrains Mono, numeric columns lose tabular alignment. Without Inter Variable, OpenType features (`cv01`, `ss03`) that define the Linear aesthetic are unavailable.

**Google Fonts import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap');
```

**Global OpenType (mandatory):**
```css
body {
  font-feature-settings: "cv01", "ss03";  /* Single-story 'a' + geometric alternates */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### Dashboard Type Scale

| Role | Font | Size | Weight | Line Height | Letter Spacing | Transform | Color Token |
|------|------|------|--------|-------------|----------------|-----------|-------------|
| Page Title | Inter Variable | 24px | 510 | 1.25 | -0.288px | — | `--sp-text-primary` |
| Panel Header | Inter Variable | 18px | 590 | 1.33 | -0.165px | — | `--sp-text-primary` |
| Section Label | Inter Variable | 11px | 590 | 1.40 | 0.08em | UPPERCASE | `--sp-text-tertiary` |
| Table Header | Inter Variable | 11px | 590 | 1.40 | 0.08em | UPPERCASE | `--sp-text-tertiary` |
| Body | Inter Variable | 15px | 400 | 1.60 | -0.165px | — | `--sp-text-secondary` |
| Body Medium | Inter Variable | 15px | 510 | 1.60 | -0.165px | — | `--sp-text-secondary` |
| Body Semibold | Inter Variable | 15px | 590 | 1.60 | -0.165px | — | `--sp-text-primary` |
| UI Label | Inter Variable | 13px | 510 | 1.50 | -0.13px | — | `--sp-text-secondary` |
| Caption | Inter Variable | 12px | 400 | 1.40 | normal | — | `--sp-text-tertiary` |
| Caption Medium | Inter Variable | 12px | 510 | 1.40 | normal | — | `--sp-text-tertiary` |
| Micro | Inter Variable | 11px | 510 | 1.40 | normal | — | `--sp-text-tertiary` |
| Data Cell | JetBrains Mono | 13px | 400 | 1.50 | normal | — | `--sp-text-primary` |
| Data Header | JetBrains Mono | 12px | 600 | 1.40 | 0.04em | — | `--sp-text-tertiary` |
| Data Large | JetBrains Mono | 16px | 400 | 1.50 | normal | — | `--sp-text-primary` |
| Data XL | JetBrains Mono | 24px | 400 | 1.25 | -0.5px | — | `--sp-text-primary` |

**Key rules:**
- Weight 510 is the default emphasis weight (between regular and medium)
- Max weight is 590 — never use 700+
- Never use pure white `#ffffff` for text — use `#f7f8f8`
- Uppercase labels MUST pair with `letter-spacing: 0.08em`

---

## 4. Color Palette Reference

### Canvas & Surface (luminance elevation)

| Token | Value | Use |
|-------|-------|-----|
| `--sp-canvas` | `#08090a` | Page background |
| `--sp-panel` | `#0f1011` | Sidebar, nav panel |
| `--sp-elevated` | `#191a1b` | Cards, dropdowns |
| `--sp-surface-overlay` | `rgba(255,255,255,0.02)` | Card fill |
| `--sp-surface-hover` | `rgba(255,255,255,0.04)` | Hover fill |
| `--sp-surface-active` | `rgba(255,255,255,0.05)` | Selected fill |
| `--sp-surface-secondary` | `#28282c` | Lightest surface |

### Text

| Token | Value | Use |
|-------|-------|-----|
| `--sp-text-primary` | `#f7f8f8` | Headings, critical data |
| `--sp-text-secondary` | `#d0d6e0` | Body, descriptions |
| `--sp-text-tertiary` | `#8a8f98` | Metadata, placeholders |
| `--sp-text-quaternary` | `#62666d` | Timestamps, disabled |
| `--sp-text-inverse` | `#08090a` | On colored backgrounds |

### Brand

| Token | Value | Use |
|-------|-------|-----|
| `--sp-brand-primary` | `#5e6ad2` | CTA backgrounds |
| `--sp-brand-accent` | `#7170ff` | Links, interactive |
| `--sp-brand-hover` | `#828fff` | Hover on accent |
| `--sp-brand-muted` | `#7a7fad` | Subtle brand elements |

### Status (IBM Carbon)

| State | Base | Subtle BG | Border | Text |
|-------|------|-----------|--------|------|
| Danger | `#da1e28` | `rgba(218,30,40,0.15)` | `rgba(218,30,40,0.3)` | `#ff8389` |
| Success | `#24a148` | `rgba(36,161,72,0.15)` | `rgba(36,161,72,0.3)` | `#6fdc8c` |
| Warning | `#f1c21b` | `rgba(241,194,27,0.15)` | `rgba(241,194,27,0.3)` | `#f1c21b` |
| Info | `#0f62fe` | `rgba(15,98,254,0.15)` | `rgba(15,98,254,0.3)` | `#78a9ff` |

### Borders

| Token | Value | Use |
|-------|-------|-----|
| `--sp-border-subtle` | `rgba(255,255,255,0.05)` | Whisper-thin, card edges |
| `--sp-border-standard` | `rgba(255,255,255,0.08)` | Standard cards, inputs |
| `--sp-border-emphasis` | `#23252a` | Prominent separations |
| `--sp-border-strong` | `#34343a` | High-contrast separators |

---

## 5. Spacing & Radius Scale

### Spacing (8px base)

| Token | CSS Var | Value | Use |
|-------|---------|-------|-----|
| `sp-1` | `--sp-space-1` | 4px | Micro gaps, icon-to-text |
| `sp-2` | `--sp-space-2` | 8px | Base unit, tight component spacing |
| `sp-3` | `--sp-space-3` | 12px | Compact padding |
| `sp-4` | `--sp-space-4` | 16px | Standard padding (cards, panels) |
| `sp-5` | `--sp-space-5` | 20px | Comfortable section spacing |
| `sp-6` | `--sp-space-6` | 24px | Panel padding, generous spacing |
| `sp-8` | `--sp-space-8` | 32px | Section breaks |
| `sp-10` | `--sp-space-10` | 40px | Major section separation |
| `sp-12` | `--sp-space-12` | 48px | Large section padding |

### Border Radius

| Token | CSS Var | Value | Use |
|-------|---------|-------|-----|
| `rounded-xs` | `--sp-radius-xs` | 2px | Inline badges, toolbar buttons |
| `rounded-sm` | `--sp-radius-sm` | 4px | Small containers |
| `rounded` / `rounded-md` | `--sp-radius-md` | 6px | Buttons, inputs |
| `rounded-lg` | `--sp-radius-lg` | 8px | Cards, dropdowns |
| `rounded-xl` | `--sp-radius-xl` | 12px | Featured panels, modals |
| `rounded-full` | `--sp-radius-full` | 9999px | Status badges |

---

## 6. Elevation & Motion

### Shadow Levels

| Token | Shadow | Use |
|-------|--------|-----|
| `sp-xs` | `rgba(0,0,0,0.03) 0px 1.2px 0px` | Micro-elevation (toolbar buttons) |
| `sp-sm` | `rgba(0,0,0,0.2) 0px 0px 0px 1px` | Standard card elevation |
| `sp-inset` | `rgba(0,0,0,0.2) 0px 0px 12px 0px inset` | Sunken panels |
| `sp-md` | `rgba(0,0,0,0.4) 0px 2px 4px` | Floating elements |
| `sp-dialog` | multi-layer (see CSS) | Dialogs, command palette, modals |
| `sp-focus` | brand ring + blur | Focus states |

### Motion

All UI transitions use:
- **Duration:** 150ms (hover state changes), 75ms (micro interactions), 200ms (panel transitions)
- **Easing:** `cubic-bezier(0.16, 1, 0.3, 1)` (ease-out snappy — Tailwind token: `ease-ui`)
- **No spring / bounce / elastic** — this is an analytical tool, not a consumer app

---

## 7. Token Mapping: Back Tester → Main App Elements

| Back Tester Usage | Back Tester Token | Main App Element | Current Main App Value | Action |
|-------------------|-------------------|------------------|------------------------|--------|
| Page canvas | `--sp-canvas` (#08090a) | `body` background | `#0C1017` dark / `hsl(210,40%,98%)` light | Replace with `#08090a`, remove light mode |
| Sidebar / nav panel | `--sp-panel` (#0f1011) | `--sidebar` var | `hsl(228,9.8%,10%)` | Replace with `#0f1011` |
| Cards | `--sp-elevated` / surface-overlay | `--card` | `hsl(228,9.8%,10%)` | Update to `#191a1b` |
| Primary CTA | `--sp-brand-primary` (#5e6ad2) | `--primary` | `#AECC41` (lime-green) | **Replace** — this is the largest visual change |
| Interactive accent | `--sp-brand-accent` (#7170ff) | `--accent` | `#AECC41` | **Replace** |
| Focus ring | `--sp-brand-primary` @ 50% | `--ring` | `#AECC41` | **Replace** |
| Body text | `--sp-text-secondary` (#d0d6e0) | `--foreground` | `hsl(200,6.7%,91.2%)` | Close — fine-tune to `#d0d6e0` |
| Muted text | `--sp-text-tertiary` (#8a8f98) | `--muted-foreground` | `#9CA3AF` | Update to `#8a8f98` |
| Subtle text | `--sp-text-quaternary` (#62666d) | No mapping exists | — | Add as `--sp-text-quaternary` |
| Standard border | `--sp-border-standard` | `--border` | `hsl(210,5.3%,14.9%)` | Replace with `rgba(255,255,255,0.08)` |
| Sidebar border | `--sp-border-subtle` | `--sidebar-border` | `hsl(205.7,15.8%,26.1%)` | Replace with `rgba(255,255,255,0.05)` |
| Danger state | `--sp-danger` (#da1e28) | `--destructive` | `hsl(356.3,90.6%,54.3%)` | Update to `#da1e28` |
| Sans font | Inter Variable | `--font-sans` | Inter (no variable font spec) | Update to Inter Variable with `opsz,wght` range |
| Mono font | JetBrains Mono | `--font-mono` | Menlo | **Add** JetBrains Mono |
| Data cells | `.data-cell` class | Not implemented | — | **Add** class with JetBrains Mono |
| Structural labels | `.label-structural` class | Not implemented | — | **Add** class (uppercase + tracking) |
| Status badges | `.badge-*` classes | Not implemented | — | **Add** all badge classes |
| Chart colors | N/A | `--chart-1..5` | Lime/teal/yellow/purple/pink | Update to brand + status palette |
| Sidebar accent bg | `--sp-surface-active` | `--sidebar-accent` | `hsl(205.7,70%,7.8%)` | Replace with `rgba(255,255,255,0.05)` |
| Sidebar accent text | `--sp-brand-accent` | `--sidebar-accent-foreground` | `#AECC41` | **Replace** with `#7170ff` |

---

## 8. shadcn/ui Theming Notes

### What Works via Tailwind Config (no per-component overrides needed)

- **Color tokens** (`background`, `foreground`, `primary`, `secondary`, etc.) — shadcn reads these from CSS variables. Updating the CSS variables + Tailwind config mapping is sufficient for all shadcn components to adopt SP colors automatically.
- **Border radius** — shadcn uses `--radius` CSS variable. Set to `0.5rem` (8px = `--sp-radius-lg`). This flows into Button, Card, Input, Badge, etc.
- **Font family** — shadcn inherits from `body`. Setting `--font-sans` to Inter Variable propagates automatically.
- **Destructive variant** — maps to `--destructive` / `--destructive-foreground`. Updating these changes all destructive Buttons and alerts.
- **Muted / Accent variants** — similarly auto-propagate.

### What Needs Per-Component Overrides or Custom Classes

| Component | Issue | Resolution |
|-----------|-------|------------|
| shadcn `Button` (default variant) | Uses `--secondary` bg — will be `#28282c`. Acceptable for SP. | No override needed if OK with darker ghost. |
| shadcn `Badge` | Generic colors, not SP IBM Carbon status tokens | Use custom `.badge-live`, `.badge-safe`, `.badge-at-risk`, `.badge-eliminated`, `.badge-pending` classes instead |
| shadcn `Table` | Plain styling, no mono numeric columns | Use `.sp-table` class wrapper or override `.sp-table th` / `.sp-table td.numeric` |
| shadcn `Input` | Will pick up `--border` and `--ring`. Focus ring color inherits from `--ring`. | Set `--ring` to `#5e6ad2` HSL value — no per-component override needed |
| shadcn `Card` | Background uses `--card`. | Set `--card` to SP elevated surface HSL — no override needed |
| shadcn `Popover` / `DropdownMenu` | Background from `--popover`. | Set `--popover` to `240 6% 11%` (#191a1b) — correct |
| shadcn `Dialog` | Needs multi-layer shadow (`sp-dialog`) | Add `shadow-sp-dialog` class to `DialogContent` |
| Nav / Sidebar | Not a shadcn component — SP builds custom | Use `.sp-panel`, border `--sp-border-subtle` |
| Typography (`@tailwindcss/typography`) | Has its own color palette (prose-*) | Add `prose-invert` class and override `--tw-prose-*` variables to match SP palette |

### shadcn Dark Mode Setup

shadcn expects either `:root` (always dark) or `.dark :root` (toggleable). SurvivorPulse is dark-only, so:

```css
/* Put all shadcn HSL vars in :root — no .dark variant needed */
:root {
  --background: 240 12% 4%;
  /* ... all SP values ... */
}

/* No .dark { } block — we are always dark */
```

Remove the `.dark` block from the main app's `index.css` entirely.

### Chart Color Recommendations for Main App

The main app has `--chart-1..5` using lime-green as chart-1. Post-migration:

```css
--chart-1: 240 100% 72%;   /* #7170ff — brand accent (primary series) */
--chart-2: 137 61% 53%;    /* #6fdc8c — success green */
--chart-3: 43 86% 54%;     /* #f1c21b — warning yellow */
--chart-4: 0 82% 76%;      /* #ff8389 — danger red */
--chart-5: 220 100% 73%;   /* #78a9ff — info blue */
```

---

## 9. Migration Path: Main App → SP Design System

### Phase 1: CSS Variable Swap (lowest risk, highest visual impact)

1. Replace `client/src/index.css` `:root` and `.dark` blocks with the CSS Custom Properties from Section 2 above
2. Remove the `.dark` block entirely (SP is dark-only)
3. Remove `--color-brand-primary: #AECC41` and related custom color vars
4. Result: all shadcn components instantly adopt SP colors

**Files changed:** `client/src/index.css` only

### Phase 2: Tailwind Config Update

1. Replace `tailwind.config.ts` `theme.extend` with the shared `survivorpulseTheme` from Section 1
2. Add `fontWeight`, `letterSpacing`, `spacing`, `boxShadow`, `transitionDuration`, `transitionTimingFunction`
3. Update `fontFamily.mono` to JetBrains Mono
4. Keep existing `keyframes` (accordion) — SP theme doesn't conflict

**Files changed:** `tailwind.config.ts`

### Phase 3: Global Base Styles

Add to `client/src/index.css` `@layer base`:

```css
body {
  font-feature-settings: "cv01", "ss03";
  font-size: 15px;
  line-height: 1.6;
  color: var(--sp-text-secondary);
  background-color: var(--sp-canvas);
}
```

### Phase 4: Add SP Utility Classes

Copy the `@layer components` block from the Back Tester's `index.css` verbatim:
- `.label-structural`
- `.data-cell` / `.data-cell-muted`
- `.sp-card` / `.sp-card-featured`
- `.badge-live` / `.badge-safe` / `.badge-at-risk` / `.badge-eliminated` / `.badge-pending`
- `.sp-table` / `.sp-table-sticky`
- `.btn-ghost` / `.btn-toolbar`
- `.entry-card` (and variants)

### Phase 5: Font Loading

Add to `client/index.html` `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap" rel="stylesheet">
```

Remove any existing Google Fonts imports from `index.css` (move to HTML for performance).

### Phase 6: Component Audit

Audit all components that currently use `#AECC41` directly in JSX/TSX:
- Hard-coded lime-green in `className` → replace with `brand` or `accent` Tailwind tokens
- Hard-coded lime-green in `style` props → replace with CSS variable references
- Tailwind `text-[#AECC41]` / `bg-[#AECC41]` arbitrary values → replace with `text-brand` / `bg-brand`

---

## 10. Quick Token Cheat Sheet

```
Canvas:         #08090a     --sp-canvas
Panel:          #0f1011     --sp-panel
Elevated:       #191a1b     --sp-elevated
Hover fill:     rgba(255,255,255,0.04)

Text primary:   #f7f8f8     --sp-text-primary
Text body:      #d0d6e0     --sp-text-secondary
Text muted:     #8a8f98     --sp-text-tertiary
Text subtle:    #62666d     --sp-text-quaternary

Brand:          #5e6ad2     --sp-brand-primary
Accent:         #7170ff     --sp-brand-accent
Accent hover:   #828fff     --sp-brand-hover

Danger:         #da1e28 / text #ff8389
Success:        #24a148 / text #6fdc8c
Warning:        #f1c21b / text #f1c21b
Info:           #0f62fe / text #78a9ff

Border:         rgba(255,255,255,0.08)
Border subtle:  rgba(255,255,255,0.05)

Font UI:        Inter Variable, "cv01" "ss03"
Font Data:      JetBrains Mono, tabular-nums
Weight default: 510 (ui)
Weight max:     590 (semibold)
```

---

*Produced by Deb the Designer — Task 2.1: Design Token Extraction*  
*Source of truth: `/private/tmp/BackTesting-Prototype/DESIGN.md` + `tailwind.config.ts` + `src/index.css`*
