"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

print(f"PATH: {Path('src')}")
print(f"PATH: {[p for p in Path('src').rglob('*.py')]}")
print(f"PATH: {Path('jmapc')}")
print(f"PATH: {[p for p in Path('jmapc').rglob('*.py')]}")
ph = "jmapc"
for path in sorted(Path(ph).rglob("*.py")):
    print(f"PATH: {path}")
    module_path = path.relative_to(ph).with_suffix("")
    doc_path = path.relative_to(ph).with_suffix(".md")
    doc_path = Path("jmapc", doc_path)
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)
    parts = ("jmapc",) + parts

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue
    print(full_doc_path, parts)

    nav[parts] = doc_path.as_posix()  #

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        if not parts or "__version__" in parts:
            continue
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:  #
    nav_file.writelines(nav.build_literate_nav())  #
