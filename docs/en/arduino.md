**Language / 언어:** [한국어](../ko/arduino.md) · [English](arduino.md)

# Arduino PC Connection Guide

With `input_method = ARDUINO`, `ai.exe` sends commands over a **serial (COM)** port. The board should appear to Windows as an extra **HID mouse** and inject relative movement.

This does **not** relay your wireless mouse. Keep the wireless receiver on the game PC; Arduino is a separate input device.

## What you need

- A board that can act as a USB HID mouse (for example Leonardo, Pro Micro, Micro-class)
- USB cable
- For two-PC serial split: USB–TTL adapter + jumper wires
- Firmware on the board that understands this app’s serial protocol

This repository does not ship Arduino firmware. Use firmware that accepts the text commands below and emits HID move/click.

## Serial commands from the app

Default baud rate `115200`. One command per line (`\n`).

| Command | Meaning |
|---|---|
| `mX,Y` | Relative move (example: `m10,-3`) |
| `c` | Click |
| `p` / `r` | Button press / release |

With `arduino_16_bit_mouse = false` (default), large moves are split into ±127 chunks.  
With `true`, a single `mX,Y` line is sent.

A console line like `[Arduino] Connected! PORT: COMx` means the serial link opened.

---

## Setup 1 — One PC (simplest)

Game and `ai.exe` on the **same** machine.

```text
[ PC ]
   │ USB
   ▼
 Arduino (HID mouse + virtual COM)
   │
   └─ ai.exe → arduino_port = COMx
```

1. Flash firmware, then **close the Arduino IDE** (avoids COM lock).
2. Plug the board into the PC over USB.
3. In Device Manager → **Ports (COM & LPT)**, note the COM number.
4. Example `config.ini` / overlay settings:

```ini
input_method = ARDUINO
arduino_port = COM3
arduino_baudrate = 115200
arduino_16_bit_mouse = false
arduino_enable_keys = false
```

5. Start `ai.exe` and confirm the desktop cursor can move.
6. Keep using your wireless mouse as usual.

Replace `COM3` with your port. `COM0` is only a placeholder.

---

## Setup 2 — Two PC (split HID and serial)

Goal:

- **Game PC:** Arduino USB → Windows HID mouse
- **Helper PC:** `ai.exe` opens COM and sends moves

A single Leonardo USB plug puts both HID and COM on **one** PC. For two PCs, run HID on the game PC and bring UART to the helper PC with USB–TTL.

```text
Helper PC                       Game PC
┌─────────────┐                ┌─────────────┐
│ ai.exe      │                │ game +      │
│ COM (TTL)   │── TX/RX/GND ──▶│ wireless    │
└─────────────┘                │ mouse       │
                               │ Arduino USB │◀── HID mouse
                               └─────────────┘
```

Wiring outline (pin names differ by board/adapter):

1. Arduino **USB** → game PC  
2. Arduino **TX** → USB–TTL **RX**  
3. Arduino **RX** → USB–TTL **TX**  
4. Shared **GND**  
5. USB–TTL → helper PC (new COM port)

Helper PC `config.ini`:

```ini
input_method = ARDUINO
arduino_port = COM5
arduino_baudrate = 115200
arduino_16_bit_mouse = false
arduino_enable_keys = false
```

`COM5` must be the TTL adapter port on the helper PC.

Notes:

- Confirm the firmware reads the UART you wired, and that the board can use USB HID and that UART together.
- Match logic level (3.3V/5V) and baud rate.
- For capture on two PCs use `udp_capture` or `virtual_camera` — see [Two-PC guide](two-pc.md).

Network devices such as `KMBOX_NET` are often simpler cabling for two-PC input.

---

## Setup 3 — USB Host Shield (reference)

Older Python tooling mentioned USB Host Shield library/debug checks.  
The C++ `ARDUINO` path still talks over **local COM serial**. If you use a Host Shield, the shield/firmware handles mouse passthrough or injection; PC↔board traffic must still match the serial (or firmware) interface you configure.

---

## Checklist / troubleshooting

| Symptom | Check |
|---|---|
| `[Arduino] Unable to connect` | COM number, cable, IDE or another app locking the port |
| Connected but no cursor move | Firmware protocol (`mX,Y`), HID-capable board, USB plugged into the game PC (two-PC) |
| Works only in IDE serial monitor | Close IDE, run only `ai.exe` |
| Two-PC moves helper cursor only | HID USB is on the helper PC instead of the game PC |

Related:

- [Two-PC guide](two-pc.md)
- [config — Arduino](../../engine/docs/config.md#arduino)
- [Input methods](../../engine/docs/guides/input-methods.md)
