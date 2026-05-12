"""
Public deployment-safe ComfyUI custom node.

This file is intentionally simplified for public/hosted deployment.
It avoids private prompt heuristics, client-specific logic, external API calls,
and proprietary production workflow details.
"""


class ExpoBoothPromptBuilder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "brand_name": ("STRING", {"default": "Brand"}),
                "brand_colors": ("STRING", {"default": "blue and white"}),
                "booth_type": (
                    ["inline booth", "corner booth", "peninsula booth", "island booth"],
                    {"default": "inline booth"},
                ),
                "open_sides": (
                    ["1 side open", "2 sides open", "3 sides open", "4 sides open"],
                    {"default": "2 sides open"},
                ),
                "material": (
                    ["Panels", "Graphic fabric", "LED Fabric"],
                    {"default": "Panels"},
                ),
                "flooring": (
                    [
                        "Only carpet",
                        "40mm raised floor",
                        "100mm raised floor with access ramp",
                    ],
                    {"default": "Only carpet"},
                ),
                "truss": (
                    [
                        "None",
                        "Only truss",
                        "Truss with LED strips",
                        "Truss with PAR lights",
                    ],
                    {"default": "None"},
                ),
                "storage": (
                    [
                        "None",
                        "1x1",
                        "2x1",
                    ],
                    {"default": "None"},
                ),
                "storage_position": (
                    [
                        "Auto",
                        "Left",
                        "Right",
                    ],
                    {"default": "Auto"},
                ),
                "width_m": ("FLOAT", {"default": 4.0, "min": 1.0, "max": 50.0, "step": 0.1}),
                "depth_m": ("FLOAT", {"default": 3.0, "min": 1.0, "max": 50.0, "step": 0.1}),
                "height_m": (
                    ["2.5", "3.0", "3.5", "4.0"],
                    {"default": "3.0"},
                ),
                "style_keywords": ("STRING", {"default": "modern, clean, premium"}),
                "product_focus": ("STRING", {"default": "product display and brand presentation"}),
                "camera_mode": (
                    ["hero", "front", "right corner", "left corner", "wide", "dramatic"],
                    {"default": "hero"},
                ),
                "user_prompt": ("STRING", {"default": "your prompt", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("final_prompt", "summary", "debug")
    FUNCTION = "build_prompt"
    CATEGORY = "ExpoBooth"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def _clean_text(self, value, max_chars=1200):
        text = str(value or "").strip()

        if text.lower() == "your prompt":
            return ""

        text = " ".join(text.split())

        if len(text) > max_chars:
            text = text[:max_chars].rsplit(" ", 1)[0].strip()
            text += " ... [text trimmed]"

        return text

    def _dimension_text(self, width_m, depth_m, height_m):
        return (
            f"booth footprint approximately {width_m:g}m wide by {depth_m:g}m deep, "
            f"maximum visual height approximately {height_m:g}m, realistic exhibition proportions"
        )

    def _camera_text(self, camera_mode):
        camera_map = {
            "hero": "hero three-quarter perspective, clear view of the stand architecture",
            "front": "straight frontal perspective, clean view of the main elevation",
            "right corner": "right corner perspective, showing depth and side visibility",
            "left corner": "left corner perspective, showing depth and side visibility",
            "wide": "wide-angle exhibition hall perspective, showing booth and surrounding context",
            "dramatic": "dramatic low-angle perspective with strong presentation impact",
        }
        return camera_map.get(camera_mode, "balanced exhibition booth perspective")

    def _booth_type_text(self, booth_type):
        booth_type_map = {
            "inline booth": "inline exhibition booth concept with a front-facing visitor side",
            "corner booth": "corner exhibition booth concept with two visible visitor-facing sides",
            "peninsula booth": "peninsula exhibition booth concept with multiple open visitor-facing sides",
            "island booth": "island exhibition booth concept open on all sides",
        }
        return booth_type_map.get(booth_type, booth_type)

    def _open_sides_text(self, open_sides):
        open_side_map = {
            "1 side open": "one open visitor-facing side",
            "2 sides open": "two open visitor-facing sides",
            "3 sides open": "three open visitor-facing sides",
            "4 sides open": "four open visitor-facing sides with an open island-style layout",
        }
        return open_side_map.get(open_sides, open_sides)

    def _material_text(self, material):
        material_map = {
            "Panels": "clean panel-based booth wall system",
            "Graphic fabric": "printed fabric graphics with clean exhibition finish",
            "LED Fabric": "illuminated graphic fabric effect with soft backlit presentation",
        }
        return material_map.get(material, material)

    def _flooring_text(self, flooring):
        flooring_map = {
            "Only carpet": "exhibition carpet flooring",
            "40mm raised floor": "low raised exhibition floor platform",
            "100mm raised floor with access ramp": "raised exhibition floor platform with access ramp",
        }
        return flooring_map.get(flooring, flooring)

    def _truss_text(self, truss):
        truss_map = {
            "None": "no overhead truss",
            "Only truss": "simple overhead truss element",
            "Truss with LED strips": "overhead truss with integrated LED strip lighting",
            "Truss with PAR lights": "overhead truss with professional event lighting fixtures",
        }
        return truss_map.get(truss, truss)

    def _storage_text(self, storage, storage_position):
        if storage == "None":
            return "no enclosed storage room", "None"

        position = storage_position if storage_position in ["Left", "Right"] else "Auto"
        return f"compact enclosed storage room approximately {storage}m, position {position.lower()}", position

    def build_prompt(
        self,
        brand_name,
        brand_colors,
        booth_type,
        open_sides,
        material,
        flooring,
        truss,
        storage,
        storage_position,
        width_m,
        depth_m,
        height_m,
        style_keywords,
        product_focus,
        camera_mode,
        user_prompt,
    ):
        try:
            width_m = float(width_m)
            depth_m = float(depth_m)
            height_m = float(height_m)

            cleaned_user_prompt = self._clean_text(user_prompt)
            storage_text, resolved_storage_position = self._storage_text(storage, storage_position)

            prompt_parts = [
                "realistic exhibition booth concept render",
                self._booth_type_text(booth_type),
                self._open_sides_text(open_sides),
                self._dimension_text(width_m, depth_m, height_m),
                f"brand name: {self._clean_text(brand_name, max_chars=80) or 'Brand'}",
                f"brand colors: {self._clean_text(brand_colors, max_chars=160) or 'brand colors'}",
                self._material_text(material),
                self._flooring_text(flooring),
                self._truss_text(truss),
                storage_text,
                f"designed for {self._clean_text(product_focus, max_chars=240) or 'product display and brand presentation'}",
                f"style direction: {self._clean_text(style_keywords, max_chars=240) or 'modern, clean, premium'}",
                "modern trade show venue context, realistic lighting, clean composition, professional presentation quality",
                self._camera_text(camera_mode),
            ]

            if cleaned_user_prompt:
                prompt_parts.append(f"additional direction: {cleaned_user_prompt}")

            final_prompt = ", ".join(
                str(part).strip() for part in prompt_parts if part and str(part).strip()
            )

            summary = (
                f"SUMMARY | {self._clean_text(brand_name, max_chars=80) or 'Brand'} | "
                f"{width_m:g}m x {depth_m:g}m x {height_m:g}m | "
                f"{booth_type} | {open_sides} | {material} | {flooring} | "
                f"{truss} | storage={storage} | camera={camera_mode}"
            )

            debug = (
                "DEBUG | public deployment version | "
                f"prompt_length={len(final_prompt)} | "
                f"storage_position={resolved_storage_position}"
            )

            return (final_prompt, summary, debug)

        except Exception as e:
            error_text = f"NODE ERROR | {type(e).__name__}: {str(e)}"
            return (error_text, error_text, error_text)


NODE_CLASS_MAPPINGS = {
    "ExpoBoothPromptBuilder": ExpoBoothPromptBuilder
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExpoBoothPromptBuilder": "📐 ExpoBooth Prompt Builder"
}
