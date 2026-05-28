from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib import error, request


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
    "on",
    "permissions",
    "safe-outputs",
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
    "Application Insights",
    "App Insights",
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
    "utilizador": "usuario",
    "utilizadores": "usuarios",
    "parametrizar": "configurar",
    "parametrizado": "configurado",
    "parametrizada": "configurada",
    "parametrizados": "configurados",
    "parametrizadas": "configuradas",
}
PT_STOPWORDS = {
    "de",
    "da",
    "do",
    "das",
    "dos",
    "que",
    "para",
    "com",
    "uma",
    "um",
    "nao",
    "não",
    "como",
    "mais",
    "se",
    "por",
    "os",
    "as",
    "ao",
    "aos",
    "ser",
    "seu",
    "sua",
    "suas",
    "seus",
    "voce",
    "você",
    "arquivo",
    "arquivos",
    "fluxo",
    "trabalho",
}
EN_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "when",
    "your",
    "into",
    "file",
    "files",
    "should",
    "must",
    "build",
    "workflow",
    "agent",
    "skill",
    "before",
    "after",
    "using",
}
MATERIALIZED_PLUGIN_DIRS = {"agents", "commands", "skills", "instructions", "hooks", "workflows"}
EXCLUDED_DIR_NAMES = {
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".next",
    ".astro",
    "out",
    "obj",
    "bin",
    "__pycache__",
    ".mypy_cache",
}
PROMPT_TEMPLATE = (
    "You are revising a Brazilian Portuguese Markdown translation that came from DeepLX.\n"
    "Return only the final revised pt-BR text.\n"
    "Do not add commentary.\n"
    "Preserve Markdown structure, YAML frontmatter, headings, lists, tables, code fences, inline code, URLs, Markdown link targets, and filenames exactly.\n"
    "Do not add or remove headings, links, code fences, or frontmatter markers.\n"
    "Keep the same meaning as the original English.\n\n"
    "ORIGINAL ENGLISH:\n{original}\n\n"
    "DEEPLX PT-BR:\n{translated}\n"
)


@dataclass
class PreflightResult:
    docker_available: bool
    docker_version: str | None
    ollama_available: bool
    ollama_version: str | None
    ollama_model_available: bool
    deeplx_url: str
    deeplx_container: str | None
    deeplx_token_available: bool
    deeplx_health_ok: bool
    deeplx_translate_ok: bool
    deeplx_health: str
    deeplx_translate_preview: str | None
    ollama_preview: str | None
    blocker: str | None = None


@dataclass
class ManifestEntry:
    source: str
    category: str
    size: int


@dataclass
class State:
    preflight: dict[str, Any] = field(default_factory=dict)
    manifest_path: str | None = None
    rules: dict[str, Any] = field(default_factory=dict)
    pilot_selection: list[str] = field(default_factory=list)
    results: dict[str, dict[str, Any]] = field(default_factory=dict)


