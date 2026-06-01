"""
Tests para el compositor de imágenes (Módulo 4).
Genera imágenes sintéticas para verificar la composición 2x2.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from gsheets.utils.image_compositor import compose_ticket_image


# ── Helpers ───────────────────────────────────────────────────────────────


def _create_test_image(
    path: str | Path, width: int, height: int, color: tuple[int, int, int]
) -> Path:
    """Crea una imagen PNG de color sólido para testing."""
    path = Path(path)
    img = Image.new("RGB", (width, height), color)
    img.save(path, "PNG")
    return path


# ── Fixtures ──────────────────────────────────────────────────────────────


@pytest.fixture
def cell_images(tmp_path):
    """Crea 4 imágenes de prueba representando celdas A3, F3, A6, F6."""
    images = {}
    images["a3"] = _create_test_image(
        tmp_path / "a3.png", 100, 25, (255, 200, 200)
    )
    images["f3"] = _create_test_image(
        tmp_path / "f3.png", 120, 25, (200, 255, 200)
    )
    images["a6"] = _create_test_image(
        tmp_path / "a6.png", 100, 30, (200, 200, 255)
    )
    images["f6"] = _create_test_image(
        tmp_path / "f6.png", 120, 30, (255, 255, 200)
    )
    return images


# ── Tests ─────────────────────────────────────────────────────────────────


class TestComposeTicketImage:
    def test_compose_creates_image(self, cell_images, tmp_path):
        output = tmp_path / "ticket_capture.png"

        result = compose_ticket_image(
            top_left_path=cell_images["a3"],
            top_right_path=cell_images["f3"],
            bottom_left_path=cell_images["a6"],
            bottom_right_path=cell_images["f6"],
            output_path=output,
        )

        assert output.exists()
        assert result == str(output.resolve())

        # Verificar dimensiones
        img = Image.open(output)
        # Ancho: max(100, 100)=100 + max(120, 120)=120 + border(2) = 222
        # Alto: max(25, 25)=25 + max(30, 30)=30 + border(2) = 57
        assert img.width == 222
        assert img.height == 57

    def test_compose_different_sizes(self, tmp_path):
        """Celdas de distinto tamaño deben alinearse correctamente."""
        tl = _create_test_image(tmp_path / "tl.png", 80, 20, (255, 0, 0))
        tr = _create_test_image(tmp_path / "tr.png", 150, 35, (0, 255, 0))
        bl = _create_test_image(tmp_path / "bl.png", 90, 40, (0, 0, 255))
        br = _create_test_image(tmp_path / "br.png", 140, 25, (255, 255, 0))

        output = tmp_path / "composed.png"
        compose_ticket_image(tl, tr, bl, br, output)

        img = Image.open(output)
        # col_left = max(80, 90) = 90
        # col_right = max(150, 140) = 150
        # row_top = max(20, 35) = 35
        # row_bottom = max(40, 25) = 40
        assert img.width == 90 + 150 + 2  # 242
        assert img.height == 35 + 40 + 2  # 77

    def test_compose_with_labels(self, cell_images, tmp_path):
        output = tmp_path / "with_labels.png"

        compose_ticket_image(
            top_left_path=cell_images["a3"],
            top_right_path=cell_images["f3"],
            bottom_left_path=cell_images["a6"],
            bottom_right_path=cell_images["f6"],
            output_path=output,
            labels={
                "top_left": "A3",
                "top_right": "F3",
                "bottom_left": "A6",
                "bottom_right": "F6",
            },
        )

        assert output.exists()

    def test_missing_file_raises(self, cell_images, tmp_path):
        output = tmp_path / "fail.png"

        with pytest.raises(FileNotFoundError):
            compose_ticket_image(
                top_left_path="nonexistent.png",
                top_right_path=cell_images["f3"],
                bottom_left_path=cell_images["a6"],
                bottom_right_path=cell_images["f6"],
                output_path=output,
            )

    def test_corrupt_file_raises(self, cell_images, tmp_path):
        corrupt = tmp_path / "corrupt.png"
        corrupt.write_text("not an image")

        output = tmp_path / "fail2.png"

        with pytest.raises(ValueError):
            compose_ticket_image(
                top_left_path=corrupt,
                top_right_path=cell_images["f3"],
                bottom_left_path=cell_images["a6"],
                bottom_right_path=cell_images["f6"],
                output_path=output,
            )
