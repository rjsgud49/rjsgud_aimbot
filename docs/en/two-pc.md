**Language / 언어:** [한국어](../ko/two-pc.md) · [English](two-pc.md)

# Two-PC Setup (External Capture + Inference)

Use a second PC so the game PC only runs the game, while the helper PC receives frames and runs inference.

Your normal wireless/wired mouse is not relayed. It stays on the game PC; the bridge device injects a **separate** mouse input.

## Roles

| Machine | Role |
|---|---|
| Game PC | Runs the game, sends video (capture card or UDP/OBS), receives mouse from an external input bridge |
| Helper PC | Runs `ai.exe`, receives frames, runs detection, sends mouse commands through KMBOX / MAKCU / Arduino / etc. |

Prefer a wired LAN between the two machines.

## Data path

```text
Game PC display
    │
    ├─(A) HDMI → capture card → helper PC (virtual_camera)
    │
    └─(B) FFmpeg/OBS → UDP MJPEG → helper PC (udp_capture)
              │
              ▼
         Helper PC: inference
              │
              ▼
         KMBOX / MAKCU / Arduino / ... → game PC mouse
```

## Method A — Capture card

1. Route game PC HDMI (or a mirrored/extended display) into the capture card on the helper PC.
2. Confirm Windows sees the capture device.
3. On the helper PC:

```ini
capture_method = virtual_camera
virtual_camera_name = ExactDeviceName
virtual_camera_width = 1920
virtual_camera_heigth = 1080
detection_resolution = 320
capture_fps = 60
```

`virtual_camera_name` must match the device name exactly. Valid `detection_resolution` values are `160`, `320`, and `640`.

You can also feed the card into OBS and select OBS Virtual Camera as `virtual_camera`.

## Method B — Software UDP (no capture card)

Helper PC receiver:

```ini
capture_method = udp_capture
udp_ip = 0.0.0.0
udp_port = 1234
detection_resolution = 320
capture_fps = 60
```

Allow inbound UDP on the helper PC, then stream from the game PC with FFmpeg/OBS. Full sender examples: [UDP capture over LAN](../../engine/docs/guides/udp-capture.md).

## Mouse input on two PCs

`WIN32` on the helper PC does not move the mouse on the game PC. Configure a bridged method such as `KMBOX_NET`, `KMBOX_A`, `MAKCU`, `ARDUINO`, `RP2350`, or `TEENSY41_HID`.

Example (network device):

```ini
input_method = KMBOX_NET
kmbox_net_ip = 10.42.42.42
kmbox_net_port = 1984
kmbox_net_uuid = DEADC0DE
```

For Arduino wiring and COM setup, see **[Arduino PC connection](arduino.md)**.  
For KMBOX (Net/A), see **[KMBOX connection](kmbox.md)**.

See also [Input methods](../../engine/docs/guides/input-methods.md) and [Input method config](../../engine/docs/config.md#input-method).

## Checklist

1. Start `ai.exe` on the helper PC with a model ready.
2. Use `virtual_camera` (A) or `udp_capture` (B).
3. Confirm the overlay preview shows the game feed.
4. Confirm the chosen `input_method` moves the game PC cursor.
5. If latency is high: use wired LAN, lower resolution / `detection_resolution`, tune UDP quality, or check capture-card pass-through delay.

## One PC vs two PC

| | One PC | Two PC |
|---|---|---|
| `capture_method` | `duplication_api` or `winrt` | `virtual_camera` or `udp_capture` |
| Capture card | Not required | Only for method A |
| Input | `WIN32` may be enough for testing | External bridge recommended |

Related docs:

- [Arduino PC connection](arduino.md)
- [KMBOX connection](kmbox.md)
- [UDP capture over LAN](../../engine/docs/guides/udp-capture.md)
- [Capture config](../../engine/docs/config.md#capture)
- [Input methods](../../engine/docs/guides/input-methods.md)
