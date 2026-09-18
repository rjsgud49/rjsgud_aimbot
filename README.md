**Language / 언어:** [한국어](README.md) · [English](README.en.md)

# Aimbot — C++ (sunone_aimbot_2)

## 실행

| 파일 | 용도 |
|------|------|
| **`CPP_build.bat`** | 빌드 (처음 1회) |
| **`CPP_run.bat`** | 실행 |

1. `CPP_build.bat`
2. `CPP_run.bat`
3. 게임에서 **Home** → 한글 설정창

이미 빌드됨: `engine\build\dml\Release\ai.exe`  
모델: `engine\build\dml\Release\models\` 에 `.onnx`

## 캡처 방식

| 구성 | `capture_method` | 캡처카드 |
|------|------------------|----------|
| **한 컴** | `duplication_api` 또는 `winrt` | 불필요 |
| **투컴 + HDMI** | `virtual_camera` | 필요 |
| **투컴 + LAN** | `udp_capture` | 불필요 |

투컴은 게임 PC에서 캡처·연산을 빼고, 연산 PC에서 `ai.exe`를 돌리는 방식입니다.

## 문서

| 문서 | 한국어 | English |
|------|--------|---------|
| 문서 인덱스 | [docs](docs/README.md) | [docs](docs/README.md) |
| 투컴 | [투컴](docs/ko/two-pc.md) | [Two-PC](docs/en/two-pc.md) |
| 아두이노 연결 | [아두이노](docs/ko/arduino.md) | [Arduino](docs/en/arduino.md) |
| KMBOX 연결 | [KMBOX](docs/ko/kmbox.md) | [KMBOX](docs/en/kmbox.md) |

## 참고

- Python 구버전은 `legacy_python\` (평소 무시)
- `engine\` 안 bat은 빌드 도구용 (`CPP_build.bat`이 `build_dml.bat` 호출)
- 엔진 영문 가이드: `engine/docs/guides.md`

## 라이선스

원본 sunone_aimbot_2 및 관련 라이선스를 따릅니다.
