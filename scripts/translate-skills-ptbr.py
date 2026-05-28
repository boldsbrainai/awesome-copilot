from __future__ import annotations

import json
import logging
import re
import argparse
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import argostranslate.translate


BASE_DIR = Path(r"C:\Users\fjuni\Projects\01-Upstream\awesome-copilot\skills")
SAMPLE_VALIDATION_SIZE = 12

TRANSLATABLE_FRONTMATTER_KEYS = {"description", "title", "summary"}
NON_TRANSLATABLE_FRONTMATTER_KEYS = {
    "name",
    "model",
    "tools",
    "agent",
    "applyTo",
    "input",
    "output",
    "tags",
    "version",
}
PRESERVE_TERMS = [
    "GitHub Copilot CLI",
    "GitHub Copilot SDK",
    "GitHub Copilot",
    "GitHub Actions",
    "GitHub",
    "Model Context Protocol",
    "MCP server",
    "MCP servers",
    "MCP",
    "Azure Monitor",
    "App Insights",
    "Application Insights",
    "ASP.NET Core",
    "Node.js",
    "TypeScript",
    "JavaScript",
    "Python",
    "Go",
    ".NET",
    "C#",
    "OpenTelemetry",
    "Bicep",
    "Terraform",
    "IaC",
    "CLI",
    "SDK",
    "Markdown",
    "YAML",
    "JSON",
    "README",
    "SKILL.md",
    "build",
    "deploy",
    "branch",
    "pull request",
    "issue",
    "token",
    "cache",
    "workspace",
    "streaming",
    "agentic",
]
BRAZILIAN_REPLACEMENTS = {
    "ficheiro": "arquivo",
    "ficheiros": "arquivos",
    "utilizador": "usuário",
    "utilizadores": "usuários",
    "parametrizar": "configurar",
    "parametrizado": "configurado",
    "parametrizada": "configurada",
    "parametrizados": "configurados",
    "parametrizadas": "configuradas",
}
SUSPICIOUS_ENGLISH = re.compile(
    r"\b(the|and|with|from|when|where|should|must|before|after|overview|install|installation|"
    r"example|examples|usage|required|optional|default|settings|configure|configuration|create|"
    r"update|review|please|provide|file|files|skill)\b",
    re.IGNORECASE,
)

logging.getLogger().setLevel(logging.ERROR)


@dataclass
class TranslationStats:
    processed: int = 0
    created: int = 0
    collisions_avoided: int = 0


def get_translation() -> object:
    return argostranslate.translate.get_translation_from_codes("en", "pt")


TRANSLATION = get_translation()


def choose_target_path(source_path: Path) -> tuple[Path, bool]:
    base = source_path.with_suffix("")
    candidate = base.with_name(f"{base.name}.pt-br").with_suffix(".md")
    if not candidate.exists():
        return candidate, False

    counter = 2
    while True:
        alt = base.with_name(f"{base.name}.pt-br-{counter}").with_suffix(".md")
        if not alt.exists():
            return alt, True
        counter += 1


def detect_newline(text: str) -> str:
    if "\r\n" in text:
        return "\r\n"
    return "\n"


