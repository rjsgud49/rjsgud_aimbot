**Language / 언어:** [한국어](dual-mouse.md) · [English](../en/dual-mouse.md)

# 입력 2개 — 무선 마우스 + Leonardo (권장)

**직접 조준**은 평소 무선 마우스(G HUB 포함), **자동 따라붙기**는 Leonardo만 담당하는 구성입니다.  
G HUB 스크립트·DPI 프로필·인게임 감도를 유지하면서 aimbot을 쓰기에 가장 무난합니다.

## 연결도

```text
[ 무선 마우스 ] ~~(무선)~~ [ USB 동글 ] ──→ PC USB (마우스 1)
                                              ↑
[ Leonardo ] ── USB (HID + COM) ─────────────┘  (마우스 2)
       ↑
   ai.exe (COM으로 mX,Y 전송)
```

- 동글은 **PC에 그대로** — G HUB가 마우스를 인식합니다.
- Leonardo는 **추가 HID 마우스** — aimbot 이동만 넣습니다.
- Host Shield **불필요**합니다.

## config.ini

```ini
input_method = ARDUINO
arduino_port = COM3
arduino_baudrate = 115200
arduino_16_bit_mouse = false
arduino_enable_keys = false

active_game = UNIFIED
```

`COM3`은 장치 관리자에서 Leonardo COM 번호로 바꿉니다.  
게임 감도는 `[Games]` 섹션 → [게임 감도 설정](game-sensitivity.md)

## 설정 순서

1. Leonardo에 **시리얼 HID 펌웨어** 업로드 (`mX,Y` / `c` / `p` / `r` 프로토콜)
2. **Arduino IDE 종료** (COM 점유 방지)
3. Leonardo USB → PC, 무선 **동글** → PC (포트 2개)
4. 장치 관리자 → Leonardo **COM 번호** 확인
5. `config.ini`에 `arduino_port` 입력
6. `ai.exe` 실행 → `[Arduino] Connected! PORT: COMx` 확인
7. 데스크톱에서 커서가 미세하게 움직이면 정상
8. G HUB 실행, 기존 프로필·스크립트 그대로 사용

## 역할 분담

| 동작 | 담당 |
|------|------|
| 직접 에임 | 무선 마우스 |
| G HUB 매크로·리코일·DPI | G HUB (본체 마우스) |
| 자동 조준 보정 | Leonardo (`ARDUINO`) |
| aimbot 이동량 계산 | `[Games]` sens / yaw / pitch |

`input_method = GHUB`와 **동시에 쓰지 않습니다.**  
조준 출력은 Leonardo(`ARDUINO`)만, 본체는 G HUB 그대로입니다.

## 자동 사격 (선택)

Leonardo로 클릭까지 보내려면:

```ini
arduino_enable_keys = true
```

펌웨어가 `p` / `r` / `c`를 지원해야 합니다.  
G HUB 클릭 매크로와 **겹치지 않게** 조정하세요.

## 투컴

- **게임 PC:** Leonardo USB (HID) + 무선 동글
- **연산 PC:** `ai.exe` + USB–TTL로 COM

배선·COM 설정 → [아두이노 — 투컴](arduino.md#구성-2--투컴-hid와-시리얼을-pc별로-분리)

## 문제 해결

| 증상 | 확인 |
|------|------|
| G HUB 스크립트 안 됨 | 동글이 Shield/Leonardo에 꽂혀 있지 않은지 |
| 조준만 이상함 | `[Games]` sens가 인게임과 같은지 |
| COM 연결 실패 | IDE 종료, COM 번호, 케이블 |
| 움직임이 두 배로 느껴짐 | FOV·속도 설정, `[Games]` yaw/pitch |

## 비교

| | 입력 2개 (이 문서) | Host Shield |
|--|-------------------|-------------|
| G HUB | ✅ | ❌ |
| USB 포트 | 동글 + Leonardo | Shield + Leonardo |
| PC가 보는 마우스 | 2개 | 1개 (합침) |

→ [입력 방식 비교](input-methods.md) · [Host Shield](arduino-host-shield.md)

## 관련

- [아두이노 PC 연결](arduino.md)
- [G HUB 방식 (Leonardo 없이)](ghub.md)
- [게임 감도](game-sensitivity.md)
