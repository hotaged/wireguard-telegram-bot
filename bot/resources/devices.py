from aiogram.utils import markdown

WG_LINK_TEXT = 'Wireguard'
WG_ANDROID_LINK = markdown.hlink(WG_LINK_TEXT, 'https://play.google.com/store/apps/details?id=com.wireguard.android')
WG_IOS_LINK = markdown.hlink(WG_LINK_TEXT, 'https://apps.apple.com/us/app/wireguard/id1441195209?ls=1')
WG_WINDOWS_LINK = markdown.hlink(WG_LINK_TEXT, 'https://download.wireguard.com/windows-client/wireguard-installer.exe')
WG_MACOS_LINK = markdown.hlink(WG_LINK_TEXT, 'https://apps.apple.com/us/app/wireguard/id1451685025?ls=1&mt=12')
WG_LINUX_LINK = markdown.hlink(WG_LINK_TEXT, 'https://www.wireguard.com/install/')

ANDROID = 'Android'
IOS = 'IOS'
MACOS = 'Mac OS'
WINDOWS = 'Windows'
LINUX = 'Linux'


docs = {
    ANDROID: f"""
        1) Установите и запустите приложение {WG_ANDROID_LINK}\n
        2) 
    """
}