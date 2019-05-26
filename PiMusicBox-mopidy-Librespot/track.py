class Track:
    def __init__(self,artist="artist", title="title", album="album", timeAudio="timeAudio", imageURI="imageURI"):
        self.artist = artist
        self.title = title
        self.album = album
        self.timeAudio = timeAudio
        self.imageURI = imageURI
    

    def __eq__(self, other):
        if isinstance(other, Track):
            return self.artist == other.artist and self.title == other.title and\
            self.album == other.album and self.timeAudio == other.timeAudio 
        return False
        
    def __str__(self):
        return "Title: "+ str(self.title.encode(encoding="utf-8", errors="replace"))+\
            "\nArtist: "+ str(self.artist.encode(encoding="utf-8", errors="replace"))+\
            "\nAlbum: "+ str(self.album.encode(encoding="utf-8", errors="replace"))+\
            "\nTime: "+self.timeAudio +\
            "\nURI: "+ self.imageURI + "\n"