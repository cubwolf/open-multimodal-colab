#!/usr/bin/env bash
# open-multimodal-colab installer for macOS / Linux.
# 1 uv  2 Python 3.12 + google-colab-cli 0.7.4  3 settings (no update check)  4 copy the skill into the agent's skills folder.
# The models are downloaded on the Colab GPU (or by omlocal.py setup), not here.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="${1:-}"

if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv ..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi
uv python install 3.12
uv tool install --force --python 3.12 "google-colab-cli==0.7.4"
export PATH="$HOME/.local/bin:$PATH"
uv run --python 3.12 python "$REPO/install/patch_colab_cli.py" || true

targets=()
if [ -n "$SKILLS_DIR" ]; then targets+=("$SKILLS_DIR"); else
  for d in "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.hermes/skills" "$HOME/.agents/skills"; do
    [ -d "$(dirname "$d")" ] && targets+=("$d")
  done
fi
[ ${#targets[@]} -eq 0 ] && targets=("$HOME/.claude/skills")
for t in "${targets[@]}"; do
  mkdir -p "$t"
  rm -rf "$t/open-multimodal-colab"
  cp -R "$REPO/open-multimodal-colab" "$t/open-multimodal-colab"
  echo "Skill installed: $t/open-multimodal-colab"
done
colab --help >/dev/null && echo "colab CLI OK"
echo "Next: python <skill>/scripts/colab_login.py url"
