"""Reinsercao de texto em GVX (versao 1 e 2) do Hajime no Ippo 2.
Procura o bloco do texto original (id + Shift-JIS + 0 + padding) e as referencias a ele:
  v1: u32 = (cnt << 16) | idx
  v2: u32 idx, u32 cnt (consecutivos)
Se o texto novo cabe, sobrescreve no lugar; senao anexa no fim do arquivo e corrige as referencias."""
import struct


def header(b):
    assert b[:4] == b'GVX0', 'nao e GVX'
    ver = b[4]
    pool = struct.unpack('<5I', b[12:32])[4]
    return ver, pool


def find_refs(b, ver, pool, idx, cnt):
    """Retorna lista de (offset, cnt_real). Aceita cnt_real >= cnt (bloco com conteudo extra)."""
    refs = []
    for o in range(0x20, pool - 4, 4):
        if ver == 1:
            v = struct.unpack_from('<I', b, o)[0]
            if (v & 0xffff) == idx and cnt <= (v >> 16) <= cnt + 512:
                refs.append((o, v >> 16))
        else:
            i, c = struct.unpack_from('<II', b, o)
            if i == idx and cnt <= c <= cnt + 512:
                refs.append((o, c))
    exact = [r for r in refs if r[1] == cnt]
    return exact or refs


def replace_all(data, pairs):
    """pairs: lista de (texto_original_str, texto_novo_bytes_sjis). Retorna (bytes, relatorio)."""
    b = bytearray(data)
    ver, pool = header(data)
    rep = {'ok': 0, 'fim': 0, 'sem_ref': [], 'nao_achou': []}
    for orig, new in pairs:
        s = orig.encode('shift_jis')
        hits = []
        start = pool
        while True:
            o = bytes(b).find(s + b"\x00", start)
            if o < 0:
                break
            hits.append(o)
            start = o + 1
        hits = [o for o in hits if (o - pool) % 4 == 0 and o - 4 >= pool]
        if not hits:
            rep['nao_achou'].append(orig[:40]); continue
        done = 0
        for o in hits:
            ent = o - 4
            idx = (ent - pool) // 4
            cnt = 1 + (len(s) + 1 + 3) // 4
            refs = find_refs(b, ver, pool, idx, cnt)
            if not refs:
                continue
            rc = refs[0][1]
            refs = [r for r, c in refs if c == rc]
            tid = b[ent:ent + 4]
            tail = bytes(b[o + len(s):ent + rc * 4]) if rc > cnt else b'\x00'
            cnt = rc
            blk = bytes(tid) + new + tail
            blk += b'\x00' * (-len(blk) % 4)
            nc = len(blk) // 4
            if nc <= cnt:
                b[ent:ent + cnt * 4] = blk + b'\x00' * ((cnt - nc) * 4)
                nidx = idx
                rep['ok'] += 1
            else:
                while len(b) % 4: b += b'\x00'
                nidx = (len(b) - pool) // 4
                b += blk
                rep['fim'] += 1
            done += 1
            for r in refs:
                if ver == 1:
                    struct.pack_into('<I', b, r, (nc << 16) | nidx)
                else:
                    struct.pack_into('<II', b, r, nidx, nc)
        if not done:
            rep.setdefault('falhou', []).append(orig[:40])
    return bytes(b), rep

