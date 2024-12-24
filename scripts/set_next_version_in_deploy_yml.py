"""
Update the default version tag in the deploy.yml file.

```yaml
on:
  workflow_dispatch:
    inputs:
      version-tag:
        description: 'Version tag'
        required: true
        default: 'v0.1.0'  # <-- HERE

# ...
```
"""

import sys
from pathlib import Path

import ruamel.yaml


def unidiff_output(expected: str, actual: str):
    """Returns a string containing the unified diff of two multiline strings."""
    import difflib

    expected_list = expected.splitlines(keepends=True)
    actual_list = actual.splitlines(keepends=True)

    diff = difflib.unified_diff(expected_list, actual_list)

    return "".join(diff)


if len(sys.argv) != 3:
    print(
        "Usage: python increase_version_in_deploy_yml.py <deploy.yml> <current_version>"
    )
    print(
        "Example: python increase_version_in_deploy_yml.py .github/workflows/_deploy.yml v0.1.0"
    )
    print(
        "This script will set on.workflow_dispatch.inputs.version-tag.default to v0.1.1"
    )
    sys.exit(1)

deploy_yml = sys.argv[1]
current_version = sys.argv[2]

split_version = current_version.split(".")
last_digit = int(split_version[-1])
split_version[-1] = str(last_digit + 1)
new_version = ".".join(split_version)

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)
original_yml_content = Path(deploy_yml).read_text()
with open(deploy_yml) as f:
    data = yaml.load(f)
data["on"]["workflow_dispatch"]["inputs"]["version-tag"]["default"] = new_version

with open(deploy_yml, "w") as f:
    yaml.dump(data, f)

new_yml_content = Path(deploy_yml).read_text()
if original_yml_content == new_yml_content:
    print(f"Version was already set to {new_version}")
else:
    print(unidiff_output(original_yml_content, new_yml_content))
