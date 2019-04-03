#based on spzZapHistory and ZapHistoryBrowser mod aka Uchkun
#created by Vasiliks 11.2015
#r0.1_r5  PLI version
from . import _
from Components.ActionMap import ActionMap
from Components.config import config, ConfigEnableDisable, ConfigInteger, ConfigSelection, ConfigSubsection, getConfigListEntry
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryProgress, MultiContentEntryText, MultiContentEntryPixmapAlphaBlend
from Components.Sources.StaticText import StaticText
from enigma import BT_SCALE, getDesktop, eListboxPythonMultiContent, eServiceCenter, eServiceReference, eTimer, gFont, loadPNG, RT_HALIGN_LEFT, RT_HALIGN_CENTER, RT_HALIGN_RIGHT, RT_WRAP, RT_VALIGN_CENTER
from Components.ParentalControl import parentalControl
from Plugins.Plugin import PluginDescriptor
from Screens.ChannelSelection import ChannelSelection
from Screens.ParentalControlSetup import ProtectedScreen
from Screens.Screen import Screen
import Screens.InfoBar
from time import localtime, time
from Tools.Directories import fileExists, resolveFilename, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN

screenWidth = getDesktop(0).size().width()

color = [("0xffffff", _("white")),
	    ("0xc0c0c0", _("lightgrey")),
	    ("0x8f8f8f", _("grey")),
	    ("0x555555", _("darkgrey")),
	    ("0xffff55", _("yellow")),
	    ("0xffcc33", _("gold")),
	    ("0xff80ff", _("pink")),
	    ("0xff8000", _("orange")),
	    ("0xff0000", _("red")),
	    ("0x800000", _("crimson")),
	    ("0x804000", _("brown")),
	    ("0x80ff00", _("lime")),
	    ("0x00ff00", _("green")),
	    ("0x008000", _("darkgreen")),
	    ("0x00ffff", _("aqua")),
	    ("0x0099ff", _("skyblue")),
	    ("0x0000ff", _("blue")),
	    ("0x000080", _("darkblue")),
	    ("0x8080ff", _("lilac")),
	    ("0x400080", _("purple"))]

config.plugins.vZapHistory = ConfigSubsection()
config.plugins.vZapHistory.enable = ConfigSelection(default='on', choices=[('off', _('disabled')), ('on', _('enabled')), ('parental_lock', _('disabled at parental lock'))])
config.plugins.vZapHistory.maxEntries = ConfigInteger(default=20, limits=(2, 60))
config.plugins.vZapHistory.viewMode = ConfigSelection(default='picons', choices=[('menu', _('standard')), ('picons', _('with picons'))])
config.plugins.vZapHistory.alignment = ConfigSelection(default='left', choices=[('left', _('left')), ('center', _('center')), ('right', _('right'))])
config.plugins.vZapHistory.autoZap = ConfigEnableDisable(default=False)
config.plugins.vZapHistory.namecolor = ConfigSelection(default="0xffffff", choices = color)
config.plugins.vZapHistory.namecolor_sel = ConfigSelection(default="0xffff55", choices = color)
config.plugins.vZapHistory.eventcolor = ConfigSelection(default="0x8f8f8f", choices = color)
config.plugins.vZapHistory.eventcolor_sel = ConfigSelection(default="0xffffff", choices = color)
config.plugins.vZapHistory.duratcolor = ConfigSelection(default="0x8f8f8f", choices = color)
config.plugins.vZapHistory.duratcolor_sel = ConfigSelection(default="0xffff55", choices = color)
config.plugins.vZapHistory.barcolor = ConfigSelection(default="0x0099ff", choices = color)
config.plugins.vZapHistory.barcolor_sel = ConfigSelection(default="0xffff55", choices = color)

