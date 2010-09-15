import re, random
from PMS import *



####################################################################################################

PLUGIN_PREFIX     = "/video/USA"
NAMESPACE   = {'media':'http://search.yahoo.com/mrss/'}

USA__URL                     = "http://www.usanetwork.com"
USA_FULL_EPISODES_SHOW_LIST = "http://video.usanetwork.com/"
USA_EP_URL                  = "http://www.usanetwork.com/series/"
usathumb                    = "icon-default.jpg"
usaart                      = "art-default.jpg"


CACHE_INTERVAL              = 3600
DEBUG                       = False

####################################################################################################

def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, "USA Network","icon-default.jpg", "art-default.jpg")
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")



  MediaContainer.art        =R(usaart)
  DirectoryItem.thumb       =R(usathumb)
  WebVideoItem.thumb        =R(usathumb)

####################################################################################################
#def MainMenu():
#    dir = MediaContainer(mediaType='video') 
#
#    dir.Append(Function(DirectoryItem(all_shows, "All Shows"), pageUrl = #USA_FULL_EPISODES_SHOW_LIST))
#    return dir
    
####################################################################################################
def MainMenu():
    pageUrl=USA_FULL_EPISODES_SHOW_LIST
    dir = MediaContainer(mediaType="video")
    content = XML.ElementFromURL(pageUrl, True)
    for item in content.xpath('//div[@id="find_it_branch_Full_Episodes"]//ul/li'):
      titleUrl = item.xpath("a")[0].get('href')
      Log(titleUrl)
      page = HTTP.Request(titleUrl)
      titleUrl2=re.compile('var _rssURL = "(.+?)";').findall(page)[0].replace('%26','&')
      Log(titleUrl2)
      Log(re.compile('var _rssURL = "(.+?)";').findall(page))
      Log(titleUrl2)
      image =""
      title = item.xpath("a")[0].text
      titleUrl2=titleUrl2 + "&networkid=103"
      Log(titleUrl2)
      dir.Append(Function(DirectoryItem(VideoPage, title), pageUrl = titleUrl2, dummyUrl=titleUrl))
    return dir 

####################################################################################################
def VideoPage(sender, pageUrl, dummyUrl):
    dir = MediaContainer(title2=sender.itemTitle)
    content = XML.ElementFromURL(pageUrl).xpath("//item")
    Log(content)
    for item in content:
      try:
        vidUrl = item.xpath('./media:content/media:player',namespaces= NAMESPACE)[0].get('url')
        Log(vidUrl)
        vidUrl=vidUrl.replace("&dst=rss||","")
        vidUrl=vidUrl.replace("http://video.nbcuni.com/player/?id=",dummyUrl + "index.html?id=")
        title = item.xpath("title")[0].text
        Log(title)
        #subtitle = Datetime.ParseDate(item.xpath('pubDate')[0].text).strftime('%a %b %d, %Y')
        #summary = item.xpath('description')[0].text.strip()
        #summary = summary[summary.find('>')+1:].strip()
        thumb = item.xpath('./media:content/media:thumbnail', namespaces=NAMESPACE)[0].get('url')
        Log(thumb)
        dir.Append(WebVideoItem(vidUrl, title=title))
      except:
        pass
    return dir