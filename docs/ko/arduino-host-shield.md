**Language / 언어:** [한국어](arduino-host-shield.md) · [English](../en/arduino-host-shield.md)

# USB Host Shield + 무선 마우스

무선 마우스 **동글**을 USB Host Shield에 꽂고, Leonardo가 **패스스루 + aimbot 주입**을 한 HID 장치로 PC에 넘기는 방식입니다.  
PC에는 **마우스 1개**만 보입니다.

G HUB 스크립트가 필요하면 이 방식 대신 → [입력 2개](dual-mouse.md) 또는 [G HUB](ghub.md)

## 연결도

```text
[ 무선 마우스 ] ~~ [ 동글 ] → USB Host Shield → Leonardo → PC USB
                              ↑
                         ai.exe (시리얼 또는 RawHID)
```

## 장단점

| | Host Shield | 입력 2개 (동글 PC + Leonardo) |
|--|-------------|------------------------------|
| PC 마우스 개수 | 1 (합침) | 2 |
| G HUB | ❌ | ✅ |
| 펌웨어 | HID_Arduino 등, MYMOUSEINFO 디버그 | 시리얼 `mX,Y` 펌웨어 |
| 난이도 | 높음 | 보통 |

## 준비물

- Arduino Leonardo (또는 호환 보드)
- USB Host Shield 2.0
- 무선 마우스 USB **수신기(동글)** — 본체가 아님
- [SunOner/HID_Arduino](https://github.com/SunOner/HID_Arduino) 또는 호환 펌웨어

## C++ 앱과의 관계

- `input_method = ARDUINO` — 시리얼 `mX,Y` (펌웨어가 Shield 패스스루 + 시리얼 수신)
- `input_method = TEENSY41_HID` — RawHID 패킷 ([HID_Arduino](https://github.com/SunOner/HID_Arduino) 계열)

펌웨어 문서에 맞는 `input_method`를 선택하세요.  
일반 [아두이노 가이드](arduino.md)의 단순 시리얼 HID와 **펌웨어가 다릅니다.**

## MYMOUSEINFO (무선·저가형)

무선 동글은 HID 리포트가 **4바이트**인 경우가 많습니다. Serial Monitor로 패턴 확인 후 `hidcustom.h` 수정.

예 (오른쪽 클릭 시 `00 EF 05 00` 형태):

```cpp
struct MYMOUSEINFO {
    uint8_t buttons;
    uint8_t dX;
    uint8_t dY;
    int8_t  wheel;
};
```

### 디버그 절차

1. 펌웨어에서 `ENABLE_UHS_DEBUGGING 1`
2. Serial Monitor **9600**
3. 마우스 이동·클릭 → 바이트열 확인 (4개 vs 6개 등)
4. `MYMOUSEINFO` 필드 타입·순서 맞추기
5. 동작 확인 후 `ENABLE_UHS_DEBUGGING 0`

Logitech G 시리즈 일부는 별도 `hidmousereport` 펌웨어가 필요할 수 있습니다.

## config.ini 예시 (시리얼 경로)

```ini
input_method = ARDUINO
arduino_port = COM3
arduino_baudrate = 115200
```

RawHID 경로:

```ini
input_method = TEENSY41_HID
teensy_hid_serial = AUTO
teensy_hid_vid_filter = AUTO
teensy_hid_pid_filter = AUTO
```

## 게임 감도

Shield 방식이어도 aimbot 이동량은 `[Games]`로 계산합니다.  
→ [게임 감도 설정](game-sensitivity.md)

## 문제 해결

| 증상 | 확인 |
|------|------|
| 커서 안 움직임 / 튐 | MYMOUSEINFO, 동글 4/6바이트 |
| G HUB 안 됨 | 정상 (동글이 PC G HUB 경로 아님) — [입력 2개](dual-mouse.md) 검토 |
| COM 없음 | Leonardo USB, 펌웨어 CDC |
| Logitech만 이상 | G 전용 펌웨어 분기 |

## 관련

- [입력 2개 — G HUB 유지](dual-mouse.md)
- [입력 방식 비교](input-methods.md)
- [아두이노 PC 연결](arduino.md)
- [HID_Arduino (GitHub)](https://github.com/SunOner/HID_Arduino)
