**Language / 언어:** [한국어](../ko/dual-mouse.md) · [English](dual-mouse.md)

# Dual Input — Wireless Mouse + Leonardo (Recommended)

**Manual aim** stays on your wireless mouse (including G HUB). **Auto tracking** goes through Leonardo only.  
This is the easiest way to keep G HUB scripts, DPI profiles, and in-game sensitivity.

## Wiring

```text
[ Wireless mouse ] ~~ [ USB dongle ] ──→ PC USB (mouse 1)
                                         ↑
[ Leonardo ] ── USB (HID + COM) ────────┘  (mouse 2)
       ↑
   ai.exe (sends mX,Y over COM)
```

- Dongle stays on the **PC** so G HUB sees your mouse.
- Leonardo is an **extra HID mouse** for aimbot movement only.
- **No Host Shield** required.

## config.ini

```ini
input_method = ARDUINO
arduino_port = COM3
arduino_baudrate = 115200
arduino_16_bit_mouse = false
arduino_enable_keys = false

active_game = UNIFIED
```

Replace `COM3` with Leonardo’s COM port from Device Manager.  
For sensitivity see [Game sensitivity](game-sensitivity.md).

## Setup steps

1. Flash **serial HID firmware** on Leonardo (`mX,Y` / `c` / `p` / `r` protocol)
2. **Close Arduino IDE** (avoid COM lock)
3. Plug Leonardo and wireless **dongle** into the PC (two USB ports)
4. Note Leonardo **COM number** in Device Manager
5. Set `arduino_port` in `config.ini`
6. Run `ai.exe` → confirm `[Arduino] Connected! PORT: COMx`
7. Slight cursor movement on desktop = OK
8. Run G HUB with your existing profiles/scripts

## Roles

| Action | Handled by |
|--------|------------|
| Manual aim | Wireless mouse |
| G HUB macros / recoil / DPI | G HUB (main mouse) |
| Auto aim assist | Leonardo (`ARDUINO`) |
| Aimbot move math | `[Games]` sens / yaw / pitch |

Do **not** use `input_method = GHUB` at the same time for output.  
Aimbot uses Leonardo (`ARDUINO`); G HUB stays on the main mouse.

## Auto-shoot (optional)

```ini
arduino_enable_keys = true
```

Firmware must handle `p` / `r` / `c`. Avoid overlapping G HUB click macros.

## Two-PC

- **Game PC:** Leonardo USB (HID) + wireless dongle
- **Helper PC:** `ai.exe` + USB–TTL for COM

Wiring → [Arduino — two-PC](arduino.md#setup-2--two-pc-split-hid-and-serial)

## Troubleshooting

| Symptom | Check |
|---------|--------|
| G HUB scripts dead | Dongle not on Shield/Leonardo |
| Aim scale wrong | `[Games]` sens matches in-game |
| COM connect fail | IDE closed, COM number, cable |
| Movement feels doubled | FOV/speed, `[Games]` yaw/pitch |

## Comparison

| | Dual input (this doc) | Host Shield |
|--|----------------------|-------------|
| G HUB | Yes | No |
| USB ports | Dongle + Leonardo | Shield + Leonardo |
| Mice seen by PC | 2 | 1 (merged) |

→ [Input methods comparison](input-methods.md) · [Host Shield](arduino-host-shield.md)

## Related

- [Arduino PC connection](arduino.md)
- [G HUB without Leonardo](ghub.md)
- [Game sensitivity](game-sensitivity.md)
