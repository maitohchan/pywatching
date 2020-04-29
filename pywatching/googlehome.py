import pychromecast


class GoogleHome(object):
    def __init__(self, name: str = None, ip_addr: str = None):
        if ip_addr:
            cast = pychromecast.Chromecast(str(ip_addr))
        elif name:
            casts = pychromecast.get_chromecasts()
            cast = next(cc for cc in casts if cc.device.friendly_name == name)
        else:
            cast = None
        self.__cast = cast

    def play(self, mp3_rl: str):
        if self.__cast is None:
            return
        self.__cast.wait()
        self.__cast.media_controller.play_media(mp3_rl, 'audio/mp3')
        self.__cast.media_controller.block_until_active()
