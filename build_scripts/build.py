import utils
import os
import subprocess

def main():
    work_folder = os.environ.get('GITHUB_WORKSPACE')
    # work_folder = os.getcwd()
    build_dir = os.path.join(work_folder, 'build')

    utils.traverse_files(work_folder)

    for root, dirs, files in os.walk(build_dir):
        for file in files:
            if file.endswith(".ass"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(build_dir, "output", file)

                # run templates
                if not file.startswith("op"):
                    print(f"Running templates on {input_path}")
                    subprocess.run(["wine", f"{work_folder}/aegisub-cli/aegisub-cli.exe", "--automation", f"{work_folder}/aegisub-cli/automation/autoload/0x.KaraTemplater.moon", input_path, input_path, "0x539's Templater"])

    for root, dirs, files in os.walk(build_dir):
        for file in files:
            if file.endswith(".ass"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(build_dir, "output", file)
                if file.startswith("ep"):
                    os.chdir(root)
                    utils.merge_files(input_path, output_path)
                    print(f"Merged {file}")

if __name__ == "__main__":
    main()