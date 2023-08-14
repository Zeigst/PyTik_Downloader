import os
import random
import requests
import time
import json
from dotenv import load_dotenv

def pytik_download_by_username(username: str) -> None:     # MAX 35 vids
    load_dotenv()
    
    url = os.environ.get("RAPIDAPI_USER_URL")
    host = os.environ.get("RAPIDAPI_HOST")
    
    api_keys = [
        os.environ.get("RAPIDAPI_KEY_1"),
        os.environ.get("RAPIDAPI_KEY_2"),
        os.environ.get("RAPIDAPI_KEY_3")
    ]
    
    api_key = random.choice(api_keys)

    params = {"unique_id":username, "count":"35", "cursor":"0"}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": host
    }

    response = requests.request("GET", url, headers=headers, params=params).json()

    if not os.path.exists(f"./tiktok_videos/{username}"):
        os.makedirs(f"./tiktok_videos/{username}")

    videos = response["data"]["videos"]

    print("[PYTIK] Start Downloading ...")
    count = 0
    for video in videos:    
        count += 1
        download_url = video["play"]
        uri = video["video_id"]
        title = video['title']
        limit = str(f'{title:80.80}')
        print(f"[Video] [Title] {limit}\r")
        start = time.time()                                      
        chunk_size = 1024

        if not os.path.exists(f"./tiktok/{username}/{uri}.mp4"):
            video_bytes = requests.get(download_url, stream=True)
            total_length = int(video_bytes.headers.get("Content-Length"))
            print(f"[Status] File size: " + "{size:.2f} MB".format(size = total_length / chunk_size /1024)) 
            with open(f'./tiktok/{username}/{uri}.mp4', 'wb') as out_file:
                out_file.write(video_bytes.content)
                end = time.time() 

                print(f"[Status] Timelapse: "+ " %.2fs" % (end - start))
                print(f"[Status] {uri}.mp4 Downloaded\n""")
                time.sleep(0.7)
            
        else:
            print(f"[Status] {uri}.mp4 already exists! Skipping...\n")
            time.sleep(0.7) 
            continue
    time.sleep(1) 
    print(f"[PYTIK] Successfully downloaded {count} videos ✓")

def pytik_download_by_video_id(video_id: str) -> None:
    load_dotenv()

    url = os.environ.get("RAPIDAPI_VIDEO_URL")
    host = os.environ.get("RAPIDAPI_HOST")
    
    api_keys = [
        os.environ.get("RAPIDAPI_KEY_1"),
        os.environ.get("RAPIDAPI_KEY_2"),
        os.environ.get("RAPIDAPI_KEY_3")
    ]
    
    api_key = random.choice(api_keys)

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": host
    }

    params = {
        "url": video_id
    }

    response = requests.get(url, headers=headers, params=params).json()
    # with open("result.json", 'w') as json_file:
    #     json.dump(response, json_file)

    if response["msg"] == "success":
        if not os.path.exists(f"./tiktok_videos/{response['data']['author']['unique_id']}"):
            os.makedirs(f"./tiktok_videos/{response['data']['author']['unique_id']}")
        if not os.path.exists(f"./tiktok_videos/{response['data']['id']}"):
            os.makedirs(f"./tiktok_videos/{response['data']['author']['unique_id']}/{response['data']['id']}")

        with open(f"./tiktok_videos/{response['data']['author']['unique_id']}/{response['data']['id']}/{response['data']['id']}.json", 'w') as json_file:
            json.dump(response, json_file)

        if not os.path.exists(f"./tiktok_videos/{response['data']['author']['unique_id']}/{response['data']['id']}/{response['data']['id']}.mp4"):
            video_bytes = requests.get(response["data"]["play"], stream=True)
            with open(f"./tiktok_videos/{response['data']['author']['unique_id']}/{response['data']['id']}/{response['data']['id']}.mp4", 'wb') as out_file:
                out_file.write(video_bytes.content)

        if not os.path.exists(f"./tiktok_videos/{response['data']['author']['unique_id']}/{response['data']['id']}/{response['data']['id']}.mp3"):
            music_bytes = requests.get(response["data"]["music"], stream=True)
            with open(f"./tiktok_videos/{response['data']['author']['unique_id']}/{response['data']['id']}/{response['data']['id']}.mp3", 'wb') as out_file:
                out_file.write(music_bytes.content)

