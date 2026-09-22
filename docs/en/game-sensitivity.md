**Language / 언어:** [한국어](../ko/game-sensitivity.md) · [English](game-sensitivity.md)

# Game Sensitivity (`[Games]` Profile)

Settings used to convert **on-screen pixel error → mouse movement counts** for the aimbot.  
Applies **regardless of** `GHUB`, `ARDUINO`, Host Shield, or other input methods.

Manual movement uses your normal in-game / G HUB sensitivity.  
Only **aimbot-generated moves** use this profile.

## config.ini

```ini
active_game = UNIFIED

[Games]
UNIFIED = 1,0.022,0.022
#         │   │     └─ pitch (engine constant)
#         │   └─ yaw
#         └─ sens (same number as in-game sensitivity)
```

With FOV scaling:

```ini
UNIFIED = 1,0.022,0.022,true,90
#                              │    └─ baseFOV
#                              └─ fovScaled
```

## Fields

| Field | Meaning | Example |
|-------|---------|---------|
| `sens` | Match **in-game sensitivity** | `1`, `2.5`, `0.8` |
| `yaw` | Horizontal scale | Source-like `0.022` |
| `pitch` | Vertical scale | Often same as yaw |
| `fovScaled` | FOV change compensation (optional) | `true` / `false` |
| `baseFOV` | Reference FOV (optional) | `90` |

## Edit in UI

`ai.exe` → **Home** → **Mouse** tab → **Game profile**

- Select / add / remove profiles
- Yaw / Pitch sliders
- Source-style preset (`0.022`) when available

## By input method

| Method | Main mouse sens | Aimbot sens |
|--------|-----------------|-------------|
| [Dual input](dual-mouse.md) | In-game + G HUB | `[Games]` |
| [G HUB](ghub.md) | In-game + G HUB | `[Games]` |
| [Host Shield](arduino-host-shield.md) | In-game (merged HID) | `[Games]` |
| [Arduino only](arduino.md) | In-game | `[Games]` |

## Tuning tips

| Symptom | Adjust |
|---------|--------|
| Overshoots target | Lower FOV / max speed, weaker prediction |
| Undershoots | Check `[Games]` sens, yaw/pitch |
| Wrong only after FOV change | `fovScaled=true`, `baseFOV` |
| Horizontal only off | Tune yaw / pitch separately |

UI FOV slider minimum (e.g. 10) may be a UI limit; lower values can be typed in `config.ini`.

## Related

- [Input methods comparison](input-methods.md)
- [Engine — config Games](../../engine/docs/config.md)
- [Engine — circle FOV](../../engine/docs/guides/circle-fov.md)
