# fleet-fdroid

An [F-Droid](https://f-droid.org) repository for the Victorious93 fleet Android apps, built with
`fdroidserver` from each app's latest GitHub release and published on GitHub Pages.

## Add to F-Droid

Repo URL:

```
https://victorious93.github.io/fleet-fdroid/repo?fingerprint=C436CD94369BA50B041F88591752D228D1F7083E0AC8A138E1F806BF2898FF7A
```

## Apps

Listed in [`apps.txt`](apps.txt). The newest release (prereleases included) with an `.apk` asset is used;
for multi-ABI releases a universal APK is preferred, then arm64-v8a.

## Refresh

There is no schedule. The index rebuilds only when:

- someone runs the workflow manually (Actions → *Update F-Droid repo* → Run workflow), or
- a `repository_dispatch` event of type `new-release` arrives.

### Optional: trigger from a source repo on release

Add a secret `FLEET_FDROID_TOKEN` (fine-grained PAT with *Contents: read & write* on `fleet-fdroid`) to the source repo, then:

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

## License

MIT for the scripts and workflow in this repo. Each app keeps its own license.
