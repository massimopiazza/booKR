def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: tuple) -> str:
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def interpolate_color(color1: str, color2: str, t: float) -> str:
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return rgb_to_hex((r, g, b))

def interpolate_palette(palette: list, n: int) -> list:
    if n <= len(palette):
        return palette[:n]
    m = len(palette)
    return [
        interpolate_color(
            palette[int(i * (m - 1) / (n - 1))],
            palette[min(int(i * (m - 1) / (n - 1)) + 1, m - 1)],
            (i * (m - 1) / (n - 1)) % 1
        )
        for i in range(n)
    ]