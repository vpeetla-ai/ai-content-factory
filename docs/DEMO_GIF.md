# Recording the README demo GIF

A 30–60 second screen recording is the highest-impact README upgrade for GitHub stars. Replace the placeholder once recorded.

## What to capture

1. Open [live demo](https://ai-content-factory-iota.vercel.app) or local `http://localhost:3000`
2. Sign in (or dev bypass locally)
3. Submit a topic (e.g. "Benefits of multi-agent systems in production")
4. Show agent log streaming (research → content → enrich)
5. **Pause on HITL review** — this is your differentiator
6. Approve one draft and show completion

Keep it under 60 seconds. No audio required.

## Tools (macOS)

| Tool | Command / link |
|------|----------------|
| **CleanShot X** | Record → GIF export |
| **Kap** | Free, open source — [getkap.co](https://getkap.co) |
| **ffmpeg** | `ffmpeg -i demo.mov -vf "fps=10,scale=960:-1" docs/assets/demo.gif` |

## After recording

1. Save as `docs/assets/demo.gif` (target width ~960px, &lt; 5 MB)
2. Update `README.md` image line:

```markdown
![AI Content Factory pipeline demo](docs/assets/demo.gif)
```

3. Commit and push:

```bash
git add docs/assets/demo.gif README.md
git commit -m "Add pipeline demo GIF to README"
git push origin main
```

## Optional: hosted GIF

For faster README loads, upload to GitHub Releases or a CDN and use that URL in the README instead of committing a large binary.
