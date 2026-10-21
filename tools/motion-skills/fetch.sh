#!/bin/bash
# Fetches the motion/web design material that is NOT committed to this repository, each at the exact commit that
# was audited (see docs/motion-design/skills-catalog.md). Nothing is ever fetched at a branch tip or @latest.
#
#   skills      skills whose licence allows a local install but not redistribution: transitions.dev (3 skills),
#               code-liam motion library (non-commercial), video-talkcraft (PolyForm Noncommercial)
#               -> .claude/skills/<name>/ (git-ignored)
#   libraries   large libraries used by committed skills: Opus Motion Library, Claude Club catalogue -> vendor/
#   references  websites and unlicensed skill repositories, to study only -> vendor/web-references/
#   all         the three
#
# usage: bash tools/motion-skills/fetch.sh [skills|libraries|references|all]   (default: skills)
# Idempotent: an item already present at its pinned commit is skipped.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WHAT="${1:-skills}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
export GIT_LFS_SKIP_SMUDGE=1

# fetch <owner/repo> <sha> <destination> [subpath] [exclude...]
fetch() {
  local repo="$1" sha="$2" dest="$3" sub="${4:-.}"
  shift 4 || shift $#
  if [ -f "$dest/.pinned-commit" ] && [ "$(cat "$dest/.pinned-commit")" = "$repo@$sha" ]; then
    echo "  ok      $repo@${sha:0:7} -> ${dest#$ROOT/}"
    return
  fi
  local work="$TMP/$(echo "$repo" | tr '/' '_')"
  if [ ! -d "$work/.git" ]; then
    git init -q "$work"
    git -C "$work" fetch -q --depth 1 "https://github.com/$repo" "$sha"
    git -C "$work" -c advice.detachedHead=false checkout -q FETCH_HEAD
  fi
  rm -rf "$dest"
  mkdir -p "$dest"
  local args=(--exclude .git --exclude node_modules)
  for x in "$@"; do args+=(--exclude "$x"); done
  (cd "$work/$sub" && tar cf - "${args[@]}" .) | (cd "$dest" && tar xf -)
  echo "$repo@$sha" > "$dest/.pinned-commit"
  echo "  fetched $repo@${sha:0:7} -> ${dest#$ROOT/}"
}

SK="$ROOT/.claude/skills"
VEN="$ROOT/vendor"

if [ "$WHAT" = skills ] || [ "$WHAT" = all ]; then
  echo "skills (local install only, licences forbid redistribution):"
  T=7ec0b0b0b8beb15788a9de68a40ec6be2d5e84b5
  for s in transitions-dev transitions-polish transitions-ui-generation; do
    fetch Jakubantalik/transitions.dev $T "$SK/$s" "skills/$s"
  done
  fetch linhaixin45-cmyk/code-liam-motion-library 80e9a0926dd59d5aba8ce332370d7dce82ad4d85 "$SK/liam-motion-library" . ./tests
  fetch Vincentwei1021/video-talkcraft a7c29edfb2404612dde6a5a1c8aa94232e85625b "$SK/video-talkcraft" . ./gallery
fi

if [ "$WHAT" = libraries ] || [ "$WHAT" = all ]; then
  echo "libraries:"
  fetch GovinduSasanka/opus-motion-library d3876a454762aa80345d95b350fc8647fbc7e902 "$VEN/opus-motion-library" . ./gallery ./site
  fetch Samin12/claude-club-motion-library-skill 455465699a25c8dd8ecf0af20ef8c5fc12d3972e "$VEN/claude-club-motion-library" . ./site ./skills
fi

if [ "$WHAT" = references ] || [ "$WHAT" = all ]; then
  echo "references (study only; copy code only from the MIT ones, see the catalogue):"
  R="$VEN/web-references"
  fetch NaeMyoAungKhing/mctc-website cf94a8da79e01bf0ddd5ad953c84755e7280f2c0 "$R/mctc-website"
  fetch cristianoleamiranda-dotcom/scroll-craft b9c8e5b6c5da42c6c95dd96cb3b557850b80d3e9 "$R/scroll-craft-site"
  fetch sukhmandult4-web/Animated_website_CSS_HTML 22655ec6a67ec75b52fa08742ce105f36832afb2 "$R/animated-website-css-html"
  fetch thebuggeddev/futureride aa6b4c526c441ea4d6defb9d22d2a183da5b5b2b "$R/futureride"
  fetch mscbuild/web-portfolio fd81ece6d283868473d0a44c50e4eb833b79c082 "$R/web-portfolio"
  fetch pennyp973/3d--motion-website c8d5a41e008d387513203b5cda34b1fdc03cce4a "$R/3d-motion-website"
  fetch ronniejbotes/claude-skills 266aa8aa5158cb2e172dae8cd83f381cc50f2f0e "$R/immersive-3d-site-skill"
  fetch Pluviobyte/video-production-skills e19f1f300eddbb4f73764e66849792ece94ff0b7 "$R/pluviobyte-video-production-skills"
fi
