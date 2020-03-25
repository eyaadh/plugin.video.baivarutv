import xbmc


def create_adroid_vlc(player_core_path):
    f = open(player_core_path, mode='w')
    f.write('<playercorefactory>\n<players>\n<player name="vlc" type="ExternalPlayer" audio="false" '
            'video="true">\n<filename>org.videolan.vlc</filename>'
            '\n<args>--fullscreen "{1}" </args>\n<hidexbmc>true</hidexbmc>\n<hideconsole>flase</hideconsole>\n'
            '<warpcursor>none</warpcursor>\n</player>\n</players>\n<rules action="prepend">\n'
            '<rule internetstream="true" player="vlc" />\n</rules>\n</playercorefactory>')
    xbmc.executebuiltin("Notification(BaivaruTV,Kodi is going to restart)")
    xbmc.executebuiltin('RestartApp')


def create_win32(player_core_path):
    f = open(player_core_path, mode='w')
    f.write('<playercorefactory>\n<players>\n<player name="vlc" type="ExternalPlayer" audio="false" '
            'video="true">\n<filename>C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe</filename>'
            '\n<args>--fullscreen "{1}" </args>\n<hidexbmc>true</hidexbmc>\n<hideconsole>flase</hideconsole>\n'
            '<warpcursor>none</warpcursor>\n</player>\n</players>\n<rules action="prepend">\n'
            '<rule internetstream="true" player="vlc" />\n</rules>\n</playercorefactory>')
    xbmc.executebuiltin("Notification(BaivaruTV,Kodi is going to restart)")
    xbmc.executebuiltin('RestartApp')


def create_win64(player_core_path):
    f = open(player_core_path, mode='w')
    f.write('<playercorefactory>\n<players>\n<player name="vlc" type="ExternalPlayer" audio="false" '
            'video="true">\n<filename>C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe</filename>'
            '\n<args>--fullscreen "{1}" </args>\n<hidexbmc>true</hidexbmc>\n<hideconsole>flase</hideconsole>\n'
            '<warpcursor>none</warpcursor>\n</player>\n</players>\n<rules action="prepend">\n'
            '<rule internetstream="true" player="vlc" />\n</rules>\n</playercorefactory>')
    xbmc.executebuiltin("Notification(BaivaruTV,Kodi is going to restart)")
    xbmc.executebuiltin('RestartApp')


def create_linux(player_core_path):
    f = open(player_core_path, mode='w')
    f.write('<playercorefactory>\n<players>\n<player name="vlc" type="ExternalPlayer" audio="false" '
            'video="true">\n<filename>/usr/bin/vlc</filename>'
            '\n<args>--fullscreen "{1}" </args>\n<hidexbmc>true</hidexbmc>\n<hideconsole>flase</hideconsole>\n'
            '<warpcursor>none</warpcursor>\n</player>\n</players>\n<rules action="prepend">\n'
            '<rule internetstream="true" player="vlc" />\n</rules>\n</playercorefactory>')
    xbmc.executebuiltin("Notification(BaivaruTV,Kodi is going to restart)")
    xbmc.executebuiltin('RestartApp')
