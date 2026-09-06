"""Decode the inline formatting used by classic WordStar documents."""

from __future__ import annotations

from html import escape
from typing import BinaryIO


STYLE_CODES = {
    0x02: ("bold", "strong"),
    0x04: ("double strike", "strong"),
    0x13: ("underline", "u"),
    0x14: ("superscript", "sup"),
    0x16: ("subscript", "sub"),
    0x18: ("strike", "s"),
    0x19: ("italic", "em"),
}


def decode_bytes(data: bytes, encoding: str = "cp437", strip_high_bit: bool = True) -> str:
    """Decode printable WordStar bytes while preserving control characters."""
    result: list[str] = []
    for value in data:
        if value == 0x1A:
            break
        printable_value = value & 0x7F if strip_high_bit else value
        if printable_value in STYLE_CODES or printable_value in (0x09, 0x0A, 0x0C, 0x0D):
            result.append(chr(printable_value))
        elif printable_value >= 0x20:
            result.append(bytes([printable_value]).decode(encoding, errors="replace"))
        else:
            result.append(chr(printable_value))
    return "".join(result)


def render_html(text: str, show_controls: bool = False, show_dot_commands: bool = True) -> str:
    """Render WordStar text as safe HTML with inline formatting."""
    html: list[str] = []
    active: dict[str, bool] = {name: False for name, _ in STYLE_CODES.values()}
    dot_line = False
    line_start = True

    def marker(label: str, value: str) -> None:
        if show_controls:
            html.append(f'<span class="ws-control">[{escape(label)}]</span>')

    for char in text:
        if line_start and char == ".":
            dot_line = True
        if char in ("\n", "\r"):
            if char == "\n":
                html.append("<br>\n")
                line_start = True
                dot_line = False
            elif show_controls:
                marker("CR", "")
            continue
        if char == "\t":
            html.append('<span class="ws-space">&#x21E5;</span>')
            line_start = False
            continue
        code = ord(char)
        if code in STYLE_CODES:
            label, tag = STYLE_CODES[code]
            active[label] = not active[label]
            html.append(f"</{tag}>" if not active[label] else f"<{tag}>")
            marker(label, "")
            line_start = False
            continue
        if code == 0x0C:
            marker("PAGE", "")
            html.append('<span class="ws-page">&#x21D3; page break</span><br>')
            line_start = True
            continue
        if code < 0x20:
            marker(f"0x{code:02X}", "")
            continue
        escaped = escape(char)
        if dot_line and not show_dot_commands:
            html.append(f'<span class="ws-dot-hidden">{escaped}</span>')
        else:
            html.append(escaped)
        line_start = False

    for label, tag in STYLE_CODES.values():
        if active[label]:
            html.append(f"</{tag}>")
    return "".join(html)


def plain_text(text: str) -> str:
    """Remove WordStar inline control bytes for a readable text download."""
    return "".join(char for char in text if ord(char) >= 0x20 or char in "\r\n\t")


def read_source(source: bytes | BinaryIO, encoding: str, strip_high_bit: bool) -> tuple[str, int]:
    """Read and decode a byte string or an uploaded binary stream."""
    data = source if isinstance(source, bytes) else source.read()
    return decode_bytes(data, encoding, strip_high_bit), len(data)