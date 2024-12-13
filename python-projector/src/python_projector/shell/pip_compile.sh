#!/usr/bin/env bash

# This script compiles all requirements.in files to requirements.txt files
# This means that all dependencies are locked to a specific version
# Plus, it checks if the requirements.in file has changed since the last time it was compiled
# If not, it skips the file rather than recompiling it (which may change version unnecessarily often)

if [[ $# -lt 3 ]]; then
    echo "Usage: $0 <requirements_in_dir> <requirements_out_dir> <python_version> <python_platforms_comma_separated>" >&2
    exit 1
fi

if ! command -v uv &> /dev/null; then
	echo "uv is not installed. Please run 'pip3 install --user uv'" >&2
	exit 1
fi

if ! command -v sha256sum &> /dev/null; then
	echo "sha256sum is not installed." >&2
	echo "If you're on Mac, run 'brew install coreutils'" >&2
	exit 1
fi

if [[ $# -lt 4 ]]; then
    TARGET_PLATFORMS=(x86_64-manylinux_2_28 aarch64-apple-darwin x86_64-apple-darwin)
else
    IFS=',' read -r -a TARGET_PLATFORMS <<< "$4"
fi

REQUIREMENTS_IN_DIR="$1"
# realpath alternative
# shellcheck disable=SC2164
REQUIREMENTS_OUT_DIR="$(cd "$(dirname -- "$2")" >/dev/null; pwd -P)/$(basename -- "$2")"
PYTHON_VERSION="$3"

# SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# REQUIREMENTS_IN_DIR="$SCRIPT_DIR/../deps"
# REQUIREMENTS_OUT_DIR="$SCRIPT_DIR/../deps"

# NOTE: sha256sum will put the file path in the hash file.
# To simplify the directory (using relative paths), we change the working directory.
cd "$REQUIREMENTS_IN_DIR" || { echo "Failure"; exit 1; }

for platform in "${TARGET_PLATFORMS[@]}"; do
    mkdir -p "$REQUIREMENTS_OUT_DIR/$platform"
done

shopt -s globstar

function get_shafile() {
	local file=$1
    local target_platform=$2
    # .requirements.in.sha256
    echo "$REQUIREMENTS_OUT_DIR/$target_platform/.$file.sha256"
}

function get_lockfile() {
	local file=$1
    local target_platform=$2
    # requirements.txt
    echo "$REQUIREMENTS_OUT_DIR/$target_platform/${file%.in}.txt"
}

function file_content_changed() {
	# Check if the file has changed since the last time it was compiled, using the hash file.
	# NOTE: returns 0 if the file has changed
	local file=$1
    local target_platform=$2
	local shafile
	shafile=$(get_shafile "$file" "$target_platform")
	if [[ -f "$shafile" ]] && sha256sum -c "$shafile" &> /dev/null; then
		return 1
	fi
	return 0
}


function deps_changed() {
	# Check if the requirements*.in file has changed since the last time it was compiled, including its dependencies (-r another_requirements.in).
	#
	# When the requirements have dependencies on other requirements files, we need to check if those have changed as well
	# e.g. requirements_dev.in has a dependency on requirements.in (-r requirements.in)
	# Note that we also need to recursively check if the dependencies of the dependencies have changed.
	# We need to recompile requirements_dev.txt if requirements.in has changed.
	# NOTE: returns 0 if the deps have changed
	local file=$1
    local target_platform=$2

	if file_content_changed "$file" "$target_platform"; then
		return 0
	fi


	local file_deps
	file_deps=$(grep -Eo -- '-r [^ ]+' "$file")
	file_deps=${file_deps//"-r "/}  # remove -r
	for dep in $file_deps; do
		echo "ℹ️ $file depends on $dep"
		dep=${dep#-r }  # requirements.in
		if deps_changed "$dep" "$target_platform"; then
			return 0
		fi
	done
	return 1
}

num_files=0
num_up_to_date=0
files_changed=()

# First, collect all files that need to be compiled.
# We don't compile them yet, because it will mess up the hash comparison.
for file in requirements*.in; do
    for target_platform in "${TARGET_PLATFORMS[@]}"; do
        # $file: requirements.in
        ((num_files++))

        lockfile=$(get_lockfile "$file" "$target_platform")
        shafile=$(get_shafile "$file" "$target_platform")
        # Process only changed files by comparing hash
        if [[ -f "$lockfile" ]]; then
            if ! deps_changed "$file" "$target_platform"; then
                echo "⚡ Skipping $file due to no changes"
                ((num_up_to_date++))
                continue
            fi
        fi
        files_changed+=("$file")
    done
done

for file in "${files_changed[@]}"; do
    for target_platform in "${TARGET_PLATFORMS[@]}"; do
        lockfile=$(get_lockfile "$file" "$target_platform")
        shafile=$(get_shafile "$file" "$target_platform")
        echo "🔒 Generating lockfile $lockfile from $file"

        uv pip compile "$file" -o "$lockfile" --python-platform "$target_platform" --python-version "$PYTHON_VERSION" > /dev/null
        RC=$?
        if [[ $RC -eq 0 ]]; then
            sha256sum "$file" > "$shafile"  # update hash
        else
            echo "❌ Failed to compile $file"
            exit $RC
        fi
    done
done

# exit code 2 when all files are up to date
if [[ $num_files -eq $num_up_to_date ]]; then
	echo "💖 All files are up to date!"
	exit 2
fi

