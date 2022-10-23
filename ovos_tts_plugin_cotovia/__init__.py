# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import shutil
import subprocess
from distutils.spawn import find_executable
from os import makedirs
from os.path import join
from tempfile import gettempdir

from ovos_plugin_manager.templates.tts import TTS, TTSValidator
from ovos_utils.log import LOG


class CotoviaTTSPlugin(TTS):
    """Interface to cotovia TTS."""

    def __init__(self, lang="es-gl", config=None):
        super(CotoviaTTSPlugin, self).__init__(
            lang, config, CotoviaTTSValidator(self), 'wav')
        self.pitch_scale_factor = self.config.get("pitch_scale_factor", 100)
        self.time_scale_factor = self.config.get("time_scale_factor", 100)
        self.data_path = self.config.get("data_path") or "/usr/share/cotovia/data"
        if self.voice == "default":
            self.voice = self.get_voices(self.data_path)[0]
        self.bin = self.config.get("bin") or find_executable("cotovia") or "/usr/bin/cotovia"
        if "gl" in lang:
            self.lang = "gl"
        else:
            self.lang = "es"

    @staticmethod
    def get_voices(data_path):
        if not os.path.isdir(data_path):
            raise RuntimeError("No cotovia voices found! did you install any?")
        return [f for f in os.listdir(data_path) if f != "lang"]

    def get_tts(self, sentence, wav_file, lang=None, voice=None,
                pitch_scale_factor=None, time_scale_factor=None):
        """Fetch tts audio using cotovia

        Arguments:
            sentence (str): Sentence to generate audio for
            wav_file (str): output file path
        Returns:
            Tuple ((str) written file, None)
        """
        # optional kwargs, OPM will send them if they are in message.data
        lang = lang or self.lang
        voice = voice or self.voice
        pitch = pitch_scale_factor or self.pitch_scale_factor
        ts = time_scale_factor or self.time_scale_factor

        if voice.lower() not in self.get_voices(self.data_path):
            LOG.warning(f"Unknown voice! using default {self.voice}")
            voice = self.voice

        # api wont let set filename only base folder!
        output_path = join(gettempdir(), "cotovia")
        makedirs(output_path, exist_ok=True)

        cmd = f'echo "{sentence}" | {self.bin} --voice={voice} --lang={lang} ' \
              f'--pitch-scale={pitch} --time-scale={ts} --wav-file-output ' \
              f'--output-dir={output_path} --data-dir={self.data_path}'
        subprocess.call(cmd, shell=True)
        shutil.move(f"{output_path}/default.wav", wav_file)

        return (wav_file, None)  # No phonemes

    @property
    def available_languages(self) -> set:
        """Return languages supported by this TTS implementation in this state
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            set: supported languages
        """
        return set(CotoviaTTSPluginConfig.keys())


class CotoviaTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(CotoviaTTSValidator, self).__init__(tts)

    def validate_lang(self):
        lang = self.tts.lang
        assert lang in ["es", "es-es", "es-gl", "gl"]

    def validate_connection(self):
        assert subprocess.call("{bin} -v".format(bin=self.tts.bin),
                               shell=True) == 1

    def get_tts_class(self):
        return CotoviaTTSPlugin


CotoviaTTSPluginConfig = {
    lang: [
        {"lang": lang, "voice": "iago",
         "meta": {"gender": "male", "display_name": f"Iago",
                  "offline": True, "priority": 60}},
        {"lang": lang, "voice": "sabela",
         "meta": {"gender": "female", "display_name": f"Sabela",
                  "offline": True, "priority": 55}}
    ] for lang in ["es-es", "es-gl"]
}

if __name__ == "__main__":
    tts = CotoviaTTSPlugin()
    tts.get_tts("hola mundo", "test.wav", voice="iago")
