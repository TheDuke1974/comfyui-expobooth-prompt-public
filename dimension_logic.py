def safe_float(value, default=3.0):
    """
    Convert a value to float with a safe fallback.
    Kept intentionally simple for public deployment.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def generate_dimension_prompt(width_m, depth_m, height_m):
    """
    Public-safe dimension helper for ComfyUI booth prompt generation.

    This version returns basic dimensional wording only.
    It avoids exposing advanced spatial heuristics, planning rules,
    proportional logic, or production-specific prompt strategy.
    """
    width_m = safe_float(width_m, 3.0)
    depth_m = safe_float(depth_m, 3.0)
    height_m = safe_float(height_m, 3.0)

    area = width_m * depth_m

    dimension_statement = (
        f"booth dimensions: {width_m:.1f}m wide x "
        f"{depth_m:.1f}m deep x {height_m:.1f}m high"
    )

    spatial_guidance = (
        "use realistic exhibition booth proportions, clear visitor access, "
        "readable layout, and a balanced presentation of brand and product areas"
    )

    summary = (
        f"{width_m:.1f}m x {depth_m:.1f}m x {height_m:.1f}m | "
        f"{area:.1f} sqm"
    )

    debug = {
        "width_m": width_m,
        "depth_m": depth_m,
        "height_m": height_m,
        "area_sqm": round(area, 2),
        "summary": summary,
    }

    return {
        "dimension_statement": dimension_statement,
        "spatial_guidance": spatial_guidance,
        "summary": summary,
        "debug": debug,
    }
