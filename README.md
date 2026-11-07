# 🎧 Spotify Compatibility Web App

Compare your full Spotify listening history with a friend: see your shared artists and songs, explore your top tracks over time, and play a two-player guessing game built from your listening patterns.

**🔗 Live site: (https://carangg.github.io/spotify-blend-analyzer/)**

![Screenshot of the app](screenshots/demo.gif)

## ✨ Features
- **Artists & Songs:** rankings for each person and shared, with All time / 12 month / 6 month views
- **Artist search:** autocomplete search with first-listen dates, rankings, and listening timelines
- **The Game:** 10 click-to-reveal questions, like each person's late-night songs, your shared listening hour, and the artist that took over a whole month
- **Steal lists:** songs your friend loves that you've barely heard

## 🔒 Privacy
Everything runs **entirely in your browser**. Your Spotify data is never uploaded to any server.

## ⚙️ How it works
1. You upload two Spotify Extended Streaming History exports (.zip)
2. **Pyodide** runs Python + Pandas directly in the browser
3. A Pandas pipeline cleans and aligns both histories
4. Stats are computed in Python and passed to JavaScript as JSON
5. JavaScript renders the tabs, tables, and game

## 🧠 Design decisions
- **30-second listen threshold:** short plays (skips) are flagged so they don't inflate rankings, matching Spotify's own stream definition
- **Aligned export dates:** exports end on different days, so both histories are cut to the same end date for fair comparisons
- **Active months only:** some stats ignore months where a user barely listened, so users with short histories aren't penalized
- **Caching:** computed results are cached per time window, making repeat views instant

## 📥 Getting your data
1. Go to Spotify's [Privacy settings](https://www.spotify.com/account/privacy/)
2. Request your **Extended streaming history** (not just "Account data")
3. Spotify emails it to you, which can take up to 30 days

## 🛠️ Tech stack
Python · Pandas · JavaScript · HTML/CSS · Pyodide · GitHub Pages

## 💻 Run locally
\```
python -m http.server 8001 --directory docs
\```
Then open `http://localhost:8001`.

---
*Not affiliated with or endorsed by Spotify.*