skin_sd = """
    <screen name="vZapHistory" position="center,center" size="530,400" >
      <widget name="list" position="0,40" size="530,350" transparent="1"  alphatest="blend"/>
      <eLabel position="10,28" size="120,3" backgroundColor="#FF0000"/>
      <eLabel position="140,28" size="120,3" backgroundColor="#00FF00"/>
      <eLabel position="270,28" size="120,3" backgroundColor="#FFFF00"/>
      <eLabel position="400,28" size="120,3" backgroundColor="#0000FF"/>
      <widget name="key_red" position="0,5" zPosition="1" size="120,20" font="Regular; 18" valign="center" halign="center" transparent="1" />
      <widget name="key_green" position="140,5" zPosition="1" size="120,20" font="Regular; 18" valign="center" halign="center" transparent="1" />
      <widget name="key_yellow" position="270,5" zPosition="1" size="120,20" font="Regular; 18" valign="center" halign="center" transparent="1" />
      <widget name="key_blue" position="400,5" zPosition="1" size="120,20" font="Regular; 18" valign="center" halign="center" transparent="1" />
    </screen>"""
skin_hd = """
    <screen name="vZapHistory" position="center,center" size="680,530" >
      <widget name="list" position="5,45" size="670,480" transparent="1"  alphatest="blend"/>
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/red.png" position="6,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/green.png" position="172,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/yellow.png" position="338,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/blue.png" position="504,7" size="160,30" transparent="1" alphatest="blend" />
      <widget name="key_red" position="6,9" zPosition="1" size="160,25" font="Regular; 16" valign="center" halign="center" transparent="1" />
      <widget name="key_green" position="172,9" zPosition="1" size="160,25" font="Regular; 16" valign="center" halign="center" transparent="1" />
      <widget name="key_yellow" position="338,9" zPosition="1" size="160,25" font="Regular; 16" valign="center" halign="center" transparent="1" />
      <widget name="key_blue" position="504,9" zPosition="1" size="160,25" font="Regular; 16" valign="center" halign="center" transparent="1" />
    </screen>"""
skin_fhd = """
    <screen name="vZapHistory" position="center,center" size="990,680" >
      <widget name="list" position="5,45" size="980,635" transparent="1" alphatest="blend"/>
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/red.png" position="65,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/green.png" position="295,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/yellow.png" position="525,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/blue.png" position="755,7" size="160,30" transparent="1" alphatest="blend" />
      <widget name="key_red" position="65,9" zPosition="1" size="160,24" font="Regular; 20" valign="center" halign="center" transparent="1" />
      <widget name="key_green" position="295,9" zPosition="1" size="160,24" font="Regular; 20" valign="center" halign="center" transparent="1" />
      <widget name="key_yellow" position="525,9" zPosition="1" size="160,24" font="Regular; 20" valign="center" halign="center" transparent="1" />
      <widget name="key_blue" position="755,9" zPosition="1" size="160,24" font="Regular; 20" valign="center" halign="center" transparent="1" />
    </screen>"""

skinConf_sd = """
    <screen name="vZapHistoryConf" position="center,center" size="530,400" >
      <widget name="config" position="0,50" size="530,350" scrollbarMode="showOnDemand" transparent="1" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/red.png" position="55,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/green.png" position="315,7" size="160,30" transparent="1" alphatest="blend" />
      <widget name="key_red" position="55,9" zPosition="5" size="160,25" font="Regular;16" valign="center" halign="center" transparent="1" shadowColor="black" />
      <widget name="key_green" position="315,9" zPosition="5" size="160,25" font="Regular;16" valign="center" halign="center" transparent="1" shadowColor="black" />
    </screen>"""
skinConf_hd = """
    <screen name="vZapHistoryConf" position="center,center" size="660,390" >
      <widget name="config" position="10,50" size="640,340" scrollbarMode="showOnDemand" transparent="1" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/red.png" position="80,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/green.png" position="400,7" size="160,30" transparent="1" alphatest="blend" />
      <widget name="key_red" position="80,9" zPosition="5" size="160,25" font="Regular;16" valign="center" halign="center" transparent="1" shadowColor="black" />
      <widget name="key_green" position="400,9" zPosition="5" size="160,25" font="Regular;16" valign="center" halign="center" transparent="1" shadowColor="black" />
    </screen>"""
