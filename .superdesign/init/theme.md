# Theme

Editorial Authority: warm cream paper, forest-green ink, muted green secondary text, and amber accents. Serif display type contrasts with a restrained sans-serif body.

```css
:root {
  --color-paper: #f5f0e5;
  --color-paper-deep: #ebe3d3;
  --color-ink: #18372a;
  --color-ink-muted: #51665b;
  --color-accent: #efb34e;
  --color-rule: rgba(24, 55, 42, 0.24);
  --font-display: Georgia, "Times New Roman", serif;
  --font-body: "Avenir Next", Avenir, "Segoe UI", sans-serif;
  --content-width: 74rem;
  --reading-width: 44rem;
}
```

Headings use fluid `clamp()` sizing. Cards use `--color-paper-deep` and a 3px amber top border. Desktop content can use two or three columns; the existing `48rem` breakpoint collapses grids to one column. Interactive controls retain visible focus indicators and reduced-motion support.
