# APPEDU2026

## Knowledge base

- `docs/motion-design/README.md`: motion design with Claude Code and HyperFrames (the HTML-to-video engine of
  heygen-com/hyperframes and the 5-step method of cblain100-prog/motion-design-claude-code). Read it, or use the
  `motion-design-hyperframes` skill, for any request about an animated video, a storyboard or HyperFrames.
- `docs/motion-design/skills-catalog.md`: the third-party motion and web design skills installed in
  `.claude/skills/`, what each is for, its source commit, licence and status. Some are not committed (licence or
  size): run `bash tools/motion-skills/fetch.sh skills` at the start of a session that needs them, and
  `fetch.sh libraries` or `fetch.sh references` for the Opus/Claude Club libraries and the reference websites.

## Third-party skills

- They are pinned to the commit that was audited. Never update or add one with `npx skills add`, `@latest` or a
  branch tip: audit the new version first (licence, network calls, remote execution, hidden instructions), then
  change the commit in `tools/motion-skills/fetch.sh` or recopy the folder, and update the catalogue.
- Respect the licences listed in the catalogue: `liam-motion-library` and `video-talkcraft` are non-commercial
  without their author's consent; repositories without a licence are references to study, never code to copy.
- `howseen-motion-design` is another studio's pipeline: use its techniques, never its brand, paths or facts.
- Offensive / dual-use security tools (`recon`, `watchtower`) are NOT installed as skills and NOT auto-fetched.
  `bash tools/motion-skills/fetch.sh security` fetches them to `vendor/security-tools/` only on an explicit,
  authorized request, for use solely against targets the user is authorized to test.
