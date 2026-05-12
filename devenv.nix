{ pkgs, lib, config, inputs, ... }:

{
  # Tools shared by every contributor. Anything driven by lefthook.yml or the
  # /blog and /wiki-* skills must be reachable from this shell.
  packages = with pkgs; [
    # Site build
    hugo                 # nixpkgs ships the extended build

    # Lint / hook drivers (lefthook.yml が PATH 経由で呼ぶ)
    lefthook
    shellcheck
    markdownlint-cli2
    ast-grep
    git-secrets
    ruff
    black

    # GitHub workflow
    gh
    git
  ];

  # Python は uv 管理。requirements.txt を venv に流し込むのは devenv 側に任せる。
  # pyproject.toml に移行したら languages.python.uv.sync.enable に切り替える。
  languages.python = {
    enable = true;
    package = pkgs.python312;
    uv.enable = true;
    venv = {
      enable = true;
      requirements = ./requirements.txt;
    };
  };

  scripts.hugo-serve = {
    exec = "hugo server --disableFastRender --buildDrafts --bind 0.0.0.0";
    description = "Hugo を draft 込みで localhost 起動";
  };

  scripts.hugo-check = {
    exec = "hugo --gc --quiet --destination .claude/temp/hugo-check";
    description = "lefthook pre-push と同等の build チェック";
  };

  scripts.drawio-export = {
    exec = ''exec ${./scripts/drawio-export.sh} "$@"'';
    description = "static/images/*.drawio を PNG/SVG にエクスポート (drawio-headless via Docker)";
  };

  scripts.wiki-lint = {
    exec = ''exec python3 .claude/skills/wiki-lint/scripts/wiki_lint.py "$@"'';
    description = "Wiki 健全性チェック";
  };

  enterShell = ''
    # 1. lefthook を冪等に install
    # ユーザー global の core.hooksPath が Nix store を指す環境では lefthook の
    # sync が読み取り専用ディレクトリを更新しようとするため、この repo は
    # 書き込み可能な .git/hooks を local 設定で使う。
    git config --local core.hooksPath .git/hooks
    if [ ! -f .git/hooks/pre-commit ] || ! grep -q lefthook .git/hooks/pre-commit 2>/dev/null; then
      lefthook install --force >/dev/null && echo "✓ lefthook hooks installed"
    fi

    # 2. Docker (drawio-export 用) はオプション扱い
    if ! command -v docker >/dev/null 2>&1; then
      echo "⚠️  docker not found — drawio-export will fail until Docker is installed."
    fi

    # 3. version banner
    echo "📚 hugo $(hugo version 2>/dev/null | awk '{print $2; exit}')  |  python $(python3 --version 2>&1 | awk '{print $2}')  |  lefthook $(lefthook version 2>/dev/null)"
  '';

  enterTest = ''
    hugo --gc --quiet --destination .claude/temp/hugo-check
    python3 .claude/skills/wiki-lint/scripts/wiki_lint.py
  '';

  # 注: git-hooks (旧 pre-commit-hooks) は使わない。
  # フック定義は lefthook.yml が source of truth。
  # See full reference at https://devenv.sh/reference/options/
}
