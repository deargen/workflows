"use strict";
require("os");
require("crypto");
require("fs");
require("path");
require("http");
require("https");
require("net");
require("tls");
require("events");
require("assert");
require("util");
require("stream");
require("buffer");
require("querystring");
require("stream/web");
require("worker_threads");
require("perf_hooks");
require("util/types");
require("async_hooks");
require("console");
require("url");
require("zlib");
require("string_decoder");
require("diagnostics_channel");
require("child_process");
require("timers");
const fs = {};
async function main() {
  const changelogPath = (void 0)("changelog-path");
  const targetVersion = (void 0)("version");
  let chglog = "";
  try {
    chglog = await fs.promises.readFile(changelogPath, "utf8");
  } catch (err) {
    return (void 0)(`Couldn't find a ${changelogPath}`);
  }
  const lines = chglog.replace(/\r/g, "").split("\n");
  const versionSectionStart = lines.findIndex(
    (l) => l.startsWith(`## [${targetVersion}]`)
  );
  if (versionSectionStart < 0) {
    return (void 0)(
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
  (void 0)("body", versionSectionBody.join("\n").trim());
}
main();
//# sourceMappingURL=index.js.map
