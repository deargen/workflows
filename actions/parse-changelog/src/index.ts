import fs from "node:fs"
import * as core from "@actions/core"

// [v1.1.0]: https://github.com/*/*/compare/v1.0.0...v1.1.0
const byReferenceLinkForVersion =
  /^\[.*\]: https?:\/\/github.com\/.*\/.*\/compare\/.*\.\.\.\.*$/

async function main() {
  const changelogPath = core.getInput("changelog-path")
  const targetVersion = core.getInput("version")

  let chglog = ""

  try {
    chglog = await fs.promises.readFile(changelogPath, "utf8")
  } catch (err) {
    return core.setFailed(`Couldn't find a ${changelogPath}`)
  }

  const lines = chglog.replace(/\r/g, "").split("\n")

  // Find the section for the target version.
  // ## [0.0.2] - 2023-10-02
  // ... // <- this is the section we want to return
  // ## [0.0.1] - 2023-10-01

  const versionSectionStart = lines.findIndex((l: string) =>
    l.startsWith(`## [${targetVersion}]`),
  )

  if (versionSectionStart < 0) {
    return core.setFailed(
      `Couldn't find the section for version ${targetVersion} in the CHANGELOG: no line with "## [${targetVersion}]". Please follow the "Keep a Changelog" format.`,
    )
  }

  let versionSectionEnd = lines.findIndex((l: string, i: number) => {
    if (i <= versionSectionStart) {
      return false
    }

    // The next section starts with "## ["
    if (l.startsWith("## [")) {
      return true
    }

    // or it is the By-Reference Link like
    // [v1.1.0]: https://github.com/*/*/compare/v1.0.0...v1.1.0
    if (l.match(byReferenceLinkForVersion)) {
      return true
    }

    return false
  })

  if (versionSectionEnd < 0) {
    // No next section found, so we take the rest of the file.
    versionSectionEnd = lines.length
  }

  // Get the lines for the target version section, excluding the header.
  const versionSectionBody = lines.slice(
    versionSectionStart + 1,
    versionSectionEnd,
  )

  core.setOutput("body", versionSectionBody.join("\n").trim())
}

main()
