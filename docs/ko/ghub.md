**Language / 언어:** [한국어](ghub.md) · [English](../en/ghub.md)

# G HUB 입력 방식

Logitech **G HUB**가 설치된 PC에서 `ghub_mouse.dll` 경로로 aimbot 이동·클릭을 넣는 방식입니다.  
무선 마우스 **동글을 PC에 직접** 꽂으면 G HUB 스크립트·DPI 프로필이 그대로 동작합니다.

## 연결도

```text
[ 무선 마우스 ] ~~ [ 동글 ] ──→ PC USB
                                    ↑
ai.exe ── ghub_mouse.dll ──────────┘  (조준·클릭 추가 입력)
         G HUB (프로필·스크립트)
```

- 본체 마우스: 직접 조준 + G HUB
- aimbot: DLL로 **추가** 상대 이동 (덮어쓰기 아님)

## 준비물

- Logitech G HUB (`C:\Program Files\LGHUB`)
- `ghub_mouse.dll` — `ai.exe`와 **같은 폴더**  
  (예: `engine/build/dml/Release/` 또는 `ai_5.0.3_DML/`)
- 무선/유선 Logitech 마우스 + 동글/케이블 → PC

## config.ini

```ini
input_method = GHUB

active_game = UNIFIED
```

게임 감도 → [게임 감도 설정](game-sensitivity.md)

## 설정 순서

1. Logitech G HUB 설치·실행
2. `ghub_mouse.dll`을 `ai.exe` 옆에 복사
3. `config.ini`에서 `input_method = GHUB`
4. `ai.exe` 실행 → Home → **마우스** 탭
5. G HUB 버전 확인 (앱은 `13.1.4` 설치를 기준으로 안내)
6. 데스크톱·게임에서 조준 동작 확인

버전·경로 문제 시 오버레이 **「GHub 문서 열기」** 링크 참고.

## G HUB vs Leonardo

| | G HUB (`GHUB`) | Leonardo (`ARDUINO`) |
|--|----------------|----------------------|
| 추가 하드웨어 | 없음 (DLL만) | Leonardo 보드 |
| G HUB 스크립트 | ✅ | ✅ (동글 PC 직결 시) |
| 게임 차단 | 일부 게임 감지 가능 | HID 장치 경로 |
| 설정 | DLL + G HUB 실행 | COM + 펌웨어 |

G HUB 스크립트 + **하드웨어 HID** 둘 다 원하면 → [입력 2개](dual-mouse.md) (본체 G HUB + Leonardo 조준).

## 주의

- 앱 오버레이: *「일부 게임에서 감지될 수 있습니다」*
- `WIN32`와 달리 Logitech 드라이버 경로를 쓰지만, 타이틀마다 동작이 다릅니다.
- **Host Shield**에 동글을 꽂으면 G HUB가 마우스를 못 봅니다 → [Host Shield](arduino-host-shield.md)

## 문제 해결

| 증상 | 확인 |
|------|------|
| DLL 로드 실패 | `ghub_mouse.dll` 경로, x64 일치 |
| 버전 경고 | `C:\Program Files\LGHUB\version`, G HUB 실행 중 |
| 박스는 보이는데 안 움직임 | `input_method = GHUB`, 게임 입력 차단 |
| 감도 안 맞음 | `[Games]` sens / yaw / pitch |

## 관련

- [입력 2개 (G HUB + Leonardo)](dual-mouse.md)
- [입력 방식 비교](input-methods.md)
- [게임 감도](game-sensitivity.md)
- [Engine — Input methods](../../engine/docs/guides/input-methods.md)