skinConf_fhd = """
    <screen name="vZapHistoryConf" position="center,center" size="900,520" >
      <widget name="config" position="10,50" size="880,460" itemHeight="35" font="Regular;25" scrollbarMode="showOnDemand" transparent="1" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/red.png" position="130,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/green.png" position="590,7" size="160,30" transparent="1" alphatest="blend" />
      <widget name="key_red" position="130,9" zPosition="5" size="160,25" font="Regular;20" valign="center" halign="center" transparent="1" shadowColor="black" />
      <widget name="key_green" position="590,9" zPosition="5" size="160,25" font="Regular;20" valign="center" halign="center" transparent="1" shadowColor="black" />
    </screen>"""

def addToHistory(instance, ref):
    if config.plugins.vZapHistory.enable.value == 'off':
        return
    else:
        if config.ParentalControl.servicepinactive.value and config.plugins.vZapHistory.enable.value == 'parental_lock':
            if parentalControl.getProtectionLevel(ref.toCompareString()) != -1:
                return
        if instance.servicePath is not None:
            tmp = instance.servicePath[:]
            tmp.append(ref)
            score = 0
            remove = -1
            for x in instance.history:
                if len(x) == 2:
                    xref = x[1]
                else:
                    xref = x[2]
                if xref == ref and remove == -1:
                    remove = score
                score += 1
            if remove > -1:
                del instance.history[remove]
            instance.history.append(tmp)
            hlen = len(instance.history)
            if hlen > config.plugins.vZapHistory.maxEntries.value:
                del instance.history[0]
                hlen -= 1
            instance.history_pos = hlen - 1

ChannelSelection.addToHistory = addToHistory

class vZapHistoryBrowserList(MenuList):

    def __init__(self, list, enableWrapAround = False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 24))
        self.l.setFont(1, gFont('Regular', 18))
        self.l.setFont(2, gFont('Regular', 15))
        self.l.setFont(3, gFont('Regular', 12))

