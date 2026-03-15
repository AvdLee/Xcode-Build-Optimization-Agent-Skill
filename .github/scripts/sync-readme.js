const fs = require("fs");
const path = require("path");

const README_PATH = path.join(process.cwd(), "README.md");
const SKILLS_ROOT = path.join(process.cwd(), "skills");
const SKILL_DIRS = [
  "xcode-build-benchmark",
  "xcode-compilation-analyzer",
  "xcode-project-analyzer",
  "spm-build-analysis",
  "xcode-build-orchestrator",
  "xcode-build-fixer",
];

const beginMarker = "<!-- BEGIN SKILL STRUCTURE -->";
const endMarker = "<!-- END SKILL STRUCTURE -->";

const describeReference = (fileName) => {
  const descriptions = {
    "benchmarking-workflow.md": "Benchmark contract, clean vs incremental rules, and artifact expectations",
    "code-compilation-checks.md": "Swift compile hotspot checks and code-level heuristics",
    "project-audit-checks.md": "Build setting, script phase, and dependency audit checklist",
    "spm-analysis-checks.md": "Package graph, plugin overhead, and module variant review guide",
    "orchestration-report-template.md": "Prioritization, approval, and verification report template",
    "fix-patterns.md": "Concrete before/after patterns for each fix category",
  };
  return descriptions[fileName] || "Reference file";
};

const buildTree = () => {
  const lines = [
    "xcode-build-optimization-agent-skill/",
    "  .claude-plugin/",
    "    marketplace.json",
    "    plugin.json",
    "  references/",
    "    benchmark-artifacts.md",
    "    build-optimization-sources.md",
    "    build-settings-best-practices.md",
    "    recommendation-format.md",
    "  schemas/",
    "    build-benchmark.schema.json",
    "  scripts/",
    "    benchmark_builds.py",
    "    diagnose_compilation.py",
    "    generate_optimization_report.py",
    "    render_recommendations.py",
    "    summarize_build_timing.py",
    "  skills/",
  ];

  for (const skillDir of SKILL_DIRS) {
    lines.push(`    ${skillDir}/`);
    lines.push("      SKILL.md");
    const referencesDir = path.join(SKILLS_ROOT, skillDir, "references");
    if (!fs.existsSync(referencesDir)) {
      continue;
    }
    const references = fs
      .readdirSync(referencesDir)
      .filter((entry) => entry.endsWith(".md"))
      .sort((left, right) => left.localeCompare(right));
    if (references.length === 0) {
      continue;
    }
    lines.push("      references/");
    for (const fileName of references) {
      lines.push(`        ${fileName} - ${describeReference(fileName)}`);
    }
  }

  return `\`\`\`text\n${lines.join("\n")}\n\`\`\``;
};

const syncReadme = () => {
  if (!fs.existsSync(README_PATH)) {
    throw new Error("README.md not found.");
  }

  const readme = fs.readFileSync(README_PATH, "utf8");
  const start = readme.indexOf(beginMarker);
  const end = readme.indexOf(endMarker);

  if (start === -1 || end === -1 || end <= start) {
    throw new Error("README skill structure markers not found.");
  }

  const prefix = readme.slice(0, start + beginMarker.length);
  const suffix = readme.slice(end);
  const replacement = `\n${buildTree()}\n`;
  const updated = `${prefix}${replacement}${suffix}`;

  if (updated !== readme) {
    fs.writeFileSync(README_PATH, updated);
    console.log("README structure block updated.");
  } else {
    console.log("README already up to date.");
  }
};

syncReadme();
