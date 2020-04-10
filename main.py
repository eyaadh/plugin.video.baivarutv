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
    kodi_token = xbmcplugin.getSetting(__handle__, "token")
    headers = {'content-type': 'application/json', 'kodi_token': kodi_token}

    with requests.get(dc, headers=headers) as response:
        if response.status_code != 200:
            return False
        data = response.json()

        collection = []

        user = None
        if 'user_name' in data['user_details'] and data['user_details']['user_name'] is not None:
            user = data['user_details']['user_name']
        elif 'f_name' in data['user_details']:
            user = data['user_details']['f_name']

        xbmc.executebuiltin("Notification(BaivaruTV,Welcome back %s)" % user)

        for item in data['playlist']:
            _data = {
                'name': item['name'],
                'thumb': item['poster'],
                'video': item['location'],
                'genre': str(item['genre']),
                "cast": item['cast'],
                "director": item['director'],
                "tagline": item['tagline'],
                "year": item['year'],
                "rating": item['imdbrating']
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

    if not videos:
        xbmc.executebuiltin("Notification(BaivaruTV,Unauthorized. Please use a valid token)")
    else:
        listing = []
        for video in videos:
            list_item = xbmcgui.ListItem(label=video['name'], thumbnailImage=video['thumb'])
            list_item.setProperty('fanart_image', video['thumb'])
            list_item.setInfo('video', {'title': video['name'], 'genre': video['genre'], 'cast': list(video['cast']),
                                        'director': video['director'], 'tagline': video['tagline'],
                                        'year': video['year'], 'rating': video['rating']})
            list_item.setProperty('IsPlayable', 'true')

            # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
            # url = '{0}?action=play&video={1}'.format(__url__, video['video'])
            url = video['video']
            is_folder = False

            listing.append((url, list_item, is_folder))

        xbmcplugin.addDirectoryItems(__handle__, listing, len(listing))
        xbmcplugin.setContent(__handle__, 'Movies')

        xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_VIDEO_TITLE)
        xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_VIDEO_RATING)
        xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_VIDEO_YEAR)

        xbmcplugin.endOfDirectory(__handle__)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring, also creates the playercorefactory file
    :param paramstring:
    :return:
    """

    player_core_path = xbmc.translatePath('special://userdata/playercorefactory.xml')
    external_player = xbmcplugin.getSetting(__handle__, "external_player")
    xbmc.executebuiltin("Notification(BaivaruTV,%s)" % external_player)

    if external_player == "1":
        if xbmc.getCondVisibility('system.platform.linux') and xbmc.getCondVisibility('system.platform.android'):
            if not os.path.exists(player_core_path):
                pf.create_adroid_vlc(player_core_path)
            else:
                file = open(player_core_path)
                read_lines = file.readlines()
                if read_lines[3] != "<filename>org.videolan.vlc</filename>":
                    pf.create_adroid_vlc(player_core_path)
        if xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility(
                'system.platform.android'):
            if not os.path.exists(player_core_path):
                pf.create_linux(player_core_path)
            else:
                file = open(player_core_path)
                read_lines = file.readlines()
                if read_lines[3] != "<filename>/usr/bin/vlc</filename>":
                    pf.create_linux(player_core_path)
        elif xbmc.getCondVisibility('system.platform.windows'):
            if os.path.exists("C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"):
                if not os.path.exists(player_core_path):
                    pf.create_win32(player_core_path)
                else:
                    file = open(player_core_path)
                    read_lines = file.readlines()
                    if read_lines[3] != "<filename>C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe</filename>":
                        pf.create_win32(player_core_path)
            elif os.path.exists("C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"):
                if not os.path.exists(player_core_path):
                    pf.create_win64(player_core_path)
                else:
                    file = open(player_core_path)
                    read_lines = file.readlines()
                    if read_lines[3] != "<filename>C:\\Program Files\\VideoLAN\\VLC\\vlc.exe</filename>":
                        pf.create_win64(player_core_path)
        elif xbmc.getCondVisibility("system.platform.osx"):
            if not os.path.exists(player_core_path):
                pf.create_osx(player_core_path)
            else:
                file = open(player_core_path)
                read_lines = file.readlines()
                if read_lines[3] != "<filename>/Applications/VLC.app/Contents/MacOS/VLC</filename>":
                    pf.create_osx(player_core_path)
    elif external_player == "2":
        if not os.path.exists(player_core_path):
            if xbmc.getCondVisibility('system.platform.linux') and xbmc.getCondVisibility('system.platform.android'):
                pf.create_android_mxplayer_free(player_core_path)
        else:
            file = open(player_core_path)
            read_lines = file.readlines()
            if xbmc.getCondVisibility('system.platform.linux') and xbmc.getCondVisibility('system.platform.android'):
                if read_lines[3] != "<filename>com.mxtech.videoplayer.ad</filename>":
                    pf.create_android_mxplayer_free(player_core_path)
    elif external_player == "3":
        if not os.path.exists(player_core_path):
            if xbmc.getCondVisibility('system.platform.linux') and xbmc.getCondVisibility('system.platform.android'):
                pf.create_android_mxplayer_pro(player_core_path)
        else:
            file = open(player_core_path)
            read_lines = file.readlines()
            if xbmc.getCondVisibility('system.platform.linux') and xbmc.getCondVisibility('system.platform.android'):
                if read_lines[3] != "<filename>com.mxtech.videoplayer.pro</filename>":
                    pf.create_android_mxplayer_pro(player_core_path)
    elif external_player == "4":
        if not os.path.exists(player_core_path):
            if xbmc.getCondVisibility('system.platform.windows'):
                if os.path.exists("C:\\Program Files (x86)\\DAUM\\PotPlayer\\PotPlayerMini.exe"):
                    pf.create_win32_pot_player(player_core_path)
                elif os.path.exists("C:\\Program Files\\DAUM\\PotPlayer\\PotPlayerMini64.exe"):
                    pf.create_win64_pot_player(player_core_path)
        else:
            file = open(player_core_path)
            read_lines = file.readlines()
            if xbmc.getCondVisibility('system.platform.windows'):
                if os.path.exists("C:\\Program Files (x86)\\DAUM\\PotPlayer\\PotPlayerMini.exe"):
                    if read_lines[3] != "<filename>C:\\Program Files (x86)\\DAUM\\PotPlayer\\PotPlayerMini.exe</filename>":
                        pf.create_win32_pot_player(player_core_path)
                elif os.path.exists("C:\\Program Files\\DAUM\\PotPlayer\\PotPlayerMini64.exe"):
                    if read_lines[3] != "<filename>C:\\Program Files\\DAUM\\PotPlayer\\PotPlayerMini64.exe</filename>":
                        pf.create_win64_pot_player(player_core_path)

    elif external_player == "0":
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
