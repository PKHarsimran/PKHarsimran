"""Build a watertight Bender fan-art STL and its responsive, animated previews.

The silhouette and the engraved details share one implicit solid. Marching
tetrahedra makes a single closed surface: no overlapping STL body parts, external
modelling packages, or downloaded character assets are needed.
"""
import argparse
from array import array
from base64 import b64encode
from collections import defaultdict
from functools import lru_cache
from html import escape
from math import ceil, cos, sqrt
from pathlib import Path
import struct
import zlib

from profile_theme import apply_theme

ROOT = Path(__file__).resolve().parents[1]


def rounded_box(x, y, z, cx, cy, cz, hx, hy, hz, radius):
    q = (abs(x-cx)-hx+radius, abs(y-cy)-hy+radius, abs(z-cz)-hz+radius)
    return sqrt(sum(max(v, 0)**2 for v in q)) + min(max(q), 0) - radius


def tube(x, y, z, start, end, radius, ribs=False):
    p = (x-start[0], y-start[1], z-start[2])
    axis = tuple(b-a for a, b in zip(start, end))
    length2 = sum(v*v for v in axis)
    t = max(0, min(1, sum(a*b for a, b in zip(p, axis))/length2))
    distance = sqrt(sum((a-t*b)**2 for a, b in zip(p, axis)))
    if ribs:
        radius += .16*cos(t*sqrt(length2)*3.1)
    return distance-radius


# Relaxed right arm, raised left arm, three fingers on each hand.
LIMBS = (
    ((11, 0, 42), (16.7, 0, 35), 2.15, True),
    ((16.7, 0, 35), (17.5, -1, 27), 1.9, True),
    ((-11, 0, 42), (-17.2, 0, 45.5), 2.15, True),
    ((-17.2, 0, 45.5), (-18.2, -1, 53), 1.9, True),
    ((-18.2, -1, 52), (-18.2, -1, 54.5), 2.4, False),
    ((17.5, -1, 27), (17.5, -1, 25.3), 2.4, False),
)
FINGERS = tuple(
    ((x, -1, z), (x+dx, -1.2, z+dz), .85, False)
    for x, z, dx, dz in ((-20, 54, -.5, 4), (-18.2, 54.5, 0, 4.5),
                         (-16.4, 54, .5, 3.6), (15.7, 25, -.2, -2.5),
                         (17.5, 25, 0, -3), (19.3, 25, .2, -2.4))
)


def field(x, y, z):
    """Negative inside; the face looks toward -Y and the antenna points +Z."""
    radial = sqrt(x*x+y*y)
    # Rounded cylindrical head, short neck and gently tapered barrel torso.
    head = sqrt(radial**2 + max(abs(z-59.1)-7, 0)**2)-7.35
    head = max(head, 49.1-z)  # Bender's flat jaw, rounded crown.
    neck = max(radial-3.7, abs(z-47.5)-3)
    body_radius = 8.6 + 2.3*max(0, min(1, (z-23)/22))
    body = max(radial-body_radius, abs(z-34)-11)-.5
    d = min(head, neck, body)
    if z > 70:
        d = min(d, max(radial-.78, abs(z-75)-5.8),
                sqrt(x*x+y*y+(z-81.2)**2)-1.65)
    if z < 25:
        for side in (-1, 1):
            d = min(d, tube(x, y, z, (side*4.8, 0, 5), (side*4.8, 0, 24), 2.15, True),
                    rounded_box(x, y, z, side*5, -2, 2.6, 3.9, 6.7, 2.6, 1.3))
    if abs(x) > 8 and 19 < z < 62:
        for start, end, radius, ribs in LIMBS+FINGERS:
            d = min(d, tube(x, y, z, start, end, radius, ribs))
    # Protruding visor frame; two raised eyes survive the recessed dark aperture.
    if 57 < z < 65 and y < -3:
        frame = rounded_box(x, y, z, 0, -6.6, 61.2, 7.9, 2.6, 2.9, 1.25)
        aperture = rounded_box(x, y, z, 0, -8.5, 61.2, 6.9, 1.7, 1.8, .8)
        d = max(min(d, frame), -aperture)
        for eye in (-3.45, 3.45):
            eyeball = rounded_box(x, y, z, eye, -7.6, 60.9, 2.85, 1.5, 1.2, .75)
            # Engraved pupils, physically present in the monochrome STL too.
            pupil = rounded_box(x, y, z, eye+.4, -9.1, 60.7, .45, .55, .63, .12)
            d = min(d, max(eyeball, -pupil))
    # Raised jaw grille with engraved tooth separators, all attached at the back.
    if 50 < z < 58 and y < -3:
        jaw = rounded_box(x, y, z, 0, -6.1, 54.3, 5.4, 1.9, 2.65, 1.1)
        d = min(d, jaw)
        groove = max(abs(x)-4.7, abs(y+8.05)-.45, abs(z-54.3)-.24)
        for tooth in (-3.2, -1.1, 1.1, 3.2):
            groove = min(groove, max(abs(x-tooth)-.21, abs(y+8.05)-.45, abs(z-54.3)-2.0))
        d = max(d, -groove)
    # Engraved belly door and its small inset handle; no unattached decoration.
    if 25 < z < 42 and y < -4:
        outer = rounded_box(x, y, z, 0, -9.4, 33.4, 5.6, 3.2, 6.5, .85)
        inner = rounded_box(x, y, z, 0, -9.4, 33.4, 5.18, 4, 6.08, .65)
        rim = max(outer, -inner)
        # Only the outer .65 mm of the curved barrel is engraved.
        rim = max(rim, -(radial-(body_radius-.15)))
        handle = rounded_box(x, y, z, 3.4, -9.3, 33.4, .45, 1.8, 1.2, .2)
        d = max(d, -min(rim, handle))
    return d


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


