import os
import requests
import pandas as pd
import re
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

CHANNEL_HANDLE = "MEDINCODEX" 

def get_channel_info_by_handle(api_key, handle):
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {"part": "snippet,contentDetails,statistics", "forHandle": handle, "key": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    return None

def get_video_ids(api_key, playlist_id):
    video_ids = []
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    next_page_token = None
    print("\n Extraction des IDs de vidéos en cours...")
    while True:
        params = {"part": "contentDetails", "playlistId": playlist_id, "maxResults": 50, "pageToken": next_page_token, "key": api_key}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                video_ids.append(item["contentDetails"]["videoId"])
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break
        else:
            break
    return video_ids

def get_video_details(api_key, video_ids):
    all_video_stats = []
    url = "https://www.googleapis.com/youtube/v3/videos"
    print(" Extraction des détails des vidéos en cours (Batching)...")
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        ids_string = ",".join(batch_ids)
        params = {"part": "snippet,contentDetails,statistics", "id": ids_string, "key": api_key}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("items", []):
                stats = {
                    "video_id": item["id"],
                    "title": item["snippet"]["title"],
                    "published_at": item["snippet"]["publishedAt"],
                    "duration": item["contentDetails"]["duration"],
                    "views": item["statistics"].get("viewCount", 0),
                    "likes": item["statistics"].get("likeCount", 0),
                    "comments": item["statistics"].get("commentCount", 0)
                }
                all_video_stats.append(stats)
    return all_video_stats

def parse_duration(duration):
    hours_match = re.search(r'(\d+)H', duration)
    minutes_match = re.search(r'(\d+)M', duration)
    seconds_match = re.search(r'(\d+)S', duration)
    
    hours = int(hours_match.group(1)) if hours_match else 0
    minutes = int(minutes_match.group(1)) if minutes_match else 0
    seconds = int(seconds_match.group(1)) if seconds_match else 0
    
    return hours * 3600 + minutes * 60 + seconds

def transform_data(video_data):
    print(" Transformation des données en cours...")
    df = pd.DataFrame(video_data)
    df['views'] = pd.to_numeric(df['views']).fillna(0).astype(int)
    df['likes'] = pd.to_numeric(df['likes']).fillna(0).astype(int)
    df['comments'] = pd.to_numeric(df['comments']).fillna(0).astype(int)
    df['published_at'] = pd.to_datetime(df['published_at'])
    df['publish_date'] = df['published_at'].dt.date
    df['publish_time'] = df['published_at'].dt.time
    df['duration_seconds'] = df['duration'].apply(parse_duration)
    df = df.drop(columns=['published_at', 'duration'])
    return df

def save_data_to_csv(df, filename="data/youtube_data.csv"):
    """Sauvegarde le DataFrame dans un fichier CSV."""
    print(f"\n Sauvegarde des données dans {filename}...")
    
    # Créer le dossier 'data' s'il n'existe pas (par précaution)
    os.makedirs("data", exist_ok=True)
    
    # Sauvegarder en CSV (utf-8-sig pour éviter les problèmes d'accents sur Windows/Excel)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f" Succès ! Les données sont prêtes et sauvegardées.")

if __name__ == "__main__":
    if API_KEY:
        uploads_id = get_channel_info_by_handle(API_KEY, CHANNEL_HANDLE)
        if uploads_id:
            videos_list = get_video_ids(API_KEY, uploads_id)
            if videos_list:
                video_data = get_video_details(API_KEY, videos_list)
                if video_data:
                    # 1. Transformer les données
                    df_final = transform_data(video_data)
                    
                    # 2. Sauvegarder les données en CSV
                    save_data_to_csv(df_final, f"data/youtube_data_{CHANNEL_HANDLE.lower()}.csv")
    else:
        print(" Clé API introuvable.")
        