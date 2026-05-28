#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { ROOT_FOLDER } from "./constants.mjs";

const PLUGINS_DIR = path.join(ROOT_FOLDER, "plugins");

// Validation functions
function validateName(name, folderName) {
  const errors = [];
  if (!name || typeof name !== "string") {
    errors.push("name is required and must be a string");
    return errors;
  }
  if (name.length < 1 || name.length > 50) {
    errors.push("name must be between 1 and 50 characters");
  }
  if (!/^[a-z0-9-]+$/.test(name)) {
    errors.push("name must contain only lowercase letters, numbers, and hyphens");
  }
  if (name !== folderName) {
    errors.push(`name "${name}" must match folder name "${folderName}"`);
  }
  return errors;
}

function validateDescription(description) {
  if (!description || typeof description !== "string") {
    return "description is required and must be a string";
  }
  if (description.length < 1 || description.length > 500) {
    return "description must be between 1 and 500 characters";
  }
  return null;
}

function validateVersion(version) {
  if (!version || typeof version !== "string") {
    return "version is required and must be a string";
  }
  return null;
}

function validateKeywords(keywords) {
  if (keywords === undefined) return null;
  if (!Array.isArray(keywords)) {
    return "keywords must be an array";
  }
  if (keywords.length > 10) {
    return "maximum 10 keywords allowed";
  }
  for (const keyword of keywords) {
    if (typeof keyword !== "string") {
      return "all keywords must be strings";
    }
    if (!/^[a-z0-9-]+$/.test(keyword)) {
      return `keyword "${keyword}" must contain only lowercase letters, numbers, and hyphens`;
    }
    if (keyword.length < 1 || keyword.length > 30) {
      return `keyword "${keyword}" must be between 1 and 30 characters`;
    }
  }
  return null;
}

function stripOptionalSuffix(value, suffixes) {
  for (const suffix of suffixes) {
    if (value.endsWith(suffix)) {
      return value.slice(0, -suffix.length);
    }
  }
  return value;
}

function validateAgentPath(entry, index) {
  if (typeof entry !== "string") {
    return [`agents[${index}] must be a string`];
  }
  if (!entry.startsWith("./")) {
    return [`agents[${index}] must start with "./"`];
  }
  if (entry === "./agents") {
    return [];
  }
  if (!entry.startsWith("./agents/")) {
    return [`agents[${index}] must be "./agents" or start with "./agents/"`];
  }

  const basename = stripOptionalSuffix(entry.slice("./agents/".length), [".agent.md", ".md", "/"]);
  if (!basename || basename.includes("/")) {
    return [`agents[${index}] must reference a single agent path`];
  }

  const candidateFiles = [
    path.join(ROOT_FOLDER, "agents", `${basename}.agent.md`),
    path.join(ROOT_FOLDER, "agents", `${basename}.md`),
  ];

  if (!candidateFiles.some((candidate) => fs.existsSync(candidate))) {
    return [`agents[${index}] source not found: agents/${basename}.agent.md`];
  }

  return [];
}

function validateSkillPath(entry, index) {
  if (typeof entry !== "string") {
    return [`skills[${index}] must be a string`];
  }
  if (!entry.startsWith("./")) {
    return [`skills[${index}] must start with "./"`];
  }
  if (!entry.startsWith("./skills/")) {
    return [`skills[${index}] must start with "./skills/"`];
  }

  const basename = stripOptionalSuffix(entry.slice("./skills/".length), ["/"]);
  if (!basename || basename.includes("/")) {
    return [`skills[${index}] must reference a single skill directory`];
  }

  const skillFile = path.join(ROOT_FOLDER, "skills", basename, "SKILL.md");
  if (!fs.existsSync(skillFile)) {
    return [`skills[${index}] source not found: skills/${basename}/SKILL.md`];
  }

  return [];
}

