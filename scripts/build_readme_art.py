"""Rebuild the README's cinematic covers from committed vectors and fonts."""
import argparse

from profile_cinematics import ROOT, hero_finish, portal
from profile_motion import animate_profile
from profile_studio import PROJECTS, hero, project
from profile_theme import apply_theme


def assets():
    result = {}
    for mobile in (False, True):
        suffix = '-mobile' if mobile else ''
        result['studio-orbit-hero'+suffix+'.svg'] = apply_theme(hero_finish(animate_profile(hero(mobile), 'hero', mobile), mobile))
        result['pixel-portal'+suffix+'.svg'] = portal(mobile)
        for item in PROJECTS:
            result['studio-'+item[0]+'-motion'+suffix+'.svg'] = apply_theme(animate_profile(project(item, mobile), item[0], mobile))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check committed artwork without modifying it')
    args = parser.parse_args()
    expected = assets()
    stale = []
    for name, source in expected.items():
        path = ROOT/'profile'/name
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != source:
                stale.append(name)
        else:
            path.write_text(source, encoding='utf-8')
    if stale:
        parser.exit(1, 'Rebuild with python3 scripts/build_readme_art.py: '+', '.join(stale)+'\n')
    print(('Verified' if args.check else 'Built') + f' {len(expected)} self-contained README covers.')


if __name__ == '__main__':
    main()