@lru_cache(maxsize=2)
def mesh(step=.65):
    """Use the same tetrahedral split in every cell so shared edges agree."""
    axes = [tuple(round(low+i*step, 6) for i in range(ceil((high-low)/step)+1))
            for low, high in ((-23.17, 23.63), (-12.13, 13.22), (-1.19, 84.61))]
    xs, ys, zs = axes
    nx, ny, nz = map(len, axes)
    points = [(x, y, z) for x in xs for y in ys for z in zs]
    values = [field(*p)-.017 for p in points]
    offsets = (0, ny*nz, ny*nz+nz, nz, 1, ny*nz+1, ny*nz+nz+1, nz+1)
    tets = ((0, 5, 1, 6), (0, 1, 2, 6), (0, 2, 3, 6),
            (0, 3, 7, 6), (0, 7, 4, 6), (0, 4, 5, 6))
    vertices = {}
    facets = []

    def edge(a, b):
        key = (min(a, b), max(a, b))
        if key not in vertices:
            a, b = key
            t = values[a]/(values[a]-values[b])
            # Store the actual float32 STL coordinates, also used by verification.
            vertices[key] = struct.unpack('<3f', struct.pack('<3f', *(u+t*(v-u) for u, v in zip(points[a], points[b]))))
        return vertices[key]

    def emit(ids, inside, outside):
        p = tuple(edge(a, b) for a, b in ids)
        normal = cross(tuple(b-a for a, b in zip(p[0], p[1])), tuple(b-a for a, b in zip(p[0], p[2])))
        # Winding points from an interior tetrahedron vertex toward the outside.
        direction = tuple(b-a for a, b in zip(points[inside], points[outside]))
        if sum(a*b for a, b in zip(normal, direction)) < 0:
            p = (p[0], p[2], p[1])
            normal = tuple(-v for v in normal)
        length = sqrt(sum(v*v for v in normal))
        if not length: raise ValueError('Degenerate Bender surface triangle')
        facets.append((tuple(v/length for v in normal), p))

    for x in range(nx-1):
        for y in range(ny-1):
            for z in range(nz-1):
                base = (x*ny+y)*nz+z
                ids = tuple(base+offset for offset in offsets)
                if all(values[i] < 0 for i in ids) or all(values[i] >= 0 for i in ids):
                    continue
                for tet in tets:
                    inside = [ids[t] for t in tet if values[ids[t]] < 0]
                    outside = [ids[t] for t in tet if values[ids[t]] >= 0]
                    if not inside or not outside: continue
                    if len(inside) == 1:
                        emit([(inside[0], b) for b in outside], inside[0], outside[0])
                    elif len(outside) == 1:
                        emit([(a, outside[0]) for a in inside], inside[0], outside[0])
                    else:
                        a, b = inside
                        c, d = outside
                        emit(((a, c), (a, d), (b, d)), a, c)
                        emit(((a, c), (b, d), (b, c)), a, c)
    return tuple(facets)