@lru_cache(maxsize=50000)
def translate_plain_text(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return text

    protected = text
    placeholders: dict[str, str] = {}

    def protect_literal(value: str) -> str:
        key = f"__PRESERVE_{len(placeholders)}__"
        placeholders[key] = value
        return key

    for term in sorted(PRESERVE_TERMS, key=len, reverse=True):
        protected = re.sub(re.escape(term), lambda m: protect_literal(m.group(0)), protected)

    patterns = [
        r"`[^`]+`",
        r"!\[[^\]]*]\([^)]+\)",
        r"\[[^\]]+]\([^)]+\)",
        r"<https?://[^>]+>",
        r"https?://\S+",
        r"\{\{[^{}]+\}\}",
        r"\$\{[^{}]+\}",
        r"\{[^{}\n]+\}",
        r"\b[A-Za-z0-9_.-]+\.(?:md|json|ya?ml|toml|cs|py|ts|js|go|java|kt|rb|php|ps1|sh)\b",
    ]
    for pattern in patterns:
        protected = re.sub(pattern, lambda m: protect_literal(m.group(0)), protected)

    translated = TRANSLATION.translate(protected)

    for source, target in BRAZILIAN_REPLACEMENTS.items():
        translated = re.sub(rf"\b{re.escape(source)}\b", target, translated, flags=re.IGNORECASE)

    for key, value in placeholders.items():
        translated = translated.replace(key, value)

    translated = translated.replace(" ,", ",").replace(" .", ".").replace(" :", ":")
    return translated


def translate_markdown_link_text(text: str) -> str:
    return translate_plain_text(text)


def translate_inline(text: str) -> str:
    if not text.strip():
        return text

    def replace_image(match: re.Match[str]) -> str:
        alt_text = translate_markdown_link_text(match.group(1))
        return f"![{alt_text}]({match.group(2)})"

    def replace_link(match: re.Match[str]) -> str:
        link_text = translate_markdown_link_text(match.group(1))
        return f"[{link_text}]({match.group(2)})"

    text = re.sub(r"!\[([^\]]*)]\(([^)]+)\)", replace_image, text)
    text = re.sub(r"\[([^\]]+)]\(([^)]+)\)", replace_link, text)
    return translate_plain_text(text)


def translate_table_line(line: str) -> str:
    newline = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
    core = line[:-len(newline)] if newline else line
    if re.fullmatch(r"\s*\|?[:\-\s|]+\|?\s*", core):
        return line

    leading_pipe = core.startswith("|")
    trailing_pipe = core.endswith("|")
    cells = core.strip("|").split("|")
    translated_cells = [translate_inline(cell) for cell in cells]
    rebuilt = "|".join(translated_cells)
    if leading_pipe:
        rebuilt = "|" + rebuilt
    if trailing_pipe:
        rebuilt = rebuilt + "|"
    return rebuilt + newline


def translate_line(line: str) -> str:
    if not line.strip():
        return line
    if re.fullmatch(r"\s*[-*_]{3,}\s*", line.strip()):
        return line
    if line.lstrip().startswith("|"):
        return translate_table_line(line)

    newline = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
    core = line[:-len(newline)] if newline else line

    prefix_match = re.match(
        r"^(\s*(?:> ?)*)(#{1,6}\s+|[-*+]\s+|\d+\.\s+|(?:[-*+]\s+\[[ xX]\]\s+)|\[[^\]]+]:\s+)?(.*)$",
        core,
    )
    if prefix_match:
        prefix = (prefix_match.group(1) or "") + (prefix_match.group(2) or "")
        body = prefix_match.group(3) or ""
        return prefix + translate_inline(body) + newline

    return translate_inline(core) + newline


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---"):
        return None, text

    newline = detect_newline(text)
    marker = f"---{newline}"
    end_marker = f"{newline}---{newline}"
    if not text.startswith(marker):
        return None, text

    end_index = text.find(end_marker, len(marker) - len(newline))
    if end_index == -1:
        return None, text

    frontmatter = text[: end_index + len(end_marker)]
    body = text[end_index + len(end_marker) :]
    return frontmatter, body


def translate_frontmatter(frontmatter: str) -> str:
    lines = frontmatter.splitlines(keepends=True)
    translated_lines: list[str] = []

    for index, line in enumerate(lines):
        if index in {0, len(lines) - 1} and line.strip() == "---":
            translated_lines.append(line)
            continue

        match = re.match(r"^(\s*)([A-Za-z0-9_-]+)(\s*:\s*)(.*?)(\r?\n?)$", line)
        if not match:
            translated_lines.append(line)
            continue

        indent, key, separator, value, newline = match.groups()
        if key in NON_TRANSLATABLE_FRONTMATTER_KEYS or not value.strip():
            translated_lines.append(line)
            continue

        if key in TRANSLATABLE_FRONTMATTER_KEYS:
            value = value.strip()
            quote = ""
            if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
                quote = value[0]
                inner = value[1:-1]
                translated_value = translate_inline(inner)
                translated_lines.append(f"{indent}{key}{separator}{quote}{translated_value}{quote}{newline}")
            else:
                translated_value = translate_inline(value)
                translated_lines.append(f"{indent}{key}{separator}{translated_value}{newline}")
            continue

        translated_lines.append(line)

    return "".join(translated_lines)


def translate_markdown_body(body: str) -> str:
    lines = body.splitlines(keepends=True)
    output: list[str] = []
    in_fence = False

    for line in lines:
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            output.append(line)
            continue

        if in_fence:
            output.append(line)
            continue

        output.append(translate_line(line))

    return "".join(output)


def translate_content(content: str) -> str:
    frontmatter, body = split_frontmatter(content)
    translated_frontmatter = translate_frontmatter(frontmatter) if frontmatter else None
    translated_body = translate_markdown_body(body)
    if translated_frontmatter is None:
        return translated_body
    return translated_frontmatter + translated_body


def count_headings(text: str) -> int:
    return len(re.findall(r"(?m)^\s*#{1,6}\s", text))


def count_fences(text: str) -> int:
    return len(re.findall(r"(?m)^\s*(```|~~~)", text))


def count_links(text: str) -> int:
    return len(re.findall(r"\[[^\]]+]\([^)]+\)", text))


def strip_non_prose(text: str) -> str:
    text = re.sub(r"(?ms)^---\r?\n.*?\r?\n---\r?\n?", "", text)
    text = re.sub(r"(?ms)^\s*(```|~~~).*?^\s*\1.*?$", "", text)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"\[[^\]]+]\(([^)]+)\)", "", text)
    text = re.sub(r"https?://\S+", "", text)
    return text


