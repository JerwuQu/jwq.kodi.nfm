import sys
import xbmcaddon
from xbmcplugin import addDirectoryItems, endOfDirectory
from xbmcgui import ListItem
import requests
from urllib.parse import parse_qsl, quote
from os.path import join

addon = xbmcaddon.Addon()
addon_url = sys.argv[0]
addon_handle = int(sys.argv[1])

def route(param):
    base_url = addon.getSetting('base_url')
    uri = param['uri'] if 'uri' in param else ''

    resp = requests.get(join(base_url, uri))
    json = resp.json()
    items = []
    for entry in json:
        name = entry['name']
        item = ListItem(label=name)
        is_dir = entry['type'] == 'directory'

        if is_dir:
            endslash = '/' if is_dir else ''
            item_url = f'{addon_url}?uri={quote(join(uri, name + endslash))}'
            items.append((item_url, item, is_dir))
        else:
            item.setInfo("video", {"title": name})
            item.setProperty("IsPlayable", "true")
            items.append((join(base_url, uri, name), item, is_dir))

    addDirectoryItems(addon_handle, items, totalItems=len(items))
    endOfDirectory(addon_handle)

if __name__ == '__main__':
    route(dict(parse_qsl(sys.argv[2][1:])))
