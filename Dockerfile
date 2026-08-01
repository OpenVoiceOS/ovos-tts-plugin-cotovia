# Cotovia Galician/Spanish unit-selection TTS served through ovos-tts-server's
# ElevenLabs-compatible API. A self-contained, offline image: any client that speaks
# the ovos-tts-server / ElevenLabs API can hit it, and it can be A/B-tested against
# other ovos-tts-server voices by pointing at a different port.
#
# The cotovia synthesis binary ships inside the plugin wheel (bin/cotovia_<arch>), but
# get_tts also needs the Galician linguistic data and at least one voice under
# /usr/share/cotovia/data. Those are distributed as .deb packages on SourceForge (not
# in the Ubuntu/Debian apt repos), so they are downloaded and installed at build time.
# The image build therefore needs network access to SourceForge.
FROM python:3.11-slim

# curl to fetch the .deb packages; installing the cotovia .deb also pulls the binary's
# shared-library dependencies (libexpat1, libasound2, libstdc++6, ...).
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Cotovia executable + Galician linguistic data + the "iago" voice (the config default).
# The voice/lang data lands in /usr/share/cotovia/data, which the plugin reads.
# `apt-get install ./*.deb` resolves the debs' own dependencies from the apt repos.
RUN apt-get update \
    && base="https://sourceforge.net/projects/cotovia/files/Debian%20packages" \
    && for pkg in cotovia_0.5_amd64.deb cotovia-lang-gl_0.5_all.deb cotovia-voice-iago_0.5_all.deb; do \
         curl -fSL --retry 5 --retry-delay 5 -o "/tmp/$pkg" "$base/$pkg/download"; \
       done \
    && apt-get install -y --no-install-recommends \
         /tmp/cotovia_0.5_amd64.deb \
         /tmp/cotovia-lang-gl_0.5_all.deb \
         /tmp/cotovia-voice-iago_0.5_all.deb \
    && rm -f /tmp/*.deb \
    && rm -rf /var/lib/apt/lists/* \
    && ls /usr/share/cotovia/data

WORKDIR /app
COPY . /app

# the plugin + the OVOS TTS server. setuptools<81 keeps ovos-plugin-manager's
# pkg_resources usage working. cotovia emits WAV natively, so no ffmpeg transcode is
# needed; the alpha floor lets pip resolve the prerelease without --pre.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "setuptools<81" "." "ovos-tts-server>=1.13.5a1"

# Served voice/lang, overridable with the COTOVIA_VOICE / COTOVIA_LANG build args.
# iago is the only voice installed above; add other voice .debs to serve them.
ARG COTOVIA_VOICE=iago
ARG COTOVIA_LANG=gl-es
RUN useradd -m -u 1000 ovos \
    && mkdir -p /home/ovos/.config/mycroft \
    && printf '{\n  "lang": "%s",\n  "tts": {\n    "module": "ovos-tts-plugin-cotovia",\n    "ovos-tts-plugin-cotovia": {\n      "lang": "%s",\n      "voice": "%s"\n    }\n  }\n}\n' "${COTOVIA_LANG}" "${COTOVIA_LANG}" "${COTOVIA_VOICE}" \
        > /home/ovos/.config/mycroft/mycroft.conf \
    && chown -R 1000:1000 /home/ovos/.config
USER 1000

EXPOSE 9666
ENTRYPOINT ["ovos-tts-server", "--engine", "ovos-tts-plugin-cotovia", \
            "--host", "0.0.0.0", "--port", "9666", "--cache"]
