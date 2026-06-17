# ovos-tts-plugin-cotovia

OVOS TTS plugin wrapping the Cotovia unit-selection synthesizer for Galician (`gl`) and Spanish (`es`).

## Setup

```bash
pip install ovos-tts-plugin-cotovia
```

The plugin shells out to the `cotovia` binary. It is not bundled by pip: install the system packages (Debian `.deb` from SourceForge, or Arch via `debtap`) plus at least one voice and the `lang` data. The plugin falls back to a bundled binary at `ovos_tts_plugin_cotovia/bin/cotovia_<machine>` (x86_64, aarch64) if `cotovia` is not on PATH, then to `/usr/bin/cotovia`. Voice/lang data is expected at `data_path` (default `/usr/share/cotovia/data`).

## Test

No test suite exists. There is no `tests/` directory and no runnable test command. A manual smoke check is the `__main__` block in `ovos_tts_plugin_cotovia/__init__.py` (requires the binary + voices installed).

## Lint/Typecheck

None configured.

## Layout

- `ovos_tts_plugin_cotovia/__init__.py` — `CotoviaTTSPlugin` (subclass of `ovos_plugin_manager.templates.tts.TTS`) and the `CotoviaTTSPluginConfig` dict. `get_tts()` pipes the sentence through the `cotovia` CLI and moves the produced WAV to the requested path.
- `ovos_tts_plugin_cotovia/bin/` — committed prebuilt `cotovia` binaries for x86_64 and aarch64.
- `ovos_tts_plugin_cotovia/data/lang/{gl,es}/` — committed linguistic data (n-grams, lexicons) for both languages.
- `ovos_tts_plugin_cotovia/version.py` — version constants (do not edit).
- `setup.py` — packaging; `requirements.txt` — single dep `ovos-plugin-manager`.

Entry-point group: **`mycroft.plugin.tts`** (OPM TTS plugin), plus `mycroft.plugin.tts.config` for the config dict. Class: `CotoviaTTSPlugin`.

## Conventions

- Branches: work on `dev`, stable is `master`. NEVER use `main`.
- Never edit `version.py`; gh-automations bumps semver from conventional-commit prefixes (`feat:`, `fix:`, `feat!:`).
- New repos private by default.
- Commit identity: `JarbasAi <jarbasai@mailfence.com>`.
- CI is provided by reusable workflows from `OpenVoiceOS/gh-automations`; reference them at `@dev`.
- No Neon / `neon-*` references.
- No meta-commentary (no history, no dates) in code, docs, commits, or PRs.

## Gotchas

- `get_tts()` builds the command with `subprocess.call(cmd, shell=True)` interpolating the raw `sentence` into a shell string — shell-injection sensitive; sentences with quotes/backticks/`$` break or misbehave.
- The Cotovia CLI cannot name its output file; it always writes `default.wav` into `--output-dir`, which the plugin then `shutil.move`s. Concurrent calls share `gettempdir()/cotovia/default.wav` and can race.
- `available_languages` returns `es-es`/`es-gl` (the keys of `CotoviaTTSPluginConfig`), but the runtime language gate accepts only the base codes `es`/`gl`; advertised vs. accepted language tags are inconsistent.
- The default config uses `lang: "gl-es"`, an unusual composite tag; only the part before `-` is used.
- `setup.py` classifiers still list Python 2.7 and very old 3.x; packaging is stale.
- `setup.py` `url`/Homepage already points at `OpenVoiceOS/ovos-tts-plugin-cotovia` (correct), but release workflows reference `TigreGotico/gh-automations` rather than `OpenVoiceOS/gh-automations`.
