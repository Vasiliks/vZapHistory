#based on spzZapHistory and ZapHistoryBrowser mod aka Uchkun
#created by Vasiliks 09.2015
#r0.1_r3  PLI version
from . import _
from Components.ActionMap import ActionMap
from Components.config import config, ConfigEnableDisable, ConfigInteger, ConfigSelection, ConfigSubsection, getConfigListEntry
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryProgress, MultiContentEntryText, MultiContentEntryPixmapAlphaBlend
from enigma import BT_SCALE, eListboxPythonMultiContent, eServiceCenter, eServiceReference, eTimer, gFont, loadPNG, RT_HALIGN_LEFT, RT_HALIGN_CENTER, RT_HALIGN_RIGHT, RT_WRAP, RT_VALIGN_CENTER
from Components.ParentalControl import parentalControl
from Plugins.Plugin import PluginDescriptor
from Screens.ChannelSelection import ChannelSelection
from Screens.ParentalControlSetup import ProtectedScreen
from Screens.Screen import Screen
from time import localtime, time
from Tools.Directories import fileExists, resolveFilename, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN

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
config.plugins.vZapHistory.namecolor = ConfigSelection(default="0xffcc33", choices = color)
config.plugins.vZapHistory.namecolor_sel = ConfigSelection(default="0xff0000", choices = color)
config.plugins.vZapHistory.eventcolor = ConfigSelection(default="0x8f8f8f", choices = color)
config.plugins.vZapHistory.eventcolor_sel = ConfigSelection(default="0x0099ff", choices = color)
config.plugins.vZapHistory.duratcolor = ConfigSelection(default="0x8f8f8f", choices = color)
config.plugins.vZapHistory.duratcolor_sel = ConfigSelection(default="0x00ffff", choices = color)
config.plugins.vZapHistory.barcolor = ConfigSelection(default="0x8f8f8f", choices = color)
config.plugins.vZapHistory.barcolor_sel = ConfigSelection(default="0xffffff", choices = color)

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

def vZapHistoryBrowserListEntry(serviceName, eventName, durationTime, bar, png):
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
    if config.plugins.vZapHistory.viewMode.value == 'picons':
        res.append(MultiContentEntryPixmapAlphaBlend(pos=(5, 5), size=(100, 60), flags = BT_SCALE, png=png))
        res.append(MultiContentEntryText(pos=(110, 3), size=(535, 25), font=0, flags=lasflags, text=serviceName, color=namecolor, color_sel=namecolor_sel))
        res.append(MultiContentEntryText(pos=(110, 28), size=(535, 40), font=1, flags=lasflags | RT_VALIGN_CENTER | RT_WRAP, text=eventName, color=eventcolor, color_sel=eventcolor_sel))
        res.append(MultiContentEntryText(pos=(660, 16), size=(165, 25), font=2, flags=lasflags, text=durationTime, color=duratcolor, color_sel=duratcolor_sel))
        if bar != 0:
            res.append(MultiContentEntryProgress(pos=(660, 45), size=(165, 10), percent=bar, borderWidth=1, foreColor=barcolor, foreColorSelected=barcolor_sel))
    elif config.plugins.vZapHistory.viewMode.value == 'menu':
        res.append(MultiContentEntryText(pos=(5, 3), size=(640, 25), font=0, flags=lasflags, text=serviceName, color=namecolor, color_sel=namecolor_sel))
        res.append(MultiContentEntryText(pos=(5, 28), size=(640, 40), font=1, flags=lasflags | RT_WRAP, text=eventName, color=eventcolor, color_sel=eventcolor_sel))
        res.append(MultiContentEntryText(pos=(660, 6), size=(165, 25), font=2, flags=lasflags, text=durationTime, color=duratcolor, color_sel=duratcolor_sel))
        if bar != 0:
            res.append(MultiContentEntryProgress(pos=(660, 30), size=(165, 10), percent=bar, borderWidth=1, foreColor=barcolor, foreColorSelected=barcolor_sel))
    return res

class vZapHistory(Screen, ProtectedScreen):
    def __init__(self, session, servicelist):
        Screen.__init__(self, session)
        ProtectedScreen.__init__(self)
        self.session = session
        self.servicelist = servicelist
        self.serviceHandler = eServiceCenter.getInstance()
        self.allowChanges = True
        self.zapDown = False
        self.time = 3
        self['list'] = vZapHistoryBrowserList([])
        self['key_green'] = Label(_('Zap'))
        self['key_red'] = Label(_('Clear'))
        self['key_yellow'] = Label(_('Delete'))
        self['key_menu'] = Label(_('Settings'))
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
        self['list'].l.setItemHeight(70)
        if config.plugins.vZapHistory.viewMode.value == 'menu':
            self['list'].l.setItemHeight(50)
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
            list.append(vZapHistoryBrowserListEntry(name, eventName, durationTime, bar, png))
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
    skin = """
    <screen name="vZapHistoryConf" position="center,center" size="660,390" title="%s">
      <widget name="config" position="10,50" size="640,340" scrollbarMode="showOnDemand" transparent="1"/>
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/red.png" position="80,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/green.png" position="400,7" size="160,30" transparent="1" alphatest="blend" />
      <widget name="key_red" position="80,9" zPosition="5" size="160,25" font="Regular;16" valign="center" halign="center" transparent="1" shadowColor="black" />
      <widget name="key_green" position="400,9" zPosition="5" size="160,25" font="Regular;16" valign="center" halign="center" transparent="1" shadowColor="black" />
    </screen>""" % _('Settings')

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label( _('Save'))
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
        {'ok': self.save,
         'green': self.save,
         'cancel': self.exit,
         'red': self.exit}, -2)

    def save(self):
        for x in self['config'].list:
            x[1].save()
        self.close()

    def exit(self):
        for x in self['config'].list:
            x[1].cancel()
        self.close()

class vZapHistoryMenu(vZapHistory):
    skin = """
    <screen name="vZapHistoryMenu" position="center,center" size="860,540" title="%s">
      <widget name="list" position="5,45" size="850,490" scrollbarMode="showOnDemand" transparent="1"/>
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/red.png" position="20,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/green.png" position="240,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/yellow.png" position="460,7" size="160,30" transparent="1" alphatest="blend" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/vZapHistory/buttons/blue.png" position="680,7" size="160,30" transparent="1" alphatest="blend" />
      <widget name="key_red" position="20,9" zPosition="1" size="160,25" font="Regular; 16" valign="center" halign="center" transparent="1" />
      <widget name="key_green" position="240,9" zPosition="1" size="160,25" font="Regular; 16" valign="center" halign="center" transparent="1" />
      <widget name="key_yellow" position="460,9" zPosition="1" size="160,25" font="Regular; 16" valign="center" halign="center" transparent="1" />
      <widget name="key_menu" position="680,9" zPosition="1" size="160,25" font="Regular; 16" valign="center" halign="center" transparent="1" />
    </screen>""" % _('ZapHistory')

    def __init__(self, session, servicelist):
        vZapHistory.__init__(self, session, servicelist)

def main(session, servicelist, **kwargs):
    session.open(vZapHistoryMenu, servicelist)

def Plugins(**kwargs):
    return PluginDescriptor(name=_('ZapHistory'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)