def verify_mesh(facets):
    """Check the serialized mesh: winding, two faces per edge, one shell, volume."""
    edges = defaultdict(list)
    volume = 0
    for index, (_, points) in enumerate(facets):
        a, b, c = points
        volume += sum(v*w for v, w in zip(a, cross(b, c)))/6
        for first, last in ((a, b), (b, c), (c, a)):
            edges[tuple(sorted((first, last)))].append((index, first, last))
    if not facets or volume <= 0: raise ValueError('Bender must enclose a positive volume')
    neighbours = defaultdict(set)
    for shared in edges.values():
        if len(shared) != 2 or shared[0][1:] != shared[1][1:][::-1]:
            raise ValueError('Bender must be watertight with consistent face winding')
        a, b = shared[0][0], shared[1][0]
        neighbours[a].add(b)
        neighbours[b].add(a)
    reached = set()
    pending = [0]
    while pending:
        face = pending.pop()
        if face in reached: continue
        reached.add(face)
        pending.extend(neighbours[face]-reached)
    if len(reached) != len(facets): raise ValueError('Bender must be one connected shell')


def stl():
    facets = mesh()
    verify_mesh(facets)
    data = bytearray(b'Bender / Futurama fan-art keepsake / PKHarsimran'.ljust(80, b' '))
    data.extend(struct.pack('<I', len(facets)))
    for normal, points in facets:
        data.extend(struct.pack('<12fH', *normal, *(v for p in points for v in p), 0))
    if len(data) >= 10_000_000: raise ValueError('Keep the model within GitHub viewer limits')
    return bytes(data)


def material(normal, center):
    x, y, z = center
    color = (174, 190, 204)
    if 59.3 < z < 63.5 and y < -6.5:
        color = (28, 38, 47)
        if abs(x) < 6.4 and 59.75 < z < 62.1 and y < -8.35:
            color = (244, 233, 183)
            if min(abs(x+3.05), abs(x-3.85)) < .56 and 60 < z < 61.4:
                color = (25, 33, 41)
    if abs(x) < 5.1 and 51.9 < z < 56.5 and y < -7.3:
        color = (239, 232, 201) if y < -7.7 else (54, 66, 77)
    if abs(x) < 5.8 and 26.6 < z < 40.2 and y < -6.7:
        color = (113, 133, 150) if normal[1] > -.65 else (174, 190, 204)
    # Smooth cylindrical highlights, with the actual facet normals on details.
    if color == (174, 190, 204) and (z > 49 or 24 < z < 45 and abs(x) < 10):
        smooth = (x, y, max(0, z-66.1) if z > 49 else -.105*sqrt(x*x+y*y))
        length = sqrt(sum(v*v for v in smooth))
        if length and normal[2] < .8 and normal[1] < .2:
            normal = tuple(v/length for v in smooth)
    diffuse = max(0, sum(a*b for a, b in zip(normal, (-.3, -.6, .74))))
    light = .69 + .31*diffuse
    return tuple(max(0, min(255, round(c*light))) for c in color)