def run_command(args: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(args, capture_output=True, text=True, check=False)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def http_json(
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: dict[str, Any] | None = None,
    timeout: int = 30,
) -> tuple[int, dict[str, Any] | str]:
    data = None
    request_headers = dict(headers or {})
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        request_headers["Content-Type"] = "application/json"

    req = request.Request(url, headers=request_headers, data=data, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as response:
            payload = response.read().decode("utf-8", errors="replace")
            try:
                return response.status, json.loads(payload)
            except json.JSONDecodeError:
                return response.status, payload
    except error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        try:
            parsed: dict[str, Any] | str = json.loads(payload)
        except json.JSONDecodeError:
            parsed = payload
        return exc.code, parsed


def detect_deeplx_token() -> tuple[str | None, str | None]:
    for env_name in ("DEEPLX_AUTH_KEY", "DEEPLX_API_KEY", "DEEPLX_TOKEN", "TOKEN"):
        value = os.environ.get(env_name)
        if value:
            return value, f"env:{env_name}"

    if not shutil.which("docker"):
        return None, None

    container_name = "deeplx-core"
    code, stdout, _ = run_command(["docker", "inspect", container_name])
    if code != 0 or not stdout:
        return None, None

    inspect_data = json.loads(stdout)
    env_entries = inspect_data[0].get("Config", {}).get("Env", [])
    for item in env_entries:
        if item.startswith("TOKEN="):
            return item.split("=", 1)[1], f"docker:{container_name}"
    return None, None


def preflight(deeplx_url: str, ollama_model: str) -> PreflightResult:
    docker_available = shutil.which("docker") is not None
    ollama_available = shutil.which("ollama") is not None
    docker_version = None
    ollama_version = None
    ollama_model_available = False
    deeplx_token, deeplx_container = detect_deeplx_token()
    deeplx_headers = {"Authorization": f"Bearer {deeplx_token}"} if deeplx_token else {}

    if docker_available:
        _, docker_version_stdout, _ = run_command(["docker", "--version"])
        docker_version = docker_version_stdout or None

    if ollama_available:
        _, ollama_version_stdout, _ = run_command(["ollama", "--version"])
        ollama_version = ollama_version_stdout or None
        _, ollama_list_stdout, _ = run_command(["ollama", "list"])
        ollama_model_available = ollama_model in ollama_list_stdout

    health_status, health_payload = http_json(deeplx_url, headers=deeplx_headers, timeout=15)
    health_text = health_payload if isinstance(health_payload, str) else json.dumps(health_payload, ensure_ascii=False)

    translate_status, translate_payload = http_json(
        deeplx_url.rstrip("/") + "/translate",
        method="POST",
        headers=deeplx_headers,
        body={"text": "Preflight translation check.", "source_lang": "EN", "target_lang": "PT-BR"},
        timeout=45,
    )
    translate_preview = None
    if isinstance(translate_payload, dict):
        translate_preview = str(translate_payload.get("data") or translate_payload.get("message") or "")[:120]
    elif isinstance(translate_payload, str):
        translate_preview = translate_payload[:120]

    ollama_preview = None
    if ollama_available and ollama_model_available:
        ollama_status, ollama_payload = http_json(
            "http://127.0.0.1:11434/api/generate",
            method="POST",
            body={
                "model": ollama_model,
                "prompt": "Translate to pt-BR and preserve Markdown if any. Text: Preflight translation check.",
                "stream": False,
            },
            timeout=90,
        )
        if ollama_status == 200 and isinstance(ollama_payload, dict):
            ollama_preview = str(ollama_payload.get("response") or "")[:120]

    blocker = None
    if not docker_available:
        blocker = "Docker is not available."
    elif not ollama_available:
        blocker = "Ollama is not available."
    elif not ollama_model_available:
        blocker = f"Ollama model {ollama_model} is not available."
    elif not deeplx_token:
        blocker = "DeepLX auth token is not available."
    elif health_status != 200:
        blocker = f"DeepLX health check failed with status {health_status}."
    elif translate_status != 200:
        blocker = f"DeepLX translate preflight failed with status {translate_status}."

    return PreflightResult(
        docker_available=docker_available,
        docker_version=docker_version,
        ollama_available=ollama_available,
        ollama_version=ollama_version,
        ollama_model_available=ollama_model_available,
        deeplx_url=deeplx_url,
        deeplx_container=deeplx_container,
        deeplx_token_available=bool(deeplx_token),
        deeplx_health_ok=health_status == 200,
        deeplx_translate_ok=translate_status == 200,
        deeplx_health=health_text,
        deeplx_translate_preview=translate_preview,
        ollama_preview=ollama_preview,
        blocker=blocker,
    )


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


def detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def strip_non_prose(text: str) -> str:
    text = re.sub(r"(?ms)^---\r?\n.*?\r?\n---\r?\n?", "", text)
    text = re.sub(r"(?ms)^\s*(```|~~~).*?^\s*\1.*?$", "", text)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"\[[^\]]+]\(([^)]+)\)", "", text)
    text = re.sub(r"https?://\S+", "", text)
    return text


def classify_category(repo_root: Path, path: Path) -> str:
    relative = path.relative_to(repo_root)
    parts = relative.parts
    if len(parts) == 1:
        return "root"
    if parts[0] == ".github":
        return "github"
    if parts[0] == "instructions":
        return "instructions"
    if parts[0] == "agents":
        return "agents"
    if parts[0] == "skills":
        return "skills"
    return parts[0]


def is_materialized_plugin_file(relative: Path) -> bool:
    parts = relative.parts
    if len(parts) < 3 or parts[0] != "plugins":
        return False
    return parts[2] in MATERIALIZED_PLUGIN_DIRS


def target_variants_exist(path: Path) -> bool:
    stem = path.stem
    for sibling in path.parent.glob(f"{stem}.pt-br*.md"):
        if sibling.exists():
            return True
    return False


def is_probably_portuguese(text: str) -> bool:
    prose = strip_non_prose(text).lower()
    words = re.findall(r"[a-zà-ÿ]+", prose)
    if len(words) < 20:
        return False
    pt_hits = sum(1 for word in words if word in PT_STOPWORDS)
    en_hits = sum(1 for word in words if word in EN_STOPWORDS)
    return pt_hits >= 6 and pt_hits >= (en_hits * 2)


def build_manifest(repo_root: Path) -> tuple[list[ManifestEntry], dict[str, int], dict[str, list[str]]]:
    manifest: list[ManifestEntry] = []
    skipped_counts: dict[str, int] = {
        "excluded_name": 0,
        "excluded_path": 0,
        "existing_translation": 0,
        "portuguese_source": 0,
    }
    skipped_samples: dict[str, list[str]] = {key: [] for key in skipped_counts}

    for path in sorted(repo_root.rglob("*.md")):
        relative = path.relative_to(repo_root)
        if path.name.endswith(".pt-br.md") or re.search(r"\.pt-br(?:[-.].*)?\.md$", path.name):
            skipped_counts["excluded_name"] += 1
            if len(skipped_samples["excluded_name"]) < 5:
                skipped_samples["excluded_name"].append(str(relative))
            continue

        if any(part in EXCLUDED_DIR_NAMES for part in relative.parts):
            skipped_counts["excluded_path"] += 1
            if len(skipped_samples["excluded_path"]) < 5:
                skipped_samples["excluded_path"].append(str(relative))
            continue

        if is_materialized_plugin_file(relative):
            skipped_counts["excluded_path"] += 1
            if len(skipped_samples["excluded_path"]) < 5:
                skipped_samples["excluded_path"].append(str(relative))
            continue

        if relative.parts[:2] == ("website", "dist") or relative.parts[:2] == ("website", ".astro"):
            skipped_counts["excluded_path"] += 1
            if len(skipped_samples["excluded_path"]) < 5:
                skipped_samples["excluded_path"].append(str(relative))
            continue

        if relative.parts and relative.parts[0] == "docs" and path.name.startswith("README."):
            skipped_counts["excluded_path"] += 1
            if len(skipped_samples["excluded_path"]) < 5:
                skipped_samples["excluded_path"].append(str(relative))
            continue

        if target_variants_exist(path):
            skipped_counts["existing_translation"] += 1
            if len(skipped_samples["existing_translation"]) < 5:
                skipped_samples["existing_translation"].append(str(relative))
            continue

        content = path.read_text(encoding="utf-8")
        if is_probably_portuguese(content):
            skipped_counts["portuguese_source"] += 1
            if len(skipped_samples["portuguese_source"]) < 5:
                skipped_samples["portuguese_source"].append(str(relative))
            continue

        manifest.append(
            ManifestEntry(
                source=str(relative).replace("\\", "/"),
                category=classify_category(repo_root, path),
                size=path.stat().st_size,
            )
        )

    return manifest, skipped_counts, skipped_samples


def select_pilot(manifest: list[ManifestEntry], size: int) -> tuple[list[str], dict[str, int]]:
    by_category: dict[str, list[ManifestEntry]] = {}
    for entry in manifest:
        by_category.setdefault(entry.category, []).append(entry)

    for entries in by_category.values():
        entries.sort(key=lambda item: (item.size, item.source))

    preferred_order = ["root", "github", "instructions", "agents", "skills"]
    selected: list[str] = []
    coverage: dict[str, int] = {category: 0 for category in preferred_order}

    for category in preferred_order:
        if len(selected) >= size:
            break
        entries = by_category.get(category, [])
        if entries:
            selected.append(entries[0].source)
            coverage[category] += 1

    pools = {key: value[1:] if value else [] for key, value in by_category.items()}
    category_cycle = [category for category in preferred_order if by_category.get(category)]
    cycle_index = 0
    while len(selected) < size:
        if not category_cycle:
            break
        category = category_cycle[cycle_index % len(category_cycle)]
        pool = pools.get(category, [])
        if pool:
            entry = pool.pop(0)
            selected.append(entry.source)
            coverage[category] = coverage.get(category, 0) + 1
        cycle_index += 1
        if cycle_index > 10000:
            break

    if len(selected) < size:
        for entry in manifest:
            if entry.source in selected:
                continue
            selected.append(entry.source)
            coverage[entry.category] = coverage.get(entry.category, 0) + 1
            if len(selected) == size:
                break

    return selected[:size], coverage


class Translator:
    def __init__(self, deeplx_url: str, deeplx_token: str, ollama_model: str) -> None:
        self.deeplx_url = deeplx_url.rstrip("/")
        self.deeplx_headers = {"Authorization": f"Bearer {deeplx_token}"}
        self.ollama_model = ollama_model

    def translate_document(self, content: str) -> str:
        frontmatter, body = split_frontmatter(content)
        translated_frontmatter = self.translate_frontmatter(frontmatter) if frontmatter else None
        translated_body = self.translate_markdown_body(body)
        deep_translated = translated_body if translated_frontmatter is None else translated_frontmatter + translated_body
        refined = self.refine_markdown_document(content, deep_translated)
        return refined if self.markdown_shape_matches(content, refined) else deep_translated

    def translate_frontmatter(self, frontmatter: str) -> str:
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
                stripped_value = value.strip()
                if (stripped_value.startswith("'") and stripped_value.endswith("'")) or (
                    stripped_value.startswith('"') and stripped_value.endswith('"')
                ):
                    quote = stripped_value[0]
                    inner = stripped_value[1:-1]
                    translated_value = self.translate_inline(inner)
                    translated_lines.append(f"{indent}{key}{separator}{quote}{translated_value}{quote}{newline}")
                else:
                    translated_value = self.translate_inline(stripped_value)
                    translated_lines.append(f"{indent}{key}{separator}{translated_value}{newline}")
                continue

            translated_lines.append(line)

        return "".join(translated_lines)

    def translate_markdown_body(self, body: str) -> str:
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

            output.append(self.translate_line(line))

        return "".join(output)

    def translate_line(self, line: str) -> str:
        if not line.strip():
            return line
        if re.fullmatch(r"\s*[-*_]{3,}\s*", line.strip()):
            return line
        if line.lstrip().startswith("|"):
            return self.translate_table_line(line)

        newline = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
        core = line[:-len(newline)] if newline else line
        prefix_match = re.match(
            r"^(\s*(?:> ?)*)"
            r"(#{1,6}\s+|[-*+]\s+|\d+\.\s+|(?:[-*+]\s+\[[ xX]\]\s+)|\[[^\]]+]:\s+)?"
            r"(.*)$",
            core,
        )
        if prefix_match:
            prefix = (prefix_match.group(1) or "") + (prefix_match.group(2) or "")
            body = prefix_match.group(3) or ""
            return prefix + self.translate_inline(body) + newline

        return self.translate_inline(core) + newline

    def translate_table_line(self, line: str) -> str:
        newline = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
        core = line[:-len(newline)] if newline else line
        if re.fullmatch(r"\s*\|?[:\-\s|]+\|?\s*", core):
            return line

        leading_pipe = core.startswith("|")
        trailing_pipe = core.endswith("|")
        cells = core.strip("|").split("|")
        translated_cells = [self.translate_inline(cell) for cell in cells]
        rebuilt = "|".join(translated_cells)
        if leading_pipe:
            rebuilt = "|" + rebuilt
        if trailing_pipe:
            rebuilt = rebuilt + "|"
        return rebuilt + newline

    def translate_inline(self, text: str) -> str:
        if not text.strip():
            return text

        def replace_image(match: re.Match[str]) -> str:
            return f"![{self.translate_plain_text(match.group(1))}]({match.group(2)})"

        def replace_link(match: re.Match[str]) -> str:
            return f"[{self.translate_plain_text(match.group(1))}]({match.group(2)})"

        text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_image, text)
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_link, text)
        return self.translate_plain_text(text)

    @lru_cache(maxsize=50000)
    def translate_plain_text(self, text: str) -> str:
        if not text.strip():
            return text

        leading = text[: len(text) - len(text.lstrip())]
        trailing = text[len(text.rstrip()) :]
        middle = text.strip()
        protected, placeholders = self.protect_literals(middle)
        translated_chunks = [self.translate_chunk(chunk) for chunk in chunk_text(protected)]
        translated = "".join(translated_chunks)

        for source, target in BRAZILIAN_REPLACEMENTS.items():
            translated = re.sub(rf"\b{re.escape(source)}\b", target, translated, flags=re.IGNORECASE)

        restored = translated
        for key, value in placeholders.items():
            restored = restored.replace(key, value)
        restored = restored.replace(" ,", ",").replace(" .", ".").replace(" :", ":")
        return leading + restored + trailing

    def protect_literals(self, text: str) -> tuple[str, dict[str, str]]:
        placeholders: dict[str, str] = {}
        protected = text

        def protect_literal(value: str) -> str:
            key = f"__PRESERVE_{len(placeholders)}__"
            placeholders[key] = value
            return key

        for term in sorted(PRESERVE_TERMS, key=len, reverse=True):
            protected = re.sub(re.escape(term), lambda match: protect_literal(match.group(0)), protected)

        patterns = [
            r"`[^`]+`",
            r"<https?://[^>]+>",
            r"https?://\S+",
            r"\{\{[^{}]+\}\}",
            r"\$\{[^{}]+\}",
            r"\{[^{}\n]+\}",
            r"\b[A-Za-z0-9_.-]+\.(?:md|json|ya?ml|toml|cs|py|ts|js|go|java|kt|rb|php|ps1|sh)\b",
        ]
        for pattern in patterns:
            protected = re.sub(pattern, lambda match: protect_literal(match.group(0)), protected)

        return protected, placeholders

    def translate_chunk(self, text: str) -> str:
        return self.call_deeplx_with_backoff(text)

    def call_deeplx_with_backoff(self, text: str, attempt: int = 0) -> str:
        status, payload = http_json(
            self.deeplx_url + "/translate",
            method="POST",
            headers=self.deeplx_headers,
            body={"text": text, "source_lang": "EN", "target_lang": "PT-BR"},
            timeout=60,
        )
        if status == 200 and isinstance(payload, dict) and payload.get("data"):
            return str(payload["data"])

        if status == 413 and len(text) > 180:
            midpoint = len(text) // 2
            split_index = text.rfind(" ", 0, midpoint)
            if split_index <= 0:
                split_index = midpoint
            return self.call_deeplx_with_backoff(text[:split_index], attempt) + self.call_deeplx_with_backoff(text[split_index:], attempt)

        if status in {408, 409, 425, 429, 500, 502, 503, 504} and attempt < 5:
            time.sleep(2 ** attempt)
            return self.call_deeplx_with_backoff(text, attempt + 1)

        raise RuntimeError(f"DeepLX translation failed with status {status}: {payload}")

    def call_gemma(self, original: str, translated: str) -> str:
        translated_word_count = max(64, len(re.findall(r"\S+", translated)) * 2)
        status, payload = http_json(
            "http://127.0.0.1:11434/api/generate",
            method="POST",
            body={
                "model": self.ollama_model,
                "prompt": PROMPT_TEMPLATE.format(original=original, translated=translated),
                "stream": False,
                "options": {
                    "temperature": 0,
                    "num_predict": min(1200, translated_word_count),
                },
            },
            timeout=120,
        )
        if status != 200 or not isinstance(payload, dict) or not payload.get("response"):
            raise RuntimeError(f"Ollama generate failed with status {status}: {payload}")
        return str(payload["response"]).strip()

    def refine_markdown_document(self, original: str, translated: str) -> str:
        original_chunks = chunk_text(original, max_chars=1800)
        translated_chunks = chunk_text(translated, max_chars=1800)
        if len(original_chunks) != len(translated_chunks):
            return translated

        refined_chunks: list[str] = []
        for original_chunk, translated_chunk in zip(original_chunks, translated_chunks):
            refined_chunks.append(self.call_gemma(original_chunk, translated_chunk))
        return "".join(refined_chunks)

    def markdown_shape_matches(self, original: str, candidate: str) -> bool:
        return (
            count_headings(original) == count_headings(candidate)
            and count_fences(original) == count_fences(candidate)
            and count_links(original) == count_links(candidate)
            and original.count("---") == candidate.count("---")
        )


