import os
import requests
import pandas as pd
import re
from dotenv import load_dotenv

# Charger la clé API
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

CHANNEL_HANDLE = "MEDINCODEX"

# 🔹 1. Récupérer l'ID de la playlist "uploads"
def get_uploads_playlist_id(api_key, handle):
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "contentDetails",
        "forHandle": handle,
        "key": api_key
    }
    res = requests.get(url, params=params).json()
    return res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# 🔹 2. Récupérer tous les IDs des vidéos
def get_video_ids(api_key, playlist_id):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    video_ids = []
    next_page = None

    while True:
        params = {
            "part": "contentDetails",
            "playlistId": playlist_id,
            "maxResults": 50,
            "pageToken": next_page,
            "key": api_key
        }
        res = requests.get(url, params=params).json()

        video_ids += [item["contentDetails"]["videoId"] for item in res.get("items", [])]

        next_page = res.get("nextPageToken")
        if not next_page:
            break

    return video_ids

# 🔹 3. Récupérer les détails des vidéos
def get_video_details(api_key, video_ids):
    url = "https://www.googleapis.com/youtube/v3/videos"
    data = []

    for i in range(0, len(video_ids), 50):
        ids = ",".join(video_ids[i:i+50])

        params = {
            "part": "snippet,contentDetails,statistics",
            "id": ids,
            "key": api_key
        }

        res = requests.get(url, params=params).json()

        for item in res.get("items", []):
            data.append({
                "video_id": item["id"],
                "title": item["snippet"]["title"],
                "published_at": item["snippet"]["publishedAt"],
                "duration": item["contentDetails"]["duration"],
                "views": item["statistics"].get("viewCount", 0),
                "likes": item["statistics"].get("likeCount", 0),
                "comments": item["statistics"].get("commentCount", 0)
            })

    return data

# 🔹 4. Convertir durée ISO → secondes
def parse_duration(duration):
    h = int(re.search(r'(\d+)H', duration).group(1)) if 'H' in duration else 0
    m = int(re.search(r'(\d+)M', duration).group(1)) if 'M' in duration else 0
    s = int(re.search(r'(\d+)S', duration).group(1)) if 'S' in duration else 0
    return h*3600 + m*60 + s

# 🔹 5. Transformer les données
def transform_data(data):
    df = pd.DataFrame(data)

    df["views"] = pd.to_numeric(df["views"])
    df["likes"] = pd.to_numeric(df["likes"])
    df["comments"] = pd.to_numeric(df["comments"])

    df["published_at"] = pd.to_datetime(df["published_at"])
    df["publish_date"] = df["published_at"].astype(str)
    df["duration_sec"] = df["duration"].apply(parse_duration)

    return df.drop(columns=["published_at", "duration"])

# 🔹 6. Sauvegarde CSV + JSON
def save_data(df, name):
    os.makedirs("data", exist_ok=True)

    csv_path = f"data/{name}.csv"
    json_path = f"data/{name}.json"

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_json(json_path, orient="records", indent=4, force_ascii=False)

    print(f"\n✅ CSV : {csv_path}")
    print(f"✅ JSON : {json_path}")

# 🔹 MAIN
if __name__ == "__main__":
    if not API_KEY:
        print("❌ Clé API manquante")
        exit()

    playlist_id = get_uploads_playlist_id(API_KEY, CHANNEL_HANDLE)
    video_ids = get_video_ids(API_KEY, playlist_id)
    video_data = get_video_details(API_KEY, video_ids)

    df = transform_data(video_data)
    save_data(df, f"youtube_data_{CHANNEL_HANDLE.lower()}")