# Extended Spotify Blend

*A full-history Spotify compatibility web app*

Compare your full Spotify listening history with a friend: see your shared artists and songs, explore your top tracks over time, and play a two-player guessing game built from your listening patterns.

Unlike Spotify Blend, which only gives you a match score based on recent listening, this uses your **entire** history to show *why* your tastes match, where they differ, and how well you really know each other's music.

Everything runs in your browser. Your Spotify data is never uploaded anywhere.

## Why I built this
My friends and I love comparing our music and discovering new music, but Spotify Blend only gives you a single match score based on recent listening. I wanted to see the full picture: who got into an artist first, what we each play late at night, and how well we actually know each other's taste. So I decided to make what I wished existed!

## [Try it live!](https://carangg.github.io/ExtendedSpotifyBlend)

## Demo
https://github.com/user-attachments/assets/1caae68e-011a-4cf5-883c-269f8b01c3d5

## App Images
| **Upload** | **Overview** |
|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/9f6860f4-ad68-4a35-a5c7-5dcb5d37b3fa" width="400" alt="Upload page"> | <img src="https://github.com/user-attachments/assets/71b25472-abfe-4c50-8e48-fff21b33ec7b" width="400" alt="Overview"> |
| Upload both users' Spotify data | Your compatibility score and listening stats at a glance |
| **Top Artists** | **Top Songs** |
| <img src="https://github.com/user-attachments/assets/3f04ea58-430d-48d0-b73c-3f246d19b473" width="400" alt="Artist search"> | <img src="https://github.com/user-attachments/assets/7973b4d5-0f7d-44f5-93a1-a16754906d76" width="400" alt="Top songs"> |
| Search any artist, and see each person's top artists and shared ones | Each person's top songs, plus the ones you both love |
| **Music Taste Game** | |
| <img src="https://github.com/user-attachments/assets/36947f55-da22-4f72-a206-fae73a12b223" width="400" alt="Music Taste Game"> | |
| 10 questions to guess each other's music taste | |

## Features
- **Overview:** a taste match score showing how similar your music taste is, plus each person's listening stats and top artists and songs
- **Top Artists & Songs:** rankings for each person and shared, filterable by time range
- **Artist search:** autocomplete search with first-listen dates, rankings, and each person's top songs by that artist
- **Music Taste Game:** 10 click-to-reveal questions, like each person's late-night songs, your shared listening hour, and the artist that took over a whole month

## How it works
1. You upload two Spotify Extended Streaming History exports (.zip)
2. **Pyodide** runs Python + Pandas directly in the browser
3. A Pandas pipeline cleans and aligns both histories
4. Stats are computed in Python and passed to JavaScript as JSON
5. JavaScript renders the tabs, tables, and game

## Design decisions
- **30-second listen threshold:** short plays (skips) are flagged so they don't inflate rankings, matching Spotify's own stream definition
- **Aligned export dates:** exports end on different days, so both histories are cut to the same end date for fair comparisons
- **Active months only:** some stats ignore months where a user barely listened, so users with short histories aren't penalized
- **Caching:** computed results are cached per time window, making repeat views instant

## Getting your data
1. Go to Spotify's [Privacy settings](https://www.spotify.com/account/privacy/)
2. Request your **Extended streaming history** (not just "Account data")
3. Spotify emails it to you, which can take up to 30 days

## Tech stack
Python · Pandas · JavaScript · HTML/CSS · Pyodide · GitHub Pages

---
*Not affiliated with or endorsed by Spotify.*
