import json
from pathlib import Path

import kino_flex
from utils import batgen
from kino_flex import FlexUrl


def download_args(i: str) -> tuple:
    fu = FlexUrl(i)
    pth = raws_pth / fu.season
    pth.mkdir(parents=True, exist_ok=True)
    return fu.url, pth / fu.episode[1:]


# Inputs and outputs for ffmpeg
def ff_io_args(i: str) -> tuple:
    fu = FlexUrl(i)
    e = fu.episode[1:]
    iv_pth = raws_pth / fu.season / (e + '.mp4')
    ia_pth = raws_pth / fu.season / (e + '.ac3')
    pth = out_pth / fu.season / (e + '.mkv')
    pth.mkdir(parents=True, exist_ok=True)
    return iv_pth, ia_pth, pth


def get_all_links(slug: str, token: str):
    ff = kino_flex.FlexFilm()
    ff.set_jwt(token)
    links = []
    for i in ff.get_links(slug):
        links.append(i)
        print(i)
    with open(f'{slug}.json', 'w') as f:
        json.dump(links, f)


def gen_bats(slug: str):
    with open(f'{slug}.json') as f:
        links = json.load(f)

    # Generating bat for downloading audios
    batgen.generate(links, 'yt-dlp %s -f audio-5.1_AC-3 -N 3 -o "%s.ac3"',
                    download_args, raws_pth / '1. download_audio.bat')
    # Generating bat for downloading videos
    batgen.generate(links, 'yt-dlp %s -f 1080 -N 3 -o "%s.mp4"',
                    download_args, raws_pth / '2. download_video.bat')
    # Generating bat for concatenate audio and video
    batgen.generate(links, 'ffmpeg -hwaccel d3d11va '
                           '-i "%s" -i "%s" '
                           '-map 0 -map 1 '
                           '-c copy "%s"',
                    ff_io_args, raws_pth / '3. concatenate.bat')
    # Generating bat for convert
    batgen.generate(links, 'ffmpeg -hwaccel d3d11va '
                           '-i "%s" -i "%s" '
                           '-c:v libsvtav1 -crf 21 -preset 8 '
                           '-c:a libopus -b:a 384k "%s"',
                    ff_io_args, raws_pth / '4. convert.bat')
    batgen.generate(links, 'del %s /Q\ndel %s/Q\nrem %s',
                    ff_io_args, raws_pth / '5. delete temp files.bat')


if __name__ == '__main__':
    raws_pth = Path(r'D:\Torrents\#fg Disenchantment (WEB-DL 1080p)')
    out_pth = Path(r'D:\Torrents\Disenchantment (WEB-DLRip 1080p)')
    # get_all_links('disenchantment', '')
    gen_bats('disenchantment')
