# SPDX-License-Identifier: MIT
"""The World, in One Day — 22 November 2026. Offline, stdlib-only renderer."""
import json
import os
from pathlib import Path
from raster import Canvas, INK, PAPER
from illustrations import RED, TEAL, globe, treaty, ship, chip, storm, factory, homes, court, miniature

ROOT = Path(__file__).resolve().parent
MUTED = '#5b6c69'
RULE = '#b9c3b9'


def section(c,x,y,number,label):
    c.rect(x,y+3,23,19,RED)
    c.text(x+11.5,y+3,number,12,'bold',PAPER,'center')
    c.text(x+33,y+3,label,12,'bold',TEAL)


def render():
    c = Canvas()
    c.rect(0,0,1024,9,INK)
    c.text(36,26,'THE DAILY ATLAS',13,'bold',TEAL)
    c.text(988,26,'SUNDAY  /  GLOBAL EDITION',12,'bold',TEAL,'right')
    c.text(31,45,'The World,',64,'display')
    c.text(34,116,'in one day.',36,'serif')
    c.text(988,42,'22',72,'display',INK,'right')
    c.text(988,125,'NOVEMBER 2026',17,'bold',INK,'right')
    c.line([(36,173),(988,173)],INK,2)
    c.text(36,182,'CLIMATE  /  CONFLICT  /  SOCIETY  /  SPORT',11,'bold',MUTED)
    c.text(988,182,'7 STORIES. ONE PLANET.',11,'bold',MUTED,'right')
    # Lead: globally consequential negotiations, without overstating total collapse.
    c.rect(36,213,952,231,'#e3e9de')
    section(c,55,225,'01','ANTALYA, TURKEY  /  CLIMATE')
    c.text(55,258,'Climate deal fails',40,'display')
    c.text(55,309,'COP31 ends without an overarching pact',18,'bold')
    c.paragraph(55,345,'EU, UK and allies reject a text that omits fossil fuels. Other decisions pass, but the main deal has no consensus.',530,16,23)
    c.text(55,418,'THE GUARDIAN  /  22 NOV',11,'bold',MUTED)
    c.illustration(globe,747,329,86)
    c.illustration(treaty,834,277)
    c.text(747,419,'NO CONSENSUS',12,'bold',RED,'center')
    # Two major stories: Africa/Europe and AI's social consequences in Asia.
    section(c,36,462,'02','BENGHAZI, LIBYA  /  WAR')
    c.text(36,494,'Russian warship',26,'display')
    c.text(36,527,'sinks at port',26,'display')
    c.illustration(ship,390,487,.95)
    c.paragraph(36,571,'Suspected sea-drone strike hits the Merkury. Satellite imagery shows it largely sunk; no claim of responsibility.',445,16,23)
    c.text(36,671,'AL JAZEERA + THE GUARDIAN',11,'bold',MUTED)
    c.line([(510,464),(510,694)],RULE,1)
    section(c,536,462,'03','SOUTH KOREA  /  AI & EDUCATION')
    c.text(536,494,'Minister quits',26,'display')
    c.text(536,527,'over AI cheating',26,'display')
    c.illustration(chip,890,477)
    c.paragraph(536,571,'Choi Kyo-jin resigns over exam security after AI-assisted cheating fears triggered a last-minute crackdown.',442,16,23)
    c.text(536,671,'THE GUARDIAN / AFP / REUTERS',11,'bold',MUTED)
    c.line([(36,700),(988,700)],INK,1.5)
    # A three-column world brief, with specific actions and locations.
    section(c,36,715,'04','BRAZIL  /  EXTREME WEATHER')
    c.illustration(miniature,storm,259,755)
    c.text(36,752,'Storm toll',23,'display')
    c.text(36,781,'rises to five',23,'display')
    c.paragraph(36,822,'Sunday update: over 250 injured after Friday’s storm in Tupanciretã, Rio Grande do Sul.',283,15,21)
    c.text(36,909,'AFP / FRANCE 24',11,'bold',MUTED)
    c.line([(343,720),(343,931)],RULE,1)
    section(c,367,715,'05','BANGLADESH  /  LABOUR')
    c.illustration(miniature,factory,586,758)
    c.text(367,752,'Wage protests',23,'display')
    c.text(367,781,'halt factories',23,'display')
    c.paragraph(367,822,'Gazipur garment workers clash with police; tear gas used and highway traffic disrupted.',283,15,21)
    c.text(367,909,'THE BUSINESS STANDARD',11,'bold',MUTED)
    c.line([(675,720),(675,931)],RULE,1)
    section(c,698,715,'06','WEST BANK  /  VIOLENCE')
    c.illustration(miniature,homes,915,758)
    c.text(698,752,'Settler arson',23,'display')
    c.text(698,781,'draws rebuke',23,'display')
    c.paragraph(698,822,'Eisenkot condemns overnight attacks on Palestinian villages; homes and vehicles burned.',283,15,21)
    c.text(698,909,'THE GUARDIAN / REUTERS',11,'bold',MUTED)
    c.rect(36,936,952,62,INK)
    c.text(51,945,'07 / TURIN',11,'bold','#b8d0c2')
    c.text(51,966,'TENNIS',11,'bold','#b8d0c2')
    c.text(161,943,'Alcaraz wins his first ATP Finals',20,'display',PAPER)
    c.text(162,975,'Beats Zverev 6–2, 7–6 (9–7 tiebreak).  /  THE GUARDIAN',12,'sans',PAPER)
    c.illustration(court,876,940)
    c.text(36,1005,'22 NOV 2026  ·  Reports available at day’s end  ·  Illustrations are symbolic',11,'sans',MUTED)
    c.text(988,1005,'DAILY ATLAS / 01',11,'bold',TEAL,'right')
    return c


def main():
    canvas = render()
    out = Path(os.environ.get('MAKEFUN_OUTPUT_DIR','/output'))
    out.mkdir(parents=True,exist_ok=True)
    image = canvas.png()
    if len(image) > 1048576:
        raise ValueError('Image exceeds competition byte cap')
    (out/'entry.png').write_bytes(image)
    if os.environ.get('ATLAS_DEBUG'):
        (out/'layout.json').write_text(json.dumps(canvas.boxes,indent=2))
    print(f'Wrote {out / "entry.png"}: 1024x1024, {len(image)} bytes')


if __name__ == '__main__':
    main()
