#define WIN32_LEAN_AND_MEAN
#define _WINSOCKAPI_
#include <winsock2.h>
#include <Windows.h>

#include "d3d11.h"
#include "imgui/imgui.h"

#include <cmath>
#include <iostream>
#include <mutex>
#include <vector>

#include "overlay.h"
#include "overlay/config_dirty.h"
#include "draw_settings.h"
#include "overlay/ui_sections.h"
#include "sunone_aimbot_2.h"
#include "runtime/thread_loops.h"
#include "other_tools.h"
#include "memory_images.h"

ID3D11ShaderResourceView* bodyTexture = nullptr;
ImVec2 bodyImageSize;

bool prev_disable_headshot = config.disable_headshot;
float prev_body_y_offset = config.body_y_offset;
float prev_head_y_offset = config.head_y_offset;
bool prev_auto_aim = config.auto_aim;
bool prev_easynorecoil = config.easynorecoil;
float prev_easynorecoilstrength = config.easynorecoilstrength;
bool prev_tracker_enabled = config.tracker_enabled;
bool prev_tracker_overlay_table_enabled = config.tracker_overlay_table_enabled;

void draw_target()
{
    if (OverlayUI::BeginSection("조준", "target_section_targeting"))
    {
        OverlayUI::CheckboxRow("헤드샷 끄기", &config.disable_headshot);
        OverlayUI::CheckboxRow("자동 조준", &config.auto_aim);
        OverlayUI::EndSection();
    }

    if (OverlayUI::BeginSection("오프셋", "target_section_offsets"))
    {
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Arrow keys: Adjust body offset");
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Shift+Arrow keys: Adjust head offset");

        OverlayUI::SliderFloatRow("몸 Y 오프셋 (대략)", &config.body_y_offset, 0.0f, 1.0f, "%.2f");
        OverlayUI::SliderFloatRow("머리 Y 오프셋 (대략)", &config.head_y_offset, 0.0f, 1.0f, "%.2f");
        OverlayUI::EndSection();
    }

    if (OverlayUI::BeginSection("미리보기", "target_section_preview"))
    {
        if (bodyTexture)
        {
            ImGui::Image((ImTextureID)(intptr_t)bodyTexture, bodyImageSize);

            ImVec2 image_pos = ImGui::GetItemRectMin();
            ImVec2 image_size = ImGui::GetItemRectSize();

            ImDrawList* draw_list = ImGui::GetWindowDrawList();

            float normalized_body_value = (config.body_y_offset - 1.0f) / 1.0f;
            float body_line_y = image_pos.y + (1.0f + normalized_body_value) * image_size.y;
            ImVec2 body_line_start = ImVec2(image_pos.x, body_line_y);
            ImVec2 body_line_end = ImVec2(image_pos.x + image_size.x, body_line_y);
            draw_list->AddLine(body_line_start, body_line_end, IM_COL32(255, 0, 0, 255), 2.0f);

            float body_y_pos_at_015 = image_pos.y + (1.0f + (0.15f - 1.0f) / 1.0f) * image_size.y;
            float head_top_pos = image_pos.y;
            float head_line_y = head_top_pos + (config.head_y_offset * (body_y_pos_at_015 - head_top_pos));

            ImVec2 head_line_start = ImVec2(image_pos.x, head_line_y);
            ImVec2 head_line_end = ImVec2(image_pos.x + image_size.x, head_line_y);
            draw_list->AddLine(head_line_start, head_line_end, IM_COL32(0, 255, 0, 255), 2.0f);

            draw_list->AddText(ImVec2(body_line_end.x + 5, body_line_y - 7), IM_COL32(255, 0, 0, 255), "몸");
            draw_list->AddText(ImVec2(head_line_end.x + 5, head_line_y - 7), IM_COL32(0, 255, 0, 255), "머리");
        }
        else
        {
            ImGui::Text("이미지를 찾을 수 없습니다!");
        }
        ImGui::Text("참고: 게임마다 플레이어 모델 크기가 달라 값이 다를 수 있습니다.");
        OverlayUI::EndSection();
    }

    if (prev_disable_headshot != config.disable_headshot ||
        prev_body_y_offset != config.body_y_offset ||
        prev_head_y_offset != config.head_y_offset ||
        prev_auto_aim != config.auto_aim ||
        prev_easynorecoil != config.easynorecoil ||
        prev_easynorecoilstrength != config.easynorecoilstrength)
    {
        prev_disable_headshot = config.disable_headshot;
        prev_body_y_offset = config.body_y_offset;
        prev_head_y_offset = config.head_y_offset;
        prev_auto_aim = config.auto_aim;
        prev_easynorecoil = config.easynorecoil;
        prev_easynorecoilstrength = config.easynorecoilstrength;
        OverlayConfig_MarkDirty();
    }
}

