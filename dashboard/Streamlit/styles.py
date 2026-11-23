"""
UI/UX Design System v4 (Sunlit Greenhouse Editorial from DESIGN.md + Antislop Certified)
Palette: Pale Sage (#eef2e3), Paper White (#fcfcfc), Deep Forest (#043f2e),
         Chartreuse Lime (#c8f169), Forest Mid (#2a6f2b), Vivid Green (#78c51c), Charcoal (#242423)
Typography: Fraunces (Grenette editorial serif substitute, 36px+, weight 400, tight tracking)
            + Inter (Graphik UI sans substitute, weights 400/500/600)
Elevation: Strictly flat three-layer botanical color stack (Zero box-shadows on cards/buttons)
"""

import streamlit as st

LIGHT_PALETTE = {
    "is_dark": False,
    "canvas": "#eff1f3",          # Clean Neutral Light Gray canvas (10.56:1 with Deep Forest)
    "white": "#fcfcfc",           # Paper White elevated cards & sidebar
    "pill_bg": "#e5e8ec",         # Subtle neutral gray hover surface
    "track_bg": "#e2e5e9",        # Capsule switcher track
    "emerald": "#043f2e",         # Deep Forest primary ink on light surfaces (11.66:1)
    "emerald_dark": "#022c20",    # Deep Forest pressed state
    "hero_bg": "#043f2e",         # Dark hero card background
    "hero_border": "none",        # Flat borderless in Light mode
    "hero_fg": "#fcfcfc",         # Crisp white ink on dark hero card
    "hero_label": "#c9dcc6",
    "hero_meta": "#d9e8cf",
    "active_bg": "#043f2e",       # Active sidebar nav pill bg
    "active_fg": "#fcfcfc",       # Active sidebar nav pill text
    "btn_bg": "#043f2e",          # Primary CTA button bg
    "btn_fg": "#fcfcfc",          # Primary CTA button text
    "btn_hover_bg": "#2a6f2b",
    "btn_hover_fg": "#fcfcfc",
    "chart_primary": "#043f2e",   # Primary line / radar stroke
    "chart_badge_bg": "#043f2e",
    "chart_badge_fg": "#c8f169",
    "chart_peak_bar": "#043f2e",
    "chart_support_bar": "#9ab391",
    "arc_flipkart": "#043f2e",
    "radar_fill": "rgba(4, 63, 46, 0.11)",
    "emerald_meta": "#c8f169",
    "emerald_label": "#c8f169",
    "teal": "#2a6f2b",
    "teal_dark": "#1f5420",
    "lime": "#c8f169",
    "lime_dark": "#043f2e",
    "vivid": "#78c51c",
    "sage_bar": "#95ab8a",
    "mint_tint": "#eef2e3",
    "good_text": "#043f2e",
    "text": "#043f2e",
    "ink": "#000000",
    "charcoal": "#242423",
    "muted": "#46534b",
    "amber": "#b45309",
    "amber_text": "#78350f",
    "amber_tint": "#fef3c7",
    "coral": "#b91c1c",
    "coral_text": "#7f1d1d",
    "coral_tint": "#fee2e2",
    "gridline": "#e7eaee",
    "hairline": "#d7dce2",
}

DARK_PALETTE = {
    "is_dark": True,
    "canvas": "#0b1411",          # Midnight Greenhouse canvas
    "white": "#121f1a",           # Dark Conservatory elevated cards & sidebar
    "pill_bg": "#1b2e26",         # Deep Moss hover & nested active surface
    "track_bg": "#182922",
    "emerald": "#ebf4e6",         # Soft Sage-White primary ink (15.05:1 on #121f1a)
    "emerald_dark": "#072b20",
    "hero_bg": "#073527",         # Lush Deep Forest hero card
    "hero_border": "1px solid #1b4738",
    "hero_fg": "#ffffff",
    "hero_label": "#b7d7c4",
    "hero_meta": "#cfe6d6",
    "active_bg": "#0c4331",       # Deep Forest active nav pill on dark rail
    "active_fg": "#ffffff",
    "btn_bg": "#c8f169",          # Luminous Chartreuse CTA in Dark mode (16.24:1 with Ink Black)
    "btn_fg": "#000000",
    "btn_hover_bg": "#d7f789",
    "btn_hover_fg": "#000000",
    "chart_primary": "#c8f169",   # Glowing Chartreuse primary line / radar stroke
    "chart_badge_bg": "#c8f169",
    "chart_badge_fg": "#000000",
    "chart_peak_bar": "#2c7a4f",
    "chart_support_bar": "#233c32",
    "arc_flipkart": "#2e7d52",
    "radar_fill": "rgba(200, 241, 105, 0.14)",
    "emerald_meta": "#c8f169",
    "emerald_label": "#c8f169",
    "teal": "#348a54",
    "teal_dark": "#25693e",
    "lime": "#c8f169",
    "lime_dark": "#043f2e",
    "vivid": "#8ee02e",
    "sage_bar": "#3d5c4e",
    "mint_tint": "#1b2e26",
    "good_text": "#c8f169",
    "text": "#ebf4e6",
    "ink": "#000000",
    "charcoal": "#d7e5dc",
    "muted": "#9eb3a5",           # Sage-Silver muted ink (7.64:1 on #121f1a)
    "amber": "#fbbf24",           # High-contrast Warm Amber (10.17:1)
    "amber_text": "#fde68a",
    "amber_tint": "#3b2a10",
    "coral": "#f87171",           # High-contrast Soft Crimson (6.14:1)
    "coral_text": "#fca5a5",
    "coral_tint": "#3d171a",
    "gridline": "#1f332a",
    "hairline": "#263d33",
}

PALETTE = dict(LIGHT_PALETTE)


def set_active_theme(theme: str = "light"):
    """Mutates PALETTE in-place so both styles.py and app.py reflect active Light or Dark theme."""
    PALETTE.clear()
    PALETTE.update(DARK_PALETTE if theme == "dark" else LIGHT_PALETTE)


