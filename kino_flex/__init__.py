import http.client
import json
from http.client import HTTPResponse

from kino_flex import headers


class FlexFilm:
    raw_data: str
    headers = {
        'authority': "back-films.ru",
        'accept': "application/json, text/plain, */*",
        'accept-language': "ru,en;q=0.9",
        'origin': "https://player-flex.ru",
        'referer': "https://player-flex.ru/",
        'sec-ch-ua': '"Not.A / Brand";v="8", "Chromium";v="114", "YaBrowser";v="23"',
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "cross-site",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    def query(self, url: str) -> HTTPResponse:
        conn = http.client.HTTPSConnection('back-films.ru')
        conn.request('GET', url,
                     headers=self.headers)
        res = conn.getresponse()
        return res

    def set_jwt(self, jwt: str):
        self.headers['authorization'] = jwt

    def get_eps(self, slug: str) -> dict:
        return json.load(self.query(f'/api/v4/films/{slug}/?utm_source=player_start'))

    def get_link(self, slug: str, id: int | str) -> dict:
        return json.load(self.query(f'/api/v4/films/{slug}/streams/?episode={id}&browser_type=web&protected=false'))

    def get_links(self, slug: str):
        res = self.get_eps(slug)
        seasons = res
        for s in seasons.get('list', []):
            series = s.get('series', [])
            for e in series:
                res = self.get_link(slug, e.get('id'))
                link = res[-1]['src']

                yield link


class FlexUrl:
    url: str
    season: str
    episode: str
    quality: str

    def __init__(self, url: str):
        self.url = url
        url = url.split('/')
        self.season, self.episode, self.quality = url[-4:-1]
