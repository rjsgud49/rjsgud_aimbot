#define WIN32_LEAN_AND_MEAN
#define _WINSOCKAPI_
#include <winsock2.h>
#include <Windows.h>

#include <string>
#include <vector>

#include "imgui/imgui.h"
#include "sunone_aimbot_2.h"
#include "overlay.h"
#include "overlay/config_dirty.h"
#include "overlay/ui_sections.h"

namespace
{
int findKeyIndexByName(const std::string& keyName)
{
    for (size_t k = 0; k < key_names.size(); ++k)
    {
        if (key_names[k] == keyName)
            return static_cast<int>(k);
    }
    return 0;
}

bool drawButtonBindingRows(const char* rowLabel, std::vector<std::string>& bindings, bool keepAtLeastOne)
{
    if (key_names_cstrs.empty())
    {
        ImGui::TextDisabled("사용 가능한 키 목록이 없습니다.");
        return false;
    }

    bool changed = false;
    if (bindings.empty() && keepAtLeastOne)
    {
        bindings.push_back("없음");
        changed = true;
    }

    for (size_t i = 0; i < bindings.size();)
    {
        std::string& currentKeyName = bindings[i];
        int currentIndex = findKeyIndexByName(currentKeyName);
        const std::string indexedLabel = (bindings.size() > 1)
            ? std::string(rowLabel) + " " + std::to_string(i + 1)
            : std::string(rowLabel);

        ImGui::PushID(static_cast<int>(i));

        const auto row = OverlayUI::BeginSettingRow(indexedLabel.c_str());
        const float actionBtnW = ImGui::GetFrameHeight();
        float comboWidth = row.controlWidth - (actionBtnW * 2.0f + 7.0f);
        if (comboWidth < 1.0f)
            comboWidth = 1.0f;
        ImGui::SetNextItemWidth(comboWidth);

        if (ImGui::Combo("##value", &currentIndex, key_names_cstrs.data(), static_cast<int>(key_names_cstrs.size())))
        {
            currentKeyName = key_names[currentIndex];
            changed = true;
        }

        ImGui::SameLine(0.0f, 4.0f);
        if (ImGui::Button("+", ImVec2(actionBtnW, 0.0f)))
        {
            bindings.insert(bindings.begin() + static_cast<std::vector<std::string>::difference_type>(i + 1), "없음");
            changed = true;
        }

        ImGui::SameLine(0.0f, 3.0f);
        bool removedCurrent = false;
        if (ImGui::Button("-", ImVec2(actionBtnW, 0.0f)))
        {
            if (bindings.size() <= 1 && keepAtLeastOne)
            {
                bindings[0] = "없음";
            }
            else
            {
                bindings.erase(bindings.begin() + static_cast<std::vector<std::string>::difference_type>(i));
                removedCurrent = true;
            }
            changed = true;
        }

        OverlayUI::EndSettingRow(row);
        ImGui::PopID();

        if (removedCurrent)
            continue;

        ++i;
    }

    return changed;
}

void drawBindingRowsAndMarkDirty(const char* rowLabel, std::vector<std::string>& bindings, bool keepAtLeastOne = true)
{
    if (drawButtonBindingRows(rowLabel, bindings, keepAtLeastOne))
        OverlayConfig_MarkDirty();
}
}

void draw_buttons()
{
    if (OverlayUI::BeginSection("단축키", "buttons_section_hotkeys"))
    {
        drawBindingRowsAndMarkDirty("조준", config.button_targeting);
        drawBindingRowsAndMarkDirty("사격", config.button_shoot);
        drawBindingRowsAndMarkDirty("줌", config.button_zoom);
        drawBindingRowsAndMarkDirty("종료", config.button_exit);
        drawBindingRowsAndMarkDirty("일시정지", config.button_pause);
        drawBindingRowsAndMarkDirty("설정 리로드", config.button_reload_config);
        drawBindingRowsAndMarkDirty("오버레이 열기", config.button_open_overlay);

        const auto row = OverlayUI::BeginSettingRow("방향키 옵션");
        if (ImGui::Checkbox("##value", &config.enable_arrows_settings))
            OverlayConfig_MarkDirty();
        OverlayUI::EndSettingRow(row);
        OverlayUI::EndSection();
    }
}
