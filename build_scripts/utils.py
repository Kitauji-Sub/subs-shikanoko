import os
import shutil
import json
import requests
from requests.exceptions import RequestException
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import ass
import subdigest
import config

class CallbackRetry(Retry):
    def __init__(self, *args, **kwargs):
        self._callback = kwargs.pop('callback', None)
        super(CallbackRetry, self).__init__(*args, **kwargs)
    def new(self, **kw):
        # pass along the subclass additional information when creating
        # a new instance.
        kw['callback'] = self._callback
        return super(CallbackRetry, self).new(**kw)
    def increment(self, method, url, *args, **kwargs):
        if self._callback:
            try:
                self._callback(url)
            except Exception:
                print('Callback raised an exception, ignoring')
        return super(CallbackRetry, self).increment(method, url, *args, **kwargs)

class SubtitleProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def replace_fonts(self, text, replacements):
        for old_font, new_font in replacements.items():
            text = text.replace(old_font, new_font)
        return text

    def cleanup_ass_file(self):
        with open(self.input_file, encoding='utf-8-sig', mode='r') as f:
            print(f"Cleaning file {self.input_file} ...")
            subs = subdigest.Subtitles(ass.parse(f), "s")
            subs.selection_set("effect", "fx").remove_selected()

            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            with open(self.output_file, encoding='utf-8-sig', mode='w+') as f_out:
                subs.dump_file(f_out)

    def traditionalize_text(self, input_text, user_pre_replace="", user_protect_replace="", timeout=10, max_tries=5):
        def retry_callback(url):
            print(f"Retrying for {url}...")

        def create_session(retries=3, backoff_factor=1, status_forcelist=[500, 502, 504, 429]):
            session = requests.Session()
            retry = CallbackRetry(
                total=retries,
                backoff_factor=backoff_factor,
                status_forcelist=status_forcelist,
                respect_retry_after_header=True,
                callback=retry_callback
            )

            adapter = HTTPAdapter(max_retries=retry)
            session.mount("https://", adapter)
            return session

        def send_request(url, data, timeout, max_tries):
            session = create_session(retries=max_tries)
            try:
                response = session.post(url, data=data, timeout=timeout)
                response.raise_for_status()
                result = response.json()
                if "data" in result and "text" in result["data"]:
                    return result["data"]["text"]
                else:
                    raise Exception("Error: Unexpected response format")
            except RequestException as e:
                print(f"Request failed: {e}")

            raise Exception("Error: Maximum number of tries exceeded")

        url = "https://api.zhconvert.org/convert"
        data = {
            "text": input_text,
            "converter": "Taiwan",
            "userPreReplace": user_pre_replace,
            "userProtectReplace": user_protect_replace
        }

        return send_request(url, data, timeout, max_tries)

    def traditionalize_ass(self, user_pre_replace="", user_protect_replace=""):
        with open(self.input_file, encoding='utf-8-sig', mode='r') as f:
            doc = ass.parse(f)
            texts_and_names = []
            temp_texts_names = [[event.text, event.name] for event in doc.events]

            print(f"Traditionalizing {self.input_file}")
            for i in range(0, len(temp_texts_names), 50):
                print(f"Traditionalizing line {i} to {i+50}...")
                slice = temp_texts_names[i:i+50]
                # replace fonts before submitting to zhconvert
                for item in slice:
                    item[0] = self.replace_fonts(item[0], config.font_replacements)
                slice = json.dumps(slice, ensure_ascii=False)
                traditionalized_slice = self.traditionalize_text(slice, user_pre_replace, user_protect_replace)
                texts_and_names += json.loads(traditionalized_slice)

            for i, (text, name) in enumerate(texts_and_names):
                doc.events[i].text = text
                doc.events[i].name = name
                if doc.events[i].effect.startswith("import"):
                    doc.events[i].text = doc.events[i].text.replace(".ass", "_tc.ass").replace("_sc_tc.ass", "_tc.ass")

            for style in doc.styles:
                if style.fontname == config.zhs_fontname:
                    style.fontsize = str(int(style.fontsize) * 0.8)
                    style.bold = "0"
                style.fontname = self.replace_fonts(style.fontname, config.font_replacements)

            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            with open(self.output_file, encoding='utf-8-sig', mode='w+') as f_out:
                doc.dump_file(f_out)

class FileManager:
    @staticmethod
    def traverse_files(folder_path):
        build_dir = os.path.join(folder_path, 'build')
        if os.path.exists(build_dir):
            print("Clean old build dirs...")
            shutil.rmtree(build_dir)

        for root, dirs, files in os.walk(folder_path):
            # Skip movies folder
            if "Movies" in root:
                continue
            for file in files:
                if file.endswith(".ass") and not file.endswith("_tc.ass"):
                    input_file = os.path.join(root, file)
                    output_file = os.path.join(build_dir, os.path.relpath(input_file, folder_path))
                    if file.endswith("_sc.ass"):
                        output_tc_file = os.path.join(build_dir, os.path.splitext(os.path.relpath(input_file, folder_path))[0].replace("_sc", "_tc") + ".ass")
                    else:
                        output_tc_file = os.path.join(build_dir, os.path.splitext(os.path.relpath(input_file, folder_path))[0] + "_tc.ass")

                    print(f'Preprocessing {input_file}...')
                    # should directly copy op/ed files
                    if file.startswith("op") or file.startswith("ed"):
                        os.makedirs(os.path.dirname(output_file), exist_ok=True)
                        shutil.copy(input_file, output_file)
                        shutil.copy(input_file.replace("_sc", "_tc"), output_file.replace("_sc", "_tc"))
                        continue

                    processor = SubtitleProcessor(input_file, output_file)
                    processor.cleanup_ass_file()
                    processor_tc = SubtitleProcessor(output_file, output_tc_file)
                    processor_tc.traditionalize_ass(user_protect_replace=config.user_protect_replace)

    @staticmethod
    def merge_files(input_file, output_file):
        with open(input_file, encoding='utf-8-sig', mode='r') as f:
            subs = subdigest.Subtitles(ass.parse(f), "s")
            subs.ms_import_rc()

            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, encoding='utf-8-sig', mode='w+') as f_out:
                subs.dump_file(f_out)

if __name__ == '__main__':
    processor = SubtitleProcessor('ep1.ass', 'ep1_out.ass')
    processor.traditionalize_ass()