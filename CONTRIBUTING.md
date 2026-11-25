# Contributing

Keep script comments and documentation in English. Report the script title, Picard version, relevant options, minimal original/new metadata and expected output. Remove private paths and do not upload audio files. Include a MusicBrainz link where it helps reproduce a problem.

Preserve package IDs for updates to the same script. Validate `.ptsp` packages with Picard's serializer and parser, and update examples, execution-order notes and regression tests when behavior changes. Test combined order as well as individual scripts. Do not describe metadata-only tests as a live audio-save verification.

Report plugin issues to the relevant linked plugin repository; this repository contains scripts and introductions only. Contributions are under the [MIT License](LICENSE).
