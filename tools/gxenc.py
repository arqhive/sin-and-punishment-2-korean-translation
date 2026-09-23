"""GX 텍스처 인코더 (RGBA8, RGB565, IA4) 및 texture.arc 제자리 교체."""
import struct
import numpy as np
import narc


def enc_rgba8(img):
    """img: (h,w,4) uint8"""
    h, w, _ = img.shape; out = bytearray()
    for by in range(0, h, 4):
        for bx in range(0, w, 4):
            blk = img[by:by + 4, bx:bx + 4].reshape(16, 4)
            ar = np.stack([blk[:, 3], blk[:, 0]], 1).ravel()
            gb = np.stack([blk[:, 1], blk[:, 2]], 1).ravel()
            out += ar.astype(np.uint8).tobytes() + gb.astype(np.uint8).tobytes()
    return bytes(out)


def enc_rgb565(img):
    h, w, _ = img.shape; out = bytearray()
    r = (img[:, :, 0].astype(np.uint16) >> 3); g = (img[:, :, 1].astype(np.uint16) >> 2); b = (img[:, :, 2].astype(np.uint16) >> 3)
    v = (r << 11 | g << 5 | b).astype('>u2')
    for by in range(0, h, 4):
        for bx in range(0, w, 4):
            out += v[by:by + 4, bx:bx + 4].tobytes()
    return bytes(out)


def _c565(c):
    return (int(c[0]) >> 3) << 11 | (int(c[1]) >> 2) << 5 | (int(c[2]) >> 3)


def _e565(v):
    r = (v >> 11) & 31; g = (v >> 5) & 63; b = v & 31
    return np.array([r << 3 | r >> 2, g << 2 | g >> 4, b << 3 | b >> 2], np.float32)


def _cmpr_block(px):
    """4x4 RGB 블록 → DXT1(4색 모드) 8바이트"""
    p = px.reshape(16, 3).astype(np.float32)
    mean = p.mean(0); cov = np.cov((p - mean).T) if p.std() > 0 else np.eye(3)
    try:
        axis = np.linalg.eigh(cov)[1][:, -1]
    except Exception:
        axis = np.array([1, 1, 1]) / 3 ** .5
    t = (p - mean) @ axis
    c0 = np.clip(mean + axis * t.max(), 0, 255); c1 = np.clip(mean + axis * t.min(), 0, 255)
    v0, v1 = _c565(c0), _c565(c1)
    if v0 < v1: v0, v1 = v1, v0
    if v0 == v1:
        return struct.pack('>HHI', v0, v1, 0)
    e0, e1 = _e565(v0), _e565(v1)
    pal = np.stack([e0, e1, (2 * e0 + e1) / 3, (e0 + 2 * e1) / 3])
    idx = ((p[:, None, :] - pal[None]) ** 2).sum(2).argmin(1)
    bits = 0
    for i in idx: bits = bits << 2 | int(i)
    return struct.pack('>HHI', v0, v1, bits)


def enc_cmpr(img):
    h, w, _ = img.shape; out = bytearray()
    for by in range(0, h, 8):
        for bx in range(0, w, 8):
            for sy, sx in ((0, 0), (0, 4), (4, 0), (4, 4)):
                out += _cmpr_block(img[by + sy:by + sy + 4, bx + sx:bx + sx + 4, :3])
    return bytes(out)


ENC = {6: enc_rgba8, 4: enc_rgb565, 14: enc_cmpr}


def tex_info(arc, name):
    """(TEX0 데이터 절대 오프셋, w, h, fmt)"""
    for n, o, s, fl in narc.parse(bytes(arc)):
        if n == name:
            d = arc[o:o + s]; i = d.find(b'TEX0')
            w, h, fmt, _ = struct.unpack('>HHII', d[i + 0x1c:i + 0x28])
            return o + i + struct.unpack('>I', d[i + 0x10:i + 0x14])[0], w, h, fmt
    raise KeyError(name)


def enc_cmpr_partial(img, orig, raw0):
    """바뀐 4x4 블록만 다시 압축하고 나머지는 원본 바이트를 유지한다."""
    h, w, _ = img.shape; out = bytearray(raw0); p = 0
    for by in range(0, h, 8):
        for bx in range(0, w, 8):
            for sy, sx in ((0, 0), (0, 4), (4, 0), (4, 4)):
                y, x = by + sy, bx + sx
                if not np.array_equal(img[y:y + 4, x:x + 4, :3], orig[y:y + 4, x:x + 4, :3]):
                    out[p:p + 8] = _cmpr_block(img[y:y + 4, x:x + 4, :3])
                p += 8
    return bytes(out)


def replace(arc, name, img):
    off, w, h, fmt = tex_info(arc, name)
    assert img.shape[:2] == (h, w), (name, img.shape, (w, h))
    if fmt == 14:
        import gxtex
        n = w * h // 2
        raw = enc_cmpr_partial(img, gxtex.decode(bytes(arc[off:off + n]), w, h, 14), bytes(arc[off:off + n]))
    else:
        raw = ENC[fmt](img)
    arc[off:off + len(raw)] = raw
