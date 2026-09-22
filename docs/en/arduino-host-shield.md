**Language / 언어:** [한국어](../ko/arduino-host-shield.md) · [English](arduino-host-shield.md)

# USB Host Shield + Wireless Mouse

Plug the wireless **dongle** into a USB Host Shield; Leonardo **passes through** physical input and **merges** aimbot injection as **one** HID mouse to the PC.

If you need G HUB scripts, use [Dual input](dual-mouse.md) or [G HUB](ghub.md) instead.

## Wiring

```text
[ Wireless mouse ] ~~ [ Dongle ] → USB Host Shield → Leonardo → PC USB
                                    ↑
                               ai.exe (serial or RawHID)
```

## Pros and cons

| | Host Shield | Dual input (dongle on PC + Leonardo) |
|--|-------------|--------------------------------------|
| Mice seen by PC | 1 (merged) | 2 |
| G HUB | No | Yes |
| Firmware | HID_Arduino, MYMOUSEINFO debug | Serial `mX,Y` firmware |
| Difficulty | High | Medium |

## Requirements

- Arduino Leonardo (or compatible)
- USB Host Shield 2.0
- Wireless mouse USB **receiver (dongle)** — not the mouse itself
- [SunOner/HID_Arduino](https://github.com/SunOner/HID_Arduino) or compatible firmware

## Relation to the C++ app

- `input_method = ARDUINO` — serial `mX,Y` (firmware passthrough + serial)
- `input_method = TEENSY41_HID` — RawHID packets ([HID_Arduino](https://github.com/SunOner/HID_Arduino) style)

Pick `input_method` to match your firmware.  
This is **not** the same as simple serial HID in the [Arduino guide](arduino.md).

## MYMOUSEINFO (wireless / generic)

Many wireless dongles use **4-byte** HID reports. Confirm in Serial Monitor, then edit `hidcustom.h`.

Example (right-click pattern like `00 EF 05 00`):

```cpp
struct MYMOUSEINFO {
    uint8_t buttons;
    uint8_t dX;
    uint8_t dY;
    int8_t  wheel;
};
```

### Debug steps

1. Set `ENABLE_UHS_DEBUGGING 1` in firmware
2. Serial Monitor at **9600**
3. Move/click mouse → note 4 vs 6 byte patterns
4. Match `MYMOUSEINFO` field types and order
5. Set `ENABLE_UHS_DEBUGGING 0` when done

Some Logitech G mice need separate `hidmousereport` firmware.

## Example config.ini (serial path)

```ini
input_method = ARDUINO
arduino_port = COM3
arduino_baudrate = 115200
```

RawHID path:

```ini
input_method = TEENSY41_HID
teensy_hid_serial = AUTO
teensy_hid_vid_filter = AUTO
teensy_hid_pid_filter = AUTO
```

## Game sensitivity

Aimbot move math still uses `[Games]` with Host Shield.  
→ [Game sensitivity](game-sensitivity.md)

## Troubleshooting

| Symptom | Check |
|---------|--------|
| No/erratic cursor | MYMOUSEINFO, 4/6-byte dongle |
| G HUB dead | Expected — try [Dual input](dual-mouse.md) |
| No COM port | Leonardo USB, firmware CDC |
| Logitech only broken | G-series firmware variant |

## Related

- [Dual input — keep G HUB](dual-mouse.md)
- [Input methods comparison](input-methods.md)
- [Arduino PC connection](arduino.md)
- [HID_Arduino (GitHub)](https://github.com/SunOner/HID_Arduino)