@lru_cache(maxsize=1)
def model_png():
    """Small self-contained render of the real mesh, with a software Z buffer.

    Baking just the sculpture keeps the SVG below 150 KB instead of embedding
    tens of thousands of polygons. SVG typography and motion stay native.
    """
    width, height, factor = 400, 740, 2
    rw, rh = width*factor, height*factor
    scale = 8*factor
    pixels = bytearray(rw*rh*4)
    depth = array('f', [-1e9])*(rw*rh)
    view = (.30, -.94, .18)
    for normal, points in mesh():
        if sum(a*b for a, b in zip(normal, view)) <= 0: continue
        center = tuple(sum(p[i] for p in points)/3 for i in range(3))
        projected = [(rw/2+(x*.953+y*.304)*scale,
                      rh-24*factor+((x*.304-y*.953)*.18-z*.984)*scale,
                      sum(a*b for a, b in zip((x, y, z), view))) for x, y, z in points]
        (ax, ay, az), (bx, by, bz), (cx, cy, cz) = projected
        denominator = (by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
        if abs(denominator) < 1e-10: continue
        color = bytes((*material(normal, center), 255))
        for py in range(max(0, int(min(ay, by, cy))), min(rh-1, ceil(max(ay, by, cy)))+1):
            for px in range(max(0, int(min(ax, bx, cx))), min(rw-1, ceil(max(ax, bx, cx)))+1):
                u = ((by-cy)*(px+.5-cx)+(cx-bx)*(py+.5-cy))/denominator
                v = ((cy-ay)*(px+.5-cx)+(ax-cx)*(py+.5-cy))/denominator
                if u < 0 or v < 0 or u+v > 1: continue
                distance = u*az+v*bz+(1-u-v)*cz
                index = py*rw+px
                if distance <= depth[index]: continue
                depth[index] = distance
                pixels[index*4:index*4+4] = color
    # Premultiplied box sampling avoids dark fringes around transparent edges.
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # PNG scanline filter: none.
        for x in range(width):
            samples = [(2*y+dy)*rw+2*x+dx for dy in (0, 1) for dx in (0, 1)]
            covered = [i*4 for i in samples if pixels[i*4+3]]
            if covered:
                raw.extend(round(sum(pixels[i+c] for i in covered)/len(covered)) for c in range(3))
                raw.append(round(255*len(covered)/4))
            else: raw.extend(b'\0\0\0\0')
    def chunk(kind, data):
        return struct.pack('>I', len(data))+kind+data+struct.pack('>I', zlib.crc32(kind+data))
    png = b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR', struct.pack('>2I5B', width, height, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(raw, 9))+chunk(b'IEND', b'')
    return b64encode(png).decode('ascii')


def illustration(mobile=False):
    w, h = (600, 670) if mobile else (1000, 390)
    mx, my, scale = (316, 605, 4.8) if mobile else (778, 342, 3.7)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
             '<title id="title">Bender / built different</title><desc id="desc">Bender from Futurama, waving with three fingers: silver barrel body, antenna, half-lidded yellow eyes, tooth grille, ribbed limbs and a chest door. The preview and downloadable 3D model share one procedural solid. A subtle hover and antenna pulse stop when reduced motion is preferred.</desc>',
             '<defs><radialGradient id="glow"><stop stop-color="#69B9FF" stop-opacity=".14"/><stop offset="1" stop-color="#69B9FF" stop-opacity="0"/></radialGradient></defs>',
             '<style>.bender-hover{animation:bender-hover 7s ease-in-out infinite}.antenna-signal{animation:antenna-signal 3.5s ease-out infinite}@keyframes bender-hover{50%{transform:translateY(-4px)}}@keyframes antenna-signal{0%,100%{opacity:0}20%{opacity:.5}70%{opacity:0}}@media(prefers-reduced-motion:reduce){.bender-hover,.antenna-signal{animation:none}.antenna-signal{opacity:.2}}</style>',
             f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="#121A26" stroke="#29364B"/>',
             f'<ellipse cx="{mx}" cy="{my-150}" rx="{180 if mobile else 190}" ry="210" fill="url(#glow)"/>',
             '<g font-family="Segoe UI,Arial,sans-serif">']
    def text(x, y, value, size=20, color='#B8C6DB', weight=400):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>')
    text(28, 37, 'BENDER / OFF THE PAGE', 18 if mobile else 13, '#69B9FF', 500)
    text(27, 94 if mobile else 111, 'Built different.', 42, '#EFF4FC', 700)
    text(28, 134 if mobile else 156, 'A little attitude. A lot of metal.', 22 if mobile else 21)
    text(28, 174 if mobile else 209, 'ROTATE / ZOOM / KEEP', 18 if mobile else 14, '#43E6C5', 500)
    if not mobile:
        parts.append('<path d="M28 243H434" stroke="#29364B"/>')
        text(28, 276, 'FUTURAMA FAN ART / PROCEDURAL 3D', 12)
    text(28, h-25, 'OPEN THE STL / NATIVE GITHUB VIEWER', 16 if mobile else 12)
    parts.append(f'<ellipse cx="{mx}" cy="{my+4}" rx="{94 if mobile else 75}" ry="10" fill="#02060D" opacity=".65"/>')
    parts.append(f'<g class="bender-hover"><g transform="translate({mx} {my}) scale({scale})">')
    parts.append('<circle class="antenna-signal" cx="0" cy="-80" r="4.2" fill="none" stroke="#69B9FF" stroke-width=".3"/>')
    parts.append(f'<image x="-25" y="-89.5" width="50" height="92.5" href="data:image/png;base64,{model_png()}"/>')
    parts.append('</g></g></g></svg>')
    return apply_theme(''.join(parts))


def assets():
    return {'bender.stl': stl(), 'bender.svg': illustration(), 'bender-mobile.svg': illustration(True)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, content in assets().items():
        path = ROOT/'profile'/name
        raw = content.encode('utf-8') if isinstance(content, str) else content
        if args.check:
            if not path.exists() or path.read_bytes() != raw:
                parser.exit(1, 'Rebuild with python scripts/build_bender_collectible.py: '+name+'\n')
        else:
            path.write_bytes(raw)
    print(f'Verified watertight, connected Bender: {len(mesh()):,} triangles; desktop and mobile previews.')


if __name__ == '__main__':
    main()
