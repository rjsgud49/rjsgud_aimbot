**Language / 언어:** [한국어](input-methods.md) · [English](../en/input-methods.md)

# 마우스 입력 방식 비교

`ai.exe`는 **aimbot이 보내는 조준·클릭**만 `input_method`로 선택합니다.  
평소 쓰는 마우스와 **별도 장치**로 쓸 수 있는 방식이 많습니다.

## 한눈에 비교

| 방식 | 연결 | G HUB 스크립트 | 무선 마우스 | 난이도 | 추천 상황 |
|------|------|----------------|-------------|--------|-----------|
| [입력 2개 (무선 + Leonardo)](dual-mouse.md) | 동글→PC, Leonardo→PC | ✅ | ✅ | 보통 | **G HUB·무선 유지 + 조준 보조** |
| [G HUB](ghub.md) | 동글→PC, `GHUB` | ✅ | ✅ | 쉬움 | Logitech + G HUB 이미 사용 중 |
| [아두이노 단독](arduino.md) | Leonardo→PC | (본체 마우스에 따라) | ✅ | 보통 | 외부 HID만 필요할 때 |
| [Host Shield](arduino-host-shield.md) | 동글→Shield→Leonardo | ❌ | ✅ | 어려움 | 마우스 1개로 합치고 싶을 때 |
| WIN32 | 소프트웨어만 | ✅ | ✅ | 쉬움 | 데스크톱 테스트 (게임 차단 많음) |
| [KMBOX](kmbox.md) | 네트워크/USB 브릿지 | (본체 마우스에 따라) | ✅ | 보통 | 투컴·하드웨어 브릿지 |
| TEENSY41_HID | RawHID 보드 | (본체 마우스에 따라) | ✅ | 보통 | [HID_Arduino](https://github.com/SunOner/HID_Arduino) 등 |

## 공통: 게임 감도

aimbot이 **얼마나 움직일지** 계산하는 `[Games]` 프로필은 **입력 방식과 무관**합니다.  
→ [게임 감도 설정](game-sensitivity.md)

## Windows에서 입력 2개

PC에 HID 마우스가 **2개** 연결되어도 Windows는 이동을 **합쳐서** 게임에 넘깁니다.

```text
마우스 1 (무선)  ──→ 직접 조준 + G HUB
마우스 2 (Leonardo) ──→ ai.exe 자동 조준만
         ↓
      게임 (합산)
```

- `input_method`는 **aimbot 출력 경로 1개**만 고릅니다.
- 본체 무선 마우스는 config에 넣을 필요 없습니다.

## config.ini 핵심 키

```ini
input_method = ARDUINO   # 또는 GHUB, TEENSY41_HID, KMBOX_NET, …
```

| 방식 | 추가 설정 |
|------|-----------|
| ARDUINO | `arduino_port`, `arduino_baudrate` |
| GHUB | `ghub_mouse.dll` (exe와 같은 폴더), Logitech G HUB 실행 |
| TEENSY41_HID | `teensy_hid_*` 필터 |
| KMBOX | `kmbox_net_*` 또는 `kmbox_a_pidvid` |

자세한 키 목록: [engine/docs/config.md](../../engine/docs/config.md)

## 어떤 걸 고를까?

```text
G HUB 스크립트·프로필을 꼭 써야 한다
  → [입력 2개](dual-mouse.md) 또는 [G HUB](ghub.md)
  → Host Shield는 G HUB와 같이 쓰기 어렵다

무선 마우스 + Leonardo 조준만 따로
  → [입력 2개](dual-mouse.md) (Host Shield 불필요)

마우스를 Leonardo 하나로 합치고 싶다 (동글을 Shield에)
  → [Host Shield](arduino-host-shield.md) (G HUB 포기)

투컴 (게임 PC / 연산 PC 분리)
  → [투컴 가이드](two-pc.md) + 위 입력 방식 중 하나
```

## 관련 문서

- [입력 2개 — 무선 + Leonardo](dual-mouse.md)
- [G HUB 입력](ghub.md)
- [아두이노 PC 연결](arduino.md)
- [USB Host Shield + 무선](arduino-host-shield.md)
- [게임 감도 (`[Games]`)](game-sensitivity.md)
- [투컴](two-pc.md) · [KMBOX](kmbox.md)
- [Engine — Input methods](../../engine/docs/guides/input-methods.md)
