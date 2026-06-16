"""End-to-end TTS intelligibility test for ovos-tts-plugin-cotovia.

Synthesises a small set of phrases with the real plugin, transcribes the
rendered audio back with a reference STT and scores the round-trip with
WER/CER via ovoscope. Report-only by default (TTS_MAX_WER=1.0).
"""
import os
import json

from ovoscope.tts_intelligibility import score_tts_intelligibility

from ovos_tts_plugin_cotovia import CotoviaTTSPlugin

# Galician (gl) is the primary supported language for this engine.
LANG = "gl-es"
PHRASES = [
    "ola mundo",
    "que tal estas",
    "moitas grazas",
    "ata logo",
    "fai bo tempo hoxe",
]


def test_tts_intelligibility():
    tts = CotoviaTTSPlugin({"lang": LANG})
    report = score_tts_intelligibility(tts, PHRASES, lang=LANG, mode="playback")
    print("::TTS-INTELLIGIBILITY:: " + json.dumps(report.to_dict()))
    assert report.mean_wer <= float(os.environ.get("TTS_MAX_WER", "1.0"))
