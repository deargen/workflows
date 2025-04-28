"use strict";
const fs = require("node:fs");
const core = require("@actions/core");
async function main() {
  const changelogPath = core.getInput("changelog-path");
  const targetVersion = core.getInput("version");
  let chglog = "";
  try {
    chglog = await fs.promises.readFile(changelogPath, "utf8");
  } catch (err) {
    return core.setFailed(`Couldn't find a ${changelogPath}`);
  }
  const lines = chglog.replace(/\r/g, "").split("\n");
  const versionSectionStart = lines.findIndex(
    (l) => l.startsWith(`## [${targetVersion}]`)
  );
  if (versionSectionStart < 0) {
    return core.setFailed(
      `Couldn't find the section for version ${targetVersion} in the CHANGELOG: no line with "## [${targetVersion}]". Please follow the "Keep a Changelog" format.`
    );
  }
  let versionSectionEnd = lines.findIndex((l, i) => {
    if (i <= versionSectionStart) {
      return false;
    }
    if (l.startsWith("## [")) {
      return true;
    }
    return false;
  });
  if (versionSectionEnd < 0) {
    versionSectionEnd = lines.length;
  }
  const versionSectionBody = lines.slice(
    versionSectionStart + 1,
    versionSectionEnd
  );
  core.setOutput("body", versionSectionBody.join("\n").trim());
}
main();
