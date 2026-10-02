"""教材の生成・保存・再読み込みを確認する。通常のpython3で実行する。"""

from pathlib import Path
import argparse
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--blender", default="/Applications/Blender.app/Contents/MacOS/Blender"
    )
    parser.add_argument("--start", type=int, default=10)
    parser.add_argument("--end", type=int, default=40)
    parser.add_argument(
        "--saved-only", action="store_true", help="生成せず、既存の出力だけ確認"
    )
    arguments = parser.parse_args()
    if not 10 <= arguments.start <= arguments.end <= 40:
        parser.error("確認範囲は10〜40で指定してください")
    log_directory = ROOT / "output" / "verification"
    log_directory.mkdir(parents=True, exist_ok=True)
    folders = sorted(
        folder
        for folder in (ROOT / "lessons").glob("[0-9][0-9]_*")
        if arguments.start <= int(folder.name[:2]) <= arguments.end
    )
    assert len(folders) == arguments.end - arguments.start + 1, "レッスンが欠けています"
    blend_paths = []
    for folder in folders:
        # Python構文の確認はBlender起動前に実施。addon.pyも対象。
        for script_path in folder.glob("*.py"):
            compile(script_path.read_text(), str(script_path), "exec")
        blend_path = ROOT / "output" / (folder.name + ".blend")
        if not arguments.saved_only:
            command = [
                arguments.blender,
                "--background",
                "--python-exit-code",
                "1",
                "--python",
                str(folder / "lesson.py"),
            ]
            with (log_directory / (folder.name + ".log")).open("w") as log_file:
                process = subprocess.run(
                    command, stdout=log_file, stderr=subprocess.STDOUT
                )
            output = (log_directory / (folder.name + ".log")).read_text()
            if process.returncode or f"CHECK OK {folder.name}" not in output:
                print(output[-6000:], file=sys.stderr)
                return 1
            print(f"GENERATE OK {folder.name}", flush=True)
        if not blend_path.is_file() or not blend_path.with_suffix(".json").is_file():
            print(f"保存結果がありません: {blend_path}", file=sys.stderr)
            return 1
        blend_paths.append(str(blend_path))
    command = [
        arguments.blender,
        "--background",
        "--python-exit-code",
        "1",
        "--python",
        str(ROOT / "lessons" / "_support" / "verify_saved.py"),
        "--",
        *blend_paths,
    ]
    process = subprocess.run(command, capture_output=True, text=True)
    (log_directory / "reopen.log").write_text(process.stdout + process.stderr)
    if process.returncode:
        print((process.stdout + process.stderr)[-6000:], file=sys.stderr)
        return 1
    for folder in folders:
        if f"REOPEN OK {folder.name}" not in process.stdout:
            print(f"再読み込み未確認: {folder.name}", file=sys.stderr)
            return 1
    print(f"REOPEN OK: {len(folders)} lessons; log: {log_directory / 'reopen.log'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
