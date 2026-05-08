import os
import re

# Characters not allowed in filenames (NTFS and cross-platform safe)
INVALID_CHARS = r'":<>|*?\r\n'

def clean_filename(name: str) -> str:
    """Remove invalid characters from a filename."""
    return re.sub(f"[{re.escape(INVALID_CHARS)}]", "", name)

def rename_invalid_files(root_dir: str = "."):
    renamed = []
    skipped = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(c in filename for c in INVALID_CHARS):
                old_path = os.path.join(dirpath, filename)
                new_filename = clean_filename(filename)

                if not new_filename:
                    print(f"[SKIPPED] Would result in empty filename: {old_path}")
                    skipped.append(old_path)
                    continue

                new_path = os.path.join(dirpath, new_filename)

                if os.path.exists(new_path):
                    print(f"[SKIPPED] Target already exists: {new_path}")
                    skipped.append(old_path)
                    continue

                os.rename(old_path, new_path)
                print(f"[RENAMED] {old_path}  ->  {new_path}")
                renamed.append((old_path, new_path))

    print(f"\nDone. {len(renamed)} file(s) renamed, {len(skipped)} skipped.")

if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    rename_invalid_files(root)
