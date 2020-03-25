import os
import sys
import requests
import xbmc
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
import resources.lib.playerfactory_handler as pf

__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])


def get_videos():
    """
    Get the list of videofiles/streams
    :return: list
    """

    dc = xbmcplugin.getSetting(__handle__, "dc")

    with requests.get(dc) as response:
        data = response.json()

        collection = []

        for item in data['playlist']:
            _data = {
                'name': item['name'],
                'thumb': item['poster'],
                'video': item['location'],
                'genre': str(item['genre']),
                "cast": item['cast'],
                "director": item['director'],
                "tagline": item['tagline']
            }
            collection.append(_data)

        VIDEOS = {'movies': collection}

    return VIDEOS['movies']


def play_video(path):
    """
    Play a video by the provided path.
    :param path: str
    :return: None
    """
    play_item = xbmcgui.ListItem(path=path)

    xbmc.Player().play(play_item, True)
    # xbmcplugin.setResolvedUrl(__handle__, True, listitem=play_item)


def list_videos():
    """
    Create the list of playable videos in the Kodi interface.
    :return: None
    """
    videos = get_videos()

    listing = []
    for video in videos:
        list_item = xbmcgui.ListItem(label=video['name'], thumbnailImage=video['thumb'])
        list_item.setProperty('fanart_image', video['thumb'])
        list_item.setInfo('video', {'title': video['name'], 'genre': video['genre'], 'cast': list(video['cast']),
                                    'director': video['director'], 'tagline': video['tagline']})
        list_item.setProperty('IsPlayable', 'true')

        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
        # url = '{0}?action=play&video={1}'.format(__url__, video['video'])
        url = video['video']
        is_folder = False

        listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))
    xbmcplugin.setContent(__handle__, 'Movies')

    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(__handle__)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring, also creates the playercorefactory file
    :param paramstring:
    :return:
    """

    player_core_path = xbmc.translatePath('special://userdata/playercorefactory.xml')
    external_player = xbmcplugin.getSetting(__handle__, "external_player") == "true"

    if external_player is True:
        if not os.path.exists(player_core_path):
            if xbmc.getCondVisibility('system.platform.linux') and xbmc.getCondVisibility('system.platform.android'):
                pf.create_adroid_vlc(player_core_path)
            if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility(
                    'system.platform.android'):
                pf.create_linux(player_core_path)
            elif xbmc.getCondVisibility('system.platform.windows'):
                if os.path.exists("C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"):
                    pf.create_win32(player_core_path)
                elif os.path.exists("C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"):
                    pf.create_win64(player_core_path)
    else:
        if os.path.exists(player_core_path):
            try:
                os.remove(player_core_path)
            except:
                pass

    params = dict(parse_qsl(paramstring[1:]))
    if params:
        if params['action'] == 'play':
            play_video(params['video'])
    else:
        list_videos()


if __name__ == '__main__':

    router(sys.argv[2])
