"""Validate the shipped packages using Picard 3.0.2's serializer and parser."""
from pathlib import Path
from types import SimpleNamespace
import unittest

from picard import config
from picard.metadata import Metadata, MultiMetadataProxy
from picard.script import ScriptParser
from picard.script.serializer import TaggingScriptInfo

config.config = SimpleNamespace(setting={})
ROOT = Path(__file__).resolve().parents[1]
ORDER = (
    'featuring-artist-formatter', 'album-artist-separator-formatter',
    'title-smart-capitalize', 'album-smart-capitalize',
    'album-edition-release-in-album-title', 'disc-subtitle-as-comment',
    'remove-disc-number-in-single-disc-albums', 'year-only-date',
)
PACKAGES = {
    name: TaggingScriptInfo.create_from_yaml(
        (ROOT / 'scripts' / (name + '.ptsp')).read_text(encoding='utf-8'),
        create_new_id=False,
    ) for name in ORDER
}


def apply(names, values, original=None):
    metadata = Metadata(values)
    context = MultiMetadataProxy(metadata, Metadata(original or {}))
    for name in names:
        ScriptParser().eval(PACKAGES[name]['script'], context)
    return metadata


class PackageTests(unittest.TestCase):
    def test_packages(self):
        self.assertEqual(len(list((ROOT / 'scripts').glob('*.ptsp'))), 8)
        self.assertEqual(len({p['id'] for p in PACKAGES.values()}), 8)
        for name, package in PACKAGES.items():
            with self.subTest(name=name):
                self.assertNotIn('\x00', package['script'])
                self.assertNotIn('\\u0000', package['script'])
                apply([name], {})

    def test_original_guest_and_current_priority(self):
        for token in ('feat', 'FEAT.', 'Ft', 'ft.', 'FEATURING'):
            with self.subTest(token=token):
                result = apply(ORDER[:1], {'title': 'Worm Mountain', 'artist': 'The Flaming Lips',
                    'albumartist': 'The Flaming Lips'}, {'title': f'Worm Mountain ({token} MGMT)'})
                self.assertEqual(result['title'], 'Worm Mountain')
                self.assertEqual(result.getall('artist'), ['The Flaming Lips', 'MGMT'])
        result = apply(ORDER[:1], {'title': 'Song', 'artists': ['Main', 'New Guest']},
                       {'title': 'Song (Feat Old Guest)'})
        self.assertEqual(result.getall('artist'), ['Main', 'New Guest'])

    def test_artist_separator(self):
        result = apply([ORDER[1]], {'albumartist': ['A', 'B'], 'artist': ['A', 'C']})
        self.assertEqual(result['albumartist'], 'A & B')
        self.assertEqual(result.getall('artist'), ['A', 'C'])

    def test_capitalization_scope(self):
        for name, tag, other in ((ORDER[2], 'title', 'album'), (ORDER[3], 'album', 'title')):
            for source, expected in (('LIVE IN USA', 'Live In Usa'), ('live in USA', 'Live In USA')):
                result = apply([name], {tag: source, other: 'UNCHANGED'})
                self.assertEqual(result[tag], expected)
                self.assertEqual(result[other], 'UNCHANGED')

    def test_edition_idempotence(self):
        result = apply([ORDER[4]] * 2, {'album': 'Album', '~releasecomment': 'DELUXE USA EDITION'})
        self.assertEqual(result['album'], 'Album (Deluxe Usa Edition)')

    def test_disc_subtitle_and_cleanup(self):
        for count in ('1', '2'):
            result = apply(ORDER[5:7], {'totaldiscs': count, 'discnumber': '1',
                           'discsubtitle': 'Bonus Disc', 'comment': 'Existing'})
            self.assertEqual(result['comment'], 'Bonus Disc' if count == '2' else 'Existing')
            self.assertNotIn('discsubtitle', result)
            self.assertEqual('discnumber' in result, count == '2')
            self.assertEqual('totaldiscs' in result, count == '2')

    def test_year(self):
        self.assertEqual(apply([ORDER[7]], {'date': '2009-10-13'})['date'], '2009')
        self.assertFalse(apply([ORDER[7]], {})['date'])

    def test_combined_order(self):
        result = apply(ORDER, {'title': 'WORM MOUNTAIN', 'artists': ['The Flaming Lips'],
            'albumartists': ['The Flaming Lips'], 'album': 'EMBRYONIC',
            '~releasecomment': 'deluxe edition', 'date': '2009-10-13',
            'totaldiscs': '1', 'discnumber': '1'}, {'title': 'Worm Mountain (Feat MGMT)'})
        self.assertEqual(result['title'], 'Worm Mountain')
        self.assertEqual(result['album'], 'Embryonic (Deluxe Edition)')
        self.assertEqual(result.getall('artist'), ['The Flaming Lips', 'MGMT'])
        self.assertEqual(result['date'], '2009')
        for tag in ('artists', 'albumartists', 'discnumber', 'totaldiscs'):
            self.assertNotIn(tag, result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