void draw_tracker()
{
    bool changed = false;
    std::vector<TrackDebugInfo> tracks;
    int lockedTrackId = -1;
    {
        std::lock_guard<std::mutex> lk(g_trackerDebugMutex);
        tracks = g_trackerDebugTracks;
        lockedTrackId = g_trackerLockedId;
    }

    if (OverlayUI::BeginSection("상태", "tracker_section_status"))
    {
        changed |= OverlayUI::CheckboxRow("트래커 사용", &config.tracker_enabled);
        changed |= OverlayUI::CheckboxRow("타겟 표 표시", &config.tracker_overlay_table_enabled);
        ImGui::Text("모드: 단순 잠금");
        ImGui::Text("Runtime: %s", config.tracker_enabled ? "트래커" : "Nearest Target");
        ImGui::Text("Locked Track ID: %d", lockedTrackId);
        ImGui::Text("Active Tracks: %d", static_cast<int>(tracks.size()));
        OverlayUI::EndSection();
    }

    if (config.tracker_overlay_table_enabled && OverlayUI::BeginSection("트랙", "tracker_section_tracks"))
    {
        if (tracks.empty())
        {
            ImGui::TextDisabled("활성 트랙 없음");
        }
        else if (ImGui::BeginTable("tracker_tracks_table", 7, ImGuiTableFlags_Borders | ImGuiTableFlags_RowBg))
        {
            ImGui::TableSetupColumn("ID");
            ImGui::TableSetupColumn("Class");
            ImGui::TableSetupColumn("Locked");
            ImGui::TableSetupColumn("Observed");
            ImGui::TableSetupColumn("Missed");
            ImGui::TableSetupColumn("Pivot");
            ImGui::TableSetupColumn("Speed");
            ImGui::TableHeadersRow();

            for (const auto& track : tracks)
            {
                const double speed = std::hypot(track.velocityX, track.velocityY);

                ImGui::TableNextRow();
                ImGui::TableSetColumnIndex(0);
                ImGui::Text("%d", track.trackId);
                ImGui::TableSetColumnIndex(1);
                ImGui::Text("%d", track.classId);
                ImGui::TableSetColumnIndex(2);
                ImGui::Text("%s", track.isLocked ? "예" : "아니오");
                ImGui::TableSetColumnIndex(3);
                ImGui::Text("%s", track.observedThisFrame ? "예" : "아니오");
                ImGui::TableSetColumnIndex(4);
                ImGui::Text("%d", track.missedFrames);
                ImGui::TableSetColumnIndex(5);
                ImGui::Text("%.0f, %.0f", track.pivotX, track.pivotY);
                ImGui::TableSetColumnIndex(6);
                ImGui::Text("%.0f", speed);
            }

            ImGui::EndTable();
        }
        OverlayUI::EndSection();
    }

    if (changed ||
        prev_tracker_enabled != config.tracker_enabled ||
        prev_tracker_overlay_table_enabled != config.tracker_overlay_table_enabled)
    {
        prev_tracker_enabled = config.tracker_enabled;
        prev_tracker_overlay_table_enabled = config.tracker_overlay_table_enabled;
        OverlayConfig_MarkDirty();
    }
}

void load_body_texture()
{
    int image_width = 0;
    int image_height = 0;

    std::string body_image = std::string(bodyImageBase64_1) + std::string(bodyImageBase64_2) + std::string(bodyImageBase64_3);

    bool ret = LoadTextureFromMemory(body_image, g_pd3dDevice, &bodyTexture, &image_width, &image_height);
    if (!ret)
    {
        std::cerr << "[Overlay] Can't load image!" << std::endl;
    }
    else
    {
        bodyImageSize = ImVec2((float)image_width, (float)image_height);
    }
}

void release_body_texture()
{
    if (bodyTexture)
    {
        bodyTexture->Release();
        bodyTexture = nullptr;
    }
}
