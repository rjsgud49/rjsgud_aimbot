**Language / 언어:** [한국어](../ko/kmbox.md) · [English](kmbox.md)

# KMBOX Connection Guide

This app supports `KMBOX_NET` (Ethernet) and `KMBOX_A` (USB PID/VID).  
Your normal wireless mouse does not have to be intercepted. The box injects a **separate** mouse input on the game PC, or you can plug a physical mouse into the box for passthrough.

Official manuals:

- [kmbox Net](https://www.kmbox.top/wiki_doc/kmboxNet-en/site/)
- [kmbox B+](https://www.kmbox.top/wiki_doc/kmboxB-en/site/) (reference; wiring differs from this app’s `KMBOX_A`)

### Where to buy

| Source | Link |
|---|---|
| Official site | [kmbox.top](https://www.kmbox.top/) |
| Net manual | [kmbox Net User Manual](https://www.kmbox.top/wiki_doc/kmboxNet-en/site/) |

Resellers vary—confirm the model (**Net** / **A** / **B+**). For two-PC setups, **Net** is usually the simplest cabling.

---

## Which type

| App setting | Device | Helper PC ↔ box | Game PC |
|---|---|---|---|
| `KMBOX_NET` | kmbox **Net** | Ethernet | USB `controlled PC` port |
| `KMBOX_A` | kmbox **A** family | USB (PID/VID) | Follow the product USB/HID layout |

You do not need a separate USB–TTL adapter for Net.

---

## Setup A — `KMBOX_NET` (recommended for two PC)

### Cables

Follow the port labels on the back of the box.

```text
Helper PC (ai.exe)            kmbox Net              Game PC
┌──────────────┐             ┌──────────┐         ┌──────────────┐
│ Ethernet     │────────────▶│ Net port │         │              │
│              │             │controlled│────────▶│ USB (HID)    │
│              │             │ PC port  │         │              │
└──────────────┘             │ mouse/KB │◀── wired mouse (optional)
                             └──────────┘         └──────────────┘
```

1. **Net port** → helper PC (or shared switch). Talk to the IP shown on the box.  
2. **controlled PC** → game PC USB. The game PC sees a HID mouse.  
3. (Optional) Physical mouse/keyboard → box input ports for passthrough.  
4. On one PC, the manual allows both Net and controlled cables on the **same** machine.

### Network

1. Install the **network adapter driver** after connecting the Net port (per the official guide).  
2. Make sure the helper PC can reach the box subnet.  
3. Copy values from the box **LCD**:
   - IP → `kmbox_net_ip`
   - Port → `kmbox_net_port`
   - MAC / UUID → `kmbox_net_uuid`  
     (passed to `kmNet_init` as mac; the config key is named `uuid`)

### Example `config.ini`

```ini
input_method = KMBOX_NET
kmbox_net_ip = 10.42.42.42
kmbox_net_port = 1984
kmbox_net_uuid = DEADC0DE
```

`10.42.42.42` / `DEADC0DE` are placeholders—**replace with the LCD values**.

In the overlay (Home) → input method, enter IP/Port/UUID and **Save & reconnect**.  
Green `kmboxNet connected` means the link is up.

Firewall rules blocking the port can cause failure. Watch for `[KmboxNet] Connection failed` in the console.

---

## Setup B — `KMBOX_A`

The box attaches over USB to the PC running `ai.exe` (or your one-PC machine). Identify it with `kmbox_a_pidvid`.

Format: **8 hex chars `PPPPVVVV`** (first 4 = PID, last 4 = VID).

```ini
input_method = KMBOX_A
kmbox_a_pidvid = C07D046D
```

The example is format-only. Read the real PID/VID from Device Manager or the vendor tool, then concatenate as `PPPPVVVV`.  
Bad format prints `[KmboxA] Invalid PIDVID format. Expected 8 hex chars (PPPPVVVV).`

Save PIDVID in the overlay, **Save & reconnect**, and confirm `kmboxA connected`.

For two-PC with A, follow the product USB layout carefully. If you want a clean network split, prefer Net.

---

## Wireless mouse

- Keep the wireless receiver on the game PC and let KMBOX inject extra HID moves, or  
- Plug a wired mouse into the box for passthrough plus software injection.  

Either way the goal is a mouse path into the game PC—not relaying your existing wireless dongle through software.

---

## Checklist

| Symptom | Check |
|---|---|
| `kmboxNet not connected` | LCD IP/Port/MAC, Ethernet, adapter IP/driver, firewall |
| `Connection failed` | Typos in `kmbox_net_*`, wrong subnet, Net cable not on helper PC |
| A connect fail | 8-char `kmbox_a_pidvid`, USB port, drivers |
| Connected but no in-game move | `controlled PC` cable on game PC, overlay still on KMBOX |

Capture for two PC is separate → [Two-PC guide](two-pc.md)  
Serial alternative → [Arduino guide](arduino.md)

Related:

- [config — Kmbox](../../engine/docs/config.md#kmbox-net)
- [Input methods](../../engine/docs/guides/input-methods.md)
