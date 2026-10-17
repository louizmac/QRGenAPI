<div align="center">

# QRGenAPI

<p>
  A lightweight, open-source QR code generation REST API.
  <br>
  Generate customizable PNG and SVG QR codes with a fully self-hosted service.
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-REST_API-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-black?style=flat-square" alt="License">
</p>

</div>

---

## Overview

QRGenAPI is a simple, self-hosted REST API that allows developers to generate customizable QR codes from text, URLs, and other data without relying on external services.

QR codes are generated locally in memory and returned directly to the client.

No database, cloud service, or external API is required.

## Features

- Generate QR codes from text and URLs
- PNG and SVG output formats
- Custom foreground and background colors
- Adjustable QR code size
- Configurable border size
- Four error correction levels
- Automatic QR code version selection
- Maximum input length of 1,000 characters
- No database or external API required
- Interactive API documentation
- Fully self-hosted

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/louizmac/QRGenAPI.git
cd QRGenAPI
```

**2. Create a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Start the server**

```bash
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive documentation:

`http://127.0.0.1:8000/docs`

## API Reference

### Generate QR Code

`GET /api/v1/generate`

Generate a QR code from text, a URL, or other data.

**Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| data | String | Required | Text or URL to encode |
| format | String | png | Output format: png or svg |
| fill_color | String | 000000 | Foreground hex color |
| back_color | String | FFFFFF | Background hex color |
| box_size | Integer | 10 | Size of each QR module (1–30) |
| border | Integer | 4 | Border width in modules (4–20) |
| error_correction | String | M | Error correction level: L, M, Q, H |

**Example Request**

```bash
curl -G "http://127.0.0.1:8000/api/v1/generate" \
  --data-urlencode "data=https://github.com/louizmac" \
  --data-urlencode "format=png" \
  --output qrcode.png
```

### Generate SVG QR Code

Generate a scalable vector QR code.

```bash
curl -G "http://127.0.0.1:8000/api/v1/generate" \
  --data-urlencode "data=Hello World" \
  --data-urlencode "format=svg" \
  --output qrcode.svg
```

### Generate Custom QR Code

Customize the colors, size, and error correction level.

```bash
curl -G "http://127.0.0.1:8000/api/v1/generate" \
  --data-urlencode "data=QRGenAPI" \
  --data-urlencode "format=png" \
  --data-urlencode "fill_color=1E40AF" \
  --data-urlencode "back_color=FFFFFF" \
  --data-urlencode "box_size=15" \
  --data-urlencode "error_correction=H" \
  --output custom.png
```

## Python Example

Install the requests library:

```bash
pip install requests
```

```python
import requests

url = "http://127.0.0.1:8000/api/v1/generate"

response = requests.get(
    url,
    params={
        "data": "https://github.com/louizmac",
        "format": "png",
        "box_size": 10,
        "error_correction": "H"
    }
)

response.raise_for_status()

with open("qrcode.png", "wb") as file:
    file.write(response.content)
```

## Supported Formats

| Format | Output |
|--------|--------|
| PNG | Yes |
| SVG | Yes |

## Error Correction

QRGenAPI supports four error correction levels.

| Level | Approximate Recovery |
|-------|----------------------|
| L | 7% |
| M | 15% |
| Q | 25% |
| H | 30% |

Higher error correction levels may increase the QR code size.

## Project Structure

```text
QRGenAPI/
├── main.py
├── core/
│   ├── __init__.py
│   └── generator.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Notes

- QR codes are generated locally in memory.
- The maximum input length is 1,000 characters.
- Colors must be six-digit hexadecimal values without `#`.
- Some color combinations may reduce QR code readability.
- SVG output supports custom foreground and background colors.
- No user data is stored by the application.
- Additional security measures are recommended before public deployment.

## License

Distributed under the MIT License. See `LICENSE` for details.

---

<div align="center">

  <sub>Built with Python, FastAPI and python-qrcode.</sub>
  <br>
  <sub>Created by <a href="https://github.com/louizmac">louizmac</a></sub>

</div>