def inject_bento_css(sidebar_expanded: bool = True, theme: str = "light"):
    set_active_theme(theme)
    # Load Fraunces (Grenette editorial serif substitute) and Inter (Graphik UI sans substitute)
    st.markdown(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )

    sb_width = "244px" if sidebar_expanded else "82px"
    sb_pad_x = "0.75rem" if sidebar_expanded else "0.4rem"
    sb_align = "stretch" if sidebar_expanded else "center"
    sb_btn_w = "100%" if sidebar_expanded else "48px"
    sb_btn_just = "flex-start" if sidebar_expanded else "center"
    sb_btn_pad = "0.55rem 0.9rem" if sidebar_expanded else "0"

    sb_bg = PALETTE["white"]
    sb_border = PALETTE["hairline"]
    sb_text = PALETTE["charcoal"]
    sb_icon = PALETTE["muted"]
    sb_hover_bg = PALETTE["pill_bg"]
    sb_hover_fg = PALETTE["emerald"]
    sb_div = PALETTE["hairline"]
    sb_sub_act_bg = PALETTE["pill_bg"]
    sb_sub_act_fg = PALETTE["emerald"]
    sb_sub_act_ic = PALETTE["chart_primary"]

    css = f"""<style>
:root {{
    --color-pale-sage: #eef2e3;
    --color-paper-white: #fcfcfc;
    --color-ink-black: #000000;
    --color-charcoal: #242423;
    --color-deep-forest: #043f2e;
    --color-chartreuse-lime: #c8f169;
    --color-forest-mid: #2a6f2b;
    --color-vivid-green: #78c51c;
    --font-serif-display: 'Fraunces', Georgia, Cambria, 'Times New Roman', serif;
    --font-ui-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

/* Base Typography & Sunlit Pale Sage Canvas */
html, body, [class*="css"] {{
    font-family: var(--font-ui-sans) !important;
    color: {PALETTE['text']};
}}
.stApp {{
    background-color: {PALETTE['canvas']} !important;
    overflow-x: hidden;
}}
#MainMenu, footer, [data-testid="stToolbarActions"], [data-testid="stDecoration"], .stAppDeployButton {{
    visibility: hidden;
    height: 0;
}}
header[data-testid="stHeader"],
[data-testid="stToolbar"] {{
    background: transparent !important;
    pointer-events: none !important;
}}
[data-testid="stExpandSidebarButton"] {{
    pointer-events: auto !important;
}}
section[data-testid="stMain"] {{
    overflow-x: hidden !important;
}}
.block-container,
[data-testid="stMainBlockContainer"] {{
    padding-top: 1.5rem !important;
    padding-bottom: 2.2rem !important;
    padding-left: 3.25rem !important;
    padding-right: 3.25rem !important;
    max-width: 100% !important;
}}
.stElementContainer:has(style) {{
    position: fixed !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    pointer-events: none !important;
}}
.yv-page-heading,
[data-testid="stMarkdownContainer"] h1.yv-page-heading {{
    font-family: var(--font-ui-sans) !important;
    font-size: clamp(24px, 2.15vw, 30px) !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
    color: {PALETTE['emerald']} !important;
    line-height: 1.15 !important;
    min-height: 44px;
    display: flex;
    align-items: center;
    margin: 0 !important;
    padding: 0 !important;
}}
.yv-brand-lockup {{
    display: inline-flex;
    align-items: flex-start;
    gap: 2px;
    cursor: default;
}}
.yv-brand-word {{
    font-family: var(--font-ui-sans);
    font-size: clamp(24px, 2.25vw, 32px);
    font-weight: 800;
    letter-spacing: -0.042em;
    color: #043f2e;
    line-height: 1;
}}
.yv-brand-star {{
    display: inline-block;
    margin-top: -7px;
    margin-left: 1px;
    transition: transform 520ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.yv-brand-lockup:hover .yv-brand-star {{
    transform: rotate(90deg) scale(1.12);
}}

/* Accessible Base Layer: Pointer Cursors & High-Contrast Focus (R-32, R-39) */
button:not(:disabled),
a[href],
select:not(:disabled),
[role="button"]:not([aria-disabled="true"]),
[role="combobox"]:not([aria-disabled="true"]),
[data-testid="stButtonGroup"] button:not(:disabled) {{
    cursor: pointer !important;
}}
button:disabled,
[aria-disabled="true"] {{
    cursor: not-allowed !important;
    opacity: 0.55 !important;
}}
button:focus-visible,
a:focus-visible,
input:focus-visible,
select:focus-visible,
[role="combobox"]:focus-visible,
[data-testid="stButtonGroup"] button:focus-visible {{
    outline: 2.5px solid {PALETTE['emerald']} !important;
    outline-offset: 2px !important;
}}

/* Respect Reduced Motion Preference (R-39) */
@media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }}
}}

/* Sidebar Shell: Stateful Collapsible Rail (244px Left-Aligned Full <-> 82px Icon-Only Rail) */
section[data-testid="stSidebar"] {{
    background-color: {sb_bg} !important;
    border-right: 1px solid {sb_border} !important;
    box-shadow: none !important;
    min-width: 0px !important;
    width: {sb_width} !important;
    max-width: {sb_width} !important;
    transition: width 180ms ease, max-width 180ms ease;
}}
@media (min-width: 769px) {{
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarHeader"] {{
        display: none !important;
    }}
}}
section[data-testid="stSidebar"] > div:first-child {{
    width: {sb_width} !important;
    padding-top: 1.25rem !important;
    padding-left: {sb_pad_x} !important;
    padding-right: {sb_pad_x} !important;
}}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{
    padding-top: 0 !important;
}}
@media (max-width: 768px) {{
    section[data-testid="stSidebar"] > div:first-child {{
        padding-top: 1.5rem !important;
    }}
}}
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
    padding-left: 0.25rem !important;
    padding-right: 0.25rem !important;
}}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
    align-items: {sb_align} !important;
    gap: 0.45rem !important;
}}
/* Force true left-alignment inside Streamlit's inner button wrapper when expanded */
section[data-testid="stSidebar"] button,
section[data-testid="stSidebar"] button > div {{
    justify-content: {sb_btn_just} !important;
    text-align: left !important;
}}
/* Active Nav Item: Deep Forest Pill with Chartreuse Icon & Left-Aligned Paper White Text */
section[data-testid="stSidebar"] button[kind="primary"],
section[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {{
    background-color: {PALETTE['active_bg']} !important;
    color: {PALETTE['active_fg']} !important;
    border: none !important;
    border-radius: 12px !important;
    width: {sb_btn_w} !important;
    min-height: 46px !important;
    padding: {sb_btn_pad} !important;
    display: flex !important;
    align-items: center !important;
    justify-content: {sb_btn_just} !important;
    gap: 10px !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    box-shadow: none !important;
    transition: background-color 140ms ease, transform 100ms ease;
}}
section[data-testid="stSidebar"] button[kind="primary"] span[data-testid="stIconMaterial"],
section[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] span[data-testid="stIconMaterial"] {{
    color: {PALETTE['lime']} !important;
    font-size: 20px !important;
    flex-shrink: 0 !important;
}}
section[data-testid="stSidebar"] button[kind="primary"]:hover,
section[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"]:hover {{
    background-color: {PALETTE['teal']} !important;
    color: {PALETTE['active_fg']} !important;
}}
/* Inactive Nav Item: Clean Flat Left-Aligned Icon + Title */
section[data-testid="stSidebar"] button[kind="secondary"],
section[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] {{
    background-color: transparent !important;
    color: {sb_text} !important;
    border: none !important;
    border-radius: 12px !important;
    width: {sb_btn_w} !important;
    min-height: 46px !important;
    padding: {sb_btn_pad} !important;
    display: flex !important;
    align-items: center !important;
    justify-content: {sb_btn_just} !important;
    gap: 10px !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    box-shadow: none !important;
    transition: background-color 140ms ease, color 140ms ease;
}}
section[data-testid="stSidebar"] button[kind="secondary"] span[data-testid="stIconMaterial"],
section[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] span[data-testid="stIconMaterial"] {{
    color: {sb_icon} !important;
    font-size: 20px !important;
    flex-shrink: 0 !important;
}}
section[data-testid="stSidebar"] button[kind="secondary"]:hover,
section[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover {{
    background-color: {sb_hover_bg} !important;
    color: {sb_hover_fg} !important;
}}
section[data-testid="stSidebar"] button[kind="secondary"]:hover span[data-testid="stIconMaterial"],
section[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover span[data-testid="stIconMaterial"] {{
    color: {sb_hover_fg} !important;
}}
section[data-testid="stSidebar"] button:active {{
    transform: translateY(1px);
}}
/* Sidebar Divider & Nested Sublist Items (Theme: Light/Dark, Language: ID/EN) */
.sb-divider {{
    height: 1px;
    background: {sb_div};
    margin: 8px 6px;
    width: calc(100% - 12px);
}}
section[data-testid="stSidebar"] div[class*="st-key-sb_sub_"] {{
    padding-left: 16px !important;
    border-left: 1.5px solid {sb_div} !important;
    margin-left: 18px !important;
    animation: ddItemIn 320ms cubic-bezier(0.22, 1, 0.36, 1) backwards;
}}
section[data-testid="stSidebar"] div[class*="st-key-sb_sub_"] + div[class*="st-key-sb_sub_"] {{
    animation-delay: 65ms;
}}
section[data-testid="stSidebar"] div[class*="st-key-sb_sub_"] button {{
    min-height: 36px !important;
    padding: 0.36rem 0.75rem !important;
    font-size: 12.5px !important;
    border-radius: 9px !important;
}}
section[data-testid="stSidebar"] div[class*="st-key-sb_sub_"][class*="_active"] button {{
    background-color: {sb_sub_act_bg} !important;
    color: {sb_sub_act_fg} !important;
    font-weight: 600 !important;
}}
section[data-testid="stSidebar"] div[class*="st-key-sb_sub_"][class*="_active"] button span[data-testid="stIconMaterial"] {{
    color: {sb_sub_act_ic} !important;
    font-size: 17px !important;
}}
section[data-testid="stSidebar"] div[class*="st-key-sb_sub_"] button span[data-testid="stIconMaterial"] {{
    font-size: 17px !important;
}}

/* 48px Vertical Gap Spacer Below Top Filter Bar */
.filter-content-spacer {{
    height: 48px;
    width: 100%;
}}

/* Editorial Display Page Headline (Fraunces Regular 400, Tight Negative Tracking per DESIGN.md) */
.qx-page-title {{
    font-family: var(--font-ui-sans) !important;
    font-size: clamp(24px, 2.15vw, 30px) !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
    color: {PALETTE['emerald']} !important;
    margin: 0;
    line-height: 1.08;
}}
.qx-page-title span {{
    font-family: var(--font-ui-sans) !important;
    font-size: clamp(14px, 1.05vw, 16px);
    font-weight: 400;
    letter-spacing: 0px;
    color: {PALETTE['muted']};
    margin-left: 6px;
}}

/* Clean Title-Case Section Heading (Gestalt Proximity: Generous Breath Above, Crisp Gap Below) */
.section-eyebrow {{
    font-family: var(--font-ui-sans) !important;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: -0.015em;
    text-transform: none;
    color: {PALETTE['emerald']};
    padding: 32px 0 8px 2px;
    margin: 0;
    line-height: 1.25;
}}
.section-eyebrow-first {{
    padding-top: 8px;
}}

/* Flat Paper White Elevated Cards (Radius 16px, ZERO Box-Shadow per DESIGN.md) */
.bento-card {{
    background: {PALETTE['white']};
    border-radius: 16px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: none !important;
    min-width: 0;
}}
.bento-hero-outer {{
    padding: 20px 22px 22px 22px;
    min-height: 320px;
    margin-bottom: 0 !important;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.bento-compact {{
    min-height: 152px;
    padding: 20px 22px !important;
    margin-bottom: 0 !important;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.bento-compact-split {{
    padding: 0 !important;
    flex-direction: row !important;
    align-items: stretch !important;
    overflow: hidden !important;
}}
.bento-split-left {{
    flex: 1;
    min-width: 0;
    padding: 20px 14px 20px 22px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.bento-split-strip {{
    width: 72px;
    flex-shrink: 0;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.bento-split-icon {{
    display: block;
    transition: transform 400ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.bento-compact-split:hover .bento-split-icon {{
    transform: scale(1.14);
}}
.stElementContainer:has(.bento-compact):not(:last-child) {{
    margin-bottom: 16px !important;
}}
div[class*="st-key-card_"] {{
    background-color: {PALETTE['white']} !important;
    border: 0px solid transparent !important;
    border-color: transparent !important;
    border-radius: 16px !important;
    padding: 18px 22px 22px 22px !important;
    box-shadow: none !important;
    min-width: 0 !important;
}}
div[class*="st-key-card_p3_drill"] {{
    min-height: 152px !important;
    padding: 20px 22px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}}
div[class*="st-key-card_p3_drill"] [data-testid="stSelectbox"] div[role="group"]::before {{
    display: none !important;
    content: none !important;
}}
div[class*="st-key-card_p3_drill"] [data-testid="stSelectbox"] div[role="group"] {{
    padding-left: 14px !important;
    padding-right: 8px !important;
}}
div[class*="st-key-card_"] > div,
div[class*="st-key-card_"] [data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background-color: transparent !important;
    border: 0px solid transparent !important;
    border-color: transparent !important;
    padding: 0 !important;
    box-shadow: none !important;
}}

/* Equal-height side-by-side Bento chart cards (0px bottom mismatch across all pages) */
div[data-testid="stHorizontalBlock"]:has(div[class*="st-key-card_"]:not([class*="st-key-card_p3_drill"])) {{
    align-items: stretch !important;
}}
div[data-testid="stColumn"]:has(div[class*="st-key-card_"]:not([class*="st-key-card_p3_drill"])):not(:has(.bento-compact)):not(:has(.nested-hero)):not(:has(.bento-leader-card)) {{
    display: flex !important;
    flex-direction: column !important;
}}
div[data-testid="stColumn"]:has(div[class*="st-key-card_"]:not([class*="st-key-card_p3_drill"])):not(:has(.bento-compact)):not(:has(.nested-hero)):not(:has(.bento-leader-card)) div:has(> div[class*="st-key-card_"]),
div[data-testid="stColumn"]:has(div[class*="st-key-card_"]:not([class*="st-key-card_p3_drill"])):not(:has(.bento-compact)):not(:has(.nested-hero)):not(:has(.bento-leader-card)) > div,
div[data-testid="stColumn"]:has(div[class*="st-key-card_"]:not([class*="st-key-card_p3_drill"])):not(:has(.bento-compact)):not(:has(.nested-hero)):not(:has(.bento-leader-card)) div[class*="st-key-card_"] {{
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
}}
div[class*="st-key-card_p1_donut"] {{
    flex: 0 0 auto !important;
    height: auto !important;
}}
.bento-leader-card {{
    background: {PALETTE['white']};
    border-radius: 16px;
    padding: 18px 22px 20px 22px;
    margin-top: 8px;
    margin-bottom: 0 !important;
    display: flex;
    flex-direction: column;
    gap: 10px;
    transition: transform 380ms cubic-bezier(0.22, 1, 0.36, 1), box-shadow 380ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.bento-leader-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, {'0.32' if PALETTE['is_dark'] else '0.07'});
}}
.leader-body {{
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 14px;
}}
.leader-left {{
    display: flex;
    flex-direction: column;
    min-width: 0;
}}
.leader-val {{
    font-size: clamp(32px, 2.85vw, 44px);
    font-weight: 600;
    letter-spacing: -0.04em;
    line-height: 1.0;
    color: {PALETTE['emerald']};
    display: flex;
    align-items: baseline;
    white-space: nowrap;
}}
.leader-channel {{
    font-size: 13.5px;
    font-weight: 600;
    color: {PALETTE['muted']};
    margin-top: 6px;
}}
.leader-right {{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    text-align: right;
    gap: 3px;
    flex-shrink: 0;
}}
.leader-share {{
    font-size: 13px;
    font-weight: 600;
    color: {PALETTE['emerald']};
    white-space: nowrap;
}}
.leader-orders {{
    font-size: 12px;
    font-weight: 500;
    color: {PALETTE['muted']};
    white-space: nowrap;
}}

/* Modern SaaS Data Table (Foto 2 Style — Clean Hairlines, Icon Badges, Dotted Status Pills) */
div[class*="st-key-card_p2_matrix"] {{
    padding: 26px 28px 32px 28px !important;
}}
.sku-highlight-stack {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 4px 0 6px 2px;
    min-height: 98px;
}}
.sku-highlight-top {{
    display: flex;
    align-items: center;
    gap: 12px;
}}
.sku-highlight-big {{
    font-size: clamp(32px, 3.1vw, 44px);
    font-weight: 800;
    letter-spacing: -0.04em;
    color: {PALETTE['emerald']};
    line-height: 1.0;
}}
.sku-highlight-sub {{
    font-size: clamp(20px, 1.85vw, 26px);
    font-weight: 600;
    letter-spacing: -0.025em;
    color: {PALETTE['emerald']};
    opacity: 0.86;
    line-height: 1.18;
    margin-top: 4px;
}}
.sku-highlight-count {{
    font-size: 12px;
    font-weight: 600;
    color: {PALETTE['emerald']};
    background: {PALETTE['pill_bg']};
    border-radius: 999px;
    padding: 5px 12px;
    white-space: nowrap;
}}
.sku-tbl-shell {{
    width: 100%;
    margin-top: 12px;
    margin-bottom: 4px;
    border: 1px solid {PALETTE['hairline']};
    border-radius: 14px;
    overflow: hidden;
    background: {PALETTE['white']};
}}
.sku-tbl-scroll {{
    max-height: 440px;
    overflow-y: auto;
    overflow-x: auto;
}}
.sku-tbl {{
    width: 100%;
    border-collapse: collapse;
    font-family: var(--font-ui-sans);
    font-variant-numeric: tabular-nums;
}}
.sku-tbl thead th {{
    position: sticky;
    top: 0;
    z-index: 5;
    background: {'#162620' if PALETTE['is_dark'] else '#f7f9f8'};
    color: {PALETTE['muted']};
    font-size: 12px;
    font-weight: 600;
    text-align: left;
    padding: 13px 16px;
    border-top: none !important;
    border-left: none !important;
    border-right: none !important;
    border-bottom: 1px solid {PALETTE['hairline']} !important;
    white-space: nowrap;
}}
.sku-tbl thead th.num,
.sku-tbl tbody td.num {{
    text-align: right;
}}
.sku-tbl tbody tr {{
    border-bottom: 1px solid {PALETTE['gridline']};
    transition: background-color 180ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.sku-tbl tbody tr:last-child {{
    border-bottom: none;
}}
.sku-tbl tbody tr:hover {{
    background: {'#182a22' if PALETTE['is_dark'] else '#f4f8f5'};
}}
.sku-tbl tbody td {{
    padding: 13px 16px;
    font-size: 13px;
    color: {PALETTE['charcoal']};
    vertical-align: middle;
    white-space: nowrap;
    border-top: none !important;
    border-left: none !important;
    border-right: none !important;
    border-bottom: none !important;
}}
/* Pill Search Bar inside SKU Performance Card (Foto 2 Style: Full Pill + Right Circular Botanical Search Badge) */
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInput"] [data-testid="InputInstructions"] {{
    display: none !important;
}}
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInputRootElement"] {{
    position: relative !important;
    background-color: {PALETTE['white']} !important;
    border: 1px solid {PALETTE['hairline']} !important;
    border-radius: 999px !important;
    min-height: 46px !important;
    height: 46px !important;
    padding: 4px 5px 4px 20px !important;
    display: flex !important;
    align-items: center !important;
    box-shadow: none !important;
    overflow: hidden !important;
    transition: border-color 200ms cubic-bezier(0.22, 1, 0.36, 1), box-shadow 200ms cubic-bezier(0.22, 1, 0.36, 1) !important;
}}
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInputRootElement"]:hover {{
    border-color: {PALETTE['emerald']} !important;
}}
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInputRootElement"]:focus-within {{
    border-color: {PALETTE['emerald']} !important;
    box-shadow: 0 0 0 2px rgba(4, 63, 46, {'0.32' if PALETTE['is_dark'] else '0.16'}) !important;
}}
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInputRootElement"] > div {{
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    flex: 1 !important;
    min-width: 0 !important;
    padding: 0 !important;
}}
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInputRootElement"]::after {{
    content: "" !important;
    display: inline-block !important;
    width: 36px !important;
    height: 36px !important;
    border-radius: 999px !important;
    flex-shrink: 0 !important;
    margin-left: 8px !important;
    background-color: {PALETTE['btn_bg']} !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: 17px 17px !important;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='{'%23043f2e' if PALETTE['is_dark'] else '%23fcfcfc'}' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='7.5'/%3E%3Cline x1='20.5' y1='20.5' x2='16.4' y2='16.4'/%3E%3C/svg%3E") !important;
    pointer-events: none !important;
    transition: transform 280ms cubic-bezier(0.22, 1, 0.36, 1) !important;
}}
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInputRootElement"]:focus-within::after {{
    transform: scale(1.06) !important;
}}
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInput"] input {{
    background: transparent !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    color: {PALETTE['emerald']} !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    padding: 0 4px 0 0 !important;
    height: 36px !important;
    line-height: 36px !important;
}}
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInput"] input:focus,
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInput"] input:focus-visible,
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInputRootElement"] div,
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInputRootElement"] div:focus,
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInputRootElement"] div:focus-within {{
    outline: none !important;
    border: none !important;
    box-shadow: none !important;
}}
div[class*="st-key-card_p2_matrix"] [data-testid="stTextInput"] input::placeholder {{
    color: {PALETTE['muted']} !important;
    font-weight: 400 !important;
}}
.sku-prod-cell {{
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 240px;
}}
.sku-avatar {{
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.02em;
    flex-shrink: 0;
}}
.sku-prod-text {{
    display: flex;
    flex-direction: column;
    min-width: 0;
}}
.sku-prod-name {{
    font-size: 13px;
    font-weight: 600;
    color: {PALETTE['emerald']};
    max-width: 290px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}
.sku-prod-id {{
    font-size: 11px;
    font-weight: 500;
    color: {PALETTE['muted']};
    margin-top: 2px;
}}
.sku-main-val {{
    font-size: 13px;
    font-weight: 600;
    color: {PALETTE['emerald']};
}}
.sku-sub-val {{
    font-size: 11px;
    color: {PALETTE['muted']};
    margin-top: 2px;
}}
.sku-status-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 11.5px;
    font-weight: 600;
    line-height: 1.2;
}}
.sku-status-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}}
div[class*="st-key-card_"]:has(.hpb-wrap),
div[class*="st-key-card_"]:has(.hpb-wrap) div:has(.hpb-wrap) {{
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
}}
div[class*="st-key-card_"]:has(.spb-wrap),
div[class*="st-key-card_"]:has(.spb-wrap) div:has(.spb-wrap) {{
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
}}

/* Segmented Control Capsule Track (Right-aligned so it sits tightly beside the dropdown filter) */
.stElementContainer:has([data-testid="stButtonGroup"]) {{
    width: 100% !important;
    display: flex !important;
    justify-content: flex-end !important;
}}
div[data-testid="stButtonGroup"] {{
    display: flex !important;
    justify-content: flex-end !important;
    margin-left: auto !important;
}}
div[data-testid="stButtonGroup"] > div {{
    background-color: {PALETTE['track_bg']} !important;
    border-radius: 999px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: none !important;
    display: inline-flex !important;
    align-items: center !important;
    width: fit-content !important;
}}
div[data-testid="stButtonGroup"] button {{
    background-color: transparent !important;
    color: {PALETTE['charcoal']} !important;
    border: none !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 0.36rem 1.05rem !important;
    min-height: 36px !important;
    border-radius: 999px !important;
    white-space: nowrap !important;
    box-shadow: none !important;
    transition: background-color 140ms ease, color 140ms ease;
}}
div[data-testid="stButtonGroup"] button:hover {{
    background-color: rgba(252, 252, 252, 0.55) !important;
    color: {PALETTE['emerald']} !important;
}}
div[data-testid="stButtonGroup"] button[aria-checked="true"],
div[data-testid="stButtonGroup"] button[kind="segmented_controlActive"],
div[data-testid="stButtonGroup"] button[data-testid="stBaseButton-segmented_controlActive"] {{
    background-color: {PALETTE['white']} !important;
    color: {PALETTE['emerald']} !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 999px !important;
    box-shadow: none !important;
}}

.bento-card-header {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 8px;
}}
.bento-title {{
    font-size: 15px;
    font-weight: 500;
    color: {PALETTE['emerald']};
    margin: 0;
    line-height: 1.3;
}}
.bento-sub {{
    font-size: 12.5px;
    font-weight: 400;
    color: {PALETTE['muted']};
    margin: 3px 0 0 0;
    line-height: 1.4;
}}

/* Nested Executive Pass Hero Cards (Near-Square Editorial Proportion + DESIGN.md Palette) */
.nested-hero {{
    border-radius: 16px;
    padding: 22px 22px 20px 22px;
    min-height: 244px;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 14px;
    min-width: 0;
    cursor: pointer;
    transform-origin: center center;
    will-change: transform;
    transition:
        transform 460ms cubic-bezier(0.22, 1, 0.36, 1),
        box-shadow 460ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.nested-hero:hover {{
    transform: translateY(-4px) scale(1.035);
    box-shadow: 0 18px 34px rgba(0, 0, 0, {'0.45' if PALETTE['is_dark'] else '0.16'});
}}
.nested-hero:active {{
    transform: translateY(-2px) scale(1.015);
    transition-duration: 160ms;
}}
.nested-hero .kpi-value {{
    transform-origin: left center;
    transition: transform 520ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.nested-hero:hover .kpi-value {{
    transform: scale(1.04);
}}
.nested-hero .hero-top-row svg {{
    transition: transform 520ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.nested-hero:hover .hero-top-row svg {{
    transform: scale(1.18) translateX(-2px);
}}
@media (prefers-reduced-motion: reduce) {{
    .nested-hero, .nested-hero .kpi-value, .nested-hero .hero-top-row svg {{
        transition: none !important;
    }}
    .nested-hero:hover, .nested-hero:hover .kpi-value, .nested-hero:hover .hero-top-row svg {{
        transform: none !important;
    }}
}}
.nested-emerald {{
    background: {PALETTE['hero_bg']};
    border: {PALETTE['hero_border']};
    color: {PALETTE['hero_fg']};
}}
.nested-teal {{
    background: {PALETTE['hero_bg']};
    border: {PALETTE['hero_border']};
    color: {PALETTE['hero_fg']};
}}
.nested-lime {{
    background: {PALETTE['lime']};
    color: {PALETTE['ink']};
}}
.hero-top-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
}}
.hero-brand-mark {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}
.hero-mid-block {{
    margin: 2px 0;
    min-width: 0;
}}
.hero-sub-label {{
    font-size: 13px;
    font-weight: 400;
    margin-bottom: 2px;
    line-height: 1.3;
}}
/* Uppercase Eyebrow Label (Used on compact cards per DESIGN.md) */
.kpi-label {{
    font-size: 11.5px;
    font-weight: 500;
    text-transform: uppercase;
    margin-bottom: 6px;
    letter-spacing: 0.06em;
}}
/* Large Stat Number (Near-Square Executive Scale, Tight Tracking) */
.kpi-value {{
    font-size: clamp(40px, 3.9vw, 60px);
    font-weight: 600;
    letter-spacing: -0.045em;
    line-height: 1.0;
    margin: 0;
    white-space: nowrap;
    display: flex;
    align-items: baseline;
}}
.kpi-unit {{
    font-size: 0.42em;
    font-weight: 500;
    letter-spacing: -0.01em;
    opacity: 0.82;
}}
.kpi-unit-pre {{
    margin-right: 0.22em;
}}
.kpi-unit-suf {{
    margin-left: 0.24em;
}}
.hero-bottom-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
    padding-top: 4px;
}}
.kpi-meta {{
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.02em;
    line-height: 1.35;
}}

/* Tags & Badges (9999px pill tags, theme-aware) */
.trend-pill-good {{
    display: inline-block;
    background: {PALETTE['mint_tint']};
    color: {PALETTE['good_text']};
    border-radius: 9999px;
    padding: 3px 10px;
    font-size: 11.5px;
    font-weight: 500;
    white-space: nowrap;
}}
.trend-pill-lime {{
    display: inline-block;
    background: {PALETTE['lime']};
    color: {PALETTE['ink']};
    border-radius: 9999px;
    padding: 3px 10px;
    font-size: 11.5px;
    font-weight: 500;
    white-space: nowrap;
}}
.trend-pill-dark {{
    display: inline-block;
    background: {PALETTE['emerald']};
    color: {PALETTE['lime']};
    border-radius: 9999px;
    padding: 3px 10px;
    font-size: 11.5px;
    font-weight: 500;
    white-space: nowrap;
}}
.trend-pill-warn {{
    display: inline-block;
    background: {PALETTE['amber_tint']};
    color: {PALETTE['amber_text']};
    border-radius: 9999px;
    padding: 3px 10px;
    font-size: 11.5px;
    font-weight: 500;
    white-space: nowrap;
}}
.trend-pill-bad {{
    display: inline-block;
    background: {PALETTE['coral_tint']};
    color: {PALETTE['coral_text']};
    border-radius: 9999px;
    padding: 3px 10px;
    font-size: 11.5px;
    font-weight: 500;
    white-space: nowrap;
}}
.kpi-icon-pill {{
    width: 38px;
    height: 38px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: transform 150ms ease;
}}
.kpi-icon-pill:hover {{
    transform: scale(1.06);
}}

/* Filter Selectbox Capsule (Streamlit 1.67 react-aria-ComboBox, Paper White Full-Pill, Flat) */
[data-testid="stSelectbox"] div[role="group"] {{
    background-color: {PALETTE['white']} !important;
    border: 1px solid {PALETTE['hairline']} !important;
    border-radius: 999px !important;
    min-height: 44px !important;
    padding-left: 16px !important;
    padding-right: 10px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    box-shadow: none !important;
    transition: border-color 140ms ease;
}}
[data-testid="stSelectbox"] div[role="group"]:hover {{
    border-color: {PALETTE['emerald']} !important;
}}
[data-testid="stSelectbox"] div[role="group"]:focus-within {{
    border-color: {PALETTE['emerald']} !important;
    box-shadow: 0 0 0 2px rgba(4, 63, 46, 0.22) !important;
}}
[data-testid="stSelectbox"] div[role="group"]::before {{
    content: "" !important;
    display: inline-block !important;
    width: 17px !important;
    height: 17px !important;
    flex-shrink: 0 !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: 17px 17px !important;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='{'%23ebf4e6' if PALETTE['is_dark'] else '%23043f2e'}' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='4' y1='6' x2='20' y2='6'/%3E%3Cline x1='7' y1='12' x2='17' y2='12'/%3E%3Cline x1='10' y1='18' x2='14' y2='18'/%3E%3C/svg%3E") !important;
}}
/* Theme-aware Selectbox Popover Menu with Staggered Easy-Ease Option Cascade */
@keyframes ddMenuDrop {{
    0% {{ opacity: 0; transform: translateY(-6px) scaleY(0.95); }}
    100% {{ opacity: 1; transform: translateY(0) scaleY(1); }}
}}
@keyframes ddItemIn {{
    0% {{ opacity: 0; transform: translateY(-9px) scale(0.97); }}
    100% {{ opacity: 1; transform: translateY(0) scale(1); }}
}}
[data-testid="stPopoverBody"],
div[role="listbox"],
ul[role="listbox"] {{
    background-color: {PALETTE['white']} !important;
    color: {PALETTE['emerald']} !important;
    border: 1px solid {PALETTE['hairline']} !important;
    border-radius: 12px !important;
    transform-origin: top center !important;
    animation: ddMenuDrop 260ms cubic-bezier(0.22, 1, 0.36, 1) backwards !important;
    box-shadow: 0 12px 28px rgba(0, 0, 0, {'0.42' if PALETTE['is_dark'] else '0.10'}) !important;
}}
[role="option"] {{
    background-color: transparent !important;
    color: {PALETTE['emerald']} !important;
    border-radius: 8px !important;
    animation: ddItemIn 320ms cubic-bezier(0.22, 1, 0.36, 1) backwards;
    transition:
        background-color 180ms cubic-bezier(0.22, 1, 0.36, 1),
        transform 220ms cubic-bezier(0.22, 1, 0.36, 1),
        color 180ms ease !important;
}}
[role="listbox"] [role="option"]:nth-child(1),
[role="listbox"] > div > div:nth-child(1) [role="option"] {{ animation-delay: 20ms; }}
[role="listbox"] [role="option"]:nth-child(2),
[role="listbox"] > div > div:nth-child(2) [role="option"] {{ animation-delay: 60ms; }}
[role="listbox"] [role="option"]:nth-child(3),
[role="listbox"] > div > div:nth-child(3) [role="option"] {{ animation-delay: 100ms; }}
[role="listbox"] [role="option"]:nth-child(4),
[role="listbox"] > div > div:nth-child(4) [role="option"] {{ animation-delay: 140ms; }}
[role="listbox"] [role="option"]:nth-child(5),
[role="listbox"] > div > div:nth-child(5) [role="option"] {{ animation-delay: 180ms; }}
[role="listbox"] [role="option"]:nth-child(6),
[role="listbox"] > div > div:nth-child(6) [role="option"] {{ animation-delay: 220ms; }}
[role="listbox"] [role="option"]:nth-child(7),
[role="listbox"] > div > div:nth-child(7) [role="option"] {{ animation-delay: 260ms; }}
[role="listbox"] [role="option"]:nth-child(8),
[role="listbox"] > div > div:nth-child(8) [role="option"] {{ animation-delay: 300ms; }}
[role="listbox"] [role="option"]:nth-child(9),
[role="listbox"] > div > div:nth-child(9) [role="option"] {{ animation-delay: 340ms; }}
[role="listbox"] [role="option"]:nth-child(10),
[role="listbox"] > div > div:nth-child(10) [role="option"] {{ animation-delay: 380ms; }}
[role="listbox"] [role="option"]:nth-child(11),
[role="listbox"] > div > div:nth-child(11) [role="option"] {{ animation-delay: 420ms; }}
[role="listbox"] [role="option"]:nth-child(n+12),
[role="listbox"] > div > div:nth-child(n+12) [role="option"] {{ animation-delay: 450ms; }}
[role="option"]:hover {{
    background-color: {PALETTE['pill_bg']} !important;
    color: {PALETTE['emerald']} !important;
    transform: translateX(4px);
}}
[role="option"][aria-selected="true"] {{
    background-color: {PALETTE['pill_bg']} !important;
    color: {PALETTE['emerald']} !important;
}}
[data-testid="stSelectbox"] div[role="group"] svg {{
    transition: transform 280ms cubic-bezier(0.22, 1, 0.36, 1);
}}
[data-testid="stSelectbox"] div[role="group"]:has(input[aria-expanded="true"]) svg {{
    transform: rotate(180deg);
}}
[data-testid="stSelectbox"] input[role="combobox"] {{
    background: transparent !important;
    border: none !important;
    color: {PALETTE['emerald']} !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    outline: none !important;
}}
[data-testid="stSelectbox"] div[role="group"] button {{
    background: transparent !important;
    border: none !important;
    border-radius: 999px !important;
    color: {PALETTE['emerald']} !important;
}}

/* Compact Mini-Pill Dropdown inside Chart Cards (Matches Foto 2: 'Month v' soft pill, no left icon) */
div[class*="st-key-card_p1_trend"] [data-testid="stSelectbox"] div[role="group"],
div[class*="st-key-card_p3_dual"] [data-testid="stSelectbox"] div[role="group"],
div[class*="st-key-card_p4_radar"] [data-testid="stSelectbox"] div[role="group"] {{
    background-color: {PALETTE['canvas']} !important;
    border: none !important;
    min-height: 36px !important;
    padding-left: 14px !important;
    padding-right: 8px !important;
}}
div[class*="st-key-card_p1_trend"] [data-testid="stSelectbox"] div[role="group"]::before,
div[class*="st-key-card_p3_dual"] [data-testid="stSelectbox"] div[role="group"]::before,
div[class*="st-key-card_p4_radar"] [data-testid="stSelectbox"] div[role="group"]::before {{
    display: none !important;
    content: none !important;
}}

/* Primary Action CTA Buttons (Unified Full-Pill, Theme-Aware) */
[data-testid="stMain"] .stButton > button {{
    background-color: {PALETTE['btn_bg']} !important;
    color: {PALETTE['btn_fg']} !important;
    border: 1px solid {PALETTE['btn_bg']} !important;
    border-radius: 999px !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    min-height: 44px !important;
    height: 44px !important;
    padding: 0 1.25rem !important;
    box-shadow: none !important;
    transition: background-color 140ms ease, border-color 140ms ease, transform 100ms ease;
}}
[data-testid="stMain"] .stButton > button:hover {{
    background-color: {PALETTE['btn_hover_bg']} !important;
    border-color: {PALETTE['btn_hover_bg']} !important;
    color: {PALETTE['btn_hover_fg']} !important;
}}
[data-testid="stMain"] .stButton > button:active {{
    background-color: {PALETTE['emerald_dark']} !important;
    border-color: {PALETTE['emerald_dark']} !important;
    color: {PALETTE['hero_fg']} !important;
    transform: translateY(1px);
}}
[data-testid="stMain"] .stButton > button:focus-visible {{
    outline: none !important;
    box-shadow: 0 0 0 2px {PALETTE['white']}, 0 0 0 4px {PALETTE['chart_primary']} !important;
}}
/* Circular Icon-Only Back Button for Drill-Through Views */
div[class*="st-key-btn_drill_back"] button {{
    width: 44px !important;
    min-width: 44px !important;
    max-width: 44px !important;
    height: 44px !important;
    min-height: 44px !important;
    padding: 0 !important;
    border-radius: 50% !important;
    background-color: {PALETTE['white']} !important;
    color: {PALETTE['emerald']} !important;
    border: 1px solid {PALETTE['hairline']} !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}
div[class*="st-key-btn_drill_back"] button:hover {{
    background-color: {PALETTE['btn_bg']} !important;
    border-color: {PALETTE['btn_bg']} !important;
    color: {PALETTE['btn_fg']} !important;
}}
div[class*="st-key-btn_drill_back"] button span {{
    font-size: 20px !important;
    margin: 0 !important;
}}

/* Full-Capsule Diagonal-Striped Pill Bar Chart (True Semicircle Top & Bottom) */
.spb-wrap {{
    width: 100%;
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    padding: 16px 8px 2px 2px;
    font-family: var(--font-ui-sans);
    user-select: none;
}}
.spb-chart-row {{
    flex: 1 1 auto;
    display: flex;
    align-items: stretch;
    gap: 12px;
}}
.spb-yaxis {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-end;
    min-width: 36px;
    padding-bottom: 0;
    font-size: 11px;
    color: {PALETTE['muted']};
    line-height: 1;
    flex-shrink: 0;
}}
.spb-plot {{
    position: relative;
    flex: 1;
    min-width: 0;
}}
.spb-gridlines {{
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    pointer-events: none;
    z-index: 1;
}}
.spb-gridline {{
    width: 100%;
    border-top: 1px dashed {PALETTE['gridline']};
}}
.spb-bars-layer {{
    position: absolute;
    inset: 0;
    z-index: 2;
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
    gap: 10px;
    padding: 0 8px;
}}
.spb-col {{
    position: relative;
    flex: 1;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
    cursor: pointer;
}}
.spb-capsule {{
    position: relative;
    width: clamp(34px, 4.6vw, 52px);
    border-radius: 9999px !important;
    transition: transform 160ms ease, filter 160ms ease;
    background-image: repeating-linear-gradient(
        -45deg,
        rgba(255, 255, 255, 0.17) 0px,
        rgba(255, 255, 255, 0.17) 4px,
        transparent 4px,
        transparent 10px
    );
}}
.spb-col:hover .spb-capsule {{
    transform: translateY(-2px);
    filter: brightness(1.06);
}}
.spb-peak-anchor {{
    position: absolute;
    top: 0;
    left: 50%;
    transform: translate(-50%, -100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    pointer-events: none;
    z-index: 4;
}}
.spb-peak-badge {{
    background: {PALETTE['chart_badge_bg']};
    color: {PALETTE['chart_badge_fg']};
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 999px;
    white-space: nowrap;
    line-height: 1.2;
}}
.spb-peak-stem {{
    width: 2px;
    height: 10px;
    background: {PALETTE['chart_badge_bg']};
}}
.spb-peak-dot {{
    width: 11px;
    height: 11px;
    border-radius: 50%;
    background: {PALETTE['chart_primary']};
    border: 2.5px solid {PALETTE['white']};
    margin-top: -2px;
    margin-bottom: -6px;
    z-index: 5;
}}
.spb-tip {{
    position: absolute;
    bottom: calc(100% + 10px);
    left: 50%;
    transform: translate(-50%, 4px);
    background: {PALETTE['white']};
    border: 1px solid {PALETTE['hairline']};
    border-radius: 10px;
    padding: 8px 11px;
    color: {PALETTE['emerald']};
    font-size: 11.5px;
    line-height: 1.45;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 140ms ease, transform 140ms ease;
    z-index: 20;
    box-shadow: 0 6px 18px rgba(4, 63, 46, 0.12);
}}
.spb-col:hover .spb-tip {{
    opacity: 1;
    transform: translate(-50%, 0px);
}}
.spb-xaxis-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-top: 12px;
}}
.spb-xaxis-spacer {{
    min-width: 36px;
    flex-shrink: 0;
}}
.spb-xlabels {{
    flex: 1;
    display: flex;
    justify-content: space-around;
    gap: 10px;
    padding: 0 8px;
}}
.spb-xlabel {{
    flex: 1;
    text-align: center;
    font-size: 11.5px;
    font-weight: 500;
    color: {PALETTE['muted']};
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

/* Informative Empty & Error States (R-27, Flat Editorial Hairline) */
.state-card {{
    background: {PALETTE['white']};
    border-radius: 16px;
    padding: 20px 22px;
    margin: 12px 0;
    border-left: 4px solid {PALETTE['emerald']};
}}
.state-card-error {{
    border-left-color: {PALETTE['coral']};
}}
.state-title {{
    font-size: 15px;
    font-weight: 600;
    color: {PALETTE['emerald']};
    margin-bottom: 4px;
}}
.state-desc {{
    font-size: 13px;
    color: {PALETTE['muted']};
    line-height: 1.5;
}}

/* Footnote / Data Provenance Strip */
.provenance-note {{
    font-size: 11.5px;
    color: {PALETTE['muted']};
    padding: 8px 4px 2px 4px;
    line-height: 1.45;
}}

/* Plotly Hover Tooltips: Flat Paper White Editorial Card with Deep Forest Hairline */
.js-plotly-plot .hoverlayer .hovertext path {{
    stroke-linejoin: round !important;
    stroke-width: 1px !important;
}}
.js-plotly-plot .hoverlayer .legend .bg {{
    rx: 12px !important;
    ry: 12px !important;
    stroke: {PALETTE['hairline']} !important;
    stroke-width: 1px !important;
}}

/* Proportional Rounded Bento Treemap (Foto 2 Style in DESIGN.md Botanical Palette) */
.tm-mosaic {{
    display: flex;
    gap: 10px;
    width: 100%;
    height: 290px;
    margin: 8px 0 4px 0;
}}
.tm-col {{
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-width: 0;
    height: 100%;
}}
.tm-row {{
    display: flex;
    gap: 10px;
    min-width: 0;
    min-height: 0;
}}
/* 4-Column BMI 1:1 Square Stacked Overlapping Product Card Deck */
.bmi-deck-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    width: 100%;
    padding: 4px 0 2px 0;
}}
@media (max-width: 1024px) {{
    .bmi-deck-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
}}
@media (max-width: 600px) {{
    .bmi-deck-grid {{
        grid-template-columns: 1fr;
    }}
}}
.bmi-col {{
    background: {PALETTE['canvas']};
    border: {'1px solid ' + PALETTE['hairline'] if PALETTE['is_dark'] else 'none'};
    border-radius: 20px;
    padding: 14px 12px 14px 12px;
    aspect-ratio: 1 / 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
    overflow: visible;
    transition: transform 420ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.bmi-col-head {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 0 4px 12px 4px;
    flex-shrink: 0;
}}
.bmi-col-title {{
    font-size: 13.5px;
    font-weight: 700;
    color: {PALETTE['emerald']};
    letter-spacing: -0.01em;
    white-space: nowrap;
}}
.bmi-col-total {{
    font-size: 11px;
    font-weight: 600;
    color: {PALETTE['muted']};
    background: {PALETTE['white']};
    border-radius: 999px;
    padding: 3px 9px;
    white-space: nowrap;
}}
.bmi-stack {{
    flex: 1;
    display: flex;
    flex-direction: column;
    position: relative;
    min-height: 0;
}}
.bmi-stack-card {{
    flex: 1;
    position: relative;
    border-radius: 20px;
    padding: 14px 16px 26px 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition:
        transform 440ms cubic-bezier(0.22, 1, 0.36, 1),
        box-shadow 440ms cubic-bezier(0.22, 1, 0.36, 1),
        opacity 340ms cubic-bezier(0.22, 1, 0.36, 1),
        filter 340ms cubic-bezier(0.22, 1, 0.36, 1);
    will-change: transform, box-shadow;
    cursor: pointer;
    min-width: 0;
    min-height: 0;
}}
.bmi-stack-card:last-child {{
    padding-bottom: 16px;
}}
.bmi-stack-card + .bmi-stack-card {{
    margin-top: -18px;
    box-shadow: 0 -6px 16px rgba(0, 0, 0, {'0.34' if PALETTE['is_dark'] else '0.10'});
}}
.bmi-stack-card:hover {{
    transform: translateY(-9px) scale(1.02);
    box-shadow: 0 14px 28px rgba(0, 0, 0, {'0.42' if PALETTE['is_dark'] else '0.16'});
}}
.bmi-stack-card:first-child:not(:last-child):hover {{
    transform: translateY(-10px) scale(1.022);
    box-shadow: 0 16px 30px rgba(0, 0, 0, {'0.44' if PALETTE['is_dark'] else '0.18'});
}}
.bmi-stack-card:first-child:not(:last-child):hover + .bmi-stack-card {{
    transform: translateY(15px) scale(0.974);
    opacity: 0.90;
    box-shadow: 0 6px 16px rgba(0, 0, 0, {'0.24' if PALETTE['is_dark'] else '0.06'});
}}
.bmi-stack-card:last-child:not(:first-child):hover {{
    transform: translateY(-10px) scale(1.022);
    box-shadow: 0 -8px 24px rgba(0, 0, 0, {'0.38' if PALETTE['is_dark'] else '0.12'}), 0 14px 28px rgba(0, 0, 0, {'0.38' if PALETTE['is_dark'] else '0.14'});
}}
.bmi-stack:has(.bmi-stack-card:last-child:not(:first-child):hover) .bmi-stack-card:first-child {{
    transform: translateY(-4px) scale(0.974);
    opacity: 0.86;
}}
.bmi-card-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
}}
.bmi-icon-badge {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: transform 420ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.bmi-stack-card:hover .bmi-icon-badge {{
    transform: scale(1.1) rotate(-4deg);
}}
.bmi-card-share {{
    font-size: 10.5px;
    font-weight: 700;
    border-radius: 999px;
    padding: 2px 8px;
    white-space: nowrap;
    transition: transform 420ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.bmi-stack-card:hover .bmi-card-share {{
    transform: scale(1.05);
}}
.bmi-card-meta {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    font-size: 11px;
    font-weight: 500;
    margin-bottom: 3px;
}}
.bmi-card-main {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 8px;
}}
.bmi-card-prod {{
    font-size: 16px;
    font-weight: 700;
    letter-spacing: -0.015em;
    line-height: 1.2;
    white-space: nowrap;
}}
.bmi-card-val {{
    font-size: clamp(22px, 1.85vw, 28px);
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.0;
    white-space: nowrap;
}}

/* Rounded Matrix Heatmap (GitHub/Editorial Style, Theme-Aware, Animated) */
@keyframes hmCellPop {{
    0% {{ opacity: 0; transform: scale(0.78); }}
    100% {{ opacity: 1; transform: scale(1); }}
}}
.hm-wrap {{
    width: 100%;
    padding: 8px 4px 6px 2px;
    font-family: var(--font-ui-sans);
    user-select: none;
}}
.hm-grid {{
    display: grid;
    grid-template-columns: 74px repeat(10, minmax(0, 1fr));
    gap: 6px;
    align-items: center;
}}
.hm-col-head {{
    text-align: center;
    font-size: 10.5px;
    font-weight: 500;
    color: {PALETTE['muted']};
    padding-bottom: 4px;
    white-space: nowrap;
}}
.hm-row-label {{
    font-size: 11.5px;
    font-weight: 600;
    color: {PALETTE['emerald']};
    text-align: right;
    padding-right: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
.hm-cell {{
    position: relative;
    z-index: 1;
    height: 48px;
    border-radius: 10px;
    transition: transform 150ms ease, filter 150ms ease;
    cursor: pointer;
    animation: hmCellPop 420ms cubic-bezier(0.22, 1, 0.36, 1) backwards;
}}
.hm-cell-peak {{
    z-index: 20 !important;
}}
.hm-cell:hover {{
    transform: scale(1.06);
    filter: brightness(1.05);
    z-index: 40 !important;
}}
.hm-peak-dot {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 11px;
    height: 11px;
    border-radius: 50%;
    background: {PALETTE['lime']};
    border: 2.5px solid {PALETTE['white']};
    pointer-events: none;
}}
.hm-peak-pill {{
    position: absolute;
    top: calc(100% + 7px);
    background: {PALETTE['chart_badge_bg']};
    color: {PALETTE['chart_badge_fg']};
    font-size: 10.5px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 999px;
    white-space: nowrap;
    pointer-events: none;
    z-index: 12;
    box-shadow: 0 4px 12px rgba(0, 0, 0, {'0.32' if PALETTE['is_dark'] else '0.12'});
}}
.hm-peak-pill-above {{
    top: auto;
    bottom: calc(100% + 7px);
}}
.hm-tip {{
    position: absolute;
    bottom: calc(100% + 8px);
    left: 50%;
    transform: translate(-50%, 4px);
    background: {PALETTE['white']};
    border: 1px solid {PALETTE['hairline']};
    border-radius: 10px;
    padding: 8px 11px;
    color: {PALETTE['emerald']};
    font-size: 11.5px;
    line-height: 1.45;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transition: opacity 130ms ease, transform 130ms ease;
    z-index: 50;
    box-shadow: 0 6px 18px rgba(0, 0, 0, {'0.35' if PALETTE['is_dark'] else '0.12'});
}}
.hm-cell:hover .hm-tip {{
    opacity: 1;
    visibility: visible;
    transform: translate(-50%, 0px);
}}
.hm-cell-left .hm-tip {{
    left: 0;
    transform: translate(0, 4px);
}}
.hm-cell-left:hover .hm-tip {{
    transform: translate(0, 0);
}}
.hm-cell-right .hm-tip {{
    left: auto;
    right: 0;
    transform: translate(0, 4px);
}}
.hm-cell-right:hover .hm-tip {{
    transform: translate(0, 0);
}}

/* Full-Pill Horizontal Bar Charts (True Semicircle Left & Right Caps, Stacked & Single) */
@keyframes hpbGrowX {{
    0% {{ transform: scaleX(0.04); opacity: 0.35; }}
    100% {{ transform: scaleX(1); opacity: 1; }}
}}
.hpb-wrap {{
    width: 100%;
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    padding: 2px 2px 4px 2px;
    font-family: var(--font-ui-sans);
    user-select: none;
}}
.hpb-legend {{
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 14px;
    padding: 2px 2px 10px 2px;
    margin-bottom: 12px;
    border-bottom: 1px solid {PALETTE['gridline']};
    font-size: 11.5px;
    font-weight: 500;
    color: {PALETTE['muted']};
    white-space: nowrap;
    flex-wrap: wrap;
}}
.hpb-leg-item {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
}}
.hpb-leg-dot {{
    width: 10px;
    height: 10px;
    border-radius: 999px;
    display: inline-block;
    flex-shrink: 0;
}}
.hpb-rows {{
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 14px;
    padding: 4px 0 2px 0;
}}
.hpb-row {{
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    gap: 14px;
    cursor: pointer;
}}
.hpb-row:hover {{
    z-index: 60 !important;
}}
.hpb-label {{
    width: 96px;
    flex-shrink: 0;
    text-align: right;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.02em;
    color: {PALETTE['muted']};
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
.hpb-label-wide {{
    width: 165px;
}}
.hpb-track {{
    flex: 1;
    min-width: 0;
    display: flex;
    align-items: center;
    height: 20px;
}}
.hpb-bar-pill {{
    height: 20px;
    min-width: 18px;
    border-radius: 9999px;
    overflow: hidden;
    display: flex;
    transform-origin: left center;
    animation: hpbGrowX 580ms cubic-bezier(0.22, 1, 0.36, 1) backwards;
    transition: filter 140ms ease, transform 140ms ease;
}}
.hpb-row:hover .hpb-bar-pill {{
    filter: brightness(1.06);
    transform: translateY(-1px);
}}
.hpb-seg {{
    height: 100%;
    min-width: 0;
}}
.hpb-tip {{
    position: absolute;
    bottom: calc(100% + 6px);
    left: 110px;
    background: {PALETTE['white']};
    border: 1px solid {PALETTE['hairline']};
    border-radius: 10px;
    padding: 8px 12px;
    color: {PALETTE['emerald']};
    font-size: 11.5px;
    line-height: 1.45;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transition: opacity 90ms ease, transform 90ms ease;
    transform: translateY(4px);
    z-index: 80;
    box-shadow: 0 6px 18px rgba(0, 0, 0, {'0.35' if PALETTE['is_dark'] else '0.12'});
}}
.hpb-row-first .hpb-tip {{
    bottom: auto;
    top: calc(100% + 6px);
    transform: translateY(-4px);
}}
.hpb-row:hover .hpb-tip {{
    opacity: 1;
    visibility: visible;
    transform: translateY(0px);
}}

/* Channel 360-Degree Segmented Donut Ring (Foto 2 Style + Bidirectional Easy-Ease Hover) */
.arc-wrap {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 4px 2px 2px 2px;
}}
.arc-svg-box {{
    flex: 0.96;
    display: flex;
    justify-content: center;
    align-items: center;
    min-width: 0;
}}
.arc-seg {{
    transform-box: view-box;
    cursor: pointer;
    transition:
        transform 420ms cubic-bezier(0.22, 1, 0.36, 1),
        opacity 320ms cubic-bezier(0.22, 1, 0.36, 1),
        filter 360ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.arc-legend {{
    flex: 1.04;
    display: flex;
    flex-direction: column;
    gap: 18px;
    min-width: 0;
}}
.arc-stat-item {{
    display: flex;
    align-items: center;
    gap: 11px;
    cursor: pointer;
    transform-origin: left center;
    transition:
        transform 420ms cubic-bezier(0.22, 1, 0.36, 1),
        opacity 320ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.arc-pill-bar {{
    width: 6px;
    height: 36px;
    border-radius: 999px;
    flex-shrink: 0;
    transition: transform 420ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.arc-stat-body {{
    display: flex;
    flex-direction: column;
    min-width: 0;
}}
.arc-stat-top {{
    display: flex;
    align-items: baseline;
    gap: 7px;
    flex-wrap: nowrap;
}}
.arc-stat-val {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: {PALETTE['emerald']};
    line-height: 1.05;
    flex-shrink: 0;
}}
.arc-stat-name {{
    font-size: 13px;
    font-weight: 500;
    color: {PALETTE['muted']};
    line-height: 1.2;
    white-space: nowrap;
}}
.arc-stat-sub {{
    font-size: 11px;
    color: {PALETTE['muted']};
    margin-top: 3px;
    opacity: 0.85;
}}
/* Synchronized Bidirectional Hover: Segment <-> Legend Item (Easy-Ease Scale-Up) */
.arc-wrap:has(.arc-seg-0:hover) .arc-seg-0,
.arc-wrap:has(.arc-leg-0:hover) .arc-seg-0,
.arc-wrap:has(.arc-seg-1:hover) .arc-seg-1,
.arc-wrap:has(.arc-leg-1:hover) .arc-seg-1,
.arc-wrap:has(.arc-seg-2:hover) .arc-seg-2,
.arc-wrap:has(.arc-leg-2:hover) .arc-seg-2 {{
    transform: scale(1.065);
    filter: drop-shadow(0 6px 14px rgba(0, 0, 0, {'0.42' if PALETTE['is_dark'] else '0.18'}));
}}
.arc-wrap:has(.arc-seg-0:hover) .arc-seg:not(.arc-seg-0),
.arc-wrap:has(.arc-leg-0:hover) .arc-seg:not(.arc-seg-0),
.arc-wrap:has(.arc-seg-1:hover) .arc-seg:not(.arc-seg-1),
.arc-wrap:has(.arc-leg-1:hover) .arc-seg:not(.arc-seg-1),
.arc-wrap:has(.arc-seg-2:hover) .arc-seg:not(.arc-seg-2),
.arc-wrap:has(.arc-leg-2:hover) .arc-seg:not(.arc-seg-2) {{
    opacity: 0.42;
}}
.arc-wrap:has(.arc-seg-0:hover) .arc-leg-0,
.arc-wrap:has(.arc-leg-0:hover) .arc-leg-0,
.arc-wrap:has(.arc-seg-1:hover) .arc-leg-1,
.arc-wrap:has(.arc-leg-1:hover) .arc-leg-1,
.arc-wrap:has(.arc-seg-2:hover) .arc-leg-2,
.arc-wrap:has(.arc-leg-2:hover) .arc-leg-2 {{
    transform: scale(1.08) translateX(5px);
}}
.arc-wrap:has(.arc-seg-0:hover) .arc-leg-0 .arc-pill-bar,
.arc-wrap:has(.arc-leg-0:hover) .arc-leg-0 .arc-pill-bar,
.arc-wrap:has(.arc-seg-1:hover) .arc-leg-1 .arc-pill-bar,
.arc-wrap:has(.arc-leg-1:hover) .arc-leg-1 .arc-pill-bar,
.arc-wrap:has(.arc-seg-2:hover) .arc-leg-2 .arc-pill-bar,
.arc-wrap:has(.arc-leg-2:hover) .arc-leg-2 .arc-pill-bar {{
    transform: scaleY(1.14);
}}
.arc-wrap:has(.arc-seg-0:hover) .arc-stat-item:not(.arc-leg-0),
.arc-wrap:has(.arc-leg-0:hover) .arc-stat-item:not(.arc-leg-0),
.arc-wrap:has(.arc-seg-1:hover) .arc-stat-item:not(.arc-leg-1),
.arc-wrap:has(.arc-leg-1:hover) .arc-stat-item:not(.arc-leg-1),
.arc-wrap:has(.arc-seg-2:hover) .arc-stat-item:not(.arc-leg-2),
.arc-wrap:has(.arc-leg-2:hover) .arc-stat-item:not(.arc-leg-2) {{
    opacity: 0.46;
}}

/* Smooth Motion & Tabular Number Transitions (60fps GPU-Composited, Reduced-Motion Safe) */
.anim-num, .kpi-value, .arc-stat-val, .bmi-card-val {{
    font-variant-numeric: tabular-nums;
}}
@keyframes spbGrowY {{
    0% {{ transform: scaleY(0.06); opacity: 0.35; }}
    100% {{ transform: scaleY(1); opacity: 1; }}
}}
@keyframes spbBadgePop {{
    0% {{ opacity: 0; transform: translate(-50%, calc(-100% + 8px)) scale(0.88); }}
    100% {{ opacity: 1; transform: translate(-50%, -100%) scale(1); }}
}}
@keyframes arcDraw {{
    0% {{ stroke-dashoffset: 620; opacity: 0.25; }}
    100% {{ stroke-dashoffset: 0; opacity: 1; }}
}}
@keyframes radarBloom {{
    0% {{ transform: scale(0.28); opacity: 0.15; }}
    100% {{ transform: scale(1); opacity: 1; }}
}}
@keyframes deckRise {{
    0% {{ opacity: 0; transform: translateY(14px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes plotlySoftEnter {{
    0% {{ opacity: 0.35; transform: scale(0.975); }}
    100% {{ opacity: 1; transform: scale(1); }}
}}
@keyframes plotlyLineSweep {{
    0% {{ clip-path: inset(-16% 100% -16% 0); opacity: 0.65; }}
    100% {{ clip-path: inset(-16% 0% -16% 0); opacity: 1; }}
}}
@keyframes plotlyAnnotPop {{
    0% {{ opacity: 0; transform: translateY(8px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes plotlyBarGrowX {{
    0% {{ transform: scaleX(0.03); opacity: 0.35; }}
    100% {{ transform: scaleX(1); opacity: 1; }}
}}
.spb-capsule {{
    transform-origin: bottom center;
    transition: height 580ms cubic-bezier(0.22, 1, 0.36, 1), transform 160ms ease, filter 160ms ease;
}}
.spb-peak-anchor {{
    animation: spbBadgePop 420ms cubic-bezier(0.22, 1, 0.36, 1) 180ms both;
}}
.arc-path-anim {{
    stroke-dasharray: 620;
    stroke-dashoffset: 0;
    animation: arcDraw 720ms cubic-bezier(0.22, 1, 0.36, 1) backwards;
}}
.radar-bloom-group {{
    transform-origin: 240px 172px;
    animation: radarBloom 560ms cubic-bezier(0.22, 1, 0.36, 1) backwards;
}}
.radar-axis-node {{
    cursor: pointer;
}}
.radar-dot {{
    transform-box: view-box;
    transition:
        transform 420ms cubic-bezier(0.22, 1, 0.36, 1),
        fill 320ms cubic-bezier(0.22, 1, 0.36, 1),
        stroke 320ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.radar-halo {{
    transform-box: view-box;
    opacity: 0;
    pointer-events: none;
    transition:
        transform 460ms cubic-bezier(0.22, 1, 0.36, 1),
        opacity 360ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.radar-label-g {{
    transform-box: view-box;
    transition: transform 420ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.radar-lbl-name,
.radar-lbl-val {{
    transition: fill 300ms cubic-bezier(0.22, 1, 0.36, 1);
}}
.radar-axis-node:hover .radar-dot {{
    transform: scale(1.65);
    fill: {'#fcfcfc' if PALETTE['is_dark'] else '#78c51c'};
    stroke: {'#c8f169' if PALETTE['is_dark'] else '#043f2e'};
}}
.radar-axis-node:hover .radar-halo {{
    transform: scale(2.8);
    opacity: {'0.26' if PALETTE['is_dark'] else '0.24'};
}}
.radar-axis-node:hover .radar-label-g {{
    transform: scale(1.16);
}}
.radar-axis-node:hover .radar-lbl-name {{
    fill: {PALETTE['emerald']};
}}
.radar-axis-node:hover .radar-lbl-val {{
    fill: {'#c8f169' if PALETTE['is_dark'] else '#2a6f2b'};
}}
.bmi-stack-card {{
    animation: deckRise 440ms cubic-bezier(0.22, 1, 0.36, 1) backwards;
}}
.yv-plotly-pulse {{
    animation: plotlySoftEnter 460ms cubic-bezier(0.22, 1, 0.36, 1) both;
}}
.yv-line-sweep {{
    animation: plotlyLineSweep 780ms cubic-bezier(0.22, 1, 0.36, 1) both;
}}
.yv-annot-pop {{
    animation: plotlyAnnotPop 420ms cubic-bezier(0.22, 1, 0.36, 1) 280ms both;
}}
.yv-bar-growx {{
    transform-box: fill-box;
    transform-origin: left center;
    animation: plotlyBarGrowX 620ms cubic-bezier(0.22, 1, 0.36, 1) both;
}}
.stElementContainer:has(iframe[height="1"]) {{
    position: fixed !important;
    bottom: 0 !important;
    right: 0 !important;
    width: 1px !important;
    height: 1px !important;
    opacity: 0 !important;
    pointer-events: none !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
}}
@media (prefers-reduced-motion: reduce) {{
    .spb-capsule, .spb-peak-anchor, .arc-path-anim, .arc-seg, .arc-stat-item, .arc-pill-bar,
    .radar-bloom-group, .bmi-stack-card,
    .radar-dot, .radar-halo, .radar-label-g, .radar-lbl-name, .radar-lbl-val,
    [data-testid="stPopoverBody"], div[role="listbox"], ul[role="listbox"], [role="option"],
    section[data-testid="stSidebar"] div[class*="st-key-sb_sub_"],
    .yv-plotly-pulse, .yv-line-sweep, .yv-annot-pop, .yv-bar-growx {{
        animation: none !important;
        transition: none !important;
    }}
}}

/* Seamless full-bleed rounded iframe aligned flush left-right with cards */
iframe[title="streamlit.components.v1.html"],
[data-testid="stIFrame"] iframe {{
    width: 100% !important;
    border-radius: 18px !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    display: block !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}}
[data-testid="stIFrame"] {{
    width: 100% !important;
    border: none !important;
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
}}

/* Responsive Reflow Breakpoints (R-03) */
@media (max-width: 1100px) {{
    .block-container {{
        padding-left: 1.75rem !important;
        padding-right: 1.75rem !important;
    }}
    .yv-brand-header {{
        margin-left: -1.75rem;
        margin-right: -1.75rem;
        width: calc(100% + 3.5rem);
        padding-left: 1.75rem;
        padding-right: 1.75rem;
    }}
}}
@media (max-width: 768px) {{
    .block-container,
    [data-testid="stMainBlockContainer"] {{
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-top: 0 !important;
    }}
    .yv-brand-header {{
        margin-left: -0.75rem;
        margin-right: -0.75rem;
        width: calc(100% + 1.5rem);
        padding-left: 0.75rem;
        padding-right: 0.75rem;
        height: 64px;
        margin-bottom: 18px;
    }}
    .bento-card {{
        border-radius: 16px;
        padding: 14px 16px;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[class*="st-key-card_"] {{
        border-radius: 16px !important;
        padding: 12px 14px !important;
    }}
}}
</style>"""
    st.markdown(css, unsafe_allow_html=True)


