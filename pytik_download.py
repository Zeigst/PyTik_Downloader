import os
import random
import requests
import time
import json
from dotenv import load_dotenv

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
        print("[PYTIK] Start Downloading ...")
        print(f"\n[Title] {response['data']['title']}\r")

        if not os.path.exists(f"./tiktok_videos/{response['data']['author']['unique_id']}"):
            os.makedirs(f"./tiktok_videos/{response['data']['author']['unique_id']}")
        if not os.path.exists(f"./tiktok_videos/{response['data']['id']}"):
            os.makedirs(f"./tiktok_videos/{response['data']['author']['unique_id']}/{response['data']['id']}")

        with open(f"./tiktok_videos/{response['data']['author']['unique_id']}/{response['data']['id']}/{response['data']['id']}.json", 'w') as json_file:
            json.dump(response, json_file)

        if not os.path.exists(f"./tiktok_videos/{response['data']['author']['unique_id']}/{response['data']['id']}/{response['data']['id']}.mp4"):
            start = time.time()
            video_bytes = requests.get(response["data"]["play"], stream=True)
            total_length = int(video_bytes.headers.get("Content-Length"))
            print(f"[Status] File size: " + "{size:.2f} MB".format(size = total_length / 1024 / 1024)) 
            with open(f"./tiktok_videos/{response['data']['author']['unique_id']}/{response['data']['id']}/{response['data']['id']}.mp4", 'wb') as out_file:
                out_file.write(video_bytes.content)
                end = time.time()
                print(f"[Status] Timelapse: "+ " %.2fs" % (end - start))
                print(f"[Status] {response['data']['id']}.mp4 Downloaded")
                time.sleep(0.7)

        if not os.path.exists(f"./tiktok_videos/{response['data']['author']['unique_id']}/{response['data']['id']}/{response['data']['id']}.mp3"):
            start = time.time()
            music_bytes = requests.get(response["data"]["music"], stream=True)
            total_length = int(music_bytes.headers.get("Content-Length"))
            print(f"[Status] File size: " + "{size:.2f} MB".format(size = total_length / 1024 / 1024)) 
            with open(f"./tiktok_videos/{response['data']['author']['unique_id']}/{response['data']['id']}/{response['data']['id']}.mp3", 'wb') as out_file:
                out_file.write(music_bytes.content)
                end = time.time()
                print(f"[Status] Timelapse: "+ " %.2fs" % (end - start))
                print(f"[Status] {response['data']['id']}.mp3 Downloaded")
                time.sleep(0.7)
    else:
        print(f"[Status] {response['msg']}")

    print("\n[PYTIK] Run Complete")

def pytik_download_by_username(username: str) -> None:    
    load_dotenv()

    url = os.environ.get("RAPIDAPI_USER_URL")
    host = os.environ.get("RAPIDAPI_HOST")
    
    api_keys = [
        os.environ.get("RAPIDAPI_KEY_1"),
        os.environ.get("RAPIDAPI_KEY_2"),
        os.environ.get("RAPIDAPI_KEY_3")
    ]
    
    api_key = random.choice(api_keys)

    params = {"unique_id":username}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": host
    }

    response = requests.request("GET", url, headers=headers, params=params).json()
    # with open("result.json", "w") as json_file:
    #     json.dump(response, json_file)
    if response["msg"] == "success":
        print("[PYTIK] Start Downloading ...")
        for video in response["data"]["videos"]:
            print(f"\n[Title] {video['title']}\r")

            if not os.path.exists(f"./tiktok_videos/{video['author']['unique_id']}"):
                os.makedirs(f"./tiktok_videos/{video['author']['unique_id']}")
            if not os.path.exists(f"./tiktok_videos/{video['author']['unique_id']}/{video['video_id']}"):
                os.makedirs(f"./tiktok_videos/{video['author']['unique_id']}/{video['video_id']}")

            with open(f"./tiktok_videos/{video['author']['unique_id']}/{video['video_id']}/{video['video_id']}.json", 'w') as json_file:
                json.dump(video, json_file)

            if not os.path.exists(f"./tiktok_videos/{video['author']['unique_id']}/{video['video_id']}/{video['video_id']}.mp4"):
                start = time.time()
                video_bytes = requests.get(video["play"], stream=True)
                total_length = int(video_bytes.headers.get("Content-Length"))
                print(f"[Status] File size: " + "{size:.2f} MB".format(size = total_length / 1024 / 1024)) 
                with open(f"./tiktok_videos/{video['author']['unique_id']}/{video['video_id']}/{video['video_id']}.mp4", 'wb') as out_file:
                    out_file.write(video_bytes.content)
                    end = time.time()
                    print(f"[Status] Timelapse: "+ " %.2fs" % (end - start))
                    print(f"[Status] {video['video_id']}.mp4 Downloaded")
                    time.sleep(0.7)
            else:
                print(f"[Status] {video['video_id']}.mp4 already exists! Skipping...")
                time.sleep(0.7) 
                continue

            if not os.path.exists(f"./tiktok_videos/{video['author']['unique_id']}/{video['video_id']}/{video['video_id']}.mp3"):
                start = time.time()
                video_bytes = requests.get(video["music"], stream=True)
                total_length = int(video_bytes.headers.get("Content-Length"))
                print(f"[Status] File size: " + "{size:.2f} MB".format(size = total_length / 1024 / 1024)) 
                with open(f"./tiktok_videos/{video['author']['unique_id']}/{video['video_id']}/{video['video_id']}.mp3", 'wb') as out_file:
                    out_file.write(video_bytes.content)
                    end = time.time()
                    print(f"[Status] Timelapse: "+ " %.2fs" % (end - start))
                    print(f"[Status] {video['video_id']}.mp3 Downloaded")
                    time.sleep(0.7)
            else:
                print(f"[Status] {video['video_id']}.mp3 already exists! Skipping...")
                time.sleep(0.7) 
                continue
    else:
        print(f"[Status] {response['msg']}")

    print(f"\n[PYTIK] Run Complete")

def test(video_id) -> None:
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
    with open("result.json", 'w') as json_file:
        json.dump(response, json_file)