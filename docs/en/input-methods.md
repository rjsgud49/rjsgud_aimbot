**Language / 언어:** [한국어](../ko/input-methods.md) · [English](input-methods.md)

# Mouse Input Methods — Comparison

`ai.exe` selects **only the path used for aimbot movement and clicks** via `input_method`.  
Many setups keep your normal mouse separate as a second device.

## At a glance

| Method | Wiring | G HUB scripts | Wireless mouse | Difficulty | Best for |
|--------|--------|---------------|----------------|------------|----------|
| [Dual input (wireless + Leonardo)](dual-mouse.md) | Dongle→PC, Leonardo→PC | Yes | Yes | Medium | **Keep G HUB + wireless + aim assist** |
| [G HUB](ghub.md) | Dongle→PC, `GHUB` | Yes | Yes | Easy | Already on Logitech G HUB |
| [Arduino only](arduino.md) | Leonardo→PC | (depends on main mouse) | Yes | Medium | External HID bridge only |
| [Host Shield](arduino-host-shield.md) | Dongle→Shield→Leonardo | No | Yes | Hard | Single merged mouse device |
| WIN32 | Software only | Yes | Yes | Easy | Desktop test (often blocked in games) |
| [KMBOX](kmbox.md) | Network/USB bridge | (depends on main mouse) | Yes | Medium | Two-PC / hardware bridge |
| TEENSY41_HID | RawHID board | (depends on main mouse) | Yes | Medium | [HID_Arduino](https://github.com/SunOner/HID_Arduino) etc. |

## Common: game sensitivity

The `[Games]` profile that converts target offset to mouse counts works **regardless of `input_method`**.  
→ [Game sensitivity](game-sensitivity.md)

## Two mice on Windows

Windows **merges relative movement** from multiple HID mice into one stream for games.

```text
Mouse 1 (wireless)  ──→ manual aim + G HUB
Mouse 2 (Leonardo)  ──→ ai.exe aim assist only
         ↓
      game (summed)
```

- `input_method` picks **one output path** for the aimbot.
- Your wireless mouse needs no extra config entry.

## Key `config.ini` settings

```ini
input_method = ARDUINO   # or GHUB, TEENSY41_HID, KMBOX_NET, …
```

| Method | Extra settings |
|--------|------------------|
| ARDUINO | `arduino_port`, `arduino_baudrate` |
| GHUB | `ghub_mouse.dll` next to `ai.exe`, Logitech G HUB running |
| TEENSY41_HID | `teensy_hid_*` filters |
| KMBOX | `kmbox_net_*` or `kmbox_a_pidvid` |

Full reference: [engine/docs/config.md](../../engine/docs/config.md)

## Which one to pick?

```text
Must keep G HUB scripts/profiles
  → [Dual input](dual-mouse.md) or [G HUB](ghub.md)
  → Host Shield does not work well with G HUB

Wireless mouse + Leonardo for aim only
  → [Dual input](dual-mouse.md) (no Host Shield)

Want one merged mouse (dongle on Shield)
  → [Host Shield](arduino-host-shield.md) (give up G HUB on that path)

Two-PC (game PC / helper PC)
  → [Two-PC guide](two-pc.md) + one of the methods above
```

## Related docs

- [Dual input — wireless + Leonardo](dual-mouse.md)
- [G HUB input](ghub.md)
- [Arduino PC connection](arduino.md)
- [USB Host Shield + wireless](arduino-host-shield.md)
- [Game sensitivity (`[Games]`)](game-sensitivity.md)
- [Two-PC](two-pc.md) · [KMBOX](kmbox.md)
- [Engine — Input methods](../../engine/docs/guides/input-methods.md)
