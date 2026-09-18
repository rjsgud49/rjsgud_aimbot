**Language / 언어:** [한국어](arduino.md) · [English](../en/arduino.md)

# 아두이노 PC 연결 가이드

`input_method = ARDUINO` 일 때 `ai.exe`는 **시리얼(COM)** 로 보드에 명령을 보내고, 보드는 **HID 마우스**처럼 PC에 상대 이동을 넣습니다.  
평소 쓰는 무선 마우스를 가로채지 않습니다. 무선 수신기는 그대로 두고, 아두이노가 **추가 마우스**로 동작합니다.

## 준비물

- HID 마우스로 쓸 수 있는 보드 (예: Leonardo, Pro Micro, Micro 계열)
- USB 케이블
- (투컴 시리얼 분리 시) USB–TTL 어댑터 + 점퍼선
- 앱이 기대하는 시리얼 프로토콜과 맞는 펌웨어가 보드에 올라가 있어야 함

이 저장소는 펌웨어 소스를 포함하지 않습니다. 보드 쪽은 `mX,Y` / `c` / `p` / `r` 텍스트 명령을 받아 HID 이동·클릭을 내는 펌웨어를 사용하세요.

## 앱이 보내는 시리얼 명령

보드레이트 기본값 `115200`. 한 줄 단위(`\n`).

| 명령 | 의미 |
|---|---|
| `mX,Y` | 상대 이동 (예: `m10,-3`) |
| `c` | 클릭 |
| `p` / `r` | 버튼 press / release |

`arduino_16_bit_mouse = false`(기본)이면 큰 이동은 ±127 단위로 쪼개서 여러 번 보냅니다.  
`true`이면 `mX,Y` 한 번에 보냅니다.

콘솔에 `[Arduino] Connected! PORT: COMx` 가 보이면 시리얼 연결은 된 상태입니다.

---

## 구성 1 — 한 컴 (가장 단순)

게임과 `ai.exe`가 **같은 PC**일 때입니다.

```text
[ PC ]
   │ USB
   ▼
 Arduino (HID 마우스 + 가상 COM)
   │
   └─ ai.exe → arduino_port = COMx
```

1. 펌웨어를 보드에 업로드한 뒤 **Arduino IDE를 종료**합니다. (COM 점유 충돌 방지)
2. USB로 PC에 연결합니다.
3. 장치 관리자 → **포트(COM & LPT)** 에서 아두이노 COM 번호를 확인합니다.
4. `config.ini` (또는 오버레이) 예시:

```ini
input_method = ARDUINO
arduino_port = COM3
arduino_baudrate = 115200
arduino_16_bit_mouse = false
arduino_enable_keys = false
```

5. `ai.exe`를 실행하고, 데스크톱에서 커서가 미세하게 움직이는지 확인합니다.
6. 무선 마우스는 그대로 사용하면 됩니다. 입력이 겹쳐 보여도 정상입니다.

`COM3` 등은 본인 PC 번호로 바꿉니다. `COM0`은 플레이스홀더입니다.

---

## 구성 2 — 투컴 (HID와 시리얼을 PC별로 분리)

목표는 다음과 같습니다.

- **게임 PC:** 아두이노 USB → Windows가 HID 마우스로 인식
- **연산 PC:** `ai.exe`가 COM으로 명령 전송

Leonardo 한 포트만 쓰면 HID와 COM이 **같은 PC**에만 붙습니다. 투컴에서는 USB–TTL로 시리얼만 연산 PC에 빼는 방식이 일반적입니다.

```text
연산 PC                         게임 PC
┌─────────────┐                ┌─────────────┐
│ ai.exe      │                │ 게임 +      │
│ COM (TTL)   │── TX/RX/GND ──▶│ 무선 마우스   │
└─────────────┘                │             │
                               │ Arduino USB │◀── HID 마우스
                               └─────────────┘
```

배선 요지 (보드·어댑터 핀맵은 제품마다 다름):

1. 아두이노 **USB** → 게임 PC  
2. 아두이노 **TX** → USB–TTL **RX**  
3. 아두이노 **RX** → USB–TTL **TX**  
4. **GND** 공통  
5. USB–TTL → 연산 PC (새 COM 포트 생김)

연산 PC `config.ini`:

```ini
input_method = ARDUINO
arduino_port = COM5
arduino_baudrate = 115200
arduino_16_bit_mouse = false
arduino_enable_keys = false
```

`COM5`는 연산 PC 장치 관리자에서 TTL 어댑터에 보이는 포트입니다.

주의:

- 보드가 USB CDC와 UART를 동시에 쓸 수 있는지, 펌웨어가 **어느 UART**를 읽는지 확인하세요.
- 전압(3.3V/5V)과 보드레이트를 맞추세요.
- 캡처는 투컴 문서대로 `udp_capture` 또는 `virtual_camera`를 씁니다. → [투컴 가이드](two-pc.md)

네트워크형 장치(`KMBOX_NET` 등)가 배선이 더 단순한 경우도 많습니다.

---

## 구성 3 — USB Host Shield (참고)

구버전 Python 쪽은 USB Host Shield 라이브러리·디버그 설정을 점검하는 안내가 있었습니다.  
C++ `ARDUINO` 경로 자체는 **로컬 COM 시리얼**입니다. Host Shield를 쓰면 보드·펌웨어가 마우스 패스스루/주입을 담당하고, PC↔보드 통신은 여전히 시리얼(또는 해당 펌웨어 방식)로 맞춰야 합니다.

---

## 체크리스트 / 문제 해결

| 증상 | 확인할 것 |
|---|---|
| `[Arduino] Unable to connect` | COM 번호, 케이블, IDE/다른 프로그램 COM 점유 |
| 연결은 되는데 커서 안 움직임 | 펌웨어 프로토콜(`mX,Y`), HID 보드 여부, 게임 PC에 USB가 꽂혔는지(투컴) |
| IDE에서만 동작 | IDE 종료 후 `ai.exe`만 실행 |
| 투컴인데 연산 PC 커서만 움직임 | HID USB가 게임 PC가 아니라 연산 PC에 연결된 상태 |

관련:

- [투컴 가이드](two-pc.md)
- [config — Arduino](../../engine/docs/config.md#arduino)
- [Input methods](../../engine/docs/guides/input-methods.md)
