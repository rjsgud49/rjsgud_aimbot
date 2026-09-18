#define WIN32_LEAN_AND_MEAN
#define _WINSOCKAPI_
#include <winsock2.h>
#include <Windows.h>

#include "imgui/imgui.h"

#include "sunone_aimbot_2.h"
#include "include/other_tools.h"
#include "overlay.h"
#include "overlay/config_dirty.h"
#include "draw_settings.h"
#include "overlay/ui_sections.h"
#ifdef USE_CUDA
#include "overlay/export_progress_panel.h"
#include "trt_monitor.h"
#endif

std::string prev_backend = config.backend;
float prev_confidence_threshold = config.confidence_threshold;
float prev_nms_threshold = config.nms_threshold;
int prev_max_detections = config.max_detections;

static bool wasExporting = false;
static bool ai_state_initialized = false;

void draw_ai()
{
#ifdef USE_CUDA
    config.backend = "TRT";
#else
    config.backend = "DML";
#endif

    if (!ai_state_initialized)
    {
        prev_backend = config.backend;
        prev_confidence_threshold = config.confidence_threshold;
        prev_nms_threshold = config.nms_threshold;
        prev_max_detections = config.max_detections;
        ai_state_initialized = true;
    }

#ifdef USE_CUDA
    if (gIsTrtExporting)
    {
        OverlayExportUI::DrawTensorRtExportPanel(
            "ai_tensor_rt_export",
            "TensorRT 엔진 내보내기",
            "최적화된 AI 추론 엔진 컴파일 중",
            config.ai_model.c_str(),
            "내보내기 취소");
    }
#endif
    std::vector<std::string> availableModels = getAvailableModels();
    if (OverlayUI::BeginSection("모델", "ai_section_model"))
    {
        if (availableModels.empty())
        {
            ImGui::Text("'models' 폴더에 사용 가능한 모델이 없습니다.");
        }
        else
        {
            int currentModelIndex = 0;
            auto it = std::find(availableModels.begin(), availableModels.end(), config.ai_model);

            if (it != availableModels.end())
            {
                currentModelIndex = static_cast<int>(std::distance(availableModels.begin(), it));
            }

            std::vector<const char*> modelsItems;
            modelsItems.reserve(availableModels.size());

            for (const auto& modelName : availableModels)
            {
                modelsItems.push_back(modelName.c_str());
            }

            {
                const auto row = OverlayUI::BeginSettingRow("모델");
                if (ImGui::Combo("##model", &currentModelIndex, modelsItems.data(), static_cast<int>(modelsItems.size())))
                {
                    if (config.ai_model != availableModels[currentModelIndex])
                    {
                        config.ai_model = availableModels[currentModelIndex];
                        OverlayConfig_MarkDirty();
                        detector_model_changed.store(true);
                    }
                }
                OverlayUI::EndSettingRow(row);
            }

            OverlayUI::TextRow(config.fixed_input_size ? "고정 모델 크기: 켜짐" : "고정 모델 크기: 꺼짐",
                IM_COL32(188, 188, 188, 255));
        }
        OverlayUI::EndSection();
    }

    if (OverlayUI::BeginSection("탐지", "ai_section_detection"))
    {
        {
            const auto row = OverlayUI::BeginSettingRow("탐지 신뢰도");
            ImGui::SliderFloat("##confidence_threshold", &config.confidence_threshold, 0.01f, 1.00f, "%.2f");
            OverlayUI::EndSettingRow(row);
        }

        {
            const auto row = OverlayUI::BeginSettingRow("NMS 임계값");
            ImGui::SliderFloat("##nms_threshold", &config.nms_threshold, 0.00f, 1.00f, "%.2f");
            OverlayUI::EndSettingRow(row);
        }

        {
            const auto row = OverlayUI::BeginSettingRow("최대 탐지 수");
            ImGui::SliderInt("##max_detections", &config.max_detections, 1, 100);
            OverlayUI::EndSettingRow(row);
        }
        OverlayUI::EndSection();
    }

    if (prev_confidence_threshold != config.confidence_threshold ||
        prev_nms_threshold != config.nms_threshold ||
        prev_max_detections != config.max_detections)
    {
        prev_nms_threshold = config.nms_threshold;
        prev_confidence_threshold = config.confidence_threshold;
        prev_max_detections = config.max_detections;
        OverlayConfig_MarkDirty();
    }

    if (prev_backend != config.backend)
    {
        prev_backend = config.backend;
        detector_model_changed.store(true);
        OverlayConfig_MarkDirty();
    }
}
