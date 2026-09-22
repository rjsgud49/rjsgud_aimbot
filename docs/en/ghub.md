**Language / 언어:** [한국어](../ko/ghub.md) · [English](ghub.md)

# G HUB Input Method

Uses `ghub_mouse.dll` on a PC with Logitech **G HUB** installed to inject aimbot movement and clicks.  
Plug the wireless **dongle directly into the PC** so G HUB scripts and DPI profiles keep working.

## Wiring

```text
[ Wireless mouse ] ~~ [ Dongle ] ──→ PC USB
                                        ↑
ai.exe ── ghub_mouse.dll ──────────────┘  (extra aim/click input)
         G HUB (profiles / scripts)
```

- Main mouse: manual aim + G HUB
- Aimbot: **additional** relative moves via DLL

## Requirements

- Logitech G HUB (`C:\Program Files\LGHUB`)
- `ghub_mouse.dll` in the **same folder as** `ai.exe`  
  (e.g. `engine/build/dml/Release/` or `ai_5.0.3_DML/`)
- Logitech mouse + dongle/cable → PC

## config.ini

```ini
input_method = GHUB

active_game = UNIFIED
```

Sensitivity → [Game sensitivity](game-sensitivity.md)

## Setup steps

1. Install and run Logitech G HUB
2. Copy `ghub_mouse.dll` next to `ai.exe`
3. Set `input_method = GHUB` in `config.ini`
4. Run `ai.exe` → Home → **Mouse** tab
5. Check G HUB version message (app expects `13.1.4` as reference)
6. Test on desktop and in game

Use the overlay **Open GHub Docs** link if version/path fails.

## G HUB vs Leonardo

| | G HUB (`GHUB`) | Leonardo (`ARDUINO`) |
|--|----------------|----------------------|
| Extra hardware | None (DLL only) | Leonardo board |
| G HUB scripts | Yes | Yes (dongle on PC) |
| Game blocking | Possible on some titles | HID device path |
| Setup | DLL + G HUB running | COM + firmware |

For G HUB scripts **and** hardware HID → [Dual input](dual-mouse.md).

## Notes

- Overlay warning: may be detected in some games — use at your own risk.
- Behavior varies by title even vs `WIN32`.
- **Host Shield** dongle path breaks G HUB → [Host Shield](arduino-host-shield.md)

## Troubleshooting

| Symptom | Check |
|---------|--------|
| DLL load fail | `ghub_mouse.dll` path, x64 match |
| Version warning | `C:\Program Files\LGHUB\version`, G HUB running |
| Boxes but no move | `input_method = GHUB`, game input block |
| Wrong sensitivity | `[Games]` sens / yaw / pitch |

## Related

- [Dual input (G HUB + Leonardo)](dual-mouse.md)
- [Input methods comparison](input-methods.md)
- [Game sensitivity](game-sensitivity.md)
- [Engine — Input methods](../../engine/docs/guides/input-methods.md)
