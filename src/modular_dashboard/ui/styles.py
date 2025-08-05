"""Modern Tailwind CSS styles and design tokens for dashboard components.

This module provides centralized styling constants using modern Tailwind CSS classes
for consistent, beautiful design across all dashboard components.
"""


class DesignSystem:
    """Modern design system with refined glass morphism styling."""

    # Base glass effect specifications
    GLASS_OPACITY = "90"
    GLASS_BLUR = "16"
    BORDER_OPACITY = "15"

    # Standard border radius
    BORDER_RADIUS_SM = "lg"
    BORDER_RADIUS_MD = "xl"
    BORDER_RADIUS_LG = "2xl"
    BORDER_RADIUS_XL = "3xl"

    # hadows with softer colors
    SHADOW_SM = "shadow-sm shadow-gray-900/5"
    SHADOW_MD = "shadow-md shadow-gray-900/10"
    SHADOW_LG = "shadow-lg shadow-gray-900/15"
    SHADOW_XL = "shadow-xl shadow-gray-900/20"
    SHADOW_2XL = "shadow-2xl shadow-gray-900/25"


class DashboardStyles:
    """Centralized styling constants for dashboard components using modern Tailwind CSS."""

    # Background styles
    MAIN_BG: str = "bg-gradient-to-br from-gray-50 to-gray-100"
    DETAIL_BG: str = "bg-gradient-to-br from-gray-50/80 to-gray-100/60"

    # Glass morphism base
    GLASS_BASE: str = (
        f"bg-white/{DesignSystem.GLASS_OPACITY} "
        f"backdrop-blur-{DesignSystem.GLASS_BLUR} "
        f"border border-gray-200/{DesignSystem.BORDER_OPACITY} "
        f"shadow-{DesignSystem.SHADOW_SM}"
    )

    # Standard card styles
    CARD: str = (
        f"{GLASS_BASE} rounded-{DesignSystem.BORDER_RADIUS_LG} "
        f"{DesignSystem.SHADOW_LG} transition-all duration-300 hover:shadow-2xl"
    )

    # Card styles
    CARD: str = (
        f"{GLASS_BASE} rounded-{DesignSystem.BORDER_RADIUS_LG} "
        f"{DesignSystem.SHADOW_MD} transition-all duration-300 "
        f"hover:shadow-xl hover:scale-[1.02] cursor-pointer"
    )

    # Header styles
    HEADER: str = (
        f"{GLASS_BASE} rounded-t-{DesignSystem.BORDER_RADIUS_LG} border-0 border-b border-gray-200/20 "
        f"{DesignSystem.SHADOW_SM}"
    )

    # Button styles
    BUTTON_PRIMARY: str = (
        f"{GLASS_BASE} rounded-{DesignSystem.BORDER_RADIUS_MD} "
        f"{DesignSystem.SHADOW_MD} text-gray-700 hover:bg-white/95 "
        f"hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300"
    )

    BUTTON_SECONDARY: str = (
        f"{GLASS_BASE} rounded-{DesignSystem.BORDER_RADIUS_MD} "
        f"{DesignSystem.SHADOW_SM} text-gray-600 hover:bg-white/90 "
        f"hover:shadow-md transition-all duration-300"
    )

    BUTTON_OUTLINE: str = (
        f"{GLASS_BASE} rounded-{DesignSystem.BORDER_RADIUS_MD} "
        f"border border-gray-300 text-gray-700 hover:bg-white/95 "
        f"hover:border-gray-400 hover:shadow-sm transition-all duration-300"
    )

    BUTTON_ACTION: str = (
        f"bg-gradient-to-r from-blue-500 to-indigo-600 "
        f"text-white rounded-{DesignSystem.BORDER_RADIUS_MD} "
        f"{DesignSystem.SHADOW_LG} hover:shadow-xl transition-all duration-300 "
        f"hover:scale-105"
    )

    # Floating action button
    FAB: str = (
        f"bg-gradient-to-r from-blue-500 to-indigo-600 text-white "
        f"rounded-full {DesignSystem.SHADOW_XL} hover:shadow-2xl "
        f"transition-all duration-300 hover:scale-110"
    )

    # Typography styles
    TITLE_H1: str = "text-4xl font-light text-gray-800 tracking-tight"
    TITLE_H2: str = "text-3xl font-light text-gray-700 tracking-tight"
    TITLE_H3: str = "text-2xl font-medium text-gray-700"
    TITLE_H4: str = "text-xl font-medium text-gray-700"
    BODY_TEXT: str = "text-base text-gray-600"
    SUBTLE_TEXT: str = "text-sm text-gray-500"
    ERROR_TEXT: str = "text-lg font-light text-gray-600 tracking-tight"
    FONT_MEDIUM: str = "font-medium"
    FONT_SEMIBOLD: str = "font-semibold"
    FONT_BOLD: str = "font-bold"
    TEXT_XS: str = "text-xs"

    # Text styles
    TEXT_PRIMARY: str = "text-gray-700"
    TEXT_SECONDARY: str = "text-gray-500"
    TEXT_MUTED: str = "text-gray-400"
    TEXT_ERROR: str = "text-red-500"
    TEXT_SUCCESS: str = "text-green-500"
    TEXT_WARNING: str = "text-amber-500"
    TEXT_SM_MEDIUM: str = "text-sm font-medium text-gray-600"
    TEXT_XS_MUTED: str = "text-xs text-gray-400"

    # Icon styles
    ICON_PRIMARY: str = "text-blue-500"
    ICON_SECONDARY: str = "text-gray-500"
    ICON_ERROR: str = "text-red-500"
    ICON_SUCCESS: str = "text-green-500"
    ICON_WARNING: str = "text-amber-500"

    # Interactive states
    HOVER_SCALE: str = "hover:scale-105 transition-all duration-200"
    HOVER_TRANSLATE: str = "hover:-translate-y-0.5 transition-all duration-200"
    HOVER_SHADOW: str = "hover:shadow-lg transition-all duration-200"
    CARD_HOVER: str = "hover:shadow-xl hover:scale-[1.02] transition-all duration-200"

    # Layout utilities
    CONTAINER_CENTER: str = "w-full items-center max-w-7xl mx-auto"
    SCREEN_CENTER: str = "w-full items-center justify-center min-h-screen"
    FULL_WIDTH: str = "w-full"
    CENTER_CONTENT: str = "items-center justify-center"
    FLEX_BETWEEN: str = "w-full justify-between items-center"
    FLEX_CENTER: str = "items-center justify-center"
    FLEX_GROW: str = "flex-grow"

    # Grid and responsive
    GRID_RESPONSIVE: str = "grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4"
    GRID_2_COL: str = "grid-cols-1 sm:grid-cols-2"
    GRID_3_COL: str = "grid-cols-1 sm:grid-cols-2 md:grid-cols-3"
    GRID_4_COL: str = "grid-cols-1 sm:grid-cols-2 md:grid-cols-4"

    # Spacing utilities
    PADDING_XS: str = "p-2"
    PADDING_SM: str = "p-3"
    PADDING_MD: str = "p-4"
    PADDING_LG: str = "p-6"
    PADDING_XL: str = "p-8"
    PADDING_XXL: str = "p-12"

    PADDING_X_XS: str = "px-2"
    PADDING_X_SM: str = "px-3"
    PADDING_X_MD: str = "px-4"
    PADDING_X_LG: str = "px-6"
    PADDING_X_XL: str = "px-12"

    PADDING_Y_XS: str = "py-2"
    PADDING_Y_SM: str = "py-3"
    PADDING_Y_MD: str = "py-4"
    PADDING_Y_LG: str = "py-6"
    PADDING_Y_XL: str = "py-8"
    PADDING_Y_XXL: str = "py-12"

    MARGIN_SM: str = "m-2"
    MARGIN_MD: str = "m-4"
    MARGIN_LG: str = "m-6"
    MARGIN_XL: str = "m-8"

    MARGIN_X_SM: str = "mx-2"
    MARGIN_X_MD: str = "mx-4"
    MARGIN_X_LG: str = "mx-6"
    MARGIN_X_XL: str = "mx-auto"

    MARGIN_Y_SM: str = "my-2"
    MARGIN_Y_MD: str = "my-4"
    MARGIN_Y_LG: str = "my-6"
    MARGIN_Y_XL: str = "my-8"

    GAP_XS: str = "gap-1"
    GAP_SM: str = "gap-2"
    GAP_MD: str = "gap-4"
    GAP_LG: str = "gap-6"
    GAP_XL: str = "gap-8"

    # Specific styles
    CARD_HOVER_EFFECT: str = "card-hover"
    LINK_NO_UNDERLINE: str = "no-underline text-inherit"
    TEXT_CENTER: str = "text-center"
    TEXT_LEFT: str = "text-left"
    TEXT_RIGHT: str = "text-right"
    MODULE_CARD: str = CARD

    # Status colors
    STATUS_SUCCESS: str = "bg-green-500 text-white"
    STATUS_ERROR: str = "bg-red-500 text-white"
    STATUS_WARNING: str = "bg-amber-500 text-white"
    STATUS_INFO: str = "bg-blue-500 text-white"

    # Badge styles
    BADGE_BLUE: str = (
        "bg-blue-50 text-blue-600 text-xs font-medium px-2.5 py-0.5 rounded-full"
    )
    BADGE_PRIMARY: str = (
        "bg-indigo-50 text-indigo-600 text-xs font-medium px-2.5 py-0.5 rounded-full"
    )
    BADGE_SECONDARY: str = (
        "bg-gray-50 text-gray-600 text-xs font-medium px-2.5 py-0.5 rounded-full"
    )
    BADGE_SUCCESS: str = (
        "bg-green-50 text-green-600 text-xs font-medium px-2.5 py-0.5 rounded-full"
    )
    BADGE_WARNING: str = (
        "bg-amber-50 text-amber-600 text-xs font-medium px-2.5 py-0.5 rounded-full"
    )

    # Border styles
    BORDER_NONE: str = "border-0"
    BORDER_LEFT: str = "border-l-4"
    BORDER_RED: str = "border-red-500"
    BORDER_GRAY: str = "border-gray-300"

    # Special elements
    GLASS_CARD: str = CARD
    GLASS_HEADER: str = HEADER
    DETAIL_CARD: str = CARD
    MODULE_CONTAINER: str = f"{FULL_WIDTH} {GAP_LG}"
    STATS_CARD: str = f"{CARD} p-6 flex-1 text-center"