function validateCommandPath(entry, index) {
  if (typeof entry !== "string") {
    return [`commands[${index}] must be a string`];
  }
  if (!entry.startsWith("./")) {
    return [`commands[${index}] must start with "./"`];
  }
  if (!(entry === "./commands" || entry.startsWith("./commands/"))) {
    return [`commands[${index}] must be "./commands" or start with "./commands/"`];
  }

  const commandPath = path.join(ROOT_FOLDER, entry.slice("./".length));
  if (!fs.existsSync(commandPath)) {
    return [`commands[${index}] source not found: ${entry.slice("./".length)}`];
  }

  return [];
}

function validateSpecPaths(plugin) {
  const errors = [];
  const validators = {
    agents: validateAgentPath,
    skills: validateSkillPath,
    commands: validateCommandPath,
  };

  for (const [field, validateEntry] of Object.entries(validators)) {
    const arr = plugin[field];
    if (arr === undefined) continue;
    if (!Array.isArray(arr)) {
      errors.push(`${field} must be an array`);
      continue;
    }
    for (let i = 0; i < arr.length; i++) {
      errors.push(...validateEntry(arr[i], i));
    }
  }
  return errors;
}

function validatePlugin(folderName) {
  const pluginDir = path.join(PLUGINS_DIR, folderName);
  const errors = [];

  // Rule 1: Must have .github/plugin/plugin.json
  const pluginJsonPath = path.join(pluginDir, ".github/plugin", "plugin.json");
  if (!fs.existsSync(pluginJsonPath)) {
    errors.push("missing required file: .github/plugin/plugin.json");
    return errors;
  }

  // Rule 2: Must have README.md
  const readmePath = path.join(pluginDir, "README.md");
  if (!fs.existsSync(readmePath)) {
    errors.push("missing required file: README.md");
  }

  // Parse plugin.json
  let plugin;
  try {
    const raw = fs.readFileSync(pluginJsonPath, "utf-8");
    plugin = JSON.parse(raw);
  } catch (err) {
    errors.push(`failed to parse plugin.json: ${err.message}`);
    return errors;
  }

  // Rule 3 & 4: name, description, version
  const nameErrors = validateName(plugin.name, folderName);
  errors.push(...nameErrors);

  const descError = validateDescription(plugin.description);
  if (descError) errors.push(descError);

  const versionError = validateVersion(plugin.version);
  if (versionError) errors.push(versionError);

  // Rule 5: keywords (or tags for backward compat)
  const keywordsError = validateKeywords(plugin.keywords ?? plugin.tags);
  if (keywordsError) errors.push(keywordsError);

  // Rule 6: agents, commands, skills paths
  const specErrors = validateSpecPaths(plugin);
  errors.push(...specErrors);

  return errors;
}

// Main validation function
function validatePlugins() {
  if (!fs.existsSync(PLUGINS_DIR)) {
    console.log("No plugins directory found - validation skipped");
    return true;
  }

  const pluginDirs = fs
    .readdirSync(PLUGINS_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name);

  if (pluginDirs.length === 0) {
    console.log("No plugin directories found - validation skipped");
    return true;
  }

  console.log(`Validating ${pluginDirs.length} plugins...\n`);

  let hasErrors = false;
  const seenNames = new Set();

  for (const dir of pluginDirs) {
    console.log(`Validating ${dir}...`);

    const errors = validatePlugin(dir);

    if (errors.length > 0) {
      console.error(`❌ ${dir}:`);
      errors.forEach((e) => {
        console.error(`   - ${e}`);
      });
      hasErrors = true;
    } else {
      console.log(`✅ ${dir} is valid`);
    }

    // Rule 10: duplicate names
    if (seenNames.has(dir)) {
      console.error(`❌ Duplicate plugin name "${dir}"`);
      hasErrors = true;
    } else {
      seenNames.add(dir);
    }
  }

  if (!hasErrors) {
    console.log(`\n✅ All ${pluginDirs.length} plugins are valid`);
  }

  return !hasErrors;
}

// Run validation
try {
  const isValid = validatePlugins();
  if (!isValid) {
    console.error("\n❌ Plugin validation failed");
    process.exit(1);
  }
  console.log("\n🎉 Plugin validation passed");
} catch (error) {
  console.error(`Error during validation: ${error.message}`);
  process.exit(1);
}
