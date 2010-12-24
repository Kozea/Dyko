from mutagen_ap import MutagenAP, MutagenProperty
from kalamar.access_point.filesystem import FileSystem, FileSystemProperty

file_properties = [
    "artist",
    "album",
    # Track is an int, which must be formatted on 2 digits
    ("track", FileSystemProperty(int, formatter="%02d")),
    "title",
    "ext"]
file_pattern = r"(.*)/(.*)/(.*) - (.*)\.(ogg|mp3)"
file_ap = FileSystem(
    "/opt/Music/", file_pattern, file_properties, content_property="stream")

mutagen_properties = {
    "artist": MutagenProperty(unicode, "Artist"),
    "album" : MutagenProperty(unicode, "Album"),
    "duration": MutagenProperty(int, "length"),
    "copyright": MutagenProperty(unicode, "copyright")}
mutagen_ap = MutagenAP(file_ap, mutagen_properties, "stream")

