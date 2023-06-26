def generate_font(
        font_name,
        font_repo,
        font_filegroup,
        font_file):
    native.genrule(
        name = "generate_{font_name}".format(font_name = font_name),
        tools = ["@imgui//:binary_to_compressed", "@{font_repo}//:{font_filegroup}".format(font_repo = font_repo, font_filegroup = font_filegroup)],
        outs = ["src/{}.inc".format(font_file)],
        cmd = "$(location @imgui//:binary_to_compressed) $(location @{font_repo}//:{font_filegroup}) {font_file} > $(@)".format(font_repo = font_repo, font_filegroup = font_filegroup, font_file = font_file),
    )

    font_header = "include/imgui_{font_file}.h".format(font_file = font_file)
    native.genrule(
        name = "generate_{font_name}_header".format(font_name = font_name),
        outs = [font_header],
        cmd = """
cat > $(@) <<END
#pragma once
#include "imgui.h"
namespace ImGui {{
ImFont* AddFont{font_file}(ImGuiIO& io, float size_pixels, const ImFontConfig* font_cfg = nullptr, const ImWchar* glyph_ranges = nullptr);
}}
END
""".format(font_name = font_name, font = font_name, font_file = font_file),
    )

    font_src = "src/imgui_{font_file}.cpp".format(font_file = font_file)
    native.genrule(
        name = "generate_{font_name}_source".format(font_name = font_name),
        outs = [font_src],
        cmd = """
cat > $(@) <<END
#include "imgui_{font}.h"
#include "{font}.inc"
ImFont* ImGui::AddFont{font}(ImGuiIO& io, float size_pixels, const ImFontConfig* font_cfg, const ImWchar* glyph_ranges) {{
  return io.Fonts->AddFontFromMemoryCompressedTTF({font}_compressed_data, {font}_compressed_size, size_pixels, font_cfg, glyph_ranges);
}}
END
""".format(font_name = font_name, font = font_file),
    )
