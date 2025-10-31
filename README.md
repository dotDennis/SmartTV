# Smart TV – Socket Programming Exercise
_Author: dotDennis • Course: IDATA2304_

---

## 📖 Overview
This project implements a simple **Smart TV** system for the IDATA2304 course.  
It consists of:

- **Smart TV server** – a TCP server that represents the TV.
- **Smart Remote client** – a TCP client that connects to the TV and sends commands.

---

## ⚡ Features
- ✅ TV starts **OFF** by default — only `on` is accepted while OFF.
- ✅ Commands for turning ON/OFF, status checking, and channel management.
- ✅ Clean **logic separation**:  
  - `logic/tv.py` → TV state & behavior  
  - `handler.py` → command parsing / validation  
  - `server.py` → networking layer  
  - `client.py` → simple CLI remote
- ✅ Easily extensible command system (just add to `COMMANDS` table).
- ✅ Multi-client server with per-connection threads (no blocking between remotes).
- ✅ Asynchronous broadcast: when one remote changes channel, others see a notice immediately.
- ✅ Unit tests for command parsing and TV logic.

---

## 🧩 Project Structure
```
smart-tv/
│── logic/
│   └── tv.py              # SmartTV class (power + channels)
│── handler.py             # Command parser & dispatcher
│── server.py              # TCP server
│── client.py              # TCP client (remote control)
│── config.py              # Shared configuration (APP_NAME, version, host/port)
│── tests/
│   ├── test_handler.py    # Unit tests for command handling
│   └── test_tv_logic.py   # Unit tests for TV core logic
└── README.md
```

---

## 🚀 Running

### 1. Start the server
```bash
python3 server.py
```
Default: binds to `127.0.0.1:1238`.

### 2. Start one or more clients
```bash
python3 client.py
```
Connects to the default host/port defined in `config.py`. You can run multiple clients at the same time; when one sends `set_ch <n>`, the others receive a `[Notice] Channel changed to <n>` message automatically.

---

## 💻 Commands
```
help           - lists available commands
version        - shows Smart TV version
on             - turns ON the TV
off            - turns OFF the TV
status         - shows if TV is ON or OFF
get_c          - returns number of available channels
get_ch         - returns currently active channel
set_ch <n>     - sets TV to channel <n>
quit           - disconnect
```

⚠️ **Important:**  
Until you turn the TV **ON**, only the `on` command works.

---

## 🧪 Testing
Unit tests are written using **pytest**.

Run them with:
```bash
pytest
```

Tests cover:
- TV logic (power state, channels, invalid ranges)
- Command parsing & validation (arguments, errors, version, help, etc.)

---

## ⚙️ Config
Edit default host/port or version in [`config.py`](config.py):
```python
APP_NAME = 'SmartTV'
APP_VERSION = '1.0'
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1238
```

---

This completes **Part 1, 2 & 3** of the assignment