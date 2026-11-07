# 🎧 Spotify Compatibility Web App

Compare your full Spotify listening history with a friend: see your shared artists and songs, explore your top tracks over time, and play a two-player guessing game built from your listening patterns.

##[🔗 Try the live app](https://carangg.github.io/spotify-blend-analyzer/)


## Watch the demo video
https://github.com/user-attachments/assets/1caae68e-011a-4cf5-883c-269f8b01c3d5

![Demo of the app](screenshots/demo.gif)

## Images
| Upload Screen | Overview |
|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/9f6860f4-ad68-4a35-a5c7-5dcb5d37b3fa" width="400" alt="Upload page"> | <img src="https://github.com/user-attachments/assets/71b25472-abfe-4c50-8e48-fff21b33ec7b" width="400" alt="Overview"> |
| Prompt to upload both users data. | Overview of both user's compatibility with general stats. |
| Top Artists | Top songs |
| <img src="https://github.com/user-attachments/assets/3f04ea58-430d-48d0-b73c-3f246d19b473" width="400" alt="Artist search"> | <img src="https://github.com/user-attachments/assets/7973b4d5-0f7d-44f5-93a1-a16754906d76" width="400" alt="Top songs"> |
| See stats for any specified artist, and view the top artists individually and shared by both users. | View the top songs individually and shared by both users. |
| Music Taste Game | |
| <img src="https://github.com/user-attachments/assets/36947f55-da22-4f72-a206-fae73a12b223" width="400" alt="Music Taste Game"> | |
| Game of ten questions to allow both user's to guess one another's music tastes. | |

## Features
- **Artists & Songs:** rankings for each person and shared, with All time / 12 month / 6 month views
- **Artist search:** autocomplete search with first-listen dates, rankings, and listening timelines
- **The Game:** 10 click-to-reveal questions, like each person's late-night songs, your shared listening hour, and the artist that took over a whole month
- **Steal lists:** songs your friend loves that you've barely heard

## Privacy
Everything runs **entirely in your browser**. Your Spotify data is never uploaded to any server.

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

## Tech Used
Python · Pandas · JavaScript · HTML/CSS · Pyodide · GitHub Pages

---
*Not affiliated with or endorsed by Spotify.*
