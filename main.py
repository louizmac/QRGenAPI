from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from core.generator import generate_qr


app = FastAPI(
    title="QRGenAPI",
    description="A lightweight, open-source QR code generation REST API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://trymyapis.rf.gd"
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "name": "QRGenAPI",
        "version": "1.0.0",
        "status": "online",
        "endpoints": [
            "/api/v1/generate"
        ]
    }


@app.get("/api/v1/generate")
def generate(
    data: str = Query(..., min_length=1, max_length=1000),
    format: str = "png",
    fill_color: str = "000000",
    back_color: str = "FFFFFF",
    box_size: int = Query(10, ge=1, le=30),
    border: int = Query(4, ge=4, le=20),
    error_correction: str = "M"
):
    try:
        image = generate_qr(
            data=data,
            output_format=format,
            fill_color=fill_color,
            back_color=back_color,
            box_size=box_size,
            border=border,
            error_correction=error_correction
        )

        output_format = format.lower()

        media_type = (
            "image/svg+xml"
            if output_format == "svg"
            else "image/png"
        )

        return Response(
            content=image,
            media_type=media_type,
            headers={
                "Content-Disposition": (
                    f'attachment; filename="qrcode.{output_format}"'
                )
            }
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
