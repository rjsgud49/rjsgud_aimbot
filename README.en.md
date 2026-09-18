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
Models: place `.onnx` under `engine\build\dml\Release\models\`

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
| Two-PC | [투컴](docs/ko/two-pc.md) | [Two-PC](docs/en/two-pc.md) |
| Arduino connection | [아두이노](docs/ko/arduino.md) | [Arduino](docs/en/arduino.md) |

## Notes

- Legacy Python lives in `legacy_python\` (ignore for normal use)
- Batch files under `engine\` are build helpers (`CPP_build.bat` calls `build_dml.bat`)
- Engine English guides: `engine/docs/guides.md`

## License

Follows the original sunone_aimbot_2 and related licenses.
