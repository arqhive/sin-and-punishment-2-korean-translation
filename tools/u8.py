"""U8 아카이브 / IMD5 / LZ77(0x10) 유틸"""
import struct, hashlib


def u8_list(b):
    root = struct.unpack('>I', b[4:8])[0]
    n = struct.unpack('>I', b[root + 8:root + 12])[0]; st = root + n * 12
    out = []; stack = []; path = []
    ents = []
    for i in range(n):
        e = b[root + i * 12:root + i * 12 + 12]
        t = e[0]; no = int.from_bytes(e[1:4], 'big'); o, sz = struct.unpack('>II', e[4:12])
        nm = b[st + no:b.index(b'\0', st + no)].decode()
        ents.append((t, nm, o, sz))
    # 경로 계산
    ends = []; cur = []
    for i, (t, nm, o, sz) in enumerate(ents):
        while ends and i >= ends[-1]:
            ends.pop(); cur.pop()
        if i == 0: continue
        if t == 1:
            cur.append(nm); ends.append(sz)
        else:
            out.append(('/'.join(cur + [nm]), i, o, sz))
    return root, ents, out


def lz77_dec(d):
    assert d[0] == 0x10
    size = int.from_bytes(d[1:4], 'little'); p = 4; out = bytearray()
    while len(out) < size:
        flags = d[p]; p += 1
        for bit in range(8):
            if len(out) >= size: break
            if flags & (0x80 >> bit):
                v = d[p] << 8 | d[p + 1]; p += 2
                ln = (v >> 12) + 3; disp = (v & 0xFFF) + 1
                for _ in range(ln): out.append(out[-disp])
            else:
                out.append(d[p]); p += 1
    return bytes(out)


def lz77_enc(d):
    """LZ77(0x10) 압축. 위치마다 최장 일치를 구한 뒤 DP로 비트 수가 가장 적은 분할을 고른다."""
    n = len(d)
    best = [(0, 0)] * n          # (길이, 거리)
    for p in range(n):
        start = max(0, p - 4096); maxl = min(18, n - p)
        if maxl < 3: continue
        lo, hi = 2, maxl; found = (0, 0)
        # 최장 일치 길이 이분 탐색 (겹치는 복사는 제외해 단순화)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            idx = d.rfind(d[p:p + mid], start, p + mid - 1)
            if idx != -1 and idx < p:
                lo = mid; found = (mid, p - idx)
            else:
                hi = mid - 1
        if found[0] >= 3:
            # 같은 길이에서 가장 가까운 위치
            idx = d.rfind(d[p:p + found[0]], start, p + found[0] - 1)
            best[p] = (found[0], p - idx)
    cost = [0] * (n + 1); choice = [0] * n
    for p in range(n - 1, -1, -1):
        c = 9 + cost[p + 1]; ch = 1
        L = best[p][0]
        for l in range(3, L + 1):
            v = 17 + cost[p + l]
            if v < c: c, ch = v, l
        cost[p] = c; choice[p] = ch
    out = bytearray([0x10]) + n.to_bytes(3, 'little'); p = 0
    while p < n:
        flagpos = len(out); out.append(0); flags = 0
        for bit in range(8):
            if p >= n: break
            l = choice[p]
            if l >= 3:
                disp = best[p][1]
                # 짧게 쓸 때도 같은 거리가 유효하다(앞부분 일치)
                v = (l - 3) << 12 | (disp - 1)
                out += bytes([v >> 8, v & 0xFF]); flags |= 0x80 >> bit; p += l
            else:
                out.append(d[p]); p += 1
        out[flagpos] = flags
    return bytes(out)


def imd5_unwrap(d):
    assert d[:4] == b'IMD5'
    body = d[32:]
    return lz77_dec(body[4:]) if body[:4] == b'LZ77' else body, body[:4] == b'LZ77'


def imd5_wrap(data, compress):
    body = (b'LZ77' + lz77_enc(data)) if compress else data
    return b'IMD5' + struct.pack('>I', len(body)) + b'\0' * 8 + hashlib.md5(body).digest() + body