def vZapHistoryBrowserListEntry(self, serviceName, eventName, durationTime, bar, png):       #
    res = [serviceName]
    lasflags = RT_HALIGN_LEFT
    if config.plugins.vZapHistory.alignment.value == 'center':
        lasflags = RT_HALIGN_CENTER
    elif config.plugins.vZapHistory.alignment.value == 'right':
        lasflags = RT_HALIGN_RIGHT
    namecolor = int(config.plugins.vZapHistory.namecolor.value, 16)
    namecolor_sel = int(config.plugins.vZapHistory.namecolor_sel.value, 16)
    eventcolor = int(config.plugins.vZapHistory.eventcolor.value, 16)
    eventcolor_sel = int(config.plugins.vZapHistory.eventcolor_sel.value, 16)
    duratcolor = int(config.plugins.vZapHistory.duratcolor.value, 16)
    duratcolor_sel = int(config.plugins.vZapHistory.duratcolor_sel.value, 16)
    barcolor = int(config.plugins.vZapHistory.barcolor.value, 16)
    barcolor_sel = int(config.plugins.vZapHistory.barcolor_sel.value, 16)

    if screenWidth == 1920:
        if config.plugins.vZapHistory.viewMode.value == 'picons':
            self['list'].l.setItemHeight(70)
            png_pos=(5, 5)
            png_size=(100, 60)
            serviceName_pos=(110, 3)
            serviceName_size=(675, 25)
            serviceName_font=0
            eventName_pos=(110, 28)
            eventName_size=(675, 40)
            eventName_font=1
            durationTime_pos=(795, 16)
            durationTime_size=(180, 25)
            durationTime_font=2
            bar_pos=(795, 45)
            bar_size=(180, 10)
        elif config.plugins.vZapHistory.viewMode.value == 'menu':
            self['list'].l.setItemHeight(50)
            serviceName_pos=(5, 1)
            serviceName_size=(785, 24)
            serviceName_font=0
            eventName_pos=(5, 25)
            eventName_size=(785, 25)
            eventName_font=1
            durationTime_pos=(795, 5)
            durationTime_size=(180, 20)
            durationTime_font=2
            bar_pos=(795, 30)
            bar_size=(180, 10)

    elif screenWidth == 1280:
        if config.plugins.vZapHistory.viewMode.value == 'picons':
            self['list'].l.setItemHeight(60)
            png_pos=(3, 3)
            png_size=(90, 54)
            serviceName_pos=(100, 2)
            serviceName_size=(420, 18)
            serviceName_font=1
            eventName_pos=(100, 24)
            eventName_size=(420, 40)
            eventName_font=2
            durationTime_pos=(525, 16)
            durationTime_size=(140, 25)
            durationTime_font=3
            bar_pos=(525, 40)
            bar_size=(140, 6)
        elif config.plugins.vZapHistory.viewMode.value == 'menu':
            self['list'].l.setItemHeight(50)
            serviceName_pos=(5, 2)
            serviceName_size=(515, 18)
            serviceName_font=1
            eventName_pos=(5, 20)
            eventName_size=(515, 30)
            eventName_font=2
            durationTime_pos=(525, 10)
            durationTime_size=(140, 20)
            durationTime_font=3
            bar_pos=(525, 33)
            bar_size=(140, 6)

    else:
        self['list'].l.setItemHeight(50)
        png_pos=(0, 0)
        png_size=(1, 1)
        serviceName_pos=(10, 2)
        serviceName_size=(360, 18)
        serviceName_font=1
        eventName_pos=(10, 20)
        eventName_size=(360, 30)
        eventName_font=2
        durationTime_pos=(380, 15)
        durationTime_size=(140, 25)
        durationTime_font=2
        bar_pos=(380, 32)
        bar_size=(140, 8)

    if config.plugins.vZapHistory.viewMode.value == 'picons':
        res.append(MultiContentEntryPixmapAlphaBlend(pos=png_pos, size=png_size, flags = BT_SCALE, png=png))
    res.append(MultiContentEntryText(pos=serviceName_pos, size=serviceName_size, font=serviceName_font, flags=lasflags, text=serviceName, color=namecolor, color_sel=namecolor_sel))
    res.append(MultiContentEntryText(pos=eventName_pos, size=eventName_size, font=eventName_font, flags=lasflags | RT_VALIGN_CENTER | RT_WRAP, text=eventName, color=eventcolor, color_sel=eventcolor_sel))
    res.append(MultiContentEntryText(pos=durationTime_pos, size=durationTime_size, font=durationTime_font, flags=lasflags, text=durationTime, color=duratcolor, color_sel=duratcolor_sel))
    if bar != 0:
        res.append(MultiContentEntryProgress(pos=bar_pos, size=bar_size, percent=bar, borderWidth=1, foreColor=barcolor, foreColorSelected=barcolor_sel))
    return res

