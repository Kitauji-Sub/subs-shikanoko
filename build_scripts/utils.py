import ass
import subdigest
import requests
import json
import os
import shutil
import requests
from requests.exceptions import RequestException
from requests.adapters import HTTPAdapter, Retry

def cleanup_ass_file(input_file, output_file):
    with open(input_file, encoding='utf-8-sig', mode='r') as f:
        subs = subdigest.Subtitles(ass.parse(f),"s")
        subs.selection_set("effect", "fx").remove_selected()

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, encoding='utf-8-sig', mode='w+') as f_out:
            subs.dump_file(f_out)

def traditionalize_text(input_text, user_pre_replace="", user_protect_replace="", timeout=10, max_tries=3):
    url = "https://api.zhconvert.org/convert"
    data = {
        "text": input_text,
        "converter": "Taiwan",
        "userPreReplace": user_pre_replace,
        "userProtectReplace": user_protect_replace
    }
    
    retry_strategy = Retry(total=max_tries, backoff_factor=0.3)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
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

def traditionalize_ass(input_file, output_file, user_pre_replace="", user_protect_replace=""):
    with open(input_file, encoding='utf-8-sig', mode='r') as f:
        doc = ass.parse(f)
        texts_and_names = []
        temp_texts_names = []
        for i in range(len(doc.events)):
            temp_texts_names.append([doc.events[i].text, doc.events[i].name])
        print(f"Traditionalizing {input_file}")
        for i in range(0, len(temp_texts_names), 50):
            print(f"Traditionalizing line {i} to {i+50}...")
            slice = temp_texts_names[i:i+50]
            slice = json.dumps(slice, ensure_ascii=False)
            traditionalized_slice = traditionalize_text(slice, user_pre_replace, user_protect_replace)
            texts_and_names += json.loads(traditionalized_slice)
        for i in range(len(texts_and_names)):
            doc.events[i].text = texts_and_names[i][0].replace("思源黑体", "Source Han Sans TC").replace("思源宋体", "Source Han Serif TC").replace("Source Han Sans SC", "Source Han Sans TC").replace("Source Han Serif SC", "Source Han Serif TC").replace("FOT-TsukuARdGothic Std E", "獅尾圓體JP-Bold").replace("仓耳周珂正大榜书", "悠哉字体")
            doc.events[i].name = texts_and_names[i][1]
            # replace import commands
            if doc.events[i].effect.startswith("import"):
                doc.events[i].text = doc.events[i].text.replace(".ass", "_tc.ass").replace("_sc_tc.ass", "_tc.ass")

        # replace styles if needed
        for i in range(len(doc.styles)):
            if doc.styles[i].fontname == "筑紫A丸 SC":
                doc.styles[i].fontsize = "55"
                if doc.styles[i].name == "note":
                    doc.styles[i].fontsize = "45"
                doc.styles[i].bold = "0"
            doc.styles[i].fontname = doc.styles[i].fontname.replace("筑紫A丸 SC", "獅尾圓體-Bold").replace("思源黑体", "Source Han Sans TC").replace("思源宋体", "Source Han Serif TC").replace("Source Han Sans SC", "Source Han Sans TC").replace("Source Han Serif SC", "Source Han Serif TC").replace("FOT-TsukuARdGothic Std E", "獅尾圓體JP-Bold").replace("仓耳周珂正大榜书", "悠哉字体")

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, encoding='utf-8-sig', mode='w+') as f_out:
            doc.dump_file(f_out)

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

                cleanup_ass_file(input_file, output_file)
                traditionalize_ass(output_file, output_tc_file, user_protect_replace='悠哉字体\n仓耳周珂正大榜书')

def merge_files(input_file, output_file):
    with open(input_file, encoding='utf-8-sig', mode='r') as f:
        subs = subdigest.Subtitles(ass.parse(f),"s")
        subs.ms_import_rc()

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, encoding='utf-8-sig', mode='w+') as f_out:
            subs.dump_file(f_out)

if __name__ == '__main__':
    traditionalize_ass('ep1.ass', 'ep1_out.ass')