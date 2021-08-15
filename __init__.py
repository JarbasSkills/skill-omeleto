from mycroft.skills.core import intent_file_handler
from pyvod import Collection, Media
from os.path import join, dirname, basename
from ovos_workshop.frameworks.playback import CommonPlayMediaType, CommonPlayPlaybackType, \
    CommonPlayMatchConfidence
from ovos_workshop.skills.video_collection import VideoCollectionSkill
import biblioteca


class OmeletoSkill(VideoCollectionSkill):

    def __init__(self):
        super().__init__("Omeleto")
        self.supported_media = [CommonPlayMediaType.MOVIE,
                                CommonPlayMediaType.SHORT_FILM,
                                CommonPlayMediaType.VIDEO]
        self.message_namespace = basename(dirname(__file__)) + ".jarbasskills"
        # load video catalog
        base_folder = biblioteca.download("ytcat_omeleto")
        path = join(base_folder, "omeleto.jsondb")
        logo = join(dirname(__file__), "res", "logo.png")
        self.media_collection = Collection("omeleto", logo=logo, db_path=path)
        self.default_image = join(dirname(__file__), "ui", "icon.png")
        self.skill_logo = join(dirname(__file__), "ui", "icon.png")
        self.skill_icon = join(dirname(__file__), "ui", "icon.png")
        self.default_bg = logo
        self.media_type = CommonPlayMediaType.SHORT_FILM
        self.playback_type = CommonPlayPlaybackType.VIDEO

    # voice interaction
    def get_intro_message(self):
        self.speak_dialog("intro")

    @intent_file_handler('home.intent')
    def handle_homescreen_utterance(self, message):
        self.handle_homescreen(message)

    # better common play
    def normalize_title(self, title):
        title = title.lower().strip()
        title = self.remove_voc(title, "omeleto")
        title = self.remove_voc(title, "movie")
        title = self.remove_voc(title, "video")
        title = self.remove_voc(title, "scifi")
        title = self.remove_voc(title, "short")
        title = self.remove_voc(title, "horror")
        title = title.replace("|", "").replace('"', "") \
            .replace(':', "").replace('”', "").replace('“', "") \
            .strip().split("|")[-1]
        return " ".join([w for w in title.split(" ") if w])  # remove extra spaces

    def match_media_type(self, phrase, media_type):
        score = 0
        if self.voc_match(phrase, "video") or media_type == CommonPlayMediaType.VIDEO:
            score += 5

        if self.voc_match(phrase, "short"):
            score += 15

        if self.voc_match(phrase, "scifi"):
            score += 5

        if self.voc_match(phrase, "horror"):
            score += 5

        if self.voc_match(phrase, "movie") or media_type == CommonPlayMediaType.MOVIE:
            score += 15

        if self.voc_match(phrase, "omeleto"):
            score += 60

        if media_type == CommonPlayMediaType.SHORT_FILM:
            score += 25

        return score


def create_skill():
    return OmeletoSkill()

