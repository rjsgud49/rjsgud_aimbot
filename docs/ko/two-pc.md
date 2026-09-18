**Language / 언어:** [한국어](two-pc.md) · [English](../en/two-pc.md)

# 투컴 (2PC) — 캡처·연산을 외부 PC로 빼기

게임 PC에서는 게임만 돌리고, **화면 캡처 + AI 연산**은 두 번째 PC(연산 PC)에서 처리하는 구성입니다.  
한 컴에서 `duplication_api` / `winrt`로 화면을 잡는 방식과 달리, 연산 PC는 게임 화면을 **외부 입력**으로 받습니다.

## 역할 분리

| PC | 하는 일 |
|---|---|
| **게임 PC** | 게임 실행, 화면 송출(캡처카드 또는 UDP/OBS), 마우스 입력 수신 |
| **연산 PC** | `ai.exe` 실행, 프레임 수신·추론, 마우스 명령을 외부 입력 장치로 전송 |

연산 PC에는 GPU가 있는 편이 좋고(DML 또는 CUDA 빌드), 게임 PC와는 **유선 랜**을 권장합니다.

## 전체 흐름

```text
게임 PC 화면
    │
    ├─(A) HDMI → 캡처카드 → 연산 PC (virtual_camera)
    │
    └─(B) FFmpeg/OBS → UDP MJPEG → 연산 PC (udp_capture)
              │
              ▼
         연산 PC: 추론
              │
              ▼
         KMBOX / MAKCU / Arduino 등 → 게임 PC 마우스
```

캡처만 외부로 빼도 되고, **캡처 + 연산 둘 다** 연산 PC에서 하는 것이 일반적인 투컴입니다.

무선 마우스는 중계하지 않습니다. 평소 마우스는 그대로 두고, 브리지 장치가 **별도 입력**을 추가로 넣습니다.

---

## 방식 A — 캡처카드 (HDMI)

게임 PC의 화면을 HDMI로 뽑아 연산 PC의 캡처카드로 넣습니다.

1. 게임 PC: HDMI 출력(또는 복제/확장 모니터) → 캡처카드 IN  
2. 연산 PC: 캡처카드가 웹캠/캡처 장치로 인식되는지 확인  
3. 연산 PC `config.ini`:

```ini
capture_method = virtual_camera
virtual_camera_name = 캡처카드장치이름
virtual_camera_width = 1920
virtual_camera_heigth = 1080
detection_resolution = 320
capture_fps = 60
```

`virtual_camera_name`은 장치 관리자/오버레이에 보이는 **정확한 장치 이름**과 맞춰야 합니다.  
해상도·FPS는 캡처카드·케이블 한도에 맞추고, `detection_resolution`은 `160` / `320` / `640`만 유효합니다.

OBS를 중간에 두면 캡처카드 → OBS Virtual Camera → `virtual_camera`로도 연결할 수 있습니다.

---

## 방식 B — 소프트웨어 UDP (캡처카드 없음)

캡처카드 없이 LAN으로 MJPEG을 보냅니다. 자세한 송수신 예시는 [UDP capture](../../engine/docs/guides/udp-capture.md)를 참고하세요.

### 연산 PC (수신)

```ini
capture_method = udp_capture
udp_ip = 0.0.0.0
udp_port = 1234
detection_resolution = 320
capture_fps = 60
```

방화벽에서 UDP `1234` 인바운드 허용:

```powershell
New-NetFirewallRule -DisplayName "Sunone UDP Capture 1234" -Direction Inbound -Protocol UDP -LocalPort 1234 -Action Allow
```

연산 PC IP 확인: `ipconfig` → `IPv4 Address`

### 게임 PC (송신)

FFmpeg 예 (해상도는 `detection_resolution`과 맞추는 것을 권장):

```bash
ffmpeg -f gdigrab -framerate 60 -i desktop -vf scale=320:320 -vcodec mjpeg -q:v 5 -f mjpeg udp://연산PC_IP:1234
```

OBS Virtual Camera를 쓸 때:

```bash
ffmpeg -f dshow -i video="OBS Virtual Camera" -vf scale=320:320 -vcodec mjpeg -q:v 5 -f mjpeg udp://연산PC_IP:1234
```

`udp://0.0.0.0:1234`로 보내면 안 됩니다. **연산 PC의 실제 IPv4**로 보냅니다.

---

## 마우스 입력 (투컴에서 필수에 가깝음)

연산 PC의 `WIN32` 마우스 이벤트는 **게임 PC에 전달되지 않습니다.**  
투컴에서는 연산 PC → 게임 PC로 마우스를 넘기는 하드웨어/네트워크 입력이 필요합니다.

예 (네트워크 장치):

```ini
input_method = KMBOX_NET
kmbox_net_ip = 10.42.42.42
kmbox_net_port = 1984
kmbox_net_uuid = DEADC0DE
```

아두이노 기준 배선·COM 설정은 **[아두이노 PC 연결](arduino.md)** 을 보세요.  
KMBOX(Net/A)는 **[KMBOX 연결](kmbox.md)** 을 보세요.

또는 `MAKCU`, `RP2350`, `TEENSY41_HID` 등 실제 연결한 장치에 맞게 설정합니다.  
상세: [Input methods](../../engine/docs/guides/input-methods.md), [config — Input](../../engine/docs/config.md#input-method)

---

## 체크리스트

1. 연산 PC에서 `ai.exe` 실행, 모델(`.onnx` 등) 준비  
2. 캡처: A면 `virtual_camera`, B면 `udp_capture`  
3. 오버레이(Home)에서 프리뷰에 게임 화면이 들어오는지 확인  
4. `input_method`를 투컴용 장치로 설정 후 게임 PC에서 커서 반응이 있는지 확인  
5. 지연이 크면: 유선 랜, 해상도/`detection_resolution` 낮추기, UDP 품질(`-q:v`) 조정, 캡처카드 통과 지연 점검  

## 한 컴 vs 투컴

| | 한 컴 | 투컴 |
|---|---|---|
| `capture_method` | `duplication_api` 또는 `winrt` | `virtual_camera` 또는 `udp_capture` |
| 캡처카드 | 불필요 | A 방식만 필요 |
| 입력 | `WIN32` 등으로 테스트 가능 | KMBOX/MAKCU/Arduino 등 외부 입력 권장 |
| 목적 | 단순 구성 | 게임 PC 부하·탐지 표면 분리 |

관련 문서:

- [아두이노 PC 연결](arduino.md)
- [KMBOX 연결](kmbox.md)
- [UDP 캡처 상세](../../engine/docs/guides/udp-capture.md)
- [캡처 설정](../../engine/docs/config.md#capture)
- [입력 방식](../../engine/docs/guides/input-methods.md)
