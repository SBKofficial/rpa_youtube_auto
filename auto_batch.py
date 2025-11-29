# auto_batch.py
import argparse, time
from generate_quote import generate_quote
from make_video import make_video_from_quote
from upload_youtube import get_authenticated_service, upload_video
from config import BATCH_SLEEP_SECONDS

def main(count=1):
    youtube = get_authenticated_service()

    for i in range(count):
        meta = generate_quote()
        quote = meta["quote"]
        title = meta["title"]
        description = meta["description"]
        tags = meta["tags"]

        print("Generating video for:", quote)

        video_path, thumb = make_video_from_quote(quote)

        print("Uploading:", video_path)

        resp = upload_video(youtube, video_path, title, description, tags, thumb)
        print("Uploaded:", resp.get("id"))

        time.sleep(BATCH_SLEEP_SECONDS)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()
    main(args.count)
