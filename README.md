# Aimbot GUI (rjsgud49)

개인용 AI 에임 보조 프로그램입니다.  
원본은 [SunOner/sunone_aimbot](https://github.com/SunOner/sunone_aimbot) (MIT) 기반입니다.

> 사용은 본인 책임입니다. 게임 이용약관 위반·제재 가능성이 있습니다.

---

## 요구 사항

| 항목 | 권장 |
|------|------|
| OS | Windows 10 / 11 |
| Python | **3.12** (`py -3.12`) |
| GPU | NVIDIA (CUDA) 권장. CPU만으로는 실전 사용이 어렵습니다. |

---

## 설치

### 1) Python 3.12

1. https://www.python.org/downloads/release/python-31210/
2. **Windows installer (64-bit)** 설치
3. **"Add python.exe to PATH"** 체크

확인:

```bat
py -3.12 --version
```

### 2) 라이브러리

프로젝트 폴더에서 **`install.bat`** 더블클릭  
또는:

```bat
py -3.12 -m pip install -r requirements.txt
```

### 3) GPU 사용 시 (NVIDIA)

```bat
py -3.12 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

그다음 `config.ini`의 `[AI]`에서:

```ini
AI_device = 0
```

(`0` = 첫 번째 GPU, `cpu` = CPU)

---

## 실행

| 파일 | 설명 |
|------|------|
| **`run_gui.bat`** | GUI로 실행 (권장) |
| `run_ai.bat` | GUI 없이 `run.py`만 실행 |

GUI에서 **에임봇 시작**을 누르면 백그라운드로 동작하고, 로그는 GUI에 표시됩니다.

### 단축키 (기본)

| 키 | 동작 |
|----|------|
| 우클릭 | 에임 보조 (누르는 동안) |
| F2 | 종료 |
| F3 | 일시정지 |
| F4 | `config.ini` 다시 읽기 |

GUI **단축키** 탭에서 변경 후 **config.ini 저장**하면 됩니다.

---

## 주요 설정 (`config.ini`)

### 탐지 / AI

| 옵션 | 설명 |
|------|------|
| `detection_window_width/height` | 탐지 영역 크기 (기본 320, 너무 키우면 느려짐) |
| `AI_model_name` | `models/` 안 모델 파일 |
| `AI_model_image_size` | 320 빠름 / 640 정확 |
| `AI_conf` | 탐지 신뢰도 (0.2~0.35) |
| `AI_device` | `0`(GPU) 또는 `cpu` |
| `disable_tracker` | `True`면 트래커 끔 (조금 더 가벼움) |

### 조준

| 옵션 | 설명 |
|------|------|
| `body_y_offset` | 몸 조준 시 위로 올리는 비율 (머리 쪽이면 0.4~0.6) |
| `disable_headshot` | `False` = 머리 우선 |
| `disable_prediction` | `True` = 예측 없이 바로 조준 |

### 마우스 속도

| 옵션 | 설명 |
|------|------|
| `mouse_sensitivity` | **낮을수록** 더 빠르게 붙음 |
| `mouse_min/max_speed_multiplier` | 속도 배율 |
| `mouse_dpi` / `mouse_fov_*` | DPI·FOV 보정값 |

자세한 값은 GUI에서 단축키를 바꾸고, 나머지는 `config.ini`를 직접 수정한 뒤 **F4**로 리로드하면 됩니다.

---

## 폴더 구조

```
├── run_gui.bat      ← 실행 (GUI, 권장)
├── run_ai.bat       ← 실행 (CLI)
├── install.bat      ← 라이브러리 설치
├── gui_main.py
├── run.py
├── config.ini
├── requirements.txt
├── models/          ← AI 모델
└── logic/           ← 핵심 코드
```

---

## 문제 해결

| 증상 | 해결 |
|------|------|
| `No module named ...` | `install.bat` 다시 실행 (`py -3.12`) |
| CUDA / torch 오류 | GPU면 CUDA PyTorch 설치 + `AI_device = 0` |
| 너무 느림 | GPU 사용, `AI_model_image_size = 320`, 디버그 창 끄기 |
| GUI가 바로 꺼짐 | `py -3.12 gui_main.py`로 에러 확인. 락 파일이면 `%TEMP%\sunone_aimbot_gui.lock` 삭제 |
| 이미 실행 중 | 기존 GUI/에임봇 종료 후 다시 실행 |

---

## 라이선스

MIT License. 원본 저작권은 SunOner 프로젝트에 있으며, 본 저장소는 개인 수정본입니다.
