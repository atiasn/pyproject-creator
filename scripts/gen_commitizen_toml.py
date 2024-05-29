from __future__ import annotations

import json
from pathlib import Path

import jinja2


current_dir = Path(__file__).parent.resolve()
with open(current_dir / "gitmoji.json") as f:
    commit_types: list[dict[str, str]] = json.load(f)


def get_info_via_type(_type: str) -> str:
    for commit in commit_types:
        if commit["change_type"] == _type:
            return f"{commit['emoji']} {commit['change_type']}".strip()
    raise KeyError(f"{_type} not found in {commit_types}")


def get_type_pattern(*args: str, exclude: list[str] | None = None) -> str:
    if exclude is None:
        exclude = []
    change_types = [
        i
        for i in commit_types
        if (not args or i["change_type"] in args) and (i["change_type"] not in exclude)
    ]
    return "|".join(i["change_type"] for i in change_types)


def get_change_type_choices() -> str:
    change_types = [
        (
            f'{{value = "{commit["emoji"]} {commit["change_type"]}", '
            f'name = "{commit["emoji"]} {commit["change_type"]}: {commit["description"]}"}}'
        )
        for commit in commit_types
    ]
    return ",\n\t".join(change_types)


def get_change_type_map_str(*args: str) -> str:
    map_strs = [f'"{i}"="{i.capitalize()}"' for i in args]
    return "{" + ", ".join(map_strs) + "}"


def main() -> None:
    with open(current_dir / "cz_toml.template") as _f:
        template = jinja2.Template(_f.read())
    pattern_type_list = [
        "breaking",
        "feat",
        "fix",
        "hotfix",
        "docs",
        "refactor",
        "config",
        "scripts",
        "style",
    ]
    template = template.render(
        release_type_str=get_info_via_type("release"),
        feat_type_str=get_info_via_type("feat"),
        schema_pattern_type_str=get_type_pattern(),
        bump_pattern_type_str=get_type_pattern(*["breaking", "feat", "fix", "hotfix"]),
        commit_parser_type_str=get_type_pattern(exclude=["release"]),
        changelog_pattern_type_str=get_type_pattern(*pattern_type_list),
        change_type_map_str=get_change_type_map_str(*pattern_type_list),
        info_commit_types_str="\n".join(
            f"- {commit['emoji']} {commit['change_type']}: {commit['description']}"
            for commit in commit_types
        ),
        change_type_choices_str=get_change_type_choices(),
    )

    with open(current_dir.parent.resolve() / ".cz.toml", "w", encoding="utf-8") as _f:
        _f.write(template + "\n")


if __name__ == "__main__":
    main()
