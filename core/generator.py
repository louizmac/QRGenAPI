from io import BytesIO
import re

import qrcode
from qrcode.constants import (
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
    ERROR_CORRECT_H
)
from qrcode.exceptions import DataOverflowError


ERROR_CORRECTION_LEVELS = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H
}


def validate_color(color):
    if not re.fullmatch(r"[0-9a-fA-F]{6}", color):
        raise ValueError(
            "Colors must be six-digit hexadecimal values"
        )

    return f"#{color}"


def generate_qr(
    data,
    output_format="png",
    fill_color="000000",
    back_color="FFFFFF",
    box_size=10,
    border=4,
    error_correction="M"
):
    output_format = output_format.lower()
    error_correction = error_correction.upper()

    if output_format not in ("png", "svg"):
        raise ValueError("Unsupported output format")

    if error_correction not in ERROR_CORRECTION_LEVELS:
        raise ValueError("Invalid error correction level")

    if not 1 <= box_size <= 30:
        raise ValueError("Invalid box size")

    if not 4 <= border <= 20:
        raise ValueError("Invalid border size")

    fill_color = validate_color(fill_color)
    back_color = validate_color(back_color)

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECTION_LEVELS[error_correction],
        box_size=box_size,
        border=border
    )

    try:
        qr.add_data(data)
        qr.make(fit=True)
    except DataOverflowError:
        raise ValueError("Data is too large for a QR code")

    output = BytesIO()

    if output_format == "svg":
        matrix = qr.get_matrix()
        size = len(matrix)
        rectangles = []

        for y, row in enumerate(matrix):
            for x, active in enumerate(row):
                if active:
                    rectangles.append(
                        f'<rect x="{x}" y="{y}" width="1" height="1"/>'
                    )

        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {size} {size}" '
            f'width="{size * box_size}" '
            f'height="{size * box_size}">'
            f'<rect width="100%" height="100%" fill="{back_color}"/>'
            f'<g fill="{fill_color}">'
            + "".join(rectangles)
            + "</g></svg>"
        )

        return svg.encode("utf-8")

    image = qr.make_image(
        fill_color=fill_color,
        back_color=back_color
    ).convert("RGB")

    image.save(output, format="PNG")

    return output.getvalue()
