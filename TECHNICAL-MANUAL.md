# Pinr Website — Technical Manual

**URL:** https://getpinr.com
**Repository:** https://github.com/builtbylee/pinr-website
**Branch:** `main`
**Last updated:** February 2025

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [File Structure](#2-file-structure)
3. [Design System](#3-design-system)
4. [Section-by-Section Breakdown](#4-section-by-section-breakdown)
5. [3D Globe (Three.js)](#5-3d-globe-threejs)
6. [Animations & Interactions](#6-animations--interactions)
7. [JavaScript Architecture](#7-javascript-architecture)
8. [Responsive Breakpoints](#8-responsive-breakpoints)
9. [External Dependencies](#9-external-dependencies)
10. [Deployment](#10-deployment)

---

## 1. Architecture Overview

The landing page is a **single-file HTML application** (`mockup5.html`) with all CSS and JavaScript inlined. There are no build tools, bundlers, or frameworks — the site is purely static and served via GitHub Pages.

**Key architectural decisions:**
- All CSS is in a single `<style>` block in `<head>`
- Main JavaScript is in a `<script>` block at the end of `<body>`
- The Three.js 3D globe uses a separate `<script type="module">` for ES module imports
- No external CSS frameworks (custom-built design system)
- `index.html` is always an exact copy of `mockup5.html` (the live deployment file)

**Design style:** Immersive Parallax — premium white backgrounds, dark navy primary, sky blue accents, wave dividers between sections, scroll-linked animations.

---

## 2. File Structure

```
pinr-website/
├── index.html              # Live deployment (copy of mockup5.html)
├── mockup5.html            # Primary working file (~2,985 lines)
├── mockup1.html            # Archive: Dark Cinematic mockup
├── mockup2.html            # Archive: Light Airy mockup
├── mockup3.html            # Archive: Bold Colorful mockup
├── mockup4.html            # Archive: Minimal Elegant mockup
├── mockups.html            # Mockup gallery/selector page
├── faq.html                # FAQ page
├── privacy-policy.html     # Privacy policy
├── terms-of-service.html   # Terms of service
├── pin.html                # Pin share flow mockup
├── share-flow-mockup.html  # Share flow mockup
├── CNAME                   # Custom domain: getpinr.com
├── .nojekyll               # Disables Jekyll processing on GitHub Pages
├── favicon.png             # Original favicon
├── favicon-v2.png          # Favicon v2
├── favicon-v3.png          # Favicon v3
├── favicon-v4.png          # Current favicon (referenced in HTML)
├── assets/                 # Static assets directory
└── .well-known/            # Well-known directory (e.g., for verification)
```

---

## 3. Design System

### 3.1 Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| **Primary (Dark Navy)** | `#1e293b` | Icon backgrounds, text, buttons |
| **Heading** | `#0f172a` | Section headings, card titles |
| **Body Text** | `#64748b` | Paragraph text |
| **Muted Text** | `#94a3b8` | Labels, secondary text |
| **Accent (Sky Blue)** | `#0ea5e9` | CTA buttons, progress dots, floating button, section label bars |
| **Accent Hover** | `#0284c7` | Hover states for accent elements |
| **Accent Light** | `#38bdf8` | Gradient endpoints, footer highlights |
| **White** | `#ffffff` | Primary section backgrounds |
| **Off-White** | `#f8f9fb` | Alternating section backgrounds (Globe, Social, Download) |
| **Light Grey** | `#f1f5f9` | Badges, timer bars, subtle fills |
| **Border** | `rgba(30, 41, 59, 0.06)` | Card borders, dividers |
| **Footer Dark** | `#0a0f1e` | Footer and footer-prelude background |

### 3.2 Typography

| Element | Font | Weight | Size |
|---------|------|--------|------|
| Headings (h1-h4) | Space Grotesk | 700 | `clamp(40px, 5vw, 96px)` |
| Body / UI | Inter | 400-600 | 14-22px |
| Nav Logo | Space Grotesk | 800 | 24px |
| Section Labels | Inter | 600 | 13px, uppercase, 0.15em tracking |
| Stat Numbers | Space Grotesk | 700 | 36px |
| Badges | Inter | 600 | 12px |

**Font loading:** Google Fonts with `preconnect` for performance:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 3.3 Icon System

All icons are **inline SVGs** with a consistent treatment across all sections:

| Context | Container Size | Border Radius | Background | Icon Size | Icon Color |
|---------|---------------|---------------|------------|-----------|------------|
| Stories features | 48x48px | 14px | `#1e293b` | 22px | `#ffffff` stroke |
| Social cards | 48x48px | 14px | `#1e293b` | 22px | `#ffffff` stroke |
| Game cards | 56x56px | 16px | `#1e293b` | 28px | `#ffffff` stroke |

SVG attributes: `fill="none"`, `stroke="currentColor"` or `stroke="#ffffff"`, `stroke-width="2"`, `stroke-linecap="round"`.

### 3.4 Accent Text Gradient

All `.accent` spans in section headings use the same gradient text treatment:
```css
background: linear-gradient(135deg, #0ea5e9, #38bdf8);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
```

### 3.5 Section Label Pattern

Each section starts with a label component:
```html
<div class="section-label reveal">
    <span>Section Name</span>
</div>
```
Styled as: uppercase, 13px, `#475569`, with a 24px sky blue bar via `::before` pseudo-element.

---

## 4. Section-by-Section Breakdown

### 4.1 Navigation (`<nav class="nav">`)

**Lines:** CSS ~50-116, HTML ~2012-2021

- Fixed position, full-width
- Text logo "Pinr" (Space Grotesk 800, `#0f172a`)
- Links: Explore, Stories, Social, Games, Download (CTA)
- **Scroll state:** Adds `.scrolled` class on `scrollY > 60` — white frosted glass background with blur + subtle bottom border
- **CTA button:** Sky blue (`#0ea5e9`) pill, white text, hover darkens to `#0284c7` with glow shadow
- Hidden on mobile (`<768px` — `display: none` on `.nav-links`)

### 4.2 Progress Dots (`<div class="progress-dots">`)

**Lines:** CSS ~118-167, HTML ~2024-2031

- Fixed right sidebar, vertical dots
- 6 dots for 6 sections (Hero, Explore, Stories, Social, Games, Download)
- Active dot: sky blue fill + glow shadow + 1.4x scale
- Hover reveals section label via `::after` pseudo-element
- Clickable — calls `scrollToSection(id)` for smooth scroll
- Hidden on mobile (`<768px`)

### 4.3 Floating Download Button

**Lines:** CSS ~169-206, HTML ~2034-2037

- Fixed bottom-right, pill-shaped, sky blue
- Play icon + "Get Pinr" text
- Visibility: appears when scrolled past 80% of viewport AND download section is not yet in view
- Animated entrance via `transform: translateY(100px)` → `translateY(0)` with `.visible` class
- Links to Google Play

### 4.4 Section 1: Hero

**Lines:** CSS ~280-598, HTML ~2040-2105

**Layout:** Two-column CSS Grid (`1fr 1fr`, 60px gap)

**Left column (text):**
- Pre-tagline: "TRAVEL MADE SOCIAL" (uppercase, tracked)
- Title: `<h1>` with three `<span class="hero-title-word">` elements — "Travel", "Made", "Social."
- **Clip-path text reveal animation:** Each word starts with `clip-path: inset(100% 0 0 0)` (hidden from bottom) and animates to `inset(0 0 0 0)` with staggered delays (0.3s, 0.5s, 0.7s)
- "Social." word uses the `.accent` gradient text
- Subtitle: descriptive paragraph
- **Download buttons:**
  - Google Play: dark navy (`#1e293b`) pill, Google Play colored SVG icon, "Now live on / Google Play"
  - App Store: ghost style (border only), muted, "Coming soon to / App Store"

**Right column (globe):**
- 480x480px Three.js canvas (see Section 5 for details)
- 5 pin markers projected onto globe surface (Paris, NYC, Tokyo, Cape Town, Rio)
- Globe shadow (radial gradient blur beneath)

**Background:**
- Animated gradient mesh (`::after` pseudo-element): 3 radial gradients in sky blue tones, slow drift animation (`meshDrift` 20s infinite)

**Scroll indicator:** Bottom-center, bouncing chevron with "Scroll to explore" text

### 4.5 Section 2: Globe / Explore

**Lines:** CSS ~639-830, HTML ~2107-2176

**Background:** `#f8f9fb` (off-white)

**Layout:** Two-column grid — text left, visual right

**Left column:**
- Section label: "The Globe"
- Heading: "Pin Your **World**"
- Description paragraph
- **Stats row** (3 stats):
  - "195 Countries" — animated counter (`data-target="195"`, counts from 0 to 195 on scroll)
  - "3D Interactive Globe" — static text
  - "∞ Pins to Drop" — static infinity symbol

**Right column — Explore Cards Stack:**
- 3 portrait destination cards (240x300px), absolutely positioned and stacked
- Each card has:
  - Full-bleed background image from Unsplash (Machu Picchu, Kyoto, Santorini)
  - Glassmorphism text overlay at bottom (`backdrop-filter: blur(16px)`, white 75% opacity)
  - Location name, coordinates, "Pinned [date]" badge with pin icon
- **Stack interaction:**
  - Default: Card 1 (front, z-index 3), Card 2 (offset right +25px, rotated +3°, scale 0.96, opacity 0.85), Card 3 (offset left -30px, rotated -4°, scale 0.92, opacity 0.7)
  - Hover: Cards fan out further — Card 2 moves right +120px/rotated +8°, Card 3 moves left -10px/rotated -8°, both become fully opaque
  - Transition: 0.5s cubic-bezier ease

**Wave divider:** SVG curve at top, fills with `#ffffff` (color of the previous hero section)

### 4.6 Section 3: Stories

**Lines:** CSS ~832-973, HTML ~2178-2274

**Background:** `#ffffff`

**Layout:** Two-column grid — visual left (CSS phone mockup), text right

**Left column — Phone mockup:**
- CSS-built phone frame: 280x560px, dark navy body, 40px border-radius, notch via `::before`
- White screen with rounded corners
- "My Stories" header
- **Animated story feed:** 5 story items that auto-scroll vertically:
  - `storyScroll` keyframes: scrolls down in steps (0→-80px→-160px→back) over 12s
  - Each item: Unsplash thumbnail (52x52px rounded), title, location, preview text
  - Locations: Machu Picchu, Paris, Bali, Iceland, Kyoto
- Phone has 3D perspective tilt (`rotateY(-5deg) rotateX(2deg)`), resets to flat on hover

**Right column:**
- Section label: "Photo Stories"
- Heading: "Your Adventures, **Beautifully Told**"
- Description paragraph
- 3 feature cards (staggered reveal):
  1. Add Photos (image icon)
  2. Write Stories (pencil icon)
  3. Share Globally (share/network icon)

### 4.7 Section 4: Social

**Lines:** CSS ~1038-1283, HTML ~2277-2365

**Background:** `#f8f9fb` (off-white)

**Layout:** Two-column grid — text left, visual right

**Left column:**
- Section label: "Social"
- Heading: "Travel Is Better **Together**"
- Description paragraph
- 3 feature cards (horizontal, with hover translateX effect):
  1. Follow Friends (people icon)
  2. React & Comment (chat icon)
  3. Discover Adventures (globe icon)

**Right column — Social Orbit Visualization:**
- 420x420px container with 3 concentric orbit rings (dashed outer)
- Center hub: 80px dark navy circle with user profile SVG icon, pulsing ring animation
- **6 orbiting avatars** at 3 orbital distances:
  - Inner ring (100px radius): 2 avatars, 46px, 18s orbit period
  - Middle ring (155px radius): 2 avatars, 42px, 25s orbit period
  - Outer ring (200px radius): 2 avatars, 36px, 35s orbit period
- Each orbit pair is offset 180° for balance
- 3 small connection dots orbit on the rings
- Profile photos from pravatar.cc

### 4.8 Section 5: Games

**Lines:** CSS ~1284-1537, HTML ~2367-2425

**Background:** `#ffffff`

**Layout:** Single-column, centered

**Floating geometric shapes:** 3 circular/rounded shapes with slow drift animations (`gameShapeDrift` 20s), very subtle borders (`rgba(30, 41, 59, 0.04)`)

**Quiz Showcase (animated):**
- Card with cycling flag emoji + country name:
  - `flagText` keyframes: cycles Japan → Brazil → France (9s, step-end)
  - `nameText` keyframes: matches flag cycle
  - Timer bar fills over 3s (`timerFill` keyframes)
  - Score dots: 3 correct (green), 1 wrong (red), 1 pending (grey)
- Uses `::after` pseudo-elements for the cycling content

**Game Cards Grid (3 columns, `perspective: 1000px`):**
- 3 cards: Flag Dash (flag icon), Pin Drop (map pin icon), Travel Battle (crossed swords icon)
- Each card: white bg, 24px rounded corners, 56px dark navy icon, title, description, badge pill
- **Staggered entrance animation:**
  - Cards start `opacity: 0; transform: translateY(40px) scale(0.95)`
  - IntersectionObserver adds `.game-card-visible` class with 150ms stagger between cards
  - Transition: 0.5s spring cubic-bezier
- **3D hover:** `translateY(-8px) rotateX(2deg) rotateY(-1deg)` with enhanced shadow

### 4.9 Section 6: Download

**Lines:** CSS ~1539-1666, HTML ~2427-2491

**Background:** `#f8f9fb` (off-white)

**Layout:** Single-column, centered

**Content:**
- Section label: "Get Started"
- Heading: "Your Next Adventure Starts **Here**"
- Description paragraph
- Download buttons (reuse hero button styles)

**Notification Stack Animation:**
- 4 notification cards stacked in a 380x260px container with `overflow: hidden`
- Each card: avatar photo, bold name + action text, timestamp, colored emoji icon
- **`notifSlide` keyframes** (12s loop, 3s stagger per card):
  1. Slides in from right (`translateX(60px)` → `translateX(0)`)
  2. Holds visible for ~17% of cycle
  3. Slides up and fades out (`translateY(-16px)`, `opacity: 0`)
- Notification content:
  - Sarah pinned Tokyo Tower (red pin)
  - Jake shared a story from Bali (blue camera)
  - Emma won Flag Dash Champion (green trophy)
  - Marco pinned Colosseum, Rome (orange pin)

### 4.10 Footer Prelude & Footer

**Lines:** CSS ~1668-1776, HTML ~2493-2516

**Footer Prelude:**
- Dark background (`#0a0f1e`) matching footer
- **Wave SVG divider** positioned above the prelude (`transform: translateY(-99%)`) — creates a smooth curved transition from the light download section to the dark footer
- Tagline: "Your world. Your pins. **Your stories.**" — muted white text with sky blue `<span>` highlight

**Footer:**
- Dark background (`#0a0f1e`)
- Flexbox layout: left (logo + links), right (signature)
- "Pinr" logo in sky blue (`#38bdf8`)
- Links: Privacy Policy, Terms of Service, FAQ, Support (mailto)
- "Built by Lee" (non-clickable `<span>`)
- Copyright: © 2025 Pinr. All rights reserved.

---

## 5. 3D Globe (Three.js)

**Lines:** ~2717-2982

**Library:** Three.js v0.160.0 via CDN (`https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js`)

### 5.1 Scene Setup

- `PerspectiveCamera` at FOV 45, positioned at z=2.6
- `WebGLRenderer` with antialiasing, transparent background, 2x pixel ratio
- Canvas size: container width × 2 for retina rendering

### 5.2 Earth Sphere

- `SphereGeometry(1, 128, 128)` — high-resolution for smooth shading
- Two textures loaded from CDN:
  - **Day map:** `earth-day.jpg` (terrain colors)
  - **Water mask:** `earth-water.png` (ocean vs land separation)

### 5.3 Custom GLSL Shader

**Vertex Shader:**
- Samples water mask to determine land/water
- **Displaces land vertices outward** along normals by `uLandHeight` (0.035), making continents physically protrude above the ocean surface
- Smoothstep at `w ∈ [0.4, 0.6]` for soft coastline transitions

**Fragment Shader:**
- **Ocean:** Bright cyan color palette (3-tone: light/mid/shade), wrap lighting, coastline shadows from raised land, subtle specular glint (power 60)
- **Land:** Day texture with brightened gamma (`pow(0.65)`), boosted green saturation, reduced red/blue, wrap lighting, coastline edge darkening
- **Atmosphere rim:** Fresnel-based rim light blending toward pale blue, strength 0.45

### 5.4 Atmosphere Glow

- Separate sphere (scale 1.18x), BackSide rendering, AdditiveBlending
- Custom glow shader based on fresnel angle from camera

### 5.5 Pin Projection System

- 5 pin markers defined in HTML with `data-lat` and `data-lng` attributes
- Locations: Paris (48.86°N, 2.35°E), NYC (40.71°N, 74.01°W), Tokyo (35.68°N, 139.69°E), Cape Town (33.92°S, 18.42°E), Rio (22.91°S, 43.17°W)
- Each frame:
  1. Convert lat/lng to 3D sphere position (r=1.06, above displaced land)
  2. Transform through globe's world matrix (accounts for rotation)
  3. Dot product with camera direction to determine front/back facing
  4. If facing < 0.05: hide pin (behind globe)
  5. If visible: project to 2D screen coordinates, apply opacity fade near edges (facing 0.05→0.25), scale based on depth (0.6→1.0)
- Globe rotates slowly: `rotation.y += 0.0006` per frame

### 5.6 Pin Marker Styling

- Teardrop shape: `border-radius: 50% 50% 50% 0` rotated -45°
- 56px body with 36px circular profile photo inside (rotated back +45°)
- 5 color variants: dark, red, blue, green, orange
- Profile photos from pravatar.cc
- Drop shadow filter for depth
- Hidden on mobile (`<768px`)

---

## 6. Animations & Interactions

### 6.1 Scroll Reveal System

**CSS:**
```css
.reveal { opacity: 0; transform: translateY(60px); transition: all 0.9s cubic-bezier(0.16, 1, 0.3, 1); }
.reveal.visible { opacity: 1; transform: translateY(0) translateX(0) scale(1); }
```

**Variants:**
- `.from-left` — slides from -80px left
- `.from-right` — slides from +80px right
- `.from-scale` — scales from 0.85

**Delay classes:** `.reveal-delay-1` through `.reveal-delay-7` (100ms increments)

**Observer:** `threshold: 0.15`, `rootMargin: '0px 0px -60px 0px'` — triggers when 15% visible with 60px bottom offset.

**Hero special case:** Hero `.reveal` elements get `.visible` added after 200ms timeout on page load (no scroll needed).

### 6.2 Clip-Path Text Reveal (Hero Title)

Each word wrapped in `<span class="hero-title-word">`:
```css
clip-path: inset(100% 0 0 0);  /* hidden: clipped from bottom */
animation: clipReveal 0.9s cubic-bezier(0.16, 1, 0.3, 1) forwards;
```
Staggered delays: 0.3s, 0.5s, 0.7s for the three words.

### 6.3 Animated Gradient Mesh (Hero Background)

Three overlapping radial gradients in sky blue tones (very subtle, 5-8% opacity), slowly drifting via `meshDrift` keyframes (20s, translate + rotate).

### 6.4 Scroll-Linked Parallax

Elements with `data-parallax` and `data-speed` attributes get vertical offset based on their position relative to viewport center:
```javascript
offset = (elementCenterY - viewportCenter) * speed;
el.style.transform = 'translateY(' + offset + 'px)';
```
Applied to: explore cards stack (0.06), stories phone (0.05), social orbit (0.05). Uses `requestAnimationFrame` throttling.

### 6.5 Magnetic Cursor Effect

Applied to: `.btn-google-play`, `.nav-cta`, `.floating-download`

On `mousemove`: translates button toward cursor position (15% of offset from button center). Resets on `mouseleave`.

### 6.6 Animated Number Counter

The "195 Countries" stat uses `data-target="195"`. Two-layer observer system:
1. **Element-level:** IntersectionObserver on `[data-target]` elements (threshold 0.1, rootMargin -50px bottom)
2. **Section-level backup:** IntersectionObserver on `#globe` section (threshold 0.3), triggers counter after 500ms delay

Counter animation: 1.5s duration, cubic ease-out (`1 - (1-t)^3`), counts from 0 to target value using `requestAnimationFrame`.

### 6.7 Staggered Game Card Entrance

IntersectionObserver watches `.games-grid` (threshold 0.2). When visible, iterates `.game-card` elements and adds `.game-card-visible` class with 150ms stagger:
```javascript
cards.forEach(function(card, i) {
    setTimeout(function() { card.classList.add('game-card-visible'); }, i * 150);
});
```
Cards transition from `opacity: 0; translateY(40px) scale(0.95)` to visible with spring easing.

### 6.8 Notification Stack (Download Section)

4 notification cards with CSS-only animation (`notifSlide` keyframes, 12s cycle):
- Each card has a 3s stagger (`animation-delay: 0s, 3s, 6s, 9s`)
- Slides in from right, holds visible for ~20% of cycle, slides up and fades out
- Creates a continuous stream of notifications

### 6.9 Story Feed Scroll

`storyScroll` keyframes on `.stories-feed`:
- Steps through 3 positions over 12s (0, -80px, -160px, back to 0)
- Creates the illusion of scrolling through a story feed on the phone mockup

### 6.10 Quiz Flag Cycle

`flagText` and `nameText` keyframes cycle through 3 flag/country pairs (Japan, Brazil, France) every 9s using `step-end` timing and `::after` pseudo-element `content` property. Timer bar fills over 3s.

### 6.11 Social Orbit

6 avatars orbit the center hub at 3 different radii and speeds using CSS `@keyframes` with `rotate() translateX() rotate()` pattern (counter-rotation keeps avatars upright). Connection dots orbit on the ring paths.

### 6.12 Wave Dividers

SVG-based curved dividers between sections:
```html
<div class="wave-divider">
    <svg viewBox="0 0 1200 60" preserveAspectRatio="none">
        <path d="M0,60 C300,0 900,0 1200,60 L1200,0 L0,0 Z" fill="#ffffff"/>
    </svg>
</div>
```
Fill color matches the background of the section above. Absolutely positioned at `top: -1px`. The footer prelude uses an inverted wave with `transform: translateY(-99%)`.

---

## 7. JavaScript Architecture

### 7.1 Main Script (non-module)

Wrapped in IIFE with `'use strict'`. Contains:

| Feature | Observer/Listener | Threshold | Notes |
|---------|-------------------|-----------|-------|
| Scroll reveal | IntersectionObserver | 0.15 | rootMargin -60px bottom |
| Progress dots | IntersectionObserver | 0.4 | Updates active dot per section |
| Nav scroll state | scroll listener | — | Adds/removes `.scrolled` class |
| Floating button | scroll listener | — | Visibility based on scroll position |
| Parallax | scroll listener | — | `requestAnimationFrame` throttled |
| Magnetic cursor | mousemove/leave | — | On CTA buttons |
| Counter | IntersectionObserver × 2 | 0.1 / 0.3 | Element-level + section-level backup |
| Game card stagger | IntersectionObserver | 0.2 | Watches `.games-grid` container |

### 7.2 Globe Script (ES Module)

Separate `<script type="module">` importing Three.js. Wrapped in IIFE. Contains:
- Scene, camera, renderer setup
- Texture loading (day map + water mask)
- Custom GLSL ShaderMaterial
- Atmosphere glow mesh
- Pin lat/lng → 3D projection system
- Animation loop (`requestAnimationFrame`)
- Resize handler

---

## 8. Responsive Breakpoints

### 8.1 Tablet (`max-width: 1024px`)

- Hero grid → single column, text centered (order 1), globe below (order 2)
- Globe wrap: 380px
- All two-column layouts (globe, stories, social) → single column
- Text content centered with auto margins
- Section inner padding-top: 120px, padding-bottom: 80px
- Social orbit: 320px
- Features/cards max-width constrained and centered

### 8.2 Mobile (`max-width: 768px`)

- Nav links hidden (logo only)
- Nav padding reduced: 16px 20px
- Section inner padding: 20px
- Progress dots hidden
- Hero logo: 36px height
- Hero content padding-top: 60px
- Games grid: single column (max-width 380px)
- Download/hero buttons: vertical stack, full width (max 280/300px)
- Two-column layouts: tighter gaps (40px), adjusted padding
- Footer: flex-direction column, centered
- Floating story cards hidden
- Globe pin markers hidden
- Floating download button: smaller padding/font

### 8.3 Small Mobile (`max-width: 480px`)

- Hero subtitle: 16px
- All section headings: 32px
- Section body text: 16px
- Globe stats: vertical column layout
- Globe wrap: 240px

---

## 9. External Dependencies

| Dependency | Version | Purpose | CDN |
|-----------|---------|---------|-----|
| Three.js | 0.160.0 | 3D globe rendering | `cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js` |
| Earth Day Texture | — | Globe terrain map | `cdn.jsdelivr.net/npm/three-globe@2.31.1/example/img/earth-day.jpg` |
| Earth Water Mask | — | Ocean/land separation | `cdn.jsdelivr.net/npm/three-globe@2.31.1/example/img/earth-water.png` |
| Inter (font) | Variable | Body/UI typography | Google Fonts |
| Space Grotesk (font) | Variable | Heading typography | Google Fonts |
| Unsplash Images | — | Location photography | `images.unsplash.com` |
| Pravatar | — | Avatar placeholder photos | `i.pravatar.cc` |

**Unsplash images used:**
- Machu Picchu: `photo-1587595431973-160d0d94add1` (explore card + story item)
- Kyoto temples: `photo-1493976040374-85c8e12f0c0e` (explore card + story item)
- Santorini: `photo-1570077188670-e3a8d69ac5ff` (explore card)
- Paris Eiffel Tower: `photo-1502602898657-3e91760cbb34` (story item)
- Bali rice terraces: `photo-1537996194471-e657df975ab4` (story item)
- Northern Lights: `photo-1531366936337-7c912a4589a7` (story item)

---

## 10. Deployment

### GitHub Pages

- Repository: `builtbylee/pinr-website`
- Branch: `main`
- Custom domain: `getpinr.com` (configured via `CNAME` file)
- `.nojekyll` file disables Jekyll processing

### Deployment workflow

1. Make changes to `mockup5.html`
2. Copy to `index.html`: `cp mockup5.html index.html`
3. Commit both files
4. Push to `main` — GitHub Pages automatically deploys

### Google Play link

All download buttons and CTAs link to:
```
https://play.google.com/store/apps/details?id=com.builtbylee.app80days
```

### Contact

- Support email: `lee@getpinr.com` (linked in footer)
