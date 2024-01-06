import random
from os.path import join, dirname

import requests
from json_database import JsonStorageXDG

from ovos_utils.ocp import MediaType, PlaybackType
from ovos_workshop.decorators.ocp import ocp_search, ocp_featured_media
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill


class OmeletoSkill(OVOSCommonPlaybackSkill):

    def __init__(self, *args, **kwargs):
        self.supported_media = [MediaType.SHORT_FILM]
        self.skill_icon = join(dirname(__file__), "ui", "icon.png")
        self.archive = JsonStorageXDG("omeleto", subfolder="OCP")
        super().__init__(*args, **kwargs)

    def initialize(self):
        self._sync_db()
        self.load_ocp_keywords()

    def load_ocp_keywords(self):
        title = []

        for url, data in self.archive.items():
            t = data["title"]  # .split("|")[0].split("(")[0]
            if "|" in t:
                t = t.split("|")[-1].strip()
                if t != "Omeleto":
                    title.append(t)

        self.register_ocp_keyword(MediaType.SHORT_FILM,
                                  "short_movie_name", title)
        self.register_ocp_keyword(MediaType.SHORT_FILM,
                                  "shorts_streaming_provider",
                                  ["Omeleto"])

    def _sync_db(self):
        bootstrap = "https://github.com/JarbasSkills/skill-omeleto/raw/dev/bootstrap.json"
        data = requests.get(bootstrap).json()
        self.archive.merge(data)
        self.schedule_event(self._sync_db, random.randint(3600, 24 * 3600))

    # ovos common play
    def get_playlist(self, num_entries=250):
        return {
            "match_confidence": 70,
            "media_type": MediaType.SHORT_FILM,
            "playlist": self.featured_media()[:num_entries],
            "playback": PlaybackType.VIDEO,
            "skill_icon": self.skill_icon,
            "image": self.skill_icon,
            "title": "Omeleto (Short Films Playlist)",
            "author": "Omeleto"
        }

    @ocp_search()
    def search_db(self, phrase, media_type):
        base_score = 15 if media_type == MediaType.SHORT_FILM else 0
        entities = self.ocp_voc_match(phrase)
        base_score += 30 * len(entities)

        title = entities.get("short_movie_name")
        skill = "shorts_streaming_provider" in entities  # skill matched

        if title:
            # only search db if user explicitly requested short films
            if title:
                candidates = [video for video in self.archive.values()
                              if title.lower() in video["title"].lower()]
                for video in candidates:
                    yield {
                        "title": video["title"],
                        "author": video["author"],
                        "match_confidence": min(100, base_score),
                        "media_type": MediaType.SHORT_FILM,
                        "uri": "youtube//" + video["url"],
                        "playback": PlaybackType.VIDEO,
                        "skill_icon": self.skill_icon,
                        "skill_id": self.skill_id,
                        "image": video["thumbnail"],
                        "bg_image": video["thumbnail"],
                    }

        if skill:
            yield self.get_playlist()

    @ocp_featured_media()
    def featured_media(self):
        return [{
            "title": video["title"],
            "image": video["thumbnail"],
            "match_confidence": 70,
            "media_type": MediaType.SHORT_FILM,
            "uri": "youtube//" + video["url"],
            "playback": PlaybackType.VIDEO,
            "skill_icon": self.skill_icon,
            "bg_image": video["thumbnail"],
            "skill_id": self.skill_id
        } for video in self.archive.values()]


if __name__ == "__main__":
    from ovos_utils.messagebus import FakeBus

    s = OmeletoSkill(bus=FakeBus(), skill_id="t.fake")
    for r in s.search_db("play First Contact", MediaType.MOVIE):
        print(r)
