def build_camera_prompt(camera_mode):
    """
    Public-safe camera prompt helper for ComfyUI exhibition booth prompt nodes.

    This helper intentionally uses generic camera descriptions only.
    It does not include private production methodology, advanced composition logic,
    client-specific terminology, or internal ExpoBooth prompt strategy.
    """
    mode = (camera_mode or "").strip().lower()

    presets = {
        "hero": (
            "three-quarter presentation view, eye-level camera, clear view of the booth front and depth, "
            "balanced composition, suitable for a professional concept render"
        ),
        "front": (
            "front-facing view, centered composition, clear view of the main booth frontage, "
            "readable branding area, clean presentation angle"
        ),
        "right corner": (
            "right-side three-quarter view, showing the front and right side of the booth, "
            "clear spatial depth and readable booth layout"
        ),
        "left corner": (
            "left-side three-quarter view, showing the front and left side of the booth, "
            "clear spatial depth and readable booth layout"
        ),
        "wide": (
            "wide view showing the full booth footprint, surrounding aisle space, "
            "and general trade show environment"
        ),
        "dramatic": (
            "slightly lower camera angle with a stronger presentation feel, "
            "showing booth height, structure, and overall visual impact while keeping the layout readable"
        ),
    }

    return presets.get(
        mode,
        "three-quarter presentation view, eye-level camera, clear booth layout, readable branding area"
    )