class vZapHistory(Screen, ProtectedScreen):
    def __init__(self, session, servicelist):
        Screen.__init__(self, session)
        ProtectedScreen.__init__(self)
        if screenWidth and screenWidth == 1280:
            self.skin = skin_hd
        elif screenWidth and screenWidth == 1920:
            self.skin = skin_fhd
        else:
            self.skin = skin_sd
        self.session = session
        self.servicelist = servicelist or Screens.InfoBar.InfoBar.instance.servicelist
        self.serviceHandler = eServiceCenter.getInstance()
        self.allowChanges = True
        self.zapDown = False
        self.time = 3
        self['list'] = vZapHistoryBrowserList([])
        self['key_green'] = Label(_('Zap'))
        self['key_red'] = Label(_('Clear'))
        self['key_yellow'] = Label(_('Delete'))
        self['key_blue'] = Label(_('Settings'))
        self["Title"] = StaticText(_("ZapHistory"))
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions', 'DirectionActions'],
        {'cancel': self.cancel,
         'left': self.keyLeft,
         'right': self.keyRight,
         'up': self.keyUp,
         'down': self.keyDown,
         'ok': self.zapAndClose,
         'blue': self.config,
         'green': self.zap,
         'yellow': self.delete,
         'red': self.clear}, -1)
        self.onLayoutFinish.append(self.buildList)
        self.timerAutoZap = eTimer()
        self.timerAutoZap.callback.append(self.zap)

    def cancel(self):
        self.timerAutoZap.stop()
        self.close()

    def findPicon(self, serviceName):
        try:
            if '::' in serviceName:
                serviceName = serviceName.split('::')[0] + ':'
        except:
            pass
        serviceName = serviceName.toString()
        serviceName = '_'.join(serviceName.split(':', 10)[:10])
        searchPaths = ['/usr/share/enigma2/picon/', '/media/hdd/picon/', '/media/usb/picon/', '/media/ba/picon/', '/media/sda1/picon/', '/media/sdb1/picon/', '/media/cf/picon/']
        for path in searchPaths:
            pngname = path + serviceName + '.png'
            if fileExists(pngname):
                return pngname
            pngname = path + 'picon_default.png'
            if fileExists(pngname):
                return pngname
        pngname = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
        if fileExists(pngname):
            return pngname
        else:
            return resolveFilename(SCOPE_SKIN_IMAGE, 'skin_default/picon_default.png')

    def buildList(self):
        list = []
        for x in self.servicelist.history:
            if len(x) == 2:
                ref = x[1]
            else:
                ref = x[2]
            png = loadPNG(self.findPicon(ref))
            info = self.serviceHandler.info(ref)
            if info:
                name = info.getName(ref).replace('\xc2\x86', '').replace('\xc2\x87', '')
                event = info.getEvent(ref)
                if event is not None:
                    eventName = event.getEventName()
                    if eventName is None:
                        eventName = ''
                    else:
                        eventName = eventName.replace('(18+)', '').replace('18+', '').replace('(16+)', '').replace('16+', '').replace('(12+)', '').replace('12+', '').replace('(7+)', '').replace('7+', '').replace('(6+)', '').replace('6+', '').replace('(0+)', '').replace('0+', '')
                    try:
                        begin = event.getBeginTime()
                        if begin is not None:
                            end = begin + event.getDuration()
                            remaining = (end - int(time())) / 60
                            prefix = ''
                            if remaining > 0:
                                prefix = "+"
                            local_begin = localtime(begin)
                            local_end = localtime(end)
                            bar = 0
                            perc = ''
                            i = (100 * (int(time()) - begin)) / event.getDuration()
                            if i < 101:
                                bar = i
                            durationTime = _("%02d.%02d - %02d.%02d (%s%d min)") % (local_begin[3],local_begin[4],local_end[3],local_end[4],prefix, remaining)
                    except:
                        durationTime = ''
                else:
                    eventName = ''
                    durationTime = ''
                    descriptionName = ''
                    bar = 0
            else:
                name = 'N/A'
                eventName = ''
                durationTime = ''
                descriptionName = ''
                bar = 0
            list.append(vZapHistoryBrowserListEntry(self, name, eventName, durationTime, bar, png))
        list.reverse()
        self['list'].setList(list)

    def keyRight(self):
        self.zapDown = False
        self.timerAutoZap.stop()
        self['list'].pageDown()
        if config.plugins.vZapHistory.autoZap.value:
            self.timerAutoZap.startLongTimer(self.time)

    def keyLeft(self):
        self.zapDown = False
        self.timerAutoZap.stop()
        self['list'].pageUp()
        if config.plugins.vZapHistory.autoZap.value:
            self.timerAutoZap.stop()
            self.timerAutoZap.startLongTimer(self.time)

    def keyUp(self):
        self.zapDown = False
        self.timerAutoZap.stop()
        pos = self['list'].getSelectionIndex()
        lon = len(self['list'].list)
        if pos == 0 and lon > 1:
            self['list'].moveToIndex(lon - 1)
        else:
            self['list'].up()
        if pos == 1:
            return
        if config.plugins.vZapHistory.autoZap.value:
            self.timerAutoZap.startLongTimer(self.time)

    def keyDown(self):
        self.zapDown = True
        self.timerAutoZap.stop()
        pos = self['list'].getSelectionIndex()
        lon = len(self['list'].list)
        if pos == lon - 1 and lon > 1:
            self['list'].moveToIndex(0)
        else:
            self['list'].down()
            if config.plugins.vZapHistory.autoZap.value:
                self.timerAutoZap.startLongTimer(self.time)

    def zapAndClose(self):
        self.zapDown = False
        self.zap()
        self.close()

    def zap(self):
        self.timerAutoZap.stop()
        length = len(self.servicelist.history)
        if length > 0:
            self.servicelist.history_pos = length - self['list'].getSelectionIndex() - 1
            self.servicelist.setHistoryPath()
            idx = length - self['list'].getSelectionIndex() - 1
            value_idx = self.servicelist.history[idx]
            del self.servicelist.history[idx]
            self.servicelist.history.append(value_idx)
            self.time = 2
            if self.zapDown:
                self.time = 5
                self.keyDown()
            self.buildList()

    def clear(self):
        self.timerAutoZap.stop()
        if self.allowChanges:
            for i in range(0, len(self.servicelist.history)):
                del self.servicelist.history[0]
            self.buildList()
            self.servicelist.history_pos = 0

    def delete(self):
        self.timerAutoZap.stop()
        if self.allowChanges:
            length = len(self.servicelist.history)
            if length > 0:
                idx = length - self['list'].getSelectionIndex() - 1
                del self.servicelist.history[idx]
                self.buildList()
                currRef = self.session.nav.getCurrentlyPlayingServiceReference()
                idx = 0
                for x in self.servicelist.history:
                    if len(x) == 2:
                        ref = x[1]
                    else:
                        ref = x[2]
                    if ref == currRef:
                        self.servicelist.history_pos = idx
                        break
                    else:
                        idx += 1

    def config(self):
        self.timerAutoZap.stop()
        self.session.openWithCallback(self.buildList, vZapHistoryConf)

    def isProtected(self):
        return config.ParentalControl.servicepinactive.value and config.ParentalControl.configured.value

    def pinEntered(self, result):
        if result is None:
            self.allowChanges = False
        elif not result:
            self.allowChanges = False
        else:
            self.allowChanges = True

