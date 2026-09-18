#define WIN32_LEAN_AND_MEAN
#define _WINSOCKAPI_
#include <winsock2.h>
#include <Windows.h>
#include <algorithm>

#include "imgui/imgui.h"
#include "sunone_aimbot_2.h"
#include "overlay.h"
#include "overlay/config_dirty.h"
#include "overlay/ui_sections.h"

void draw_overlay()
{
    constexpr int kMinReadableOpacity = 252;

    if (OverlayUI::BeginSection("비주얼", "overlay_section_visual"))
    {
        {
            const auto row = OverlayUI::BeginSettingRow("오버레이 불투명도");
            int prev_opacity = config.overlay_opacity;
            if (ImGui::SliderInt("##overlay_opacity_slider", &config.overlay_opacity, kMinReadableOpacity, 255))
            {
                if (config.overlay_opacity < kMinReadableOpacity) config.overlay_opacity = kMinReadableOpacity;
                if (config.overlay_opacity > 255) config.overlay_opacity = 255;

                Overlay_SetOpacity(config.overlay_opacity);

                if (config.overlay_opacity != prev_opacity)
                    OverlayConfig_MarkDirty();
            }
            OverlayUI::EndSettingRow(row);
        }

        float ui_scale = std::clamp(config.overlay_ui_scale, 0.85f, 1.35f);
        if (ui_scale != config.overlay_ui_scale)
            config.overlay_ui_scale = ui_scale;

        {
            const auto row = OverlayUI::BeginSettingRow("UI 배율");
            if (ImGui::SliderFloat("##overlay_ui_scale_slider", &ui_scale, 0.85f, 1.35f, "%.2f"))
            {
                config.overlay_ui_scale = ui_scale;
                OverlayConfig_MarkDirty();
            }
            OverlayUI::EndSettingRow(row);
        }

        {
            const auto row = OverlayUI::BeginSettingRow("녹화에서 오버레이 숨기기");
            if (ImGui::Checkbox("##hide_overlay_from_recording", &config.overlay_exclude_from_capture))
            {
                Overlay_ApplyCaptureExclusion();
                OverlayConfig_MarkDirty();
            }
            OverlayUI::EndSettingRow(row);
        }

        OverlayUI::EndSection();
    }
}
