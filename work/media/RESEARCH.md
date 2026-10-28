# Verified song media research

Verified 2026-10-28 (Asia/Taipei). All 21 catalog keys have exact Spotify track links and official artwork URLs in `media-map.json`. No Spotify tracks unresolved.

## Verification

1. Used the public [Kworb Fujii Kaze song index](https://kworb.net/spotify/artist/6bDWAcdtVR3WHz2xtiIPUi_songs.html) only to discover track IDs.
2. Queried Spotify official oEmbed for each exact track link and saved returned title and thumbnail.
3. Read each official Spotify embed document's public entity metadata and asserted the exact song title and artist URI `spotify:artist:6bDWAcdtVR3WHz2xtiIPUi` (Fujii Kaze).
4. Selected the 640px cover URL explicitly returned by Spotify's metadata; retained oEmbed's 300px thumbnail too. URLs were not guessed or rewritten. Saved sanitized title/artist/date/duration/image metadata per song.

## Integration

Use `coverUrl` in both catalog and song page; link it or nearby Spotify attribution to `coverSourceUrl`. Use `spotify` for exact track playback link. Keep artwork uncropped and without color filters. All chosen tracks are original studio titles rather than remix/live/karaoke/instrumental variants. Several track references point at album editions; shared cover images across those songs are intentional. This does not promise each track uses a single-edition cover. The exact track edition and its cover always match. Spotify metadata can relink a track to currently available releases: e.g. `You` resolves to 2026-09-25, and several bonus tracks resolve to the 2025-09-05 release.

## Optional official YouTube videos

`youtube-map.json` contains 16 existing catalog songs explicitly listed by Fujii Kaze's [official video page](https://fujiikaze.com/video/). The artist site's exact `dat-video` identifiers and titles were extracted, with direct title matching except the Japanese `満ちてゆく` / English `Michi Teyu Ku (Overflowing)` correspondence. These IDs are also merged into `media-map.json`. This verifies provenance, not browser playback or embeddability in each territory. No line timings are included or inferred.

Songs without an artist-video-page match: `shinunoga-e-wa`, `garden`, `okay-goodbye`, `forever-young`, `masshiro`. The main agent separately verified the pilot `shinunoga-e-wa` official Not a MV video `dawrQnvwMTY`; its data/timings are handled separately.

No remote images/audio/video downloaded; only public metadata and HTML were read. Application source was not edited.