class vZapHistoryConf(ConfigListScreen, Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        if screenWidth == 1920:
            self.skin = skinConf_fhd
        elif screenWidth == 1280:
            self.skin = skinConf_hd
        else:
            self.skin = skinConf_sd
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label( _('Save'))
        self["Title"] = StaticText(_('Settings'))
        ConfigListScreen.__init__(self, [getConfigListEntry(_('Enable zap history:'), config.plugins.vZapHistory.enable),
         getConfigListEntry(_('View mode:'), config.plugins.vZapHistory.viewMode),
         getConfigListEntry(_('Alignment list:'), config.plugins.vZapHistory.alignment),
         getConfigListEntry(_('Maximum zap history entries:'), config.plugins.vZapHistory.maxEntries),
         getConfigListEntry(_('Autozap when move in list:'), config.plugins.vZapHistory.autoZap),
         getConfigListEntry(_('Service name color:'), config.plugins.vZapHistory.namecolor),
         getConfigListEntry(_('Event color:'), config.plugins.vZapHistory.eventcolor),
         getConfigListEntry(_('Duration time color:'), config.plugins.vZapHistory.duratcolor),
         getConfigListEntry(_('Progress bar color:'), config.plugins.vZapHistory.barcolor),
         getConfigListEntry(_('Selected service name color:'), config.plugins.vZapHistory.namecolor_sel),
         getConfigListEntry(_('Selected event color:'), config.plugins.vZapHistory.eventcolor_sel),
         getConfigListEntry(_('Selected duration time color:'), config.plugins.vZapHistory.duratcolor_sel),
         getConfigListEntry(_('Selected progress bar color:'), config.plugins.vZapHistory.barcolor_sel)])
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'],
        {'ok': self.save, 'green': self.save,
         'cancel': self.exit, 'red': self.exit}, -2)

    def save(self):
        for x in self['config'].list:
            x[1].save()
        self.close()

    def exit(self):
        for x in self['config'].list:
            x[1].cancel()
        self.close()

def main(session, servicelist = None, **kwargs):
    session.open(vZapHistory, servicelist)

def Plugins(**kwargs):
    return PluginDescriptor(name=_('ZapHistory'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)

