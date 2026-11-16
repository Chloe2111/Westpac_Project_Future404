# Westpac Project Future404

## Layout

- `autopilot/` — React + TypeScript + Vite frontend, built with Westpac's GEL design system (`@westpac/ui`, `@westpac/style-config`, Tailwind CSS 4.1). Run with `cd autopilot && npm install && npm run dev`.
- `src/future404/`, `app/`, `tests/` — Python backend / Streamlit prototype.

## Frontend rules (GEL integration requirements)

Before writing or changing any UI in `autopilot/`, use the `using-westpac-ui` skill (`.claude/skills/using-westpac-ui/`) and check the component's reference file in `reference/components/` for its real props. Don't guess props.

- **Use GEL components first.** Import them individually, e.g. `import { Button } from '@westpac/ui/button'`. Only build a custom component when GEL has nothing suitable, and wrap it in GEL layout/spacing.
- **Tokens only, no hardcoded styling.** Use GEL's semantic Tailwind classes (`bg-surface-primary`, `text-text-body`, `border-border-muted`, `typography-body-8`, `rounded-md`). Never use hex/RGB colours, arbitrary values like `bg-[#da1710]` or `rounded-[7px]`, inline `style` for colours/spacing, or invented token names. If a token seems missing, raise it with the team rather than working around it.
- **Don't restyle GEL components** with global CSS or element selectors. Prefer built-in props (`look`, `size`, `soft`, `block`) over `className`.
- **Component API conventions:** use `tag` (not `as`) to change the element; pass icons as components (`iconBefore={ArrowRightIcon}`), not elements; responsive props take breakpoint objects keyed `initial | xsl | sm | md | lg | xl`.
- **Accessibility:** don't remove or change ARIA attributes or keyboard behaviour on GEL components. Custom components must meet WCAG 2.1 AA.
- **Brand/theme:** `index.html` sets `data-brand="wbc" data-theme="light"`. Dark mode is disabled in GEL, so keep `light`.
- **Versions:** keep `@westpac/ui` and `@westpac/style-config` on the latest stable release. Tailwind must stay on `~4.1.12` (GEL's peer dependency).
- **Testing:** use Vitest (GEL recommends it; Jest needs extra transform config for `@westpac/ui`).
