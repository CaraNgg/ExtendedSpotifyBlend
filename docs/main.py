import json
import pandas as pd
from spotify_loading import load_history, align_end_dates, filter_window
from songs_tab import individual_song_report, shared_song_report
from artists_tab import show_individual_artists_ranking, show_shared_artists_ranking, artist_report
from blend_funny_tab import (loop_record, one_person_likes_other_doesnt_touch, ride_or_die, most_plays_after_twelve,
                             top_shared_after_twelve, top_shared_season_songs, biggest_percent_of_month_artist,
                             top_shared_song_one_day, top_shared_hour_top_song, top_clicked_song, top_shared_month_songs)

both_clean = None #initial dataframe with nothing

#LOAD THOSE TWO ZIPS
def load_both(name_a, name_b):
    global both_clean
    a = load_history("/a.zip", name_a)
    b = load_history("/b.zip", name_b)
    both_clean = align_end_dates(pd.concat([a, b], ignore_index=True))

def get_songs(name_a, name_b, window="all"):
    windowed_data = filter_window(both_clean, window)
    table_a, table_b = individual_song_report(windowed_data, name_a, name_b)

    result = {
        name_a: table_a.reset_index().head(100).to_dict("records"),
        name_b: table_b.reset_index().head(100).to_dict("records"),
    }
    return json.dumps(result) #cannot read python, so turn into json so javascript can read

def get_shared_songs(name_a, name_b, window="all"):
    windowed_data = filter_window(both_clean, window)
    table = shared_song_report(windowed_data, name_a, name_b)

    result = table.reset_index().head(100).to_dict("records")
    return json.dumps(result)

def get_artists(name_a, name_b, window="all"):
    windowed_data = filter_window(both_clean, window)
    table_a, table_b = show_individual_artists_ranking(windowed_data, name_a, name_b)

    result = {
        name_a: table_a.reset_index().head(50).to_dict("records"),
        name_b: table_b.reset_index().head(50).to_dict("records"),
    }
    return json.dumps(result)  # cannot read python, so turn into json so javascript can read

def get_shared_artists(name_a, name_b, window="all"):
    windowed_data = filter_window(both_clean, window)
    table = show_shared_artists_ranking(windowed_data, name_a, name_b)
    result = table.reset_index().head(50).to_dict("records")
    return json.dumps(result)  # cannot read python, so turn into json so javascript can read

def get_artist_report(name_a, name_b, artist_name):
    result = artist_report(both_clean, artist_name, name_a, name_b)
    return json.dumps(result, default=str)

def get_all_artists():
    real_plays = both_clean[both_clean["counted"]]                    # 1. only real plays (30+ sec)

    totals = real_plays.groupby("artist")["ms_played"].sum()          # 2. total time per artist, both people combined
    totals = totals.sort_values(ascending=False)                      # 3. most-listened first

    artist_names = list(totals.index)                                 # 4. just the names, as a list
    return json.dumps(artist_names)
