**Language / 언어:** [한국어](game-sensitivity.md) · [English](../en/game-sensitivity.md)

# 게임 감도 (`[Games]` 프로필)

aimbot이 **화면 픽셀 오차 → 마우스 이동량**으로 바꿀 때 쓰는 설정입니다.  
`GHUB`, `ARDUINO`, Host Shield 등 **입력 방식과 무관**하게 적용됩니다.

직접 손으로 움직일 때는 게임·G HUB 감도가 그대로 쓰이고,  
**aimbot이 보내는 이동**만 이 프로필로 계산됩니다.

## config.ini

```ini
active_game = UNIFIED

[Games]
UNIFIED = 1,0.022,0.022
#         │   │     └─ pitch (게임 엔진 계수)
#         │   └─ yaw
#         └─ sens (인게임 감도와 동일한 숫자)
```

FOV 보정이 필요하면:

```ini
UNIFIED = 1,0.022,0.022,true,90
#                              │    └─ baseFOV
#                              └─ fovScaled
```

## 필드 설명

| 필드 | 의미 | 예 |
|------|------|-----|
| `sens` | 게임 설정창 **감도**와 같은 값 | `1`, `2.5`, `0.8` |
| `yaw` | 수평 변환 계수 | Source 계열 `0.022` |
| `pitch` | 수직 변환 계수 | 보통 yaw와 동일 |
| `fovScaled` | FOV 변경 시 보정 (선택) | `true` / `false` |
| `baseFOV` | 기준 FOV (선택) | `90` |

## UI에서 수정

`ai.exe` → **Home** → **마우스** 탭 → **게임 프로필**

- 프로필 선택 / 추가 / 삭제
- Yaw·Pitch 슬라이더
- Source 계열 프리셋 버튼 (있을 경우 `0.022` 적용)

## 입력 방식별 정리

| 방식 | 본체 마우스 감도 | aimbot 감도 |
|------|------------------|-------------|
| [입력 2개](dual-mouse.md) | 인게임 + G HUB | `[Games]` |
| [G HUB](ghub.md) | 인게임 + G HUB | `[Games]` |
| [Host Shield](arduino-host-shield.md) | 인게임 (합쳐진 HID) | `[Games]` |
| [아두이노 단독](arduino.md) | 인게임 | `[Games]` |

## 튜닝 팁

| 증상 | 조정 |
|------|------|
| 조준이 목표를 지나침 (과보정) | FOV·최대 속도 낮추기, 예측 약하게 |
| 조준이 덜 붙음 | `[Games]` sens 확인, yaw/pitch |
| FOV 바꿨을 때만 어긋남 | `fovScaled=true`, `baseFOV` |
| 좌우만 이상 | yaw / pitch 따로 조정 |

FOV 슬라이더 최소값(예: 10)은 UI 한도일 수 있습니다. 더 낮은 값은 `config.ini`에 직접 입력할 수 있습니다.

## 관련

- [입력 방식 비교](input-methods.md)
- [Engine — config Games](../../engine/docs/config.md)
- [Engine — circle FOV](../../engine/docs/guides/circle-fov.md)
