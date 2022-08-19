from flask import Flask, render_template, request, url_for, jsonify
from flask import Flask
from pytube import YouTube, Search


app = Flask(__name__)


def checkIfYoutube(url: str):
    return url.__contains__("youtube") or url.__contains__('youtu.be')


def isUrl(url: str):
    return url.startswith("http://") or url.startswith("https://")


def get_audio(query):
    url = str(query)

    if not url.__contains__("https://"):
        se = Search(url)
        yt = se.results[0]
    else:
        # Get video info
        yt = YouTube(url)

    video = yt.streams.filter(
        only_audio=True).filter(abr="128kbps").first()

    title = str(video.title)
    stream_url = video.url

    return {'title': title, 'stream_url': stream_url}


def get_video(videoQuery):
    url = str(videoQuery)

    if url.__contains__("https://"):
        if checkIfYoutube(url):
            yt = YouTube(url)
        else:
            return {'title': None, 'url': url}
    else:
        se = Search(url)
        yt = se.results[0]

        # Get video info

    video = yt.streams\
        .filter(progressive=True, file_extension='mp4') \
        .order_by('resolution') \
        .desc() \
        .first()

    if video:
        return {'title': video.title, 'url': video.url}
    else:
        return {'title': None, 'url': None}

# Pass the required route to the decorator.


@app.route('/', methods=['POST'])
def index_post():
    input_json = request.get_json(force=True)
    # force=True, above, is necessary if another developer
    # forgot to set the MIME type to 'application/json'

    if input_json:
        if input_json['type'] == 'video':
            return get_video(input_json['query'])
        if input_json['type'] == 'audio':
            return get_audio(input_json['query'])
    else:
        return {'usage': 'POST'}


@app.route("/")
def index():
    return "Usage: POST"


if __name__ == '__main__':
    app.run(debug=True)
