# MusicBrainz Picard Toolkit

Importable tagging scripts and a directory of independent plugins for MusicBrainz Picard: consistent artist credits, clean titles, album editions, disc metadata, genres and cover-art comparison.

**Author:** Borunzio · **Collection version:** 1.0.0 · **License:** MIT

**Compatibility target:** MusicBrainz Picard 3.0.2

The eight `.ptsp` packages in this repository are tagging scripts. Install the linked Python plugins separately from their own repositories. No Python installation is needed to import these scripts into Picard.

## Import the scripts

1. Download this repository with **Code → Download ZIP** and extract it, or download individual `.ptsp` files from the table below using GitHub's raw download button.
2. Open **Options → Scripting** in Picard and use **Import** to select a `.ptsp` file. Repeat for the scripts you want, enable them and arrange them in the order below.
3. Save the options, run Lookup or refresh the matched album, review the new tags, then save your audio files normally.

Import these under **Scripting**, not File Naming and not Plugins. Disable older copies of the same scripts to avoid running duplicate versions. Import may give a script a new internal ID; importing again is not guaranteed to update an existing copy.

## Scripts and recommended order

| Order | Script | What it does |
| --- | --- | --- |
| 1 | [Featuring Artist Formatter](scripts/featuring-artist-formatter.ptsp) | Moves explicit featured guests from titles into artist values, prioritizes current credits, and can recover guests from the original file title when available. |
| 2 | [Album Artist Separator Formatter](scripts/album-artist-separator-formatter.ptsp) | Joins album artists with ` & ` while leaving track artist formatting unchanged. |
| 3 | [Title Smart Capitalize](scripts/title-smart-capitalize.ptsp) | Capitalizes track titles, preserving existing uppercase letters unless the whole title is uppercase. |
| 4 | [Album Smart Capitalize](scripts/album-smart-capitalize.ptsp) | Applies the same capitalization policy to the album title only. |
| 5 | [Album Edition/Release in Album Title](scripts/album-edition-release-in-album-title.ptsp) | Appends the matched release's disambiguation comment in parentheses, with capitalization and duplicate checking. |
| 6 | [Disc Subtitle as Comment](scripts/disc-subtitle-as-comment.ptsp) | Copies a named disc's subtitle into `comment` for multi-disc albums, then removes `discsubtitle`. |
| 7 | [Remove Disc Number In Single Disk Albums](scripts/remove-disc-number-in-single-disc-albums.ptsp) | Removes `discnumber` and `totaldiscs` when `totaldiscs` is exactly 1. |
| 8 | [Year Only Date](scripts/year-only-date.ptsp) | Keeps the first four characters of a populated `date` tag. |

Featuring must precede the album artist separator because it can copy plural album artist values back into `albumartist`. Album capitalization precedes edition formatting. Disc subtitles are read before disc-number cleanup. The scripts are optional; this order describes the complete set.

## Behavior and limits

### Artist credits and featuring

Current `artists`, hidden Keep Only Tags artists, `artist` and `albumartist` are consulted in that order. Album artist plural values are read before being removed. The result is a proper multivalue `artist` tag; `; ` is its readable representation, not necessarily a literal storage separator in every audio format. Album artists are formatted separately with ` & `.

`feat`, `feat.`, `ft`, `ft.` and `featuring` are recognized case-insensitively. For example, `Song (FEAT Guest)` becomes title `Song` with the guest added to `artist`. The supplied pattern requires whitespace before the credit and supports round parentheses. `Song(Feat Guest)` and `Song [Feat Guest]` are not covered. Duplicate removal uses Picard's value matching, not artist-identity or alias resolution.

The original title is consulted only when current credits do not already identify guests: the new list has at most one artist or matches the album artist list, and no new featuring expression was found. Example: original `Worm Mountain (Feat MGMT)`, new title `Worm Mountain` and new artist `The Flaming Lips` can produce `The Flaming Lips; MGMT` without restoring the old title or main artist spelling.

In **Picard 3.0.2**, separate original-file metadata is exposed during file matching through the **Clear existing tags** branch. Otherwise `$get_original(title)` can resolve to the current title. Seeing the old title in the Original Value column does not establish that a script can read it. This collection does not change that global setting. The fallback must run in a file context; album-only evaluation has no individual original title.