def render_brand_header():
    """Renders the full-bleed edge-to-edge Chartreuse Lime brand header with YuuukosooVexa wordmark & 4-point star."""
    star_svg = (
        '<svg class="yv-brand-star" width="21" height="23" viewBox="0 0 24 26" fill="none" aria-hidden="true">'
        '<path d="M12 0.8L13.7 10.6L23.2 13L13.7 15.4L12 25.2L10.3 15.4L0.8 13L10.3 10.6L12 0.8Z" fill="#043f2e"/>'
        '</svg>'
    )
    html = (
        '<header class="yv-brand-header" role="banner" aria-label="YuuukosooVexa Header">'
        '<div class="yv-brand-lockup">'
        '<span class="yv-brand-word">YuuukosooVexa</span>'
        f'{star_svg}'
        '</div>'
        '</header>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_top_header(source_badge: str):
    # Kept as helper if needed, unused in minimalist icon-rail layout
    pass


def render_page_title(bold_part: str, muted_part: str):
    st.markdown(
        f'<div class="qx-page-title">{bold_part} <span>{muted_part}</span></div>',
        unsafe_allow_html=True,
    )


def render_section_eyebrow(label: str):
    is_first = label.strip().startswith("01")
    clean = label.split("·", 1)[-1].strip() if "·" in label else label
    cls = "section-eyebrow section-eyebrow-first" if is_first else "section-eyebrow"
    st.markdown(
        f'<div class="{cls}">{clean}</div>',
        unsafe_allow_html=True,
    )


def render_nested_hero_card(
    outer_title: str,
    outer_sub: str,
    kpi_label: str,
    kpi_value: str,
    kpi_meta: str,
    variant: str = "emerald",
    badge_html: str = "",
):
    is_dark = variant in ("emerald", "teal")
    brand_color = PALETTE["hero_fg"] if is_dark else "#043f2e"
    wave_color = PALETTE["lime"] if is_dark else "#043f2e"
    label_color = PALETTE["hero_label"] if is_dark else "#043f2e"
    meta_color = PALETTE["hero_meta"] if is_dark else "#043f2e"

    # Format kpi_label cleanly into natural title case (like "Credit Card" in reference)
    nice_label = (
        kpi_label.title()
        .replace("(Inr)", "(INR)")
        .replace("Aqi", "AQI")
        .replace(" Us ", " US ")
        .replace("Sku", "SKU")
        .replace("Mrp", "MRP")
    )

    # Split kpi_meta into left & right footer items (like "**** 909090" vs "EXP 09/26")
    if " | " in kpi_meta:
        left_meta, right_meta = kpi_meta.split(" | ", 1)
    else:
        left_meta = kpi_meta
        right_meta = "DWH VERIFIED" if is_dark else "LIVE MART"

    brand_text = "YV · DWH" if is_dark else "YV · VOL"
    wave_svg = (
        f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        f'<path d="M8.5 14.5a3.5 3.5 0 0 0 0-5" stroke="{wave_color}" stroke-width="1.8" stroke-linecap="round"/>'
        f'<path d="M12 17a7 7 0 0 0 0-10" stroke="{wave_color}" stroke-width="1.8" stroke-linecap="round"/>'
        f'<path d="M15.5 19.5a10.5 10.5 0 0 0 0-15" stroke="{wave_color}" stroke-width="1.8" stroke-linecap="round"/>'
        f'</svg>'
    )

    import re as _re
    slug_id = _re.sub(r"[^a-z0-9]+", "_", f"hero_{outer_title}_{kpi_label}".lower()).strip("_")

    # Split currency prefix and unit suffix so the number itself dominates (like "$6.4K")
    val_str = str(kpi_value).strip()
    m_val = _re.match(r"^([A-Za-z]+\s+)?([+-]?\d[\d,]*(?:\.\d+)?[KMB%]?)(\s+[A-Za-z/]+)?$", val_str)
    if m_val:
        pre_txt = (m_val.group(1) or "").strip()
        num_txt = m_val.group(2)
        suf_txt = (m_val.group(3) or "").strip()
    else:
        pre_txt, num_txt, suf_txt = "", val_str, ""
    pre_html = f'<span class="kpi-unit kpi-unit-pre">{pre_txt}</span>' if pre_txt else ""
    suf_html = f'<span class="kpi-unit kpi-unit-suf">{suf_txt}</span>' if suf_txt else ""

    html = (
        f'<div class="bento-card bento-hero-outer">'
        f'<div class="bento-card-header" style="margin-bottom:14px;">'
        f'<div class="bento-title">{outer_title}</div>'
        f'</div>'
        f'<div class="nested-hero nested-{variant}">'
        f'<div class="hero-top-row">'
        f'<span class="hero-brand-mark" style="color:{brand_color};">{brand_text}</span>'
        f'{wave_svg}</div>'
        f'<div class="hero-mid-block">'
        f'<div class="hero-sub-label" style="color:{label_color};">{nice_label}</div>'
        f'<div class="kpi-value">{pre_html}<span id="yv_num_{slug_id}" class="anim-num">{num_txt}</span>{suf_html}</div>'
        f'</div>'
        f'<div class="hero-bottom-row">'
        f'<span class="kpi-meta" style="color:{meta_color};">{left_meta}</span>'
        f'<span class="kpi-meta" style="color:{meta_color};">{right_meta}</span>'
        f'</div></div></div>'
    )
    st.markdown(html, unsafe_allow_html=True)




def render_kpi_icon_badge(icon_name: str, tone: str = "good", tooltip: str = "") -> str:
    """Returns a sleek 38px circular icon-only badge with accessible hover tooltip."""
    import html as _html

    tone_map = {
        "good": (PALETTE["mint_tint"], PALETTE["good_text"]),
        "warn": (PALETTE["amber_tint"], PALETTE["amber_text"]),
        "bad": (PALETTE["coral_tint"], PALETTE["coral_text"]),
    }
    bg, fg = tone_map.get(tone, tone_map["good"])
    icons = {
        "check": '<path d="M20 6L9 17l-5-5" />',
        "percent": '<line x1="19" y1="5" x2="5" y2="19" /><circle cx="6.5" cy="6.5" r="2.5" /><circle cx="17.5" cy="17.5" r="2.5" />',
        "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />',
        "trend_up": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17" /><polyline points="16 7 22 7 22 13" />',
        "trend_down": '<polyline points="22 17 13.5 8.5 8.5 13.5 2 7" /><polyline points="16 17 22 17 22 11" />',
        "alert": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" />',
        "moon": '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />',
        "tag": '<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z" /><line x1="7" y1="7" x2="7.01" y2="7" />',
        "bag": '<path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z" /><line x1="3" y1="6" x2="21" y2="6" /><path d="M16 10a4 4 0 0 1-8 0" />',
    }
    svg_inner = icons.get(icon_name, icons["check"])
    tip_esc = _html.escape(tooltip)
    return (
        f'<span class="kpi-icon-pill" title="{tip_esc}" aria-label="{tip_esc}" '
        f'style="background:{bg}; color:{fg};">'
        f'<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{svg_inner}</svg>'
        f'</span>'
    )


def render_compact_kpi_card(
    label: str,
    value: str,
    badge_html: str = "",
    sub: str = "",
    accent_strip: str | None = None,
    strip_tone: str = "forest",
    strip_tooltip: str = "",
):
    import html as _html
    import re as _re

    slug_id = _re.sub(r"[^a-z0-9]+", "_", f"cmp_{label}".lower()).strip("_")
    sub_html = f'<div class="bento-sub" style="margin-top:8px;">{sub}</div>' if sub else ""

    if accent_strip:
        tip_esc = _html.escape(strip_tooltip)
        if strip_tone == "lime":
            strip_bg = "#c8f169"
            strip_fg = "#043f2e"
        else:
            strip_bg = "#2a6f2b" if PALETTE["is_dark"] else "#043f2e"
            strip_fg = "#fcfcfc"

        strip_icons = {
            "exclamation": (
                f'<svg class="bento-split-icon" width="32" height="32" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
                f'<rect x="10.2" y="3" width="3.6" height="11.5" rx="1.8" fill="{strip_fg}" />'
                f'<circle cx="12" cy="19.2" r="2.1" fill="{strip_fg}" />'
                f'</svg>'
            ),
            "alert": (
                f'<svg class="bento-split-icon" width="32" height="32" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
                f'<rect x="10.2" y="3" width="3.6" height="11.5" rx="1.8" fill="{strip_fg}" />'
                f'<circle cx="12" cy="19.2" r="2.1" fill="{strip_fg}" />'
                f'</svg>'
            ),
            "moon": (
                f'<svg class="bento-split-icon" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="{strip_fg}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                f'<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" /></svg>'
            ),
            "check": (
                f'<svg class="bento-split-icon" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="{strip_fg}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                f'<path d="M20 6L9 17l-5-5" /></svg>'
            ),
            "percent": (
                f'<svg class="bento-split-icon" width="29" height="29" viewBox="0 0 24 24" fill="none" stroke="{strip_fg}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                f'<line x1="19" y1="5" x2="5" y2="19" /><circle cx="6.5" cy="6.5" r="2.5" /><circle cx="17.5" cy="17.5" r="2.5" /></svg>'
            ),
            "star": (
                f'<svg class="bento-split-icon" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="{strip_fg}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                f'<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" /></svg>'
            ),
            "trend_up": (
                f'<svg class="bento-split-icon" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="{strip_fg}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                f'<polyline points="22 7 13.5 15.5 8.5 10.5 2 17" /><polyline points="16 7 22 7 22 13" /></svg>'
            ),
            "trend_down": (
                f'<svg class="bento-split-icon" width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="{strip_fg}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                f'<polyline points="22 17 13.5 8.5 8.5 13.5 2 7" /><polyline points="16 17 22 17 22 11" /></svg>'
            ),
            "tag": (
                f'<svg class="bento-split-icon" width="29" height="29" viewBox="0 0 24 24" fill="none" stroke="{strip_fg}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                f'<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z" /><line x1="7" y1="7" x2="7.01" y2="7" /></svg>'
            ),
            "bag": (
                f'<svg class="bento-split-icon" width="29" height="29" viewBox="0 0 24 24" fill="none" stroke="{strip_fg}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                f'<path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z" /><line x1="3" y1="6" x2="21" y2="6" /><path d="M16 10a4 4 0 0 1-8 0" /></svg>'
            ),
        }
        icon_svg = strip_icons.get(accent_strip, strip_icons["check"])
        html = (
            f'<div class="bento-card bento-compact bento-compact-split">'
            f'<div class="bento-split-left">'
            f'<div class="kpi-label" style="color:{PALETTE["muted"]}; margin-bottom:0;">{label}</div>'
            f'<div style="display:flex; align-items:center; gap:8px; margin:6px 0;">'
            f'<div id="yv_num_{slug_id}" class="anim-num" style="font-size:clamp(24px, 1.85vw, 29px); font-weight:500; letter-spacing:-0.018em; color:{PALETTE["emerald"]}; line-height:1.12;">{value}</div>'
            f'</div>{sub_html}</div>'
            f'<div class="bento-split-strip" style="background:{strip_bg};" title="{tip_esc}" aria-label="{tip_esc}">{icon_svg}</div>'
            f'</div>'
        )
    else:
        html = (
            f'<div class="bento-card bento-compact">'
            f'<div class="kpi-label" style="color:{PALETTE["muted"]}; margin-bottom:0;">{label}</div>'
            f'<div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap; margin:6px 0;">'
            f'<div id="yv_num_{slug_id}" class="anim-num" style="font-size:clamp(24px, 1.85vw, 29px); font-weight:500; letter-spacing:-0.018em; color:{PALETTE["emerald"]}; line-height:1.12;">{value}</div>'
            f'{badge_html}</div>{sub_html}</div>'
        )
    st.markdown(html, unsafe_allow_html=True)




def render_chart_card_header(title: str, subtitle: str = ""):
    html = (
        f'<div class="bento-card-header" style="margin-bottom:10px;">'
        f'<div class="bento-title">{title}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)




def render_empty_state(title: str, reason: str, action_hint: str):
    html = (
        f'<div class="state-card" role="status">'
        f'<div class="state-title">{title}</div>'
        f'<div class="state-desc">{reason} {action_hint}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)




def render_error_state(title: str, reason: str, action_hint: str):
    html = (
        f'<div class="state-card state-card-error" role="alert">'
        f'<div class="state-title">{title}</div>'
        f'<div class="state-desc">{reason} {action_hint}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)




def apply_bento_plotly_style(fig, height: int = 310, show_legend: bool = True, legend_bottom: bool = False):
    legend_cfg = (
        dict(
            orientation="h",
            yanchor="top",
            y=-0.20,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color=PALETTE["muted"]),
            title_text="",
        )
        if legend_bottom
        else dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            font=dict(size=11, color=PALETTE["muted"]),
            title_text="",
        )
    )
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        uirevision="yv_constant",
        transition=dict(duration=520, easing="cubic-in-out"),
        font=dict(family="Inter, -apple-system, Segoe UI, sans-serif", color=PALETTE["emerald"], size=12),
        margin=dict(l=8, r=14, t=16, b=48 if legend_bottom else 16),
        showlegend=show_legend,
        legend=legend_cfg,
        hoverlabel=dict(
            bgcolor=PALETTE["white"],
            bordercolor=PALETTE["hairline"],
            font_size=12.5,
            font_family="Inter, -apple-system, Segoe UI, sans-serif",
            font_color=PALETTE["emerald"],
            align="left",
            namelength=-1,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(color=PALETTE["muted"], size=11),
            title_font=dict(color=PALETTE["muted"], size=11),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=PALETTE["gridline"],
            griddash="dot",
            zeroline=False,
            tickfont=dict(color=PALETTE["muted"], size=11),
            title_font=dict(color=PALETTE["muted"], size=11),
        ),
    )
    return fig


def build_striped_pill_bar(
    x_vals,
    y_vals,
    peak_badge_text: str,
    customdata=None,
    hovertemplate: str = "",
    height: int = 312,
):
    """Builds the signature diagonal-striped pill bar chart with peak dot + callout pill."""
    import plotly.graph_objects as go

    x_list = list(x_vals)
    y_list = [float(v) for v in y_vals]
    if not y_list:
        return go.Figure()

    max_val = max(y_list)
    peak_idx = y_list.index(max_val)

    # Solid botanical fill with subtle tone-on-tone diagonal stripes overlaid
    bg_colors = [PALETTE["chart_peak_bar"] if i == peak_idx else PALETTE["chart_support_bar"] for i in range(len(y_list))]

    fig = go.Figure(
        go.Bar(
            x=x_list,
            y=y_list,
            name="",
            marker=dict(
                color=bg_colors,
                cornerradius=24,
                pattern=dict(
                    shape="/",
                    fillmode="overlay",
                    fgcolor="rgba(255, 255, 255, 0.14)",
                    solidity=0.30,
                    size=10,
                ),
            ),
            customdata=customdata,
            hovertemplate=hovertemplate if hovertemplate else f"<span style='color:{PALETTE['muted']}'>Value</span>  <b>%{{y:,.0f}}</b><extra></extra>",
        )
    )

    # White-ringed peak indicator dot seated cleanly on top of the highest bar
    fig.add_trace(
        go.Scatter(
            x=[x_list[peak_idx]],
            y=[max_val],
            mode="markers",
            hoverinfo="skip",
            showlegend=False,
            marker=dict(
                size=12,
                color=PALETTE["chart_primary"],
                line=dict(color=PALETTE["white"], width=3),
            ),
        )
    )

    # Floating callout badge above peak bar
    fig.add_annotation(
        x=x_list[peak_idx],
        y=max_val,
        text=f"<b>{peak_badge_text}</b>",
        showarrow=True,
        arrowhead=0,
        arrowwidth=2,
        arrowcolor=PALETTE["chart_badge_bg"],
        ax=0,
        ay=-30,
        bgcolor=PALETTE["chart_badge_bg"],
        bordercolor=PALETTE["chart_badge_bg"],
        borderwidth=1,
        borderpad=5,
        font=dict(size=11, color=PALETTE["chart_badge_fg"], family="Inter, sans-serif"),
    )

    fig.update_layout(bargap=0.30, hovermode="x unified")
    fig.update_xaxes(tickangle=0, tickfont=dict(size=11, color=PALETTE["muted"]))
    fig.update_yaxes(title_text="", range=[0, max_val * 1.28 if max_val > 0 else 1])
    apply_bento_plotly_style(fig, height=height, show_legend=False)
    fig.update_layout(margin=dict(l=8, r=12, t=22, b=16))
    return fig


def render_striped_pill_bar(
    x_vals,
    y_vals,
    peak_badge_text: str,
    full_labels=None,
    value_fmt: str = "inr",
    extra_lines=None,
    height: int = 335,
):
    """Renders a true full-capsule (semicircular top & bottom) diagonal-striped bar chart."""
    import html as _html
    import math

    x_list = [str(x) for x in x_vals]
    y_list = [float(v) for v in y_vals]
    if not y_list:
        return

    max_val = max(y_list)
    peak_idx = y_list.index(max_val)

    # Compute crisp nice Y-axis ceiling & 5 intervals
    if max_val <= 0:
        nice_max = 100.0
        step = 20.0
    else:
        raw_step = (max_val * 1.15) / 5.0
        mag = 10 ** math.floor(math.log10(raw_step))
        norm = raw_step / mag
        if norm <= 1.0:
            nice_step = 1.0 * mag
        elif norm <= 2.0:
            nice_step = 2.0 * mag
        elif norm <= 2.5:
            nice_step = 2.5 * mag
        elif norm <= 5.0:
            nice_step = 5.0 * mag
        else:
            nice_step = 10.0 * mag
        step = nice_step
        nice_max = step * math.ceil((max_val * 1.10) / step)

    n_ticks = max(4, min(6, int(round(nice_max / step))))
    ticks = [nice_max - i * (nice_max / n_ticks) for i in range(n_ticks + 1)]

    def fmt_tick(v: float) -> str:
        if v <= 0:
            return "0"
        if v >= 1e6:
            return f"{v / 1e6:g}M"
        if v >= 1e3:
            return f"{v / 1e3:g}K"
        return f"{v:g}"

    def fmt_val(v: float) -> str:
        if value_fmt == "inr":
            return f"INR {v:,.0f}"
        if value_fmt == "ugm3":
            return f"{v:.1f} ug/m3"
        return f"{v:,.1f}"

    plot_h = max(190, height - 86)
    y_ticks_html = "".join(f"<span>{fmt_tick(tv)}</span>" for tv in ticks)
    grid_html = "".join('<div class="spb-gridline"></div>' for _ in ticks)

    cols_html = []
    xlabels_html = []
    for i, (xl, yv) in enumerate(zip(x_list, y_list)):
        pct_h = (yv / nice_max * 100.0) if nice_max > 0 else 0.0
        bar_bg = PALETTE["chart_peak_bar"] if i == peak_idx else PALETTE["chart_support_bar"]
        full_lbl = _html.escape(str(full_labels[i])) if full_labels is not None else _html.escape(xl)
        extra_h = ""
        if extra_lines is not None and extra_lines[i]:
            extra_h = f"<br><span style='color:{PALETTE['muted']};'>{_html.escape(str(extra_lines[i]))}</span>"

        peak_html = ""
        if i == peak_idx:
            peak_html = (
                f'<div class="spb-peak-anchor">'
                f'<div class="spb-peak-badge">{_html.escape(peak_badge_text)}</div>'
                f'<div class="spb-peak-stem"></div>'
                f'<div class="spb-peak-dot"></div>'
                f'</div>'
            )

        min_px = "min-height:16px;" if yv > 0 else "min-height:0px;"
        import re as _re
        bar_slug = _re.sub(r"[^a-z0-9]+", "_", xl.lower()).strip("_")
        cols_html.append(
            f'<div class="spb-col">'
            f'<div id="yv_bar_{bar_slug}" class="spb-capsule" style="height:{pct_h:.2f}%; {min_px} background-color:{bar_bg};">'
            f'{peak_html}'
            f'<div class="spb-tip">'
            f'<div style="font-weight:700;color:{PALETTE["emerald"]};">{full_lbl}</div>'
            f'<div><b>{fmt_val(yv)}</b>{extra_h}</div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
        xlabels_html.append(f'<div class="spb-xlabel">{_html.escape(xl)}</div>')

    html = (
        f'<div class="spb-wrap">'
        f'<div class="spb-chart-row" style="min-height:{plot_h}px;">'
        f'<div class="spb-yaxis">{y_ticks_html}</div>'
        f'<div class="spb-plot">'
        f'<div class="spb-gridlines">{grid_html}</div>'
        f'<div class="spb-bars-layer">{"".join(cols_html)}</div>'
        f'</div>'
        f'</div>'
        f'<div class="spb-xaxis-row">'
        f'<div class="spb-xaxis-spacer"></div>'
        f'<div class="spb-xlabels">{"".join(xlabels_html)}</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_bento_treemap(df_filtered, lang: str = "en"):
    """Renders 4 BMI columns with overlapping stacked wallet-style product cards inside each tier."""
    import html as _html

    is_id = (lang == "id")
    agg = (
        df_filtered.groupby(["bmi_category", "recommended_supplement_category", "fitness_goal"], as_index=False)["member_count"]
        .sum()
    )
    total = float(agg["member_count"].sum())
    if total <= 0 or agg.empty:
        return

    bmi_order = ["Underweight", "Normal", "Overweight", "Obese"]
    present_bmis = [b for b in bmi_order if b in agg["bmi_category"].values]
    for b in sorted(agg["bmi_category"].unique().tolist()):
        if b not in present_bmis:
            present_bmis.append(b)

    short_cat = {
        "Protein Supplement": "Protein",
        "Milk Drink Mixes": "Milk Mix",
        "Energy Drinks": "Energy",
    }
    goal_tr = {
        "Muscle Gain": "Massa Otot" if is_id else "Muscle Gain",
        "Fat Burn": "Bakar Lemak" if is_id else "Fat Burn",
    }
    of_tier_lbl = "dari segmen" if is_id else "of tier"
    prof_lbl = "profil" if is_id else "profiles"

    # Layer color tokens (bg, fg, meta_fg, icon_bg, icon_stroke, badge_bg, badge_fg)
    layer_styles = [
        (
            "#073527" if PALETTE["is_dark"] else "#043f2e",
            "#fcfcfc",
            "#c3d9c8",
            "rgba(200, 241, 105, 0.16)",
            "#c8f169",
            "rgba(200, 241, 105, 0.18)",
            "#c8f169",
        ),
        (
            "#c8f169",
            "#000000",
            "#1d3b27",
            "rgba(4, 63, 46, 0.12)",
            "#043f2e",
            "rgba(4, 63, 46, 0.14)",
            "#043f2e",
        ),
        (
            "#2a6f2b",
            "#fcfcfc",
            "#d7ebd9",
            "rgba(255, 255, 255, 0.16)",
            "#fcfcfc",
            "rgba(255, 255, 255, 0.18)",
            "#fcfcfc",
        ),
    ]

    def prod_icon(cat_s: str, stroke_col: str) -> str:
        if cat_s == "Protein":
            return (
                f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none">'
                f'<path d="M6.5 6.5v11M17.5 6.5v11M3 9.5v5M21 9.5v5M6.5 12h11" '
                f'stroke="{stroke_col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            )
        if cat_s == "Energy":
            return (
                f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none">'
                f'<path d="M13 2L4 14h7l-1 8 9-12h-7l1-8z" '
                f'stroke="{stroke_col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            )
        return (
            f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none">'
            f'<path d="M12 2.5C12 2.5 6 9.2 6 14a6 6 0 0 0 12 0c0-4.8-6-11.5-6-11.5z" '
            f'stroke="{stroke_col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        )

    cols_html = []
    for bmi in present_bmis:
        sub = agg[agg["bmi_category"] == bmi].sort_values("member_count", ascending=False)
        bmi_tot = int(sub["member_count"].sum())
        bmi_pct = bmi_tot / total * 100.0

        cards_html = []
        for idx, row in enumerate(sub.itertuples(index=False)):
            bg, fg, m_fg, ic_bg, ic_col, b_bg, b_fg = layer_styles[idx % len(layer_styles)]
            cnt = int(row.member_count)
            share_all = cnt / total * 100.0
            share_bmi = cnt / bmi_tot * 100.0 if bmi_tot else 0.0
            cat_s = short_cat.get(row.recommended_supplement_category, row.recommended_supplement_category)
            goal_disp = goal_tr.get(str(row.fitness_goal), str(row.fitness_goal))
            tip = _html.escape(f"{row.recommended_supplement_category} | {goal_disp} | {bmi} ({cnt:,} {prof_lbl}, {share_all:.1f}%)")
            cards_html.append(
                f'<div class="bmi-stack-card" title="{tip}" style="background:{bg}; color:{fg}; z-index:{idx + 1}; animation-delay:{idx * 75}ms;">'
                f'<div class="bmi-card-top">'
                f'<div style="display:inline-flex; align-items:center; gap:9px; min-width:0;">'
                f'<div class="bmi-icon-badge" style="background:{ic_bg};">{prod_icon(cat_s, ic_col)}</div>'
                f'<span class="bmi-card-prod">{_html.escape(cat_s)}</span>'
                f'</div>'
                f'<span class="bmi-card-share" style="background:{b_bg}; color:{b_fg};">{share_all:.1f}%</span>'
                f'</div>'
                f'<div>'
                f'<div class="bmi-card-meta" style="color:{m_fg}; justify-content:flex-end;">'
                f'<span>{share_bmi:.0f}% {of_tier_lbl}</span>'
                f'</div>'
                f'<div class="bmi-card-main">'
                f'<span class="bmi-card-goal" style="color:{m_fg}; font-size:13px; font-weight:600;">{_html.escape(goal_disp)}</span>'
                f'<span id="yv_num_bmi_{bmi.lower()}_{cat_s.lower().replace(" ", "_")}" class="bmi-card-val anim-num">{cnt:,}</span>'
                f'</div>'
                f'</div>'
                f'</div>'
            )

        cols_html.append(
            f'<div class="bmi-col">'
            f'<div class="bmi-col-head">'
            f'<span class="bmi-col-title">{_html.escape(bmi)}</span>'
            f'<span class="bmi-col-total">{bmi_tot:,} &middot; {bmi_pct:.1f}%</span>'
            f'</div>'
            f'<div class="bmi-stack">{"".join(cards_html)}</div>'
            f'</div>'
        )

    st.markdown(f'<div class="bmi-deck-grid">{"".join(cols_html)}</div>', unsafe_allow_html=True)


def render_rounded_heatmap(
    x_labels,
    y_labels,
    z_matrix,
    sku_matrix,
    units_matrix,
    peak_badge_fn=None,
    lang: str = "en",
):
    """Renders a rounded-cell botanical matrix heatmap with smart peak callout and flat hover tooltips."""
    import html as _html
    import numpy as np

    is_id = (lang == "id")
    lbl_peak = "Puncak" if is_id else "Peak"
    lbl_rev = "Pendapatan Bersih" if is_id else "Net Revenue"
    lbl_skus = "SKU Aktif" if is_id else "Active SKUs"
    lbl_units = "Unit" if is_id else "Units"

    n_rows = len(y_labels)
    n_cols = len(x_labels)
    if n_rows == 0 or n_cols == 0:
        return

    z_arr = np.asarray(z_matrix, dtype=float)
    max_z = float(z_arr.max()) if z_arr.size else 0.0

    stops = (
        [
            (0.00, (23, 39, 32)),
            (0.14, (30, 58, 45)),
            (0.38, (42, 111, 43)),
            (0.68, (120, 197, 28)),
            (1.00, (200, 241, 105)),
        ]
        if PALETTE["is_dark"]
        else [
            (0.00, (242, 244, 241)),
            (0.12, (226, 236, 208)),
            (0.35, (200, 241, 105)),
            (0.65, (42, 111, 43)),
            (1.00, (4, 63, 46)),
        ]
    )

    def interp_color(ratio: float) -> str:
        r = max(0.0, min(1.0, ratio))
        for idx in range(len(stops) - 1):
            t0, c0 = stops[idx]
            t1, c1 = stops[idx + 1]
            if r <= t1:
                f = (r - t0) / (t1 - t0) if t1 > t0 else 0.0
                cr = int(round(c0[0] + (c1[0] - c0[0]) * f))
                cg = int(round(c0[1] + (c1[1] - c0[1]) * f))
                cb = int(round(c0[2] + (c1[2] - c0[2]) * f))
                return f"rgb({cr},{cg},{cb})"
        c = stops[-1][1]
        return f"rgb({c[0]},{c[1]},{c[2]})"

    pk_r, pk_c = (-1, -1)
    if max_z > 0:
        pk_r, pk_c = np.unravel_index(int(np.argmax(z_arr)), z_arr.shape)

    cells = ['<div></div>']
    for xl in x_labels:
        cells.append(f'<div class="hm-col-head">{_html.escape(str(xl))}</div>')

    for r_idx, yl in enumerate(y_labels):
        cells.append(f'<div class="hm-row-label">{_html.escape(str(yl))}</div>')
        for c_idx, xl in enumerate(x_labels):
            val = float(z_arr[r_idx, c_idx])
            ratio = (val / max_z) if max_z > 0 else 0.0
            bg = interp_color(ratio)
            skus = int(sku_matrix[r_idx, c_idx])
            units = int(units_matrix[r_idx, c_idx])
            delay = (r_idx * 35) + (c_idx * 18)

            edge_cls = " hm-cell-left" if c_idx <= 1 else (" hm-cell-right" if c_idx >= n_cols - 2 else "")
            is_pk = (r_idx == pk_r and c_idx == pk_c and max_z > 0)
            peak_cls = " hm-cell-peak" if is_pk else ""
            peak_html = ""
            if is_pk:
                pk_txt = peak_badge_fn(val) if peak_badge_fn else f"INR {val / 1e6:,.2f}M"
                pill_pos = "left:0;" if c_idx <= 1 else ("right:0;" if c_idx >= n_cols - 2 else "left:50%; transform:translateX(-50%);")
                above_cls = " hm-peak-pill-above" if r_idx == n_rows - 1 else ""
                peak_html = (
                    f'<div class="hm-peak-dot"></div>'
                    f'<div class="hm-peak-pill{above_cls}" style="{pill_pos}">{lbl_peak} {_html.escape(pk_txt)}</div>'
                )

            cells.append(
                f'<div class="hm-cell{edge_cls}{peak_cls}" style="background:{bg}; animation-delay:{delay}ms;">'
                f'{peak_html}'
                f'<div class="hm-tip">'
                f'<div style="font-weight:700;color:{PALETTE["emerald"]};">{_html.escape(str(yl))} &middot; {_html.escape(str(xl))}</div>'
                f'<div><span style="color:{PALETTE["muted"]};">{lbl_rev}</span> <b>INR {val:,.0f}</b></div>'
                f'<div><span style="color:{PALETTE["muted"]};">{lbl_skus}</span> <b>{skus:,}</b> &middot; '
                f'<span style="color:{PALETTE["muted"]};">{lbl_units}</span> <b>{units:,}</b></div>'
                f'</div>'
                f'</div>'
            )

    html = (
        f'<div class="hm-wrap">'
        f'<div class="hm-grid" style="grid-template-columns: 74px repeat({n_cols}, minmax(0, 1fr));">'
        f'{"".join(cells)}'
        f'</div></div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_horizontal_pill_bars(
    rows: list,
    legend_items: list | None = None,
    wide_labels: bool = False,
):
    """Renders full-pill (semicircle left & right) horizontal single or stacked bars with clean hover tooltips.
    Each item in `rows`: {'label': str, 'segments': [(val, color), ...], 'tip_html': str}
    """
    import html as _html

    if not rows:
        return

    totals = [sum(max(0.0, float(v)) for v, _ in r["segments"]) for r in rows]
    max_tot = max(totals) if totals else 1.0
    if max_tot <= 0:
        max_tot = 1.0

    leg_html = ""
    if legend_items:
        items_h = "".join(
            f'<span class="hpb-leg-item"><span class="hpb-leg-dot" style="background:{col};"></span>{_html.escape(str(lbl))}</span>'
            for lbl, col in legend_items
        )
        leg_html = f'<div class="hpb-legend">{items_h}</div>'

    lbl_cls = "hpb-label hpb-label-wide" if wide_labels else "hpb-label"
    rows_html = []
    for idx, (r, tot) in enumerate(zip(rows, totals)):
        pct_w = (tot / max_tot * 100.0) if max_tot > 0 else 0.0
        segs_h = []
        for sv, scol in r["segments"]:
            sv_f = max(0.0, float(sv))
            if sv_f <= 0 or tot <= 0:
                continue
            seg_pct = (sv_f / tot) * 100.0
            segs_h.append(f'<div class="hpb-seg" style="width:{seg_pct:.2f}%; background:{scol};"></div>')
        delay = idx * 45
        first_cls = " hpb-row-first" if idx == 0 else ""
        rows_html.append(
            f'<div class="hpb-row{first_cls}">'
            f'<div class="{lbl_cls}" title="{_html.escape(str(r["label"]))}">{_html.escape(str(r["label"]))}</div>'
            f'<div class="hpb-track">'
            f'<div class="hpb-bar-pill" style="width:{pct_w:.2f}%; animation-delay:{delay}ms;">{"".join(segs_h)}</div>'
            f'</div>'
            f'<div class="hpb-tip">{r["tip_html"]}</div>'
            f'</div>'
        )

    out_html = (
        f'<div class="hpb-wrap">'
        f'{leg_html}'
        f'<div class="hpb-rows">{"".join(rows_html)}</div>'
        f'</div>'
    )
    st.markdown(out_html, unsafe_allow_html=True)


def render_channel_arc_gauge(ch_agg, total_net_rev: float, center_sub_label: str = "Total Net Revenue", lang: str = "en"):
    """Renders a 360-degree rounded segmented donut ring with vertical bar legend and synced easy-ease hover."""
    import html as _html
    import math

    if ch_agg.empty or total_net_rev <= 0:
        return
    ord_lbl = "pesanan" if lang == "id" else "orders"

    def fmt_compact(v: float) -> str:
        if abs(v) >= 1e6:
            return f"INR {v / 1e6:,.2f}M"
        if abs(v) >= 1e3:
            return f"INR {v / 1e3:,.1f}K"
        return f"INR {v:,.0f}"

    color_map = {
        "Flipkart Health": PALETTE["arc_flipkart"],
        "Tata 1mg": PALETTE["lime"],
    }
    ordered = ch_agg.sort_values("net_rev", ascending=False).reset_index(drop=True)

    cx, cy, r = 120.0, 120.0, 86.0
    start_base = -90.0
    n = len(ordered)
    gap_deg = 22.0 if n > 1 else 0.0
    total_sweep = 360.0 if n > 1 else 359.8
    usable = total_sweep - gap_deg * n if n > 1 else total_sweep

    def pt(deg: float):
        rad = math.radians(deg)
        return cx + r * math.cos(rad), cy + r * math.sin(rad)

    arcs_svg = []
    leg_html = []
    cur = start_base + (gap_deg / 2.0 if n > 1 else 0.0)
    for idx, row in enumerate(ordered.itertuples(index=False)):
        share = float(row.net_rev) / total_net_rev
        share_pct = share * 100.0
        sweep = max(share * usable, 8.0)
        x1, y1 = pt(cur)
        x2, y2 = pt(cur + sweep)
        large = 1 if sweep > 180.0 else 0
        col = color_map.get(row.channel_name, PALETTE["teal"])
        tip = _html.escape(f"{row.channel_name}: {fmt_compact(float(row.net_rev))} ({share_pct:.1f}%)")
        ch_slug = str(row.channel_name).lower().replace(" ", "_")

        arcs_svg.append(
            f'<path id="yv_arc_{ch_slug}" class="arc-seg arc-seg-{idx} arc-path-anim" '
            f'd="M {x1:.2f} {y1:.2f} A {r:.1f} {r:.1f} 0 {large} 1 {x2:.2f} {y2:.2f}" '
            f'fill="none" stroke="{col}" stroke-width="24" stroke-linecap="round" '
            f'style="transform-origin:{cx:.0f}px {cy:.0f}px;">'
            f'<title>{tip}</title></path>'
        )

        bar_border = "border:1px solid rgba(4,63,46,0.22);" if col == PALETTE["lime"] and not PALETTE["is_dark"] else ""
        leg_html.append(
            f'<div class="arc-stat-item arc-leg-{idx}">'
            f'<span class="arc-pill-bar" style="background:{col};{bar_border}"></span>'
            f'<div class="arc-stat-body">'
            f'<div class="arc-stat-top">'
            f'<span id="yv_num_arc_pct_{ch_slug}" class="arc-stat-val anim-num">{share_pct:.1f}%</span>'
            f'<span class="arc-stat-name">{_html.escape(str(row.channel_name))}</span>'
            f'</div>'
            f'<div class="arc-stat-sub">{fmt_compact(float(row.net_rev))} &bull; {int(row.orders):,} {ord_lbl}</div>'
            f'</div></div>'
        )
        cur += sweep + gap_deg

    center_val = fmt_compact(total_net_rev)
    svg_html = (
        f'<svg viewBox="0 0 240 240" width="100%" style="max-width:206px; overflow:visible;" role="img" aria-label="Channel revenue share donut">'
        f'{"".join(arcs_svg)}'
        f'<text id="yv_num_arc_center" class="anim-num" x="{cx:.0f}" y="{cy + 2:.0f}" text-anchor="middle" font-family="Inter, sans-serif" font-size="21" font-weight="700" letter-spacing="-0.02em" fill="{PALETTE["emerald"]}">{center_val}</text>'
        f'<text x="{cx:.0f}" y="{cy + 21:.0f}" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="500" fill="{PALETTE["muted"]}">{_html.escape(str(center_sub_label))}</text>'
        f'</svg>'
    )

    html = (
        f'<div class="arc-wrap">'
        f'<div class="arc-svg-box">{svg_html}</div>'
        f'<div class="arc-legend">{"".join(leg_html)}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_sku_modern_table(df_skus, title: str, lang: str = "en"):
    """Renders a modern SaaS-style data table (Foto 2) with big highlight headline, icon badges, and dotted status pills."""
    import html as _html

    if df_skus is None or df_skus.empty:
        return

    is_id = (lang == "id")
    h_prod = "Produk" if is_id else "Product"
    h_chan = "Kanal" if is_id else "Channel"
    h_cat = "Kategori" if is_id else "Category"
    h_price = "Harga" if is_id else "Price"
    h_disc = "Diskon" if is_id else "Discount"
    h_rev = "Pendapatan" if is_id else "Net Revenue"
    h_state = "Status"
    unit_lbl = "unit" if is_id else "units"

    short_cat = {
        "Vitamin Supplement": "Vitamins",
        "Protein Supplement": "Protein",
        "Energy Drinks": "Energy",
        "Milk Drink Mixes": "Milk Mix",
        "Digestive Probiotic": "Probiotic",
    }

    is_dark = bool(PALETTE["is_dark"])
    rows_h = []
    for r in df_skus.itertuples(index=False):
        sku_id = _html.escape(str(r.sku_natural_id))
        pname_raw = str(r.product_name)
        pname = _html.escape(pname_raw)
        ch = str(r.channel_source)
        ch_esc = _html.escape(ch)
        cat_s = _html.escape(short_cat.get(str(r.category_name), str(r.category_name)))
        mrp = float(r.mrp_inr)
        sell = float(r.selling_price_inr)
        disc = float(r.discount_pct)
        units = int(r.total_units_sold)
        net_r = float(r.total_net_revenue_inr)

        is_fk = "flipkart" in ch.lower()
        if is_fk:
            av_txt = "FK"
            av_bg = "#1b3a2e" if is_dark else "#e6f2ec"
            av_fg = "#c8f169" if is_dark else "#043f2e"
        else:
            av_txt = "1M"
            av_bg = "#273b22" if is_dark else "#eef8d5"
            av_fg = "#c8f169" if is_dark else "#2a6f2b"

        if disc <= 15.0:
            st_lbl = "Optimal"
            st_bg = "#19382a" if is_dark else "#e7f6ec"
            st_fg = "#c8f169" if is_dark else "#043f2e"
            st_dot = "#c8f169" if is_dark else "#2a6f2b"
        elif disc <= 35.0:
            st_lbl = "Promo"
            st_bg = "#243822" if is_dark else "#f1fae0"
            st_fg = "#a3e635" if is_dark else "#3b6e12"
            st_dot = "#a3e635" if is_dark else "#78c51c"
        else:
            st_lbl = "Diskon Dalam" if is_id else "Deep Disc"
            st_bg = "#1d2b25" if is_dark else "#eef1f0"
            st_fg = "#b8cbc0" if is_dark else "#495851"
            st_dot = "#7da08f" if is_dark else "#6b7c74"

        rows_h.append(
            f'<tr>'
            f'<td><div class="sku-prod-cell">'
            f'<div class="sku-avatar" style="background:{av_bg}; color:{av_fg};">{av_txt}</div>'
            f'<div class="sku-prod-text">'
            f'<div class="sku-prod-name" title="{pname}">{pname}</div>'
            f'<div class="sku-prod-id">{sku_id}</div>'
            f'</div></div></td>'
            f'<td>{ch_esc}</td>'
            f'<td>{cat_s}</td>'
            f'<td class="num"><div class="sku-main-val">INR {sell:,.0f}</div><div class="sku-sub-val">MRP {mrp:,.0f}</div></td>'
            f'<td class="num">{disc:.1f}%</td>'
            f'<td class="num"><div class="sku-main-val">INR {net_r:,.0f}</div><div class="sku-sub-val">{units:,} {unit_lbl}</div></td>'
            f'<td><span class="sku-status-pill" style="background:{st_bg}; color:{st_fg};">'
            f'<span class="sku-status-dot" style="background:{st_dot};"></span>{st_lbl}</span></td>'
            f'</tr>'
        )

    head_html = (
        f'<div class="sku-highlight-head">'
        f'<span class="sku-highlight-title">{_html.escape(title)}</span>'
        f'<span class="sku-highlight-count">{len(df_skus)} SKUs</span>'
        f'</div>'
    ) if title else ""
    out_html = (
        f'{head_html}'
        f'<div class="sku-tbl-shell"><div class="sku-tbl-scroll">'
        f'<table class="sku-tbl">'
        f'<thead><tr>'
        f'<th>{h_prod}</th><th>{h_chan}</th><th>{h_cat}</th>'
        f'<th class="num">{h_price}</th><th class="num">{h_disc}</th>'
        f'<th class="num">{h_rev}</th><th>{h_state}</th>'
        f'</tr></thead>'
        f'<tbody>{"".join(rows_h)}</tbody>'
        f'</table></div></div>'
    )
    st.markdown(out_html, unsafe_allow_html=True)


def render_aqi_hero_map(
    city_agg,
    demand_lift: float,
    season_label: str = "All Seasons",
    region_label: str = "All Regions",
    height: int = 472,
    hud_labels: dict | None = None,
):
    """Renders a theme-aware full-bleed Esri Gray Canvas map with floating frosted HUD cards."""
    import html as _html
    import json
    import streamlit.components.v1 as components

    if city_agg.empty:
        return

    lbl = hud_labels or {}
    L_ALL = _html.escape(lbl.get("map_all_cities", "All Cities"))
    L_RISK = _html.escape(lbl.get("map_high_risk", "High Risk (>150)"))
    L_CORRIDOR = _html.escape(lbl.get("map_demand_corridor", "Demand Corridor"))
    L_LEG_NORM = _html.escape(lbl.get("map_leg_normal", "Normal"))
    L_LEG_WATCH = _html.escape(lbl.get("map_leg_watch", "Watch"))
    L_LEG_HIGH = _html.escape(lbl.get("map_leg_high", "High Risk"))
    L_PEAK = _html.escape(lbl.get("map_peak_label", "Peak Pollution Exposure"))
    L_ABOVE100 = _html.escape(lbl.get("map_above100_label", "Cities Above 100 AQI"))
    L_FOCUS = _html.escape(lbl.get("map_focus_peak", "Focus Peak"))
    L_VIEWALL = _html.escape(lbl.get("map_view_all", "View All"))
    L_ALERT_EYE = _html.escape(lbl.get("map_alert_eyebrow", "Air Quality Alert"))

    is_dark = bool(PALETTE["is_dark"])
    tile_base = (
        "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}"
        if is_dark
        else "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"
    )
    tile_ref = (
        "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}"
        if is_dark
        else "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer/tile/{z}/{y}/{x}"
    )
    tile_filter = "brightness(1.08) contrast(0.95)" if is_dark else "brightness(1.06) contrast(0.90) sepia(0.06) saturate(0.85)"
    map_bg = "#131c19" if is_dark else "#f7f9f4"
    hud_bg = "rgba(18, 31, 26, 0.92)" if is_dark else "rgba(252, 252, 252, 0.92)"
    hud_tab_bg = "rgba(18, 31, 26, 0.94)" if is_dark else "rgba(252, 252, 252, 0.94)"
    hud_tab_border = "rgba(200, 241, 105, 0.25)" if is_dark else "rgba(4, 63, 46, 0.22)"
    hud_ghost_bg = "#121f1a" if is_dark else "#ffffff"
    hud_track_bg = "#21362d" if is_dark else "#dde5d2"
    marker_normal = "#34d399" if is_dark else PALETTE["emerald"]
    marker_border = "#121f1a" if is_dark else "#ffffff"
    shadow_col = "rgba(0, 0, 0, 0.32)" if is_dark else "rgba(4, 63, 46, 0.06)"

    df_sorted = city_agg.sort_values("mean_aqi", ascending=False).reset_index(drop=True)
    records = []
    for r in df_sorted.itertuples(index=False):
        records.append(
            {
                "city": str(r.city),
                "state": str(r.state),
                "region": str(r.region),
                "lat": float(r.latitude),
                "lon": float(r.longitude),
                "aqi": round(float(r.mean_aqi), 1),
                "pm25": round(float(r.mean_pm25), 1),
                "rev": round(float(r.vit_rev), 0),
                "units": int(r.vit_units),
            }
        )

    peak = records[0]
    total_n = len(records)
    elevated_n = sum(1 for x in records if x["aqi"] > 100.0)
    high_n = sum(1 for x in records if x["aqi"] > 150.0)
    elevated_pct = int(round((elevated_n / total_n) * 100)) if total_n else 0

    is_severe = peak["aqi"] > 150.0
    alert_color = PALETTE["coral"] if is_severe else (PALETTE["amber"] if peak["aqi"] > 100.0 else marker_normal)
    alert_title = _html.escape(
        lbl.get("map_alert_severe", "Severe AQI Hotspot") if is_severe
        else (lbl.get("map_alert_watch", "Elevated AQI Watch") if peak["aqi"] > 100.0 else lbl.get("map_alert_normal", "Normal Air Quality"))
    )
    lift_str = f"{demand_lift:+.1f}%"
    alert_body = (
        f"{_html.escape(peak['city'])} averaged {peak['aqi']:.1f} US AQI "
        f"({lift_str} vitamin lift on high-AQI days). "
        f"Prioritize {_html.escape(peak['region'])} India immunity inventory."
    )
    peak_city_esc = _html.escape(peak["city"])
    peak_state_esc = _html.escape(peak["state"])
    scope_tag = _html.escape(season_label if region_label in ("All Regions", "Semua Wilayah") else region_label)
    cities_json = json.dumps(records)

    map_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: {PALETTE['canvas']};
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: {PALETTE['emerald']};
  }}
  .hero-map-shell {{
    position: relative;
    width: 100%;
    height: {height}px;
    border-radius: 18px;
    overflow: hidden;
    border: 4px solid {PALETTE['white']};
    outline: none;
    background: {map_bg};
  }}
  #aqiMap {{
    width: 100%;
    height: 100%;
    background: {map_bg};
    border: none;
  }}
  .leaflet-tile-pane {{
    filter: {tile_filter};
  }}
  .leaflet-control-attribution {{
    font-size: 9px !important;
    background: {hud_bg} !important;
    color: {PALETTE['muted']} !important;
    padding: 1px 6px !important;
    border-top-right-radius: 6px;
  }}
  .leaflet-control-attribution a {{
    color: {PALETTE['muted']} !important;
  }}

  /* Top-Left Floating Pill Tabs */
  .hud-tabs {{
    position: absolute;
    top: 18px;
    left: 18px;
    z-index: 650;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }}
  .hud-tab {{
    appearance: none;
    border: 1px solid {hud_tab_border};
    background: {hud_tab_bg};
    backdrop-filter: blur(8px);
    color: {PALETTE['emerald']};
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 500;
    padding: 7px 14px;
    border-radius: 999px;
    cursor: pointer;
    transition: all 0.16s ease;
    line-height: 1.2;
  }}
  .hud-tab:hover {{
    background: {PALETTE['pill_bg']};
    border-color: {PALETTE['chart_primary']};
  }}
  .hud-tab.active {{
    background: {PALETTE['btn_bg']};
    color: {PALETTE['btn_fg']};
    border-color: {PALETTE['btn_bg']};
    font-weight: 600;
  }}
  .hud-tab.active-risk {{
    background: {PALETTE['coral']};
    color: {'#000000' if is_dark else '#ffffff'};
    border-color: {PALETTE['coral']};
    font-weight: 600;
  }}

  /* Left Floating Metric Cards */
  .hud-left-stack {{
    position: absolute;
    top: 66px;
    left: 18px;
    z-index: 650;
    width: 262px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    pointer-events: none;
  }}
  .hud-card {{
    background: {hud_bg};
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: {'1px solid ' + PALETTE['hairline'] if is_dark else 'none'};
    box-shadow: 0 4px 20px {shadow_col};
    border-radius: 14px;
    padding: 14px 16px;
    pointer-events: auto;
  }}
  .hud-label {{
    font-size: 11.5px;
    font-weight: 500;
    color: {PALETTE['muted']};
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .hud-scope {{
    font-size: 10px;
    color: {PALETTE['muted']};
    background: {PALETTE['canvas']};
    padding: 2px 8px;
    border-radius: 999px;
    font-weight: 600;
    white-space: nowrap;
    flex-shrink: 0;
  }}
  .hud-big-row {{
    display: flex;
    align-items: baseline;
    gap: 5px;
    line-height: 1.1;
  }}
  .hud-big-val {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.025em;
    color: {alert_color};
  }}
  .hud-big-unit {{
    font-size: 11.5px;
    font-weight: 600;
    color: {alert_color};
  }}
  .hud-big-slash {{
    font-size: 15px;
    font-weight: 400;
    color: {PALETTE['muted']};
    margin: 0 2px;
  }}
  .hud-big-sec {{
    font-size: 15px;
    font-weight: 600;
    color: {PALETTE['emerald']};
  }}
  .hud-sub {{
    font-size: 11px;
    color: {PALETTE['muted']};
    margin-top: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  /* Progress Bar Card */
  .hud-prog-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 4px 0 6px 0;
  }}
  .hud-pct {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: {alert_color};
    line-height: 1;
    min-width: 52px;
  }}
  .hud-bar-track {{
    flex: 1;
    height: 5px;
    border-radius: 999px;
    background: {hud_track_bg};
    overflow: hidden;
  }}
  .hud-bar-fill {{
    height: 100%;
    border-radius: 999px;
    background: {alert_color};
    width: {elevated_pct}%;
    transition: width 0.35s ease;
  }}
  .hud-btn-row {{
    display: flex;
    gap: 8px;
    margin-top: 12px;
  }}
  .hud-btn {{
    flex: 1;
    appearance: none;
    border-radius: 999px;
    padding: 7px 10px;
    font-family: 'Inter', sans-serif;
    font-size: 11.5px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.16s ease;
    text-align: center;
  }}
  .hud-btn-primary {{
    background: {PALETTE['btn_bg']};
    color: {PALETTE['btn_fg']};
    border: 1px solid {PALETTE['btn_bg']};
  }}
  .hud-btn-primary:hover {{
    background: {PALETTE['btn_hover_bg']};
    border-color: {PALETTE['btn_hover_bg']};
  }}
  .hud-btn-ghost {{
    background: {hud_ghost_bg};
    color: {PALETTE['emerald']};
    border: 1px solid {hud_tab_border};
  }}
  .hud-btn-ghost:hover {{
    background: {PALETTE['pill_bg']};
  }}

  /* Top-Right Legend & Custom Zoom */
  .hud-top-right {{
    position: absolute;
    top: 18px;
    right: 18px;
    z-index: 650;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .hud-legend {{
    display: flex;
    align-items: center;
    gap: 11px;
    background: {hud_bg};
    backdrop-filter: blur(10px);
    border: {'1px solid ' + PALETTE['hairline'] if is_dark else 'none'};
    box-shadow: 0 2px 12px {shadow_col};
    border-radius: 999px;
    padding: 7px 14px;
    font-size: 11px;
    font-weight: 500;
    color: {PALETTE['charcoal']};
  }}
  .leg-item {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    white-space: nowrap;
  }}
  .leg-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
  }}
  .hud-zoom-group {{
    display: flex;
    background: {hud_bg};
    border: {'1px solid ' + PALETTE['hairline'] if is_dark else 'none'};
    box-shadow: 0 2px 12px {shadow_col};
    border-radius: 999px;
    overflow: hidden;
  }}
  .hud-zoom-btn {{
    width: 30px;
    height: 30px;
    border: none;
    background: transparent;
    color: {PALETTE['emerald']};
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .hud-zoom-btn:hover {{
    background: {PALETTE['pill_bg']};
  }}
  .hud-zoom-btn + .hud-zoom-btn {{
    border-left: 1px solid {PALETTE['hairline']};
  }}

  /* Bottom-Right Floating Alert Card */
  .hud-alert {{
    position: absolute;
    bottom: 18px;
    right: 18px;
    z-index: 650;
    width: 296px;
    background: {hud_bg};
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: {'1px solid ' + PALETTE['hairline'] if is_dark else 'none'};
    box-shadow: 0 4px 20px {shadow_col};
    border-radius: 16px;
    padding: 14px 16px;
  }}
  .hud-alert-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
  }}
  .hud-alert-eyebrow {{
    font-size: 11px;
    font-weight: 500;
    color: {PALETTE['muted']};
  }}
  .hud-alert-badge {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: {alert_color};
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}
  .hud-alert-head {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 5px;
  }}
  .hud-alert-title {{
    font-size: 14px;
    font-weight: 700;
    color: {PALETTE['emerald']};
    letter-spacing: -0.01em;
  }}
  .hud-alert-metric {{
    font-size: 11px;
    font-weight: 600;
    color: {alert_color};
    white-space: nowrap;
  }}
  .hud-alert-body {{
    font-size: 11.5px;
    line-height: 1.45;
    color: {PALETTE['muted']};
  }}

  /* Numbered Glowing Hotspot Pins (1, 2, 3) */
  .rank-pin-wrap {{
    position: relative;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .rank-pin-halo {{
    position: absolute;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    opacity: 0.22;
    pointer-events: none;
  }}
  .rank-pin-core {{
    position: relative;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
    font-size: 11.5px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid #ffffff;
    box-shadow: 0 2px 6px rgba(4, 63, 46, 0.22);
  }}

  /* Paper White Flat Bento Popup */
  .leaflet-popup-content-wrapper {{
    background: {PALETTE['white']} !important;
    color: {PALETTE['emerald']} !important;
    border-radius: 12px !important;
    border: 1px solid {PALETTE['hairline']} !important;
    box-shadow: 0 6px 18px rgba(4, 63, 46, 0.10) !important;
    padding: 0 !important;
  }}
  .leaflet-popup-content {{
    margin: 11px 13px !important;
    font-family: 'Inter', sans-serif !important;
    min-width: 175px;
  }}
  .leaflet-popup-tip {{
    background: {PALETTE['white']} !important;
    border: 1px solid {PALETTE['hairline']} !important;
  }}
  .pop-city {{
    font-size: 13.5px;
    font-weight: 700;
    color: {PALETTE['emerald']};
    line-height: 1.2;
  }}
  .pop-state {{
    font-size: 10.5px;
    color: {PALETTE['muted']};
    margin-bottom: 8px;
  }}
  .pop-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 10px;
    border-top: 1px solid {PALETTE['gridline']};
    padding-top: 7px;
  }}
  .pop-k {{
    font-size: 9.5px;
    color: {PALETTE['muted']};
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}
  .pop-v {{
    font-size: 12px;
    font-weight: 700;
    color: {PALETTE['emerald']};
  }}
  @media (max-width: 780px) {{
    .hud-left-stack {{ width: 215px; top: 62px; }}
    .hud-alert {{ width: 230px; }}
    .hud-legend {{ display: none; }}
  }}
</style>
</head>
<body>
<div class="hero-map-shell">
  <div id="aqiMap"></div>

  <!-- Top-Left Floating Layer Tabs -->
  <div class="hud-tabs" role="tablist" aria-label="Map view layers">
    <button class="hud-tab active" id="tabAll" onclick="setMode('all')">{L_ALL} ({total_n})</button>
    <button class="hud-tab" id="tabRisk" onclick="setMode('risk')">{L_RISK} ({high_n})</button>
    <button class="hud-tab" id="tabDemand" onclick="setMode('demand')">{L_CORRIDOR}</button>
  </div>

  <!-- Top-Right Legend & Zoom -->
  <div class="hud-top-right">
    <div class="hud-legend">
      <span class="leg-item"><span class="leg-dot" style="background:{marker_normal}"></span>&le;100 {L_LEG_NORM}</span>
      <span class="leg-item"><span class="leg-dot" style="background:{PALETTE['amber']}"></span>101-150 {L_LEG_WATCH}</span>
      <span class="leg-item"><span class="leg-dot" style="background:{PALETTE['coral']}"></span>&gt;150 {L_LEG_HIGH}</span>
    </div>
    <div class="hud-zoom-group">
      <button class="hud-zoom-btn" onclick="map.zoomIn()" aria-label="Zoom in">+</button>
      <button class="hud-zoom-btn" onclick="map.zoomOut()" aria-label="Zoom out">&minus;</button>
    </div>
  </div>

  <!-- Left Stacked Frosted HUD Cards -->
  <div class="hud-left-stack">
    <div class="hud-card">
      <div class="hud-label">
        <span id="hudFocusLabel">{L_PEAK}</span>
        <span class="hud-scope">{scope_tag}</span>
      </div>
      <div class="hud-big-row">
        <span class="hud-big-val" id="hudAqiVal">{peak['aqi']:.1f}</span>
        <span class="hud-big-unit" id="hudAqiUnit">AQI</span>
        <span class="hud-big-slash">/</span>
        <span class="hud-big-sec" id="hudPmVal">{peak['pm25']:.1f} ug/m3</span>
      </div>
      <div class="hud-sub" id="hudCitySub">{peak_city_esc}, {peak_state_esc}</div>
    </div>

    <div class="hud-card">
      <div class="hud-label">
        <span>{L_ABOVE100}</span>
        <span style="font-weight:600;color:{PALETTE['emerald']};">{elevated_n}/{total_n}</span>
      </div>
      <div class="hud-prog-row">
        <span class="hud-pct">{elevated_pct}%</span>
        <div class="hud-bar-track"><div class="hud-bar-fill"></div></div>
      </div>
      <div class="hud-sub">{high_n} (&gt;150) &middot; Vitamin {lift_str}</div>
      <div class="hud-btn-row">
        <button class="hud-btn hud-btn-primary" onclick="focusPeak()">{L_FOCUS}</button>
        <button class="hud-btn hud-btn-ghost" onclick="resetView()">{L_VIEWALL}</button>
      </div>
    </div>
  </div>

  <!-- Bottom-Right Floating Alert Card -->
  <div class="hud-alert">
    <div class="hud-alert-top">
      <span class="hud-alert-eyebrow">{L_ALERT_EYE}</span>
      <div class="hud-alert-badge" aria-hidden="true">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
          <path d="M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M13.73 21a2 2 0 0 1-3.46 0" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>
    <div class="hud-alert-head">
      <span class="hud-alert-title">{alert_title}</span>
      <span class="hud-alert-metric">AQI {peak['aqi']:.0f}</span>
    </div>
    <div class="hud-alert-body">{alert_body}</div>
  </div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
  const CITIES = {cities_json};
  const COL_EMERALD = "{marker_normal}";
  const COL_AMBER = "{PALETTE['amber']}";
  const COL_CORAL = "{PALETTE['coral']}";
  const COL_VIVID = "{PALETTE['teal']}";
  const COL_BORDER = "{marker_border}";

  const map = L.map('aqiMap', {{
    zoomControl: false,
    scrollWheelZoom: false,
    zoomSnap: 0.25,
    attributionControl: true
  }});

  L.tileLayer('{tile_base}', {{
    attribution: '&copy; Esri, HERE, Garmin, OpenStreetMap',
    maxZoom: 14,
    minZoom: 3
  }}).addTo(map);

  L.tileLayer('{tile_ref}', {{
    maxZoom: 14,
    minZoom: 3,
    opacity: 0.72
  }}).addTo(map);

  const markerLayer = L.layerGroup().addTo(map);
  const routeLayer = L.layerGroup().addTo(map);
  let activeMarkers = [];
  let currentMode = 'all';

  function aqiColor(aqi) {{
    if (aqi > 150) return COL_CORAL;
    if (aqi > 100) return COL_AMBER;
    return COL_EMERALD;
  }}

  function fmtInr(v) {{
    if (v >= 1e6) return 'INR ' + (v / 1e6).toFixed(2) + 'M';
    if (v >= 1e3) return 'INR ' + (v / 1e3).toFixed(1) + 'K';
    return 'INR ' + Math.round(v).toLocaleString();
  }}

  function popupHtml(c, rankNum) {{
    const col = aqiColor(c.aqi);
    const badge = rankNum ? `<span style="display:inline-block;margin-left:6px;padding:1px 6px;border-radius:999px;background:${{col}};color:#fff;font-size:10px;font-weight:700;">#${{rankNum}}</span>` : '';
    return `
      <div class="pop-city">${{c.city}}${{badge}}</div>
      <div class="pop-state">${{c.state}} &middot; ${{c.region}} India</div>
      <div class="pop-grid">
        <div><div class="pop-k">Mean US AQI</div><div class="pop-v" style="color:${{col}}">${{c.aqi.toFixed(1)}}</div></div>
        <div><div class="pop-k">Mean PM2.5</div><div class="pop-v">${{c.pm25.toFixed(1)}} ug/m3</div></div>
        <div><div class="pop-k">Vitamin Rev</div><div class="pop-v">${{fmtInr(c.rev)}}</div></div>
        <div><div class="pop-k">Units Sold</div><div class="pop-v">${{c.units.toLocaleString()}}</div></div>
      </div>
    `;
  }}

  function animateMapNum(el, fromVal, toVal, decimals, suffix) {{
    if (!el) return;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {{
      el.textContent = toVal.toFixed(decimals) + (suffix || '');
      return;
    }}
    const start = performance.now();
    const dur = 480;
    function step(now) {{
      const t = Math.min(1, (now - start) / dur);
      const ease = 1 - Math.pow(1 - t, 3);
      const cur = fromVal + (toVal - fromVal) * ease;
      el.textContent = cur.toFixed(decimals) + (suffix || '');
      if (t < 1) requestAnimationFrame(step);
    }}
    requestAnimationFrame(step);
  }}

  function updateFocusCard(c, labelText) {{
    const col = aqiColor(c.aqi);
    document.getElementById('hudFocusLabel').textContent = labelText || 'Selected City Exposure';
    const aqiEl = document.getElementById('hudAqiVal');
    const unitEl = document.getElementById('hudAqiUnit');
    const pmEl = document.getElementById('hudPmVal');
    const prevAqi = parseFloat(aqiEl.textContent) || 0;
    const prevPm = parseFloat(pmEl.textContent) || 0;
    aqiEl.style.color = col;
    unitEl.style.color = col;
    animateMapNum(aqiEl, prevAqi, c.aqi, 1, '');
    animateMapNum(pmEl, prevPm, c.pm25, 1, ' ug/m3');
    document.getElementById('hudCitySub').textContent = c.city + ', ' + c.state + ' (' + fmtInr(c.rev) + ')';
  }}

  function pickSpacedTop3(list) {{
    const picked = [];
    for (const c of list) {{
      if (picked.length >= 3) break;
      const tooClose = picked.some(p => Math.hypot(p.lat - c.lat, p.lon - c.lon) < 2.2);
      if (!tooClose) picked.push(c);
    }}
    if (picked.length < Math.min(3, list.length)) {{
      for (const c of list) {{
        if (picked.length >= 3) break;
        if (!picked.includes(c)) picked.push(c);
      }}
    }}
    return picked;
  }}

  function smoothCurvePoints(pts) {{
    if (pts.length < 2) return pts.map(p => [p.lat, p.lon]);
    const out = [];
    for (let i = 0; i < pts.length - 1; i++) {{
      const p0 = pts[i];
      const p1 = pts[i + 1];
      const midLat = (p0.lat + p1.lat) / 2;
      const midLon = (p0.lon + p1.lon) / 2;
      const dLat = p1.lat - p0.lat;
      const dLon = p1.lon - p0.lon;
      const bend = (i % 2 === 0 ? 0.18 : -0.18);
      const ctrlLat = midLat - dLon * bend;
      const ctrlLon = midLon + dLat * bend;
      const steps = 28;
      for (let s = 0; s <= steps; s++) {{
        const t = s / steps;
        const inv = 1 - t;
        const lat = inv * inv * p0.lat + 2 * inv * t * ctrlLat + t * t * p1.lat;
        const lon = inv * inv * p0.lon + 2 * inv * t * ctrlLon + t * t * p1.lon;
        out.push([lat, lon]);
      }}
    }}
    return out;
  }}

  function fitSmart(list) {{
    if (!list.length) return;
    if (list.length === 1) {{
      map.setView([list[0].lat, list[0].lon], 6.5, {{ animate: true }});
      return;
    }}
    const bounds = L.latLngBounds(list.map(c => [c.lat, c.lon]));
    map.fitBounds(bounds, {{
      paddingTopLeft: [275, 28],
      paddingBottomRight: [40, 28],
      maxZoom: 6.5,
      animate: true
    }});
  }}

  function renderLayer(mode) {{
    currentMode = mode;
    markerLayer.clearLayers();
    routeLayer.clearLayers();
    activeMarkers = [];

    let subset = CITIES.slice();
    let corridorColor = CITIES[0] && CITIES[0].aqi > 150 ? COL_CORAL : COL_EMERALD;

    if (mode === 'risk') {{
      const highOnly = CITIES.filter(c => c.aqi > 150);
      subset = highOnly.length ? highOnly : CITIES.filter(c => c.aqi > 100);
      if (!subset.length) subset = CITIES.slice(0, 5);
      corridorColor = COL_CORAL;
    }} else if (mode === 'demand') {{
      subset = CITIES.slice().sort((a, b) => b.rev - a.rev);
      corridorColor = COL_EMERALD;
    }}

    const maxRev = Math.max(...subset.map(c => c.rev), 1);
    const minRev = Math.min(...subset.map(c => c.rev), 0);
    const top3 = pickSpacedTop3(subset);
    const top3Names = new Set(top3.map(c => c.city));

    // Smooth glowing corridor polyline connecting top 3
    if (top3.length >= 2) {{
      const orderedRoute = top3.slice().sort((a, b) => a.lon - b.lon);
      const curvePts = smoothCurvePoints(orderedRoute);
      L.polyline(curvePts, {{
        color: corridorColor,
        weight: 10,
        opacity: 0.14,
        lineCap: 'round'
      }}).addTo(routeLayer);
      L.polyline(curvePts, {{
        color: corridorColor,
        weight: 3.2,
        opacity: 0.88,
        lineCap: 'round'
      }}).addTo(routeLayer);
    }}

    // Supporting proportional circle markers
    subset.forEach(c => {{
      if (top3Names.has(c.city)) return;
      const ratio = maxRev > minRev ? (c.rev - minRev) / (maxRev - minRev) : 0.5;
      const rad = 6 + ratio * 7;
      const col = mode === 'demand' ? COL_VIVID : aqiColor(c.aqi);
      const m = L.circleMarker([c.lat, c.lon], {{
        radius: rad,
        fillColor: col,
        color: '#ffffff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.86
      }}).addTo(markerLayer);
      m.bindPopup(popupHtml(c, null), {{ offset: [0, -4] }});
      m.on('click', () => updateFocusCard(c, 'Selected City Exposure'));
      activeMarkers.push({{ city: c, marker: m }});
    }});

    // Top-3 glowing numbered pins (1, 2, 3)
    top3.forEach((c, idx) => {{
      const col = mode === 'demand' ? COL_EMERALD : aqiColor(c.aqi);
      const icon = L.divIcon({{
        className: '',
        html: `<div class="rank-pin-wrap"><div class="rank-pin-halo" style="background:${{col}};"></div><div class="rank-pin-core" style="background:${{col}};">${{idx + 1}}</div></div>`,
        iconSize: [28, 28],
        iconAnchor: [14, 14],
        popupAnchor: [0, -14]
      }});
      const m = L.marker([c.lat, c.lon], {{ icon, zIndexOffset: 500 - idx * 10 }}).addTo(markerLayer);
      m.bindPopup(popupHtml(c, idx + 1));
      m.on('click', () => updateFocusCard(c, mode === 'demand' ? 'Top Demand City #' + (idx + 1) : 'Top Exposure City #' + (idx + 1)));
      activeMarkers.push({{ city: c, marker: m }});
    }});

    fitSmart(subset);
  }}

  function setMode(mode) {{
    ['tabAll', 'tabRisk', 'tabDemand'].forEach(id => {{
      const el = document.getElementById(id);
      el.classList.remove('active', 'active-risk');
    }});
    if (mode === 'all') document.getElementById('tabAll').classList.add('active');
    if (mode === 'risk') document.getElementById('tabRisk').classList.add('active-risk');
    if (mode === 'demand') document.getElementById('tabDemand').classList.add('active');
    renderLayer(mode);
  }}

  function focusPeak() {{
    const target = activeMarkers.find(x => x.city.city === CITIES[0].city) || activeMarkers[0];
    if (!target) return;
    map.flyTo([target.city.lat, target.city.lon], 7, {{ duration: 0.7 }});
    setTimeout(() => target.marker.openPopup(), 450);
    updateFocusCard(target.city, 'Peak Pollution Exposure');
  }}

  function resetView() {{
    map.closePopup();
    if (CITIES[0]) updateFocusCard(CITIES[0], 'Peak Pollution Exposure');
    renderLayer(currentMode);
  }}

  renderLayer('all');
</script>
</body>
</html>"""

    components.html(map_html, height=height, scrolling=False)


def render_wellness_radar(df_slice, tier_label: str = "All Tiers", lang: str = "en"):
    """Renders a clean hexagonal spider-web radar SVG with 2-line muted label + bold value vertex callouts."""
    import math

    if df_slice.empty:
        return

    is_id = (lang == "id")
    avg_sleep = float(df_slice["sleep_duration_hrs"].mean())
    avg_qual = float(df_slice["quality_of_sleep"].mean())
    avg_act = float(df_slice["physical_activity_level"].mean())
    avg_stress = float(df_slice["stress_level"].mean())
    avg_steps = float(df_slice["daily_steps"].mean())
    avg_hr = float(df_slice["heart_rate_bpm"].mean()) if "heart_rate_bpm" in df_slice.columns else 70.0

    def clamp(v: float) -> float:
        return max(0.16, min(0.98, v))

    # 6 vertices matching Foto 2 exact flat-top / pointy-sides hexagon orientation
    # Order clockwise: Top-Left (-120), Top-Right (-60), Right (0), Bottom-Right (60), Bottom-Left (120), Left (180)
    axes = [
        {"label": "Jam Tidur" if is_id else "Sleep Hrs", "val_str": f"{avg_sleep:.1f} {'jam' if is_id else 'hrs'}", "norm": clamp(avg_sleep / 9.0), "deg": -120, "anchor": "end", "dx": -6, "dy": -18},
        {"label": "Kualitas Tidur" if is_id else "Sleep Quality", "val_str": f"{avg_qual:.1f} / 10", "norm": clamp(avg_qual / 10.0), "deg": -60, "anchor": "start", "dx": 6, "dy": -18},
        {"label": "Aktivitas" if is_id else "Activity", "val_str": f"{avg_act:.0f} {'mnt' if is_id else 'min'}", "norm": clamp(avg_act / 100.0), "deg": 0, "anchor": "start", "dx": 16, "dy": -4},
        {"label": "Tingkat Stres" if is_id else "Stress Level", "val_str": f"{avg_stress:.1f} / 10", "norm": clamp(avg_stress / 10.0), "deg": 60, "anchor": "start", "dx": 6, "dy": 14},
        {"label": "Detak Jantung" if is_id else "Heart Rate", "val_str": f"{avg_hr:.0f} bpm", "norm": clamp(avg_hr / 100.0), "deg": 120, "anchor": "end", "dx": -6, "dy": 14},
        {"label": "Langkah Harian" if is_id else "Daily Steps", "val_str": f"{avg_steps:,.0f}", "norm": clamp(avg_steps / 10000.0), "deg": 180, "anchor": "end", "dx": -16, "dy": -4},
    ]

    cx, cy, max_r = 240.0, 172.0, 108.0

    def pt(deg: float, radius: float):
        rad = math.radians(deg)
        return cx + radius * math.cos(rad), cy + radius * math.sin(rad)

    grid_svg = []
    # 3 concentric polygonal rings (33%, 66%, 100%)
    for frac in (0.33, 0.66, 1.0):
        pts_str = " ".join(f"{pt(a['deg'], max_r * frac)[0]:.1f},{pt(a['deg'], max_r * frac)[1]:.1f}" for a in axes)
        grid_svg.append(
            f'<polygon points="{pts_str}" fill="none" stroke="{PALETTE["gridline"]}" stroke-width="1.25" />'
        )
    # 6 radial spokes
    for a in axes:
        vx, vy = pt(a["deg"], max_r)
        grid_svg.append(
            f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{vx:.1f}" y2="{vy:.1f}" stroke="{PALETTE["gridline"]}" stroke-width="1.15" />'
        )

    # Data polygon + ringed vertex dots
    data_pts = [pt(a["deg"], max_r * a["norm"]) for a in axes]
    data_pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in data_pts)
    poly_svg = (
        f'<polygon points="{data_pts_str}" fill="{PALETTE["radar_fill"]}" '
        f'stroke="{PALETTE["chart_primary"]}" stroke-width="2.2" stroke-linejoin="round" />'
    )

    nodes_svg = []
    halo_col = "#c8f169" if PALETTE["is_dark"] else "#78c51c"
    for a, (dx_pt, dy_pt) in zip(axes, data_pts):
        tip = f"{tier_label} | {a['label']}: {a['val_str']} ({a['norm'] * 100:.0f}%)"
        lx, ly = pt(a["deg"], max_r)
        tx = lx + a["dx"]
        ty = ly + a["dy"]
        ax_slug = a["label"].lower().replace(" ", "_")
        nodes_svg.append(
            f'<g class="radar-axis-node">'
            f'<title>{tip}</title>'
            f'<circle class="radar-halo" cx="{dx_pt:.1f}" cy="{dy_pt:.1f}" r="5.2" fill="{halo_col}" '
            f'style="transform-origin:{dx_pt:.1f}px {dy_pt:.1f}px;" />'
            f'<circle class="radar-dot" cx="{dx_pt:.1f}" cy="{dy_pt:.1f}" r="5.2" fill="{PALETTE["chart_primary"]}" '
            f'stroke="{PALETTE["white"]}" stroke-width="2.5" style="transform-origin:{dx_pt:.1f}px {dy_pt:.1f}px;" />'
            f'<circle cx="{dx_pt:.1f}" cy="{dy_pt:.1f}" r="18" fill="transparent" />'
            f'<g class="radar-label-g" style="transform-origin:{tx:.1f}px {ty + 8:.1f}px;">'
            f'<text class="radar-lbl-name" x="{tx:.1f}" y="{ty:.1f}" text-anchor="{a["anchor"]}" '
            f'font-family="Inter, sans-serif" font-size="12" font-weight="400" fill="{PALETTE["muted"]}">{a["label"]}</text>'
            f'<text id="yv_num_radar_{ax_slug}" class="radar-lbl-val anim-num" x="{tx:.1f}" y="{ty + 20:.1f}" text-anchor="{a["anchor"]}" '
            f'font-family="Inter, sans-serif" font-size="16.5" font-weight="700" letter-spacing="-0.02em" fill="{PALETTE["emerald"]}">{a["val_str"]}</text>'
            f'</g>'
            f'</g>'
        )

    svg = (
        f'<div style="display:flex; align-items:center; justify-content:center; width:100%; padding:4px 0 2px 0;">'
        f'<svg viewBox="0 0 480 344" width="100%" style="max-width:490px; height:auto; overflow:visible;" '
        f'role="img" aria-label="Hexagonal wellness profile radar for {tier_label}">'
        f'{"".join(grid_svg)}'
        f'<g id="yv_radar_group" class="radar-bloom-group">{poly_svg}</g>'
        f'{"".join(nodes_svg)}'
        f'</svg></div>'
    )
    st.markdown(svg, unsafe_allow_html=True)


def inject_motion_engine(nonce: str = ""):
    """Injects a permanent main-window script into window.parent.document.head for 60fps counting & chart morphing."""
    import json
    import time
    import streamlit.components.v1 as components

    tick = f"{nonce}_{int(time.time() * 1000)}"
    parent_script = r"""
(function() {
  if (window.__yvMotionVer === 4) {
    if (window.__yvRunSweep) window.__yvRunSweep();
    return;
  }
  if (window.__yvMotionObs) {
    try { window.__yvMotionObs.disconnect(); } catch (e) {}
  }
  window.__yvMotionVer = 6;
  if (!window.__yvNumStore) window.__yvNumStore = new Map();
  if (!window.__yvBarStore) window.__yvBarStore = new Map();
  if (!window.__yvSvgStore) window.__yvSvgStore = new Map();
  if (!window.__yvPlotlyStore) window.__yvPlotlyStore = new Map();
  if (!window.__yvRafMap) window.__yvRafMap = new WeakMap();
  if (!window.__yvClipRafMap) window.__yvClipRafMap = new Map();

  const SVG_NS = 'http://www.w3.org/2000/svg';
  const reducedMotion = () =>
    Boolean(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  function parseNum(str) {
    const clean = String(str || '').trim();
    const m = clean.match(/^([^0-9\-+]*?)([+-]?\d[\d,]*(?:\.\d+)?)(.*)$/);
    if (!m) return null;
    const prefix = m[1];
    const raw = m[2];
    const suffix = m[3];
    const hasPlus = raw.startsWith('+');
    const hasComma = raw.indexOf(',') !== -1;
    const dot = raw.indexOf('.');
    const decimals = dot === -1 ? 0 : (raw.length - dot - 1);
    const val = parseFloat(raw.replace(/,/g, ''));
    if (isNaN(val)) return null;
    return { prefix, val, decimals, hasComma, hasPlus, suffix };
  }

  function formatNum(p, v) {
    let fixed = v.toFixed(p.decimals);
    if (p.hasComma) {
      const parts = fixed.split('.');
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      fixed = parts.join('.');
    }
    const plus = (p.hasPlus && v >= 0 && !fixed.startsWith('+')) ? '+' : '';
    return p.prefix + plus + fixed + p.suffix;
  }

  function animateNumberEl(el, idx) {
    if (el.__yvWriting) return;
    const currentText = (el.textContent || '').trim();
    if (!currentText) return;
    if (el.__yvTargetText === currentText) return;
    if (el.__yvAnimDisplayed === currentText) return;

    const parsed = parseNum(currentText);
    if (!parsed) {
      el.__yvTargetText = currentText;
      return;
    }

    const key = el.id || ('yv_auto_' + idx + '_' + parsed.prefix + '_' + parsed.suffix);
    const hasPrev = window.__yvNumStore.has(key);
    const fromVal = hasPrev ? window.__yvNumStore.get(key) : 0;
    window.__yvNumStore.set(key, parsed.val);
    el.__yvTargetText = currentText;

    if (reducedMotion() || (hasPrev && Math.abs(parsed.val - fromVal) < 1e-9)) {
      return;
    }

    const prevRaf = window.__yvRafMap.get(el);
    if (prevRaf) window.cancelAnimationFrame(prevRaf);

    const start = performance.now();
    const duration = 700;
    function step(now) {
      if (!document.contains(el)) return;
      const t = Math.min(1, (now - start) / duration);
      const ease = 1 - Math.pow(1 - t, 3);
      const curVal = fromVal + (parsed.val - fromVal) * ease;
      const txt = t >= 1 ? currentText : formatNum(parsed, curVal);
      el.__yvWriting = true;
      el.__yvAnimDisplayed = txt;
      el.textContent = txt;
      el.__yvWriting = false;
      if (t < 1) {
        window.__yvRafMap.set(el, window.requestAnimationFrame(step));
      }
    }
    window.__yvRafMap.set(el, window.requestAnimationFrame(step));
  }

  function animateCapsuleBars() {
    if (reducedMotion()) return;
    document.querySelectorAll('.spb-capsule').forEach((bar, idx) => {
      const targetH = bar.style.height;
      if (!targetH || bar.__yvAnimH === targetH) return;
      const key = bar.id || ('spb_' + idx);
      const prevH = window.__yvBarStore.has(key) ? window.__yvBarStore.get(key) : '0%';
      window.__yvBarStore.set(key, targetH);
      bar.__yvAnimH = targetH;
      if (prevH === targetH) return;

      bar.style.transition = 'none';
      bar.style.height = prevH;
      void bar.offsetHeight;
      bar.style.transition = 'height 640ms cubic-bezier(0.22, 1, 0.36, 1), transform 160ms ease, filter 160ms ease';
      bar.style.height = targetH;
    });
  }

  function animateSvgShapes() {
    if (reducedMotion()) return;
    document.querySelectorAll('.arc-path-anim').forEach((pathEl, idx) => {
      const d = pathEl.getAttribute('d') || '';
      const key = pathEl.id || ('arc_' + idx);
      const prevD = window.__yvSvgStore.get(key);
      if (prevD && prevD !== d) {
        pathEl.style.animation = 'none';
        void pathEl.getBoundingClientRect();
        pathEl.style.animation = 'arcDraw 720ms cubic-bezier(0.22, 1, 0.36, 1) both';
      }
      window.__yvSvgStore.set(key, d);
    });

    const radarGrp = document.getElementById('yv_radar_group');
    if (radarGrp) {
      const poly = radarGrp.querySelector('polygon');
      const pts = poly ? (poly.getAttribute('points') || '') : '';
      const prevPts = window.__yvSvgStore.get('yv_radar_pts');
      if (prevPts && prevPts !== pts) {
        radarGrp.style.animation = 'none';
        void radarGrp.getBoundingClientRect();
        radarGrp.style.animation = 'radarBloom 580ms cubic-bezier(0.22, 1, 0.36, 1) both';
      }
      window.__yvSvgStore.set('yv_radar_pts', pts);
    }
  }

  function sweepSvgLayerWithClipPath(mainSvg, targetLayers, annotations, clipId, durationMs) {
    if (!mainSvg || !targetLayers.length) return;
    let defs = mainSvg.querySelector('defs');
    if (!defs) {
      defs = document.createElementNS(SVG_NS, 'defs');
      mainSvg.insertBefore(defs, mainSvg.firstChild);
    }
    let clipEl = mainSvg.querySelector('#' + clipId);
    if (clipEl) clipEl.remove();

    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    targetLayers.forEach(layer => {
      try {
        const bb = layer.getBBox();
        if (bb && bb.width > 0) {
          minX = Math.min(minX, bb.x);
          minY = Math.min(minY, bb.y);
          maxX = Math.max(maxX, bb.x + bb.width);
          maxY = Math.max(maxY, bb.y + bb.height);
        }
      } catch (e) {}
    });
    if (!isFinite(minX) || maxX <= minX) {
      const r = mainSvg.getBoundingClientRect();
      minX = 0; minY = 0; maxX = r.width || 900; maxY = r.height || 400;
    }

    const padX = 18;
    const padY = 44;
    const fullW = (maxX - minX) + padX * 2;
    const fullH = (maxY - minY) + padY * 2;

    clipEl = document.createElementNS(SVG_NS, 'clipPath');
    clipEl.setAttribute('id', clipId);
    const rect = document.createElementNS(SVG_NS, 'rect');
    rect.setAttribute('x', String(minX - padX));
    rect.setAttribute('y', String(minY - padY));
    rect.setAttribute('width', '0');
    rect.setAttribute('height', String(fullH));
    clipEl.appendChild(rect);
    defs.appendChild(clipEl);

    targetLayers.forEach(layer => layer.setAttribute('clip-path', 'url(#' + clipId + ')'));
    annotations.forEach(an => { an.style.opacity = '0'; });

    const prevRaf = window.__yvClipRafMap.get(clipId);
    if (prevRaf) window.cancelAnimationFrame(prevRaf);

    const start = performance.now();
    function frame(now) {
      if (!document.contains(mainSvg)) return;
      const t = Math.min(1, (now - start) / durationMs);
      const ease = 1 - Math.pow(1 - t, 3);
      rect.setAttribute('width', String(ease * fullW));

      if (annotations.length) {
        const aT = Math.max(0, Math.min(1, (t - 0.35) / 0.55));
        annotations.forEach(an => { an.style.opacity = String(aT); });
      }

      if (t < 1) {
        window.__yvClipRafMap.set(clipId, window.requestAnimationFrame(frame));
      } else {
        targetLayers.forEach(layer => layer.removeAttribute('clip-path'));
        annotations.forEach(an => { an.style.opacity = '1'; });
        if (clipEl && clipEl.parentNode) clipEl.remove();
      }
    }
    window.__yvClipRafMap.set(clipId, window.requestAnimationFrame(frame));
  }

  function animatePlotlyCharts() {
    if (reducedMotion()) return;
    document.querySelectorAll('[data-testid="stPlotlyChart"]').forEach((box, idx) => {
      const mainSvg = box.querySelector('svg.main-svg');
      const plotLayer = box.querySelector('.plot');
      if (!mainSvg || !plotLayer) return;

      const linePaths = box.querySelectorAll('.scatterlayer .js-line');
      const barPaths = box.querySelectorAll('.barlayer path');
      let sigParts = [];
      linePaths.forEach(p => sigParts.push(p.getAttribute('d') || ''));
      if (!sigParts.length && barPaths.length) {
        barPaths.forEach((p, bi) => { if (bi < 12) sigParts.push(p.getAttribute('d') || ''); });
      }
      if (!sigParts.length) {
        const hm = box.querySelector('.heatmaplayer, .hmlayer');
        sigParts.push(hm ? String(hm.innerHTML.length) : String(plotLayer.innerHTML.length));
      }
      const sig = sigParts.join('|');
      if (!sig) return;

      const key = 'plt_' + idx;
      const prevSig = window.__yvPlotlyStore.get(key);
      if (prevSig === sig) return;
      window.__yvPlotlyStore.set(key, sig);

      if (linePaths.length > 0) {
        const scatterLayers = Array.from(box.querySelectorAll('.scatterlayer'));
        const annots = Array.from(box.querySelectorAll('.infolayer .annotation'));
        sweepSvgLayerWithClipPath(mainSvg, scatterLayers, annots, 'yv_clip_line_' + idx, 820);
      } else if (barPaths.length > 0) {
        const barLayers = Array.from(box.querySelectorAll('.barlayer'));
        sweepSvgLayerWithClipPath(mainSvg, barLayers, [], 'yv_clip_bar_' + idx, 660);
      } else {
        const start = performance.now();
        plotLayer.style.opacity = '0.2';
        function fadeStep(now) {
          if (!document.contains(plotLayer)) return;
          const t = Math.min(1, (now - start) / 480);
          plotLayer.style.opacity = String(0.2 + 0.8 * (1 - Math.pow(1 - t, 3)));
          if (t < 1) window.requestAnimationFrame(fadeStep);
        }
        window.requestAnimationFrame(fadeStep);
      }
    });
  }

  function syncPairedCardHeights() {
    document.querySelectorAll('[data-testid="stHorizontalBlock"]').forEach(row => {
      const cols = Array.from(row.children).filter(
        c => c.getAttribute && c.getAttribute('data-testid') === 'stColumn'
      );
      if (cols.length !== 2) return;
      const cards = cols.map(col => {
        if (col.querySelector('.bento-compact') || col.querySelector('.nested-hero') || col.querySelector('.bento-leader-card')) return null;
        const found = col.querySelector('div[class*="st-key-card_"]');
        if (!found || found.className.includes('st-key-card_p3_drill') || found.className.includes('st-key-card_p1_donut')) return null;
        return found;
      });
      if (!cards[0] || !cards[1]) return;

      cards[0].style.minHeight = '';
      cards[1].style.minHeight = '';
      const r0 = cards[0].getBoundingClientRect();
      const r1 = cards[1].getBoundingClientRect();
      if (Math.abs(r0.top - r1.top) > 24) return;

      const maxH = Math.ceil(Math.max(r0.height, r1.height));
      if (maxH > 120) {
        cards[0].style.minHeight = maxH + 'px';
        cards[1].style.minHeight = maxH + 'px';
      }
    });
  }

  function runSweep() {
    document.querySelectorAll('.anim-num').forEach(animateNumberEl);
    animateCapsuleBars();
    animateSvgShapes();
    animatePlotlyCharts();
    syncPairedCardHeights();
  }

  window.__yvRunSweep = runSweep;
  if (window.__yvResizeHandler) {
    window.removeEventListener('resize', window.__yvResizeHandler);
  }
  window.__yvResizeHandler = () => {
    window.requestAnimationFrame(syncPairedCardHeights);
  };
  window.addEventListener('resize', window.__yvResizeHandler);

  let debounceTimer = null;
  const obs = new MutationObserver(() => {
    if (debounceTimer) window.clearTimeout(debounceTimer);
    debounceTimer = window.setTimeout(runSweep, 25);
  });
  obs.observe(document.body, {
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
    attributeFilter: ['d', 'points']
  });
  window.__yvMotionObs = obs;

  runSweep();
})();
"""
    script_json = json.dumps(parent_script)
    bootstrap_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8" /></head><body>
<script>
(function() {{
  try {{
    const pWin = window.parent;
    const pDoc = pWin.document;
    if (!pDoc || !pDoc.head) return;
    if (pWin.__yvMotionVer !== 6) {{
      ['yv-motion-engine-v2', 'yv-motion-engine-v3', 'yv-motion-engine-v4', 'yv-motion-engine-v5', 'yv-motion-engine-v6'].forEach(id => {{
        const old = pDoc.getElementById(id);
        if (old) old.remove();
      }});
      const s = pDoc.createElement('script');
      s.id = 'yv-motion-engine-v6';
      s.textContent = {script_json};
      pDoc.head.appendChild(s);
    }} else if (typeof pWin.__yvRunSweep === 'function') {{
      pWin.__yvRunSweep();
    }}
    pWin.setTimeout(() => {{ if (typeof pWin.__yvRunSweep === 'function') pWin.__yvRunSweep(); }}, 60);
    pWin.setTimeout(() => {{ if (typeof pWin.__yvRunSweep === 'function') pWin.__yvRunSweep(); }}, 240);
    pWin.setTimeout(() => {{ if (typeof pWin.__yvRunSweep === 'function') pWin.__yvRunSweep(); }}, 520);
  }} catch (e) {{}}
}})();
</script>
</body></html>"""
    components.html(bootstrap_html, height=1, scrolling=False)