def chunk_text(text: str, max_chars: int = 900) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    remaining = text
    while len(remaining) > max_chars:
        split_index = max(remaining.rfind("\n\n", 0, max_chars), remaining.rfind(". ", 0, max_chars), remaining.rfind(" ", 0, max_chars))
        if split_index <= 0:
            split_index = max_chars
        chunk = remaining[:split_index]
        remaining = remaining[split_index:]
        chunks.append(chunk)
    if remaining:
        chunks.append(remaining)
    return chunks


def count_headings(text: str) -> int:
    return len(re.findall(r"(?m)^\s*#{1,6}\s", text))


def count_fences(text: str) -> int:
    return len(re.findall(r"(?m)^\s*(```|~~~)", text))


def count_links(text: str) -> int:
    return len(re.findall(r"\[[^\]]+]\([^)]+\)", text))


def load_state(path: Path) -> State:
    if not path.exists():
        return State()
    payload = json.loads(path.read_text(encoding="utf-8"))
    return State(**payload)


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--manifest-path", default=".translation/pt-br-manifest.json")
    parser.add_argument("--state-path", default=".translation/pt-br-state.json")
    parser.add_argument("--pilot-size", type=int, default=10)
    parser.add_argument("--pilot-source", action="append", default=[])
    parser.add_argument("--deeplx-url", default=os.environ.get("DEEPLX_URL", "http://127.0.0.1:1188"))
    parser.add_argument("--ollama-model", default="translategemma:4b")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest_path = (repo_root / args.manifest_path).resolve()
    state_path = (repo_root / args.state_path).resolve()

    state = load_state(state_path)
    preflight_result = preflight(args.deeplx_url, args.ollama_model)
    state.preflight = preflight_result.__dict__
    save_json(state_path, state.__dict__)

    if preflight_result.blocker:
        raise SystemExit(json.dumps({"preflight": state.preflight}, ensure_ascii=False, indent=2))

    manifest, skipped_counts, skipped_samples = build_manifest(repo_root)
    manifest_payload = {
        "repoRoot": str(repo_root),
        "deeplxUrl": args.deeplx_url,
        "ollamaModel": args.ollama_model,
        "rules": {
            "include": ["**/*.md"],
            "excludeNames": ["*.pt-br.md", "*.pt-br-*.md", "*.pt-br.*.md"],
            "excludeDirs": sorted(EXCLUDED_DIR_NAMES),
            "excludeGenerated": ["docs/README*.md", "plugins/*/{agents,commands,skills,instructions,hooks,workflows}/**"],
            "skipPortugueseHeuristic": True,
            "skipExistingTranslationVariants": True,
        },
        "counts": {
            "eligible": len(manifest),
            **skipped_counts,
        },
        "skippedSamples": skipped_samples,
        "entries": [entry.__dict__ for entry in manifest],
    }
    save_json(manifest_path, manifest_payload)

    state.manifest_path = str(manifest_path)
    state.rules = manifest_payload["rules"]

    deeplx_token, _ = detect_deeplx_token()
    if not deeplx_token:
        raise SystemExit(json.dumps({"preflight": state.preflight, "error": "DeepLX token not found after preflight."}, ensure_ascii=False, indent=2))

    translator = Translator(args.deeplx_url, deeplx_token, args.ollama_model)
    if args.pilot_source:
        manifest_sources = {entry.source: entry for entry in manifest}
        missing_sources = [source for source in args.pilot_source if source not in manifest_sources]
        if missing_sources:
            raise SystemExit(
                json.dumps(
                    {
                        "error": "Explicit pilot sources are not eligible under the current manifest rules.",
                        "missingSources": missing_sources,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
        pilot_selection = args.pilot_source[: args.pilot_size]
        coverage: dict[str, int] = {}
        for source in pilot_selection:
            category = manifest_sources[source].category
            coverage[category] = coverage.get(category, 0) + 1
    else:
        pilot_selection, coverage = select_pilot(manifest, args.pilot_size)
    state.pilot_selection = pilot_selection
    save_json(state_path, state.__dict__)

    for relative_source in pilot_selection:
        existing = state.results.get(relative_source)
        if existing and existing.get("status") in {"translated", "skipped"}:
            continue

        source_path = repo_root / relative_source
        target_path = source_path.with_name(f"{source_path.stem}.pt-br.md")
        if target_path.exists() or target_variants_exist(source_path):
            state.results[relative_source] = {
                "status": "skipped",
                "reason": "existing translation target or variant already present",
                "target": str(target_path.relative_to(repo_root)).replace("\\", "/"),
            }
            save_json(state_path, state.__dict__)
            continue

        try:
            content = source_path.read_text(encoding="utf-8")
            newline = detect_newline(content)
            translated = translator.translate_document(content)
            if newline == "\r\n":
                translated = translated.replace("\n", "\r\n")
            target_path.write_text(translated, encoding="utf-8", newline="")
            state.results[relative_source] = {
                "status": "translated",
                "target": str(target_path.relative_to(repo_root)).replace("\\", "/"),
            }
        except Exception as exc:  # noqa: BLE001
            state.results[relative_source] = {
                "status": "failed",
                "error": str(exc),
            }
        save_json(state_path, state.__dict__)

    output = {
        "preflight": state.preflight,
        "manifestPath": str(manifest_path.relative_to(repo_root)).replace("\\", "/"),
        "pilotSelection": pilot_selection,
        "coverage": coverage,
        "results": {key: state.results.get(key) for key in pilot_selection},
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
