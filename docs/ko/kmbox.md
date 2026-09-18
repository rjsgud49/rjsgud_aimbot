**Language / 언어:** [한국어](kmbox.md) · [English](../en/kmbox.md)

# KMBOX 연결 가이드

이 앱은 `KMBOX_NET`(네트워크)과 `KMBOX_A`(USB PID/VID)를 지원합니다.  
평소 무선 마우스를 가로채지 않아도 됩니다. 박스가 게임 PC에 **별도 마우스 입력**을 넣거나, 물리 마우스를 박스에 꽂아 패스스루할 수 있습니다.

공식 매뉴얼:

- [kmbox Net](https://www.kmbox.top/wiki_doc/kmboxNet-en/site/)
- [kmbox B+](https://www.kmbox.top/wiki_doc/kmboxB-en/site/) (참고; 이 앱의 `KMBOX_A`와 포트/설정 방식이 다름)

### 구매

| 출처 | 링크 |
|---|---|
| 공식 사이트 | [kmbox.top](https://www.kmbox.top/) |
| Net 매뉴얼 | [kmbox Net User Manual](https://www.kmbox.top/wiki_doc/kmboxNet-en/site/) |

재판매·중고는 스펙(Net / A / B+)을 꼭 확인하세요. **투컴에는 Net이 배선이 가장 단순**합니다.

---

## 어떤 타입을 고를지

| 앱 설정 | 장치 | 연산 PC ↔ 박스 | 게임 PC |
|---|---|---|---|
| `KMBOX_NET` | kmbox **Net** | 이더넷(랜) | USB `controlled PC` 포트 |
| `KMBOX_A` | kmbox **A** 계열 | USB (PID/VID) | 박스 USB가 게임 PC에 HID로 붙는 구성 |

아두이노처럼 USB–TTL을 따로 살 필요는 없습니다(Net 기준).

---

## 구성 A — `KMBOX_NET` (투컴 권장)

### 케이블

박스 뒷면 포트 이름을 따릅니다(제품 매뉴얼 기준).

```text
연산 PC (ai.exe)          kmbox Net              게임 PC
┌──────────────┐         ┌──────────┐         ┌──────────────┐
│ 이더넷       │────────▶│ Net port │         │              │
│              │         │controlled│────────▶│ USB (HID)    │
│              │         │ PC 포트  │         │              │
└──────────────┘         │ mouse/KB │◀── 유선 마우스(선택)
                         └──────────┘         └──────────────┘
```

1. **Net port** → 연산 PC (또는 같은 스위치/허브). 박스에 표시된 IP로 통신합니다.  
2. **controlled PC** → 게임 PC USB. 게임 PC에 마우스(HID)로 인식됩니다.  
3. (선택) 물리 마우스/키보드 → 박스 입력 포트. 패스스루를 쓰면 무선 수신기 대신 여기로 꽂는 구성도 가능합니다.  
4. 한 컴만 쓸 때는 매뉴얼대로 Net·controlled를 **같은 PC**에 연결해도 됩니다.

### 네트워크

1. Net 포트 연결 후 안내에 따라 **네트워크 어댑터 드라이버**를 설치합니다.  
2. 연산 PC에서 박스와 통신 가능한 IP 대역인지 확인합니다.  
3. 박스 **화면(LCD)** 에 표시된 값을 그대로 씁니다.
   - IP → `kmbox_net_ip`
   - Port → `kmbox_net_port`
   - MAC / UUID → `kmbox_net_uuid`  
     (코드상 `kmNet_init`의 mac 인자. config 키 이름은 `uuid`)

### `config.ini` 예시

```ini
input_method = KMBOX_NET
kmbox_net_ip = 10.42.42.42
kmbox_net_port = 1984
kmbox_net_uuid = DEADC0DE
```

`10.42.42.42` / `DEADC0DE` 는 플레이스홀더입니다. **박스 화면에 나온 값으로 교체**하세요.

오버레이(Home) → 입력 방법에서 IP/Port/UUID 입력 후 **저장 및 재연결**.  
초록색 `kmboxNet connected` 가 보이면 연결 성공입니다.

방화벽이 UDP/해당 포트를 막으면 연결이 실패할 수 있습니다. 실패 시 콘솔에 `[KmboxNet] Connection failed` 가 출력됩니다.

---

## 구성 B — `KMBOX_A`

USB로 연산 PC(또는 한 컴 PC)에 붙고, `kmbox_a_pidvid`로 장치를 지정합니다.

형식: **8자리 hex `PPPPVVVV`** (앞 4 = PID, 뒤 4 = VID).

```ini
input_method = KMBOX_A
kmbox_a_pidvid = C07D046D
```

예시는 형식 설명용입니다. 장치 관리자·제조 도구에서 실제 PID/VID를 확인한 뒤 `PPPPVVVV`로 이어 붙이세요.  
잘못된 형식이면 `[KmboxA] Invalid PIDVID format. Expected 8 hex chars (PPPPVVVV).` 가 나옵니다.

오버레이에서 PIDVID 저장 후 **저장 및 재연결**, `kmboxA connected` 확인.

투컴에서 A를 쓸 때는 **어느 PC에 어떤 USB가 꽂히는지** 제품 매뉴얼을 따르세요. 네트워크 분리가 필요하면 Net을 쓰는 편이 단순합니다.

---

## 무선 마우스

- 게임 PC에 수신기를 그대로 두고, KMBOX만 추가 HID로 주입해도 됩니다.  
- 또는 유선 마우스를 박스에 꽂아 패스스루 + 소프트웨어 주입을 함께 쓰는 구성도 가능합니다.  
어느 쪽이든 **중계가 목적이 아니라**, 박스가 게임 PC에 마우스 이벤트를 넣는 경로입니다.

---

## 체크리스트

| 증상 | 확인할 것 |
|---|---|
| `kmboxNet not connected` | LCD의 IP/Port/MAC, 랜 케이블, 어댑터 IP/드라이버, 방화벽 |
| `Connection failed` | `kmbox_net_*` 오타, 박스가 다른 대역에 있음, Net 포트가 연산 PC가 아님 |
| A 연결 실패 | `kmbox_a_pidvid` 8자리 hex, USB 포트, 드라이버 |
| 연결됐는데 게임에서 안 움직임 | controlled PC 케이블이 게임 PC인지, 오버레이에서 입력이 KMBOX인지 |

캡처(투컴)는 별도입니다 → [투컴 가이드](two-pc.md)  
시리얼 보드 대안 → [아두이노 가이드](arduino.md)

관련:

- [config — Kmbox](../../engine/docs/config.md#kmbox-net)
- [Input methods](../../engine/docs/guides/input-methods.md)
