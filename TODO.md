# TODO

## Open issues

- [ ] #17 Dependency Dashboard (Renovate bot)

## Gaps

- [ ] No test suite (no `tests/` directory, no test command) — add unit tests covering language gating, voice fallback, and command construction.
- [ ] Migrate CI to `OpenVoiceOS/gh-automations` reusable workflows at `@dev`. Current workflows reference `TigreGotico/gh-automations@master` and a hand-rolled `publish_pypi`/`propose_release`.
- [ ] Missing standard gh-automations workflows: `coverage`, `license-check`, and OPM `opm-check` (this declares a `mycroft.plugin.tts` entry point).
- [ ] `build_tests.yml` has broken YAML indentation in the "Build Source Packages" step (`run:` nested under the step name) and installs irrelevant heavy system deps (swig, libfann, portaudio) for a thin CLI wrapper.
- [ ] Committed scratch/build artifact: `ovos_tts_plugin_cotovia.egg-info/` is tracked in the repo.
- [ ] Stale packaging in `setup.py`: Python 2.7 and ancient 3.x classifiers.
- [ ] Shell-injection / WAV race in `get_tts()` (see AGENTS.md Gotchas) — harden command construction and output path handling.
- [ ] Advertised `available_languages` (`es-es`/`es-gl`) do not match accepted runtime codes (`es`/`gl`); reconcile language tags.

## Code TODOs

None found.