def validate_sample(sample_pairs: list[tuple[Path, Path]]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []

    for source_path, target_path in sample_pairs:
        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8")
        stripped_target = strip_non_prose(target_text)
        suspicious_matches = SUSPICIOUS_ENGLISH.findall(stripped_target)

        results.append(
            {
                "source": str(source_path.relative_to(BASE_DIR)),
                "target": str(target_path.relative_to(BASE_DIR)),
                "headings_preserved": count_headings(source_text) == count_headings(target_text),
                "fences_preserved": count_fences(source_text) == count_fences(target_text),
                "links_preserved": count_links(source_text) == count_links(target_text),
                "suspicious_english_hits": len(suspicious_matches),
                "sample_english_hits": suspicious_matches[:10],
            }
        )

    return results


def iter_source_files(limit: int | None = None) -> list[Path]:
    files = sorted(
        path
        for path in BASE_DIR.rglob("*.md")
        if "node_modules" not in path.parts and not path.name.endswith(".pt-br.md")
    )
    if limit is not None:
        return files[:limit]
    return files


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    stats = TranslationStats()
    sample_pairs: list[tuple[Path, Path]] = []
    files = iter_source_files(limit=args.limit)

    for index, source_path in enumerate(files):
        content = source_path.read_text(encoding="utf-8")
        newline = detect_newline(content)
        translated = translate_content(content)
        if newline == "\r\n":
            translated = translated.replace("\n", "\r\n")

        target_path, had_collision = choose_target_path(source_path)
        target_path.write_text(translated, encoding="utf-8", newline="")

        stats.processed += 1
        stats.created += 1
        if had_collision:
            stats.collisions_avoided += 1

        if len(sample_pairs) < SAMPLE_VALIDATION_SIZE:
            sample_pairs.append((source_path, target_path))
        else:
            step = max(1, len(files) // SAMPLE_VALIDATION_SIZE)
            if index % step == 0 and len(sample_pairs) < SAMPLE_VALIDATION_SIZE * 2:
                sample_pairs.append((source_path, target_path))

    validation = validate_sample(sample_pairs[:SAMPLE_VALIDATION_SIZE])
    print(
        json.dumps(
            {
                "processed": stats.processed,
                "created": stats.created,
                "collisions_avoided": stats.collisions_avoided,
                "sample_validation": validation,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
