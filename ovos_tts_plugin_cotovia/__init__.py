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
from ovos_plugin_manager.templates.tts import TTS, TTSValidator
import subprocess
from tempfile import gettempdir
from os.path import join, isdir
from os import makedirs


class CotoviaTTSPlugin(TTS):
    """Interface to cotovia TTS."""
    def __init__(self, lang="es-gl", config=None):
        super(CotoviaTTSPlugin, self).__init__(
            lang, config, CotoviaTTSValidator(self), 'wav')
        self.pitch_scale_factor = config.get("pitch_scale_factor", 100)
        self.time_scale_factor = config.get("time_scale_factor", 100)
        self.voice = config.get("voice", "iago")
        self.bin = config.get("bin", "/usr/bin/cotovia")
        if "gl" in lang:
            self.lang = "gl"
        else:
            self.lang = "es"
        # stupid api!
        self.output_path = join(gettempdir(), "cotovia")
        if not isdir(self.output_path):
            makedirs(self.output_path)

    def get_tts(self, sentence, wav_file):
        """Fetch tts audio using cotovia

        Arguments:
            sentence (str): Sentence to generate audio for
            wav_file (str): output file path
        Returns:
            Tuple ((str) written file, None)
        """

        cmd = 'echo "{sentence}" | {bin} --voice={voice} --lang={lang} ' \
              '--pitch-scale={pitch} --time-scale={ts} --wav-file-output ' \
              '--output-dir={p} '

        subprocess.call(cmd.format(voice=self.voice, lang=self.lang,
                                   sentence=sentence,
                                   p=self.output_path,
                                   bin=self.bin,
                                   pitch=self.pitch_scale_factor,
                                   ts=self.time_scale_factor),
                        shell=True)
        # stupid api!
        with open(join(self.output_path, "default.wav"), "rb") as f:
            audio_data = f.read()
        with open(wav_file, "wb") as f:
            f.write(audio_data)

        return (wav_file, None)  # No phonemes


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
