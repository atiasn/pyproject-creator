from __future__ import annotations

import jinja2

commit_types: list[dict[str, str]] = [
    {"emoji": "✨", "change_type": "feat", "description": "Introduce new features."},
    {"emoji": "🐛", "change_type": "fix", "description": "Fix a bug."},
    {"emoji": "🚑️", "change_type": "hotfix", "description": "Hotfix a bug."},
    {"emoji": "📝", "change_type": "docs", "description": "Add or update documentation."},
    {"emoji": "📄", "change_type": "license", "description": "Add or update license."},
    {
        "emoji": "🎨",
        "change_type": "style",
        "description": "Improve structure/format of the code.",
    },
    {"emoji": "🔊", "change_type": "logs", "description": "Add or update logs."},
    {"emoji": "🔇", "change_type": "rm_logs", "description": "Remove logs."},
    {"emoji": "♻️", "change_type": "refactor", "description": "Refactor code."},
    {"emoji": "✅", "change_type": "test", "description": "Add, update, or pass tests."},
    {"emoji": "🚀", "change_type": "deploy", "description": "Deploy stuff."},
    {"emoji": "🔧", "change_type": "config", "description": "Add or update configuration files."},
    {"emoji": "🔨", "change_type": "scripts", "description": "Add or update development scripts."},
    {"emoji": "💚", "change_type": "ci_fix", "description": "Fix CI Build."},
    {"emoji": "👷", "change_type": "ci_update", "description": "Add or update CI build system."},
    {"emoji": "💄", "change_type": "ui", "description": "Add or update the UI and style files."},
    {"emoji": "🔖", "change_type": "release", "description": "Release / Version tags."},
    {"emoji": "🏷️", "change_type": "types", "description": "Add or update types."},
    {"emoji": "🚨", "change_type": "lint", "description": "Fix compiler/linter warnings."},
    {"emoji": "➕", "change_type": "add_dep", "description": "Add a dependency."},
    {"emoji": "➖", "change_type": "rm_dep", "description": "Remove a dependency."},
    {"emoji": "⬇️", "change_type": "downgrade", "description": "Downgrade dependencies."},
    {"emoji": "⬆️", "change_type": "upgrade", "description": "Upgrade dependencies."},
    {"emoji": "📌", "change_type": "pin", "description": "Pin dependencies to specific versions."},
    {
        "emoji": "📈",
        "change_type": "analytics",
        "description": "Add or update analytics or track code.",
    },
    {
        "emoji": "🌐",
        "change_type": "i18n",
        "description": "Internationalization and localization.",
    },
    {"emoji": "✏️", "change_type": "typos", "description": "Fix typos."},
    {"emoji": "🎉", "change_type": "init", "description": "Begin a project."},
    {"emoji": "🚧", "change_type": "wip", "description": "Work in progress."},
    {"emoji": "⏪️", "change_type": "revert", "description": "Revert changes."},
    {"emoji": "🔀", "change_type": "merge", "description": "Merge branches."},
    {
        "emoji": "📦️",
        "change_type": "compiled",
        "description": "Add or update compiled files or packages.",
    },
    {
        "emoji": "👽️",
        "change_type": "api",
        "description": "Update code due to external API changes.",
    },
    {
        "emoji": "🚚",
        "change_type": "move",
        "description": "Move or rename resources (e.g., files, paths, routes).",
    },
    {"emoji": "💥", "change_type": "breaking", "description": "Introduce breaking changes."},
    {"emoji": "♿️", "change_type": "accessibility", "description": "Improve accessibility."},
    {
        "emoji": "💡",
        "change_type": "comments",
        "description": "Add or update comments in source code.",
    },
    {"emoji": "🍻", "change_type": "drunk", "description": "Write code drunkenly."},
    {"emoji": "🚸", "change_type": "ux", "description": "Improve user experience/usability."},
    {"emoji": "🏗️", "change_type": "architecture", "description": "Make architectural changes."},
    {"emoji": "🙈", "change_type": "gitignore", "description": "Add or update a .gitignore file."},
    {
        "emoji": "🚩",
        "change_type": "flags",
        "description": "Add, update, or remove feature flags.",
    },
    {"emoji": "🥅", "change_type": "catch_errors", "description": "Catch errors."},
    {
        "emoji": "🗑️",
        "change_type": "deprecate",
        "description": "Deprecate code that needs to be cleaned up.",
    },
    {"emoji": "⚰️", "change_type": "rm_dead_code", "description": "Remove dead code."},
    {"emoji": "🧑‍💻", "change_type": "dev_exp", "description": "Improve developer experience."},
    {"emoji": "⚡️", "change_type": "performance", "description": "Improve performance."},
    {"emoji": "🔥", "change_type": "rm_code", "description": "Remove code or files."},
    {"emoji": "🍱", "change_type": "assets", "description": "Add or update assets."},
]


def get_info_via_type(_type: str) -> str:
    for commit in commit_types:
        if commit["change_type"] == _type:
            return f"{commit['emoji']} {commit['change_type']}".strip()
    raise KeyError(f"{_type} not found in {commit_types}")


def get_type_pattern(*args: str) -> str:
    change_types = [i for i in commit_types if not args or i["change_type"] in args]
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


def main() -> None:
    with open("cz_toml.template") as f:
        template = jinja2.Template(f.read())

    template = template.render(
        release_type_str=get_info_via_type("release"),
        feat_type_str=get_info_via_type("feat"),
        schema_pattern_type_str=get_type_pattern(),
        bump_pattern_type_str=get_type_pattern(*["breaking", "feat", "fix", "hotfix"]),
        commit_parser_type_str=get_type_pattern(),
        changelog_pattern_type_str=get_type_pattern(),
        info_commit_types_str="\n".join(
            f"- {commit['emoji']} {commit['change_type']}: {commit['description']}"
            for commit in commit_types
        ),
        change_type_choices_str=get_change_type_choices(),
    )

    with open(".cz.toml", "w", encoding="utf-8") as f:
        f.write(template + "\n")


if __name__ == "__main__":
    main()