### Capitalization

`BACK IN BLACK` becomes `Back In Black`; `live in USA` becomes `Live In USA`. A fully uppercase `LIVE IN USA` becomes `Live In Usa`, because the whole value is lowercased first. Correct such acronym exceptions manually. This is simple word capitalization, not language-aware editorial title casing.

### Edition notes

`_releasecomment` is MusicBrainz's release disambiguation comment. It may contain an edition name, but also a country, pressing detail or year. The script appends the complete comment; it does not prove that it is a deluxe-edition label or translate it. It handles a simple final parenthesized suffix and avoids an already present identical parenthesized comment ignoring case. Nested parentheses and multiple unrelated suffixes are not semantically merged.

### Disc metadata and dates

Disc Subtitle as Comment overwrites an existing `comment` only when the album has more than one disc and a subtitle is available. Otherwise it leaves the comment alone. It always removes `discsubtitle` after reading it, and can use `_ko_discsubtitle` when Keep Only Tags supplied that hidden value. It does not infer disc names.

Disc-number cleanup applies only to an explicit `totaldiscs = 1`; missing totals are not guessed. Year Only Date truncates an existing date, assuming a year-first value; it does not validate arbitrary text, change `originaldate` or select a different release.

## Independent plugins

Each plugin has its own repository, installation, options, version and detailed documentation. This repository does not bundle their source code.

| Plugin | Purpose |
| --- | --- |
| [Advanced Genre Mapper](https://github.com/NunzioLangiulli/picard-advanced-genre-mapper) | Normalize genre spellings, apply a common album genre list and compare available genre sources. |
| [Cover Art From Hidden Tags](https://github.com/NunzioLangiulli/picard-cover-art-from-hidden-tags) | Retrieve Cover Art Archive artwork using hidden MusicBrainz IDs retained by Keep Only Tags. |
| [Album Cover Compare](https://github.com/NunzioLangiulli/picard-album-cover-compare) | Compare embedded, local and online cover candidates and choose an album front image. |
| [Bilingual Names](https://github.com/NunzioLangiulli/picard-bilingual-names) | Format artists, albums and compatible translated track titles in two languages. Independent separators; English is the new-installation track-language default. |
| [Earliest Compatible Release](https://github.com/NunzioLangiulli/picard-earliest-compatible-release) | Prefer the oldest compatible official edition after the initial match, while respecting later manual release selections. |

**Publication status:** the first three links were verified public during preparation. Bilingual Names and Earliest Compatible Release are prepared publication targets; their links become active after those repositories are created. See [PUBLISHING.md](PUBLISHING.md).

These scripts work without the plugins. Keep Only Tags is optional and is not distributed here; the scripts can read its hidden variables when supplied. For an enabled allowlist, retain the final tags you want to save: `albumartist`, `album`, `artist`, `title`, `date`, `discnumber`, `totaldiscs` and `comment` as applicable. Plural artist tags are consumed and removed by the featuring script.

Bilingual Names runs after tagging scripts and may replace display names/titles with its configured output, preserving alias spelling. Earliest Compatible Release reloads the chosen edition through Picard's normal processing. Cover-art plugins retain their separately documented save protections. Consult the individual READMEs for interactions and limits.

## Validation and provenance

The packages were prepared from the owner's eight exported `.ptsp` files. Titles and IDs were retained; filenames were made suitable for repository links. A stray trailing `\u0000` artifact was removed from Album Artist Separator Formatter. The other script bodies retain their supplied behavior. The original files were not modified.

`tests/test_scripts.py` loads the packages with Picard's serializer and evaluates them using its real script parser, including the combined recommended order. These are metadata-only tests, not a live application or audio-save certification.

To run development checks, make Picard 3.0.2 and its Python dependencies importable, then run:

```sh
python -B tests/test_scripts.py
```

## License and feedback

Released under the [MIT License](LICENSE), author Borunzio. Independent community tools, not official MusicBrainz plugins. See [CONTRIBUTING.md](CONTRIBUTING.md) for issue-report details and [CHANGELOG.md](CHANGELOG.md) for changes.
