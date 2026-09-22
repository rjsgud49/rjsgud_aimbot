**Language / 언어:** [한국어](README.md) · [English](README.en.md)

# Aimbot — C++ (sunone_aimbot_2)

## Run

| File | Purpose |
|------|---------|
| **`CPP_build.bat`** | Build (first time) |
| **`CPP_run.bat`** | Run |

1. `CPP_build.bat`
2. `CPP_run.bat`
3. In game, press **Home** for the settings overlay

Prebuilt binary: `engine\build\dml\Release\ai.exe`  
Models: put `.onnx` in root `models\` then run `CPP_run.bat` (copies into Release).  
`.pt` is ignored by DML. Pick the model in Home → AI.

## Capture modes

| Setup | `capture_method` | Capture card |
|------|------------------|--------------|
| **One PC** | `duplication_api` or `winrt` | Not required |
| **Two PC + HDMI** | `virtual_camera` | Required |
| **Two PC + LAN** | `udp_capture` | Not required |

Two-PC moves capture and inference off the game PC onto a helper PC running `ai.exe`.

## Docs

| Topic | 한국어 | English |
|------|--------|---------|
| Docs index | [docs](docs/README.md) | [docs](docs/README.md) |
| **Input methods (overview)** | [입력 방식](docs/ko/input-methods.md) | [Input methods](docs/en/input-methods.md) |
| Dual input (wireless + Leonardo) | [입력 2개](docs/ko/dual-mouse.md) | [Dual input](docs/en/dual-mouse.md) |
| G HUB | [G HUB](docs/ko/ghub.md) | [G HUB](docs/en/ghub.md) |
| Host Shield + wireless | [Host Shield](docs/ko/arduino-host-shield.md) | [Host Shield](docs/en/arduino-host-shield.md) |
| Game sensitivity | [게임 감도](docs/ko/game-sensitivity.md) | [Sensitivity](docs/en/game-sensitivity.md) |
| Two-PC | [투컴](docs/ko/two-pc.md) | [Two-PC](docs/en/two-pc.md) |
| Arduino connection | [아두이노](docs/ko/arduino.md) | [Arduino](docs/en/arduino.md) |
| KMBOX connection | [KMBOX](docs/ko/kmbox.md) | [KMBOX](docs/en/kmbox.md) |

## Notes

- Legacy Python lives in `legacy_python\` (ignore for normal use)
- Batch files under `engine\` are build helpers (`CPP_build.bat` calls `build_dml.bat`)
- Engine English guides: `engine/docs/guides.md`

## License

Follows the original sunone_aimbot_2 and related licenses.
