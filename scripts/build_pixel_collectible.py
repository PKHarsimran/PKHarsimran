"""Build Pocket Pixel's closed voxel mesh and matching isometric README art."""
import argparse
from collections import defaultdict
from html import escape
from pathlib import Path
import struct

from profile_theme import apply_theme

ROOT=Path(__file__).resolve().parents[1]
SPRITE=(
    '........##........',
    '........##........',
    '........##........',
    '....##########....',
    '...############...',
    '..##############..',
    '.################.',
    '##################',
    '##################',
    '##################',
    '.################.',
    '..##############..',
    '...############...',
    '....##########....',
    '....####..####....',
    '....####..####....',
    '....####..####....',
    '....####..####....',
)
FACES=(
    ((-1,0,0),((0,0,0),(0,0,1),(0,1,1),(0,1,0))),
    ((1,0,0),((1,0,0),(1,1,0),(1,1,1),(1,0,1))),
    ((0,-1,0),((0,0,0),(1,0,0),(1,0,1),(0,0,1))),
    ((0,1,0),((0,1,0),(0,1,1),(1,1,1),(1,1,0))),
    ((0,0,-1),((0,0,0),(0,1,0),(1,1,0),(1,0,0))),
    ((0,0,1),((0,0,1),(1,0,1),(1,1,1),(0,1,1))),
)


def eyes(x,row):
    return x in (5,6,11,12) and 6<=row<=8


def voxels():
    result=set()
    for row,line in enumerate(SPRITE):
        for x,cell in enumerate(line):
            if cell!='#':continue
            for depth in range(4):
                recess=(4<=x<=13 and 6<=row<=9 and not eyes(x,row)) or (x in (8,9) and row==11)
                if depth==0 and recess:continue
                result.add((x,depth,len(SPRITE)-1-row))
    return result


def skin():
    solid=voxels()
    for x,y,z in sorted(solid):
        for normal,corners in FACES:
            if (x+normal[0],y+normal[1],z+normal[2]) in solid:continue
            yield normal,tuple((x+a,y+b,z+c) for a,b,c in corners),(x,y,z)


def triangles():
    for normal,corners,_ in skin():
        for indices in ((0,1,2),(0,2,3)):
            yield normal,tuple(((corners[i][0]-9)*2.5,corners[i][1]*2.5,corners[i][2]*2.5) for i in indices)


def verify_mesh(facets):
    """Reject holes, inconsistent winding, disconnected shells and zero volume."""
    edges=defaultdict(list)
    volume=0
    for index,(_,points) in enumerate(facets):
        a,b,c=points
        volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
        for first,last in ((a,b),(b,c),(c,a)):
            edges[tuple(sorted((first,last)))].append((index,first,last))
    if not facets or volume<=0:raise ValueError('Pixel must enclose a positive volume')
    neighbours=defaultdict(set)
    for shared in edges.values():
        if len(shared)!=2 or shared[0][1:]!=shared[1][1:][::-1]:
            raise ValueError('Pixel must be watertight with consistent face winding')
        a,b=shared[0][0],shared[1][0]
        neighbours[a].add(b);neighbours[b].add(a)
    reached=set();pending=[0]
    while pending:
        face=pending.pop()
        if face in reached:continue
        reached.add(face);pending.extend(neighbours[face]-reached)
    if len(reached)!=len(facets):raise ValueError('Pixel must be one connected shell')


def stl():
    facets=list(triangles())
    verify_mesh(facets)
    data=bytearray(b'Pocket Pixel / repository-owned voxel keepsake'.ljust(80,b' '))
    data.extend(struct.pack('<I',len(facets)))
    for normal,points in facets:
        data.extend(struct.pack('<12fH',*normal,*(v for point in points for v in point),0))
    return bytes(data)


def material(normal,origin):
    x,y,z=origin;row=len(SPRITE)-1-z
    if row<3:return '#F36BAA'
    if y==0 and eyes(x,row):return '#43E6C5'
    if normal==(0,-1,0) and y>0:return '#172139'
    return '#C9B9FF' if normal==(0,0,1) else '#7860AA' if normal==(1,0,0) else '#A995FF'


def illustration(mobile=False):
    w,h=(600,460) if mobile else (1000,290)
    model_x,model_y,scale=(300,400,9) if mobile else (782,238,10)
    def project(point):
        x,y,z=point;x-=9
        return (model_x+(x+y)*.866*scale,model_y+((x-y)*.45-z)*scale)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
           '<title id="title">Pocket Pixel / another dimension</title><desc id="desc">An isometric preview of the same voxel mesh available as an STL file. Pixel has a violet body, a pink antenna, and raised mint eyes inside a recessed face. Open the model in GitHub to rotate and zoom. The preview gently floats; reduced motion keeps it still.</desc>',
           '<style>.pocket-float{animation:pocket-float 8s ease-in-out infinite}@keyframes pocket-float{50%{transform:translateY(-5px)}}@media(prefers-reduced-motion:reduce){.pocket-float{animation:none}}</style>',
           f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="#121A26" stroke="#29364B"/>',
           '<g font-family="Segoe UI,Arial,sans-serif">']
    def text(x,y,value,size=20,color='#B8C6DB',weight=400):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>')
    text(28,35,'PIXEL / POCKET EDITION',18 if mobile else 13,'#A995FF',500)
    text(27,89,'Another dimension.',38,'#EFF4FC',700)
    text(28,130,'A tiny voxel bot, ready to turn.',22 if mobile else 20)
    text(28,170,'ROTATE / ZOOM / KEEP',18 if mobile else 14,'#43E6C5',500)
    text(28,h-24,'OPEN THE STL / NATIVE GITHUB VIEWER',16 if mobile else 12)
    parts.append(f'<ellipse cx="{model_x+5}" cy="{model_y+12}" rx="100" ry="15" fill="#A995FF" opacity=".08"/>')
    faces=[item for item in skin() if item[0] in ((0,-1,0),(1,0,0),(0,0,1))]
    faces.sort(key=lambda item:sum(p[0]-p[1]+p[2] for p in item[1])/4)
    parts.append('<g class="pocket-float">')
    for normal,corners,origin in faces:
        points=' '.join(f'{a:.1f},{b:.1f}' for a,b in map(project,corners))
        color=material(normal,origin)
        parts.append(f'<polygon points="{points}" fill="{color}" stroke="{color}" stroke-width=".3"/>')
    parts.extend(['</g></g></svg>'])
    return apply_theme(''.join(parts))


def assets():
    return {'pixel-pocket.stl':stl(),'pixel-pocket.svg':illustration(),
            'pixel-pocket-mobile.svg':illustration(True)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    for name,content in assets().items():
        path=ROOT/'profile'/name
        raw=content.encode('utf-8') if isinstance(content,str) else content
        if args.check:
            if not path.exists() or path.read_bytes()!=raw:
                parser.exit(1,'Rebuild with python scripts/build_pixel_collectible.py: '+name+'\n')
        else:path.write_bytes(raw)
    print('Verified closed, connected Pocket Pixel mesh and both preview layouts.')


if __name__=='__main__':main()