def get_game(name_a, name_b, window="all"):
    data = filter_window(both_clean, window)
    questions = []

    # Q1: most plays of one song in a single day
    loop = loop_record(data, name_a, name_b)
    cards = []
    for name in [name_a, name_b]:
        cards.append({
            "prompt": name,
            "answer": f"{loop[name]['track']} by {loop[name]['artist']}",
            "detail": f"{loop[name]['plays']} plays on {loop[name]['date']}",
        })
    questions.append({"title": "🔁 Most plays of one song in a single day", "cards": cards})

    # Q2: a top artist the other person has never played
    blind = one_person_likes_other_doesnt_touch(data, name_a, name_b)
    cards = []
    for name, other in [(name_a, name_b), (name_b, name_a)]:
        x = blind[name]
        cards.append({
            "prompt": f"{name} loves, {other} has never played:",
            "answer": x["artist"] if x else "None!",
            "detail": f"{name}'s #{x['rank']} artist · {x['hours']} hours" if x
                      else f"{other} has listened to every artist {name} loves",
        })
    questions.append({"title": "🙈 A top artist the other person has never played", "cards": cards})

    # Q3: the song played in the most months
    rideordie = ride_or_die(data, name_a, name_b)
    cards = []
    for name in [name_a, name_b]:
        x = rideordie[name]
        cards.append({
            "prompt": name,
            "answer": f"{x['track']} by {x['artist']}",
            "detail": f"Played in {x['months']} of {x['active_months']} active months",
        })
    questions.append({"title": "💍 The song played in the most months", "cards": cards})

    # Q4: top songs after midnight (each person + shared)
    after_twelve = most_plays_after_twelve(data, name_a, name_b)
    cards = []
    for name in [name_a, name_b]:
        lines = []
        for i, song in enumerate(after_twelve[name], start=1):
            lines.append(f"{i}. {song['track']} by {song['artist']} ({song['plays']} plays)")
        cards.append({
            "prompt": name,
            "answer": "<br>".join(lines) if lines else "No late-night listening!",
            "detail": "Most played between 12am and 5am",
        })

    lines = []
    for i, song in enumerate(top_shared_after_twelve(data, name_a, name_b), start=1):
        lines.append(f"{i}. {song['track']} by {song['artist']}")
    cards.append({
        "prompt": "Both of you",
        "answer": "<br>".join(lines) if lines else "No shared late-night songs!",
        "detail": "Songs you've both played between 12am and 5am",
    })
    questions.append({"title": "🌙 Top songs between 12am and 5am", "cards": cards})

    # Q5: the season you both listen the most + top songs in it
    season = top_shared_season_songs(data, name_a, name_b)
    s = season["season"]
    emojis = {"Spring": "🌸", "Summer": "☀️", "Fall": "🍂", "Winter": "❄️"}
    info = {
        "main": f"Your top season is: {s} {emojis[s]}",
        "detail": f"{season['shares'][name_a]:.0%} of {name_a}'s and "
                  f"{season['shares'][name_b]:.0%} of {name_b}'s listening happens in {s}",
    }

    cards = []
    for name in [name_a, name_b]:
        lines = []
        for i, song in enumerate(season[name], start=1):
            lines.append(f"{i}. {song['track']} by {song['artist']} ({song['plays']} plays)")
        cards.append({
            "prompt": name,
            "answer": "<br>".join(lines) if lines else "No songs found!",
            "detail": f"Most played during {s}",
        })

    lines = []
    for i, song in enumerate(season["shared"], start=1):
        lines.append(f"{i}. {song['track']} by {song['artist']}")
    cards.append({
        "prompt": "Both of you",
        "answer": "<br>".join(lines) if lines else "No shared songs this season!",
        "detail": f"Songs you've both played during {s}",
    })
    questions.append({"title": "🍂 The season you both listen the most", "info": info, "cards": cards})

    # Q6: the artist that took over a whole month
    takeover = biggest_percent_of_month_artist(data, name_a, name_b)
    cards = []
    for name in [name_a, name_b]:
        x = takeover[name]
        cards.append({
            "prompt": name,
            "answer": x["artist"] if x else "No takeover found!",
            "detail": f"{x['share']:.0%} of {name}'s listening in {x['month']} "
                      f"({x['artist_hours']} of {x['month_hours']} hours)" if x
                      else f"{name} spreads their listening out",
        })
    questions.append({"title": "👑 The artist that took over a whole month", "cards": cards})

    # Q7: a song you've both played the most in one day
    shared_obsession = top_shared_song_one_day(data, name_a, name_b)
    if shared_obsession:
        so = shared_obsession
        answer = f"{so['track']} by {so['artist']}"
        detail = (f"{name_a}: {so[name_a]['plays']} plays on {so[name_a]['date']}<br>"
                  f"{name_b}: {so[name_b]['plays']} plays on {so[name_b]['date']}")
    else:
        answer = "No shared obsession yet!"
        detail = "You haven't both binged the same song in one day"
    questions.append({
        "title": "🔂 A song you've both played the most in one day",
        "cards": [{"prompt": "Both of you", "answer": answer, "detail": detail}],
    })

    # Q8: the hour you're most likely listening at the same time + top songs then
    hour_data = top_shared_hour_top_song(data, name_a, name_b)
    h = hour_data["hour"]
    time_range = f"{h:02d}:00–{(h + 1) % 24:02d}:00"
    info = {
        "main": f"You're most likely listening at the same time between {time_range}",
        "detail": f"{hour_data['shares'][name_a]:.0%} of {name_a}'s and "
                  f"{hour_data['shares'][name_b]:.0%} of {name_b}'s listening happens then",
    }

    cards = []
    for name in [name_a, name_b]:
        lines = []
        for i, song in enumerate(hour_data[name], start=1):
            lines.append(f"{i}. {song['track']} by {song['artist']} ({song['plays']} plays)")
        cards.append({
            "prompt": name,
            "answer": "<br>".join(lines) if lines else "No songs found!",
            "detail": f"Most played between {time_range}",
        })

    lines = []
    for i, song in enumerate(hour_data["shared"], start=1):
        lines.append(f"{i}. {song['track']} by {song['artist']}")
    cards.append({
        "prompt": "Both of you",
        "answer": "<br>".join(lines) if lines else "No shared songs in this hour!",
        "detail": f"Songs you've both played between {time_range}",
    })
    questions.append({"title": "🕚 The hour you're most likely listening together", "info": info, "cards": cards})

    # Q9: the song each person taps play on the most
    most_clicks = top_clicked_song(data, name_a, name_b)
    cards = []
    for name in [name_a, name_b]:
        x = most_clicks[name]
        cards.append({
            "prompt": name,
            "answer": f"{x['track']} by {x['artist']}" if x else "No tapped songs!",
            "detail": f"Tapped {x['clicks']} times" if x else "",
        })
    questions.append({"title": "🔍 The song you tap play on the most", "cards": cards})

    # Q10: the month you both listen the most + top songs then
    month_data = top_shared_month_songs(data, name_a, name_b, n=3)
    m = month_data["month"]
    info = {
        "main": f"Your top month is: {m} 📅",
        "detail": f"{month_data['shares'][name_a]:.0%} of {name_a}'s and "
                  f"{month_data['shares'][name_b]:.0%} of {name_b}'s listening happens in {m}",
    }

    cards = []
    for name in [name_a, name_b]:
        lines = []
        for i, song in enumerate(month_data[name], start=1):
            lines.append(f"{i}. {song['track']} by {song['artist']} ({song['plays']} plays)")
        cards.append({
            "prompt": name,
            "answer": "<br>".join(lines) if lines else "No songs found!",
            "detail": f"Most played in {m}",
        })

    lines = []
    for i, song in enumerate(month_data["shared"], start=1):
        lines.append(f"{i}. {song['track']} by {song['artist']}")
    cards.append({
        "prompt": "Both of you",
        "answer": "<br>".join(lines) if lines else "No shared songs this month!",
        "detail": f"Songs you've both played in {m}",
    })
    questions.append({"title": "📅 The month you both listen the most", "info": info, "cards": cards})

    return json.dumps(questions, default=str)


