## Description

This is the OVOS TTS plugin for [Cotovia TTS](http://gtm.uvigo.es/cotovia).

Cotovia is a unit-selection text-to-speech system. It builds the speech signal
by joining prerecorded segments. Cotovia determines the sequence of sounds,
their intonation, and their duration from the input text. It considers several
intonation contours in parallel, and for each one it selects a sequence of
speech units. It picks the final intonation contour based on how well the
selected speech units fit together.

### Voices

Two Galician voices are available on SourceForge. These voices also work for
Spanish, with little distortion, because Spanish phonemes are a subset of
Galician phonemes. The nicknames of the two speakers are Iago and Sabela.
Cotovia offers three voice options:

* `iago`: a Galician male speaker, with 80 minutes of recording. It was
  Cotovia's first voice, so its quality is limited by the short recording
  time.
* `sabela-large`: a Galician female speaker, with 14.5 hours of recording. Use
  this voice for the highest quality speech when execution time does not
  matter.
* `sabela`: the default speaker. It uses a subset of Sabela's recordings
  (about 4 hours), which balances quality against execution time.

## Install

Install the plugin.

```bash
pip install ovos-tts-plugin-cotovia
```

Then download and install [Cotovia](https://sourceforge.net/projects/cotovia/files/Debian%20packages/).

### Debian

To run Cotovia, install these packages:

    cotovia_0.5_amd64.deb          --- Cotovia executable
    cotovia-lang-gl_0.5_all.deb    --- Galician linguistic data
    cotovia-lang-es_0.5_all.deb    --- Spanish linguistic data

Also install at least one voice:

    cotovia-voice-iago_0.5_all.deb
    cotovia-voice-sabela-large_0.5_all.deb
    cotovia-voice-sabela_0.5_all.deb

### Arch

Arch Linux users can find packages converted with `debtap` on the
[releases page](https://github.com/OpenVoiceOS/ovos-tts-plugin-cotovia/releases/tag/0.4.1).

```bash
sudo pacman -U /home/miro/Transferências/cotovia-0.5-1-x86_64.pkg.tar.zst
sudo pacman -U /home/miro/Transferências/cotovia-lang-es-0.5-1-any.pkg.tar.zst
sudo pacman -U /home/miro/Transferências/cotovia-lang-gl-0.5-1-any.pkg.tar.zst
sudo pacman -U /home/miro/Transferências/cotovia-voice-iago-0.5-1-any.pkg.tar.zst
sudo pacman -U /home/miro/Transferências/cotovia-voice-sabela-0.5-1-any.pkg.tar.zst
sudo pacman -U /home/miro/Transferências/cotovia-voice-sabela-large-0.5-1-any.pkg.tar.zst
```

If you do not use `debtap` packages, see this guide on
[how to install a .deb package in Arch Linux](https://www.baeldung.com/linux/arch-install-deb-package).

## Configuration

```json
  "tts": {
    "module": "ovos-tts-plugin-cotovia",
    "ovos-tts-plugin-cotovia": {
      "voice": "iago"
    }
  }
```

### Advanced config

You can set these additional parameters:

- `lang`: `gl` for Galician or `es` for Spanish.
- `voice`: `iago` or `sabela`.
- `pitch_scale_factor`: changes pitch (default `100`).
- `time_scale_factor`: changes speed (default `100`).
- `bin`: path to the executable (default `/usr/bin/cotovia`).

```json
  "tts": {
    "module": "ovos-tts-plugin-cotovia",
    "ovos-tts-plugin-cotovia": {
      "voice": "sabela",
      "lang": "es",
      "pitch_scale_factor": 80,
      "time_scale_factor": 80,
      "bin": "/usr/bin/cotovia"
    }
  }
```

## Docker (ovos-tts-server)

A container image runs the plugin as an
[`ovos-tts-server`](https://github.com/OpenVoiceOS/ovos-tts-server) (ElevenLabs-compatible
API). CI builds and pushes this image to GHCR on every push to `dev` or `master`.

```bash
docker run -p 9666:9666 ghcr.io/openvoiceos/ovos-tts-plugin-cotovia:latest
curl "http://localhost:9666/synthesize/ola%20mundo?lang=gl" --output ola.wav
```

The image bundles the Cotovia binary from the wheel. At build time, it also
downloads the Galician linguistic data and the `iago` voice from SourceForge,
into `/usr/share/cotovia/data`. This makes the running container fully offline.
The build args `COTOVIA_VOICE` (default `iago`) and `COTOVIA_LANG` (default
`gl-es`) bake the served voice and language into the image. To serve `sabela`,
add its `.deb` package to the Dockerfile and rebuild. See the bundled
`docker-compose.yml` for an example.

## Related projects

- [OpenVoiceOS/ovos-tts-server](https://github.com/OpenVoiceOS/ovos-tts-server) — serves this plugin over an ElevenLabs-compatible HTTP API.

## License

Apache-2.0. See [LICENSE](LICENSE).
