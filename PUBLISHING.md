# Publish this collection manually

Recommended repository: **NunzioLangiulli/picard-toolkit**. Initial release tag: **v1.0.0**.

1. Publish `picard-bilingual-names` and `picard-earliest-compatible-release` first, following each project's PUBLISHING.md. Verify all five plugin links, then remove the temporary Publication status paragraph in this README once both new links work.
2. Create a public GitHub repository named `picard-toolkit`. Do not initialize an additional README, license or .gitignore.
3. Upload this folder's **contents** to the repository root using GitHub's upload interface. Include `scripts/`, `tests/`, README, LICENSE, changelog and guides. Do not upload `.git`, caches, source music or an extra enclosing folder.
4. Commit the upload. Open README and verify all eight script links and all five plugin links. Download a `.ptsp` using the raw download button and check that Picard imports it.
5. Optionally create a GitHub release tagged **v1.0.0** from the uploaded default branch. Users can download the whole repository ZIP; each script is also directly available under `scripts/`.
6. Set the repository description to: **Importable MusicBrainz Picard tagging scripts and links to Borunzio's independent genre, artwork and bilingual metadata plugins.** Suggested topics: `musicbrainz`, `picard`, `tagging`, `audio-metadata`, `scripts`.

Git is not required for these browser steps. Browser upload does not transfer local Git history or tags. The prepared local files do not publish or create repositories by themselves.

When updating packages, preserve their IDs and update the collection changelog. For new behavior, create a new release tag rather than moving a published one.
