<div align="center">

<img src="docs/assets/logo.svg" width="420" alt="fleet-fdroid logo"/>

# fleet-fdroid

**An F-Droid repository for the Victorious fleet apps.**

<p>
  <a href="https://github.com/Victorious93/fleet-fdroid/actions/workflows/update.yml"><img src="https://img.shields.io/github/actions/workflow/status/Victorious93/fleet-fdroid/update.yml?branch=main&style=flat-square&labelColor=0B0F1A&logo=githubactions&logoColor=00E5FF&label=CI" alt="CI"/></a>
  <img src="https://img.shields.io/badge/platform-F--Droid-00E5FF?style=flat-square&labelColor=0B0F1A" alt="Platform"/>
  <a href="https://victorious-framework.pages.dev"><img src="https://img.shields.io/badge/Victorious-Framework-FF2BD6?style=flat-square&labelColor=0B0F1A" alt="Victorious Framework"/></a>
</p>

<p><a href="https://github.com/Victorious93/fleet-fdroid/releases">Releases</a> · <a href="https://victorious-framework.pages.dev">Victorious Framework</a></p>

</div>

---

## What it is

An [F-Droid](https://f-droid.org) repository for the Victorious fleet Android apps. A GitHub Actions workflow runs `fdroidserver` over each app's latest GitHub release and publishes the repo on GitHub Pages.

## Add to F-Droid

In the F-Droid client, add this repository URL (the fingerprint is included):

```
https://victorious93.github.io/fleet-fdroid/repo?fingerprint=C436CD94369BA50B041F88591752D228D1F7083E0AC8A138E1F806BF2898FF7A
```

## Apps

The list lives in [`apps.txt`](apps.txt): pyra-claw, victorgps, EDL-Commander, matchvictorious, victorious-mesh, victorlaunch, victormango, victortaskbar, victorsms, victorspoof, File-Manager, droidcommand-AI, rootforge-os and Victorious-Keyboard. For each, the newest release (prereleases included) that has an `.apk` asset is used. For multi-ABI releases a universal APK is preferred, then `arm64-v8a`. An app only appears once it has a release with an APK.

## Refreshing the index

There is no schedule. The index rebuilds only when:

- someone runs the workflow manually (Actions → *Update F-Droid repo* → Run workflow), or
- a `repository_dispatch` event of type `new-release` arrives.

### Optional: trigger from a source repo on release

Add a secret `FLEET_FDROID_TOKEN` (a fine-grained PAT with *Contents: read & write* on `fleet-fdroid`) to the source repo, then:

```yaml
# .github/workflows/notify-fdroid.yml
on:
  release:
    types: [published]
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - run: |
          curl -fsS -X POST \
            -H "Authorization: Bearer ${{ secrets.FLEET_FDROID_TOKEN }}" \
            -H "Accept: application/vnd.github+json" \
            https://api.github.com/repos/Victorious93/fleet-fdroid/dispatches \
            -d '{"event_type":"new-release","client_payload":{"repo":"${{ github.repository }}","tag":"${{ github.event.release.tag_name }}"}}'
```

Or from a shell: `gh api repos/Victorious93/fleet-fdroid/dispatches -f event_type=new-release`

## Layout

| Path | What |
|---|---|
| `apps.txt` | Source repos to publish |
| `scripts/fetch_apks.py` | Downloads each app's latest APK release asset |
| `.github/workflows/update.yml` | Builds the F-Droid index and deploys it to GitHub Pages |

---

## Victorious fleet

fleet-fdroid is part of the [Victorious Framework](https://victorious-framework.pages.dev), a family of Android and PC tools by Don Victor. **Every app works standalone; fleet integrations are optional** and never required.

Related: [victorious-fleet](https://github.com/Victorious93/victorious-fleet) (index of all fleet apps), [fleet-manifest](https://github.com/Victorious93/fleet-manifest) (fleet status feed), [droidcommand-AI](https://github.com/Victorious93/droidcommand-AI) (fleet controller). The full roster lives in [victorious-fleet](https://github.com/Victorious93/victorious-fleet), and live status is in [fleet-manifest](https://github.com/Victorious93/fleet-manifest).

## Contributing

Issues and pull requests are welcome. Keep changes focused, match the existing code style, never commit secrets or release keys, and keep any fleet integration optional so the app still works on its own. Open a PR against the default branch and wait for CI to pass.

## License

The README states: MIT for the scripts and workflow in this repo; each app keeps its own license. There is no LICENSE file in the repository yet, so this statement is the only licensing text.