import numpy as np

#show the overview
def get_overview(name_a, name_b, window="all"):
    data = filter_window(both_clean, window)
    real_plays = data[data["counted"]]

    # hours per artist per person
    artist_hours = (
        real_plays.groupby(["artist", "person"])["ms_played"].sum()
        .unstack("person", fill_value=0)
        .reindex(columns=[name_a, name_b], fill_value=0) / 3_600_000
    )
    a, b = artist_hours[name_a], artist_hours[name_b]

    # plays per song per person
    song_plays = (
        real_plays.groupby(["track", "artist", "person"]).size()
        .unstack("person", fill_value=0)
        .reindex(columns=[name_a, name_b], fill_value=0)
    )

    # 1. shared stat: taste match
    contributions = (a * b) / (np.sqrt((a**2).sum()) * np.sqrt((b**2).sum()))
    score = float(contributions.sum())
    if score >= 0.8:
        label = "Musical twins"
    elif score >= 0.6:
        label = "Very in sync"
    elif score >= 0.4:
        label = "Solid overlap"
    elif score >= 0.2:
        label = "Different but connected"
    else:
        label = "Opposites attract"
    driven_by = list(contributions.sort_values(ascending=False).head(3).index)
    shared_artist_count = int(((a > 0) & (b > 0)).sum())

    # 2. each person's stats
    people = {}
    for name in [name_a, name_b]:
        p = real_plays[real_plays["person"] == name]
        days_active = max((p["ts"].max() - p["ts"].min()).days, 1) if not p.empty else 1
        people[name] = {
            "total_hours": int(round(p["ms_played"].sum() / 3_600_000)),
            "avg_hours_per_day": round(p["ms_played"].sum() / 3_600_000 / days_active, 1),
            "plays": int(len(p)),
            "artists": int(p["artist"].nunique()),
            "songs": int(p.groupby(["track", "artist"]).ngroups),
        }

    # helper: top n rows of a column, as a list of {name, value}
    def top_list(series, n=3):
        top = series[series > 0].sort_values(ascending=False).head(n)
        return [{"name": idx if isinstance(idx, str) else f"{idx[0]} by {idx[1]}",
                 "value": round(float(v), 1)} for idx, v in top.items()]

    # 3. top 3 artists: each person + shared
    shared_art = artist_hours[(a > 0) & (b > 0)]
    top_artists = {
        name_a: top_list(a),
        name_b: top_list(b),
        "shared": top_list(shared_art.min(axis=1)),
    }

    # 4. top 3 songs: each person + shared
    shared_songs = song_plays[(song_plays[name_a] > 0) & (song_plays[name_b] > 0)]
    top_songs = {
        name_a: top_list(song_plays[name_a]),
        name_b: top_list(song_plays[name_b]),
        "shared": top_list(shared_songs.min(axis=1)),
    }

    return json.dumps({
        "taste_match": {"score": score, "label": label, "driven_by": driven_by},
        "shared_artist_count": shared_artist_count,
        "date_range": {"start": str(data["ts"].min().date()), "end": str(data["ts"].max().date())},
        "people": people,
        "top_artists": top_artists,
        "top_songs": top_songs,
    })