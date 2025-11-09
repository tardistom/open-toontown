from .BattleBase import *
import random
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
from toontown.suit import SuitAttributes
notify = DirectNotifyGlobal.directNotify.newCategory('SuitBattleGlobals')
debugAttackSequence = {}

def pickFromFreqList(freqList):
    randNum = random.randint(0, 99)
    count = 0
    index = 0
    level = None
    for f in freqList:
        count = count + f
        if randNum < count:
            level = index
            break
        index = index + 1

    return level


def getActualFromRelativeLevel(name, relLevel):
    data = SuitAttributes[name]
    actualLevel = data['level'] + relLevel
    return actualLevel

def getSuitTier(name):
    data = SuitAttributes[name]
    suitTier = data['level']
    return suitTier


def getSuitVitals(name, level = -1):
    data = SuitAttributes[name]
    FreqList = (50, 50, 50, 10, 5, 5)
    if level == -1:
        level = pickFromFreqList(FreqList)
    dict = {}
    dict['level'] = getActualFromRelativeLevel(name, level)
    if dict['level'] == 11:
        level = 0
    attacks = data['attacks']
    alist = []
    for a in attacks:
        adict = {}
        name = a[0]
        adict['name'] = name
        adict['animName'] = SuitAttacks[name][0]
        adict['hp'] = a[1][level]
        adict['acc'] = a[2][level]
        adict['freq'] = a[3][level]
        adict['hpMod'] = a[4][level]
        adict['accMod'] = a[5][level]
        adict['feqMod'] = a[6][level]
        adict['group'] = SuitAttacks[name][1]
        alist.append(adict)

    dict['attacks'] = alist
    return dict


def pickSuitAttack(attacks, suitLevel):
    attackNum = None
    randNum = random.randint(0, 99)
    notify.debug('pickSuitAttack: rolled %d' % randNum)
    count = 0
    index = 0
    total = 0

    for c in attacks:
        count = count + c[3]
        if randNum < count:
            attackNum = index
            notify.debug('picking attack %d' % attackNum)
            break
        index = index + 1

    configAttackName = simbase.config.GetString('attack-type', 'random')
    if configAttackName == 'random':
        return attackNum
    elif configAttackName == 'sequence':
        for i in range(len(attacks)):
            if attacks[i] not in debugAttackSequence:
                debugAttackSequence[attacks[i]] = 1
                return i

        return attackNum
    else:
        for i in range(len(attacks)):
            if attacks[i][0] == configAttackName:
                return i

        return attackNum
    return


def getSuitAttack(suitName, suitLevel, attackNum = -1):
    attackChoices = SuitAttributes[suitName]['attacks']
    if attackNum == -1:
        notify.debug('getSuitAttack: picking attacking for %s' % suitName)
        attackNum = pickSuitAttack(attackChoices, suitLevel)
    attack = attackChoices[attackNum]
    adict = {}
    adict['suitName'] = suitName
    name = attack[0]
    adict['name'] = name
    adict['id'] = list(SuitAttacks.keys()).index(name)
    adict['animName'] = SuitAttacks[name][0]
    adict['hp'] = attack[1]
    adict['acc'] = attack[2]
    adict['freq'] = attack[3]
    adict['hpMod'] = attack[4]
    adict['accMod'] = attack[5]
    adict['freqMod'] = attack[6]
    adict['group'] = SuitAttacks[name][1]
    return adict


SuitAttributes = SuitAttributes.SuitAttributes
                    

                    

ATK_TGT_UNKNOWN = 1
ATK_TGT_SINGLE = 2
ATK_TGT_GROUP = 3
SuitAttacks = {'Audit': ('phone', ATK_TGT_SINGLE),
 'Bite': ('throw-paper', ATK_TGT_SINGLE),
 'BounceCheck': ('throw-paper', ATK_TGT_SINGLE),
 'BrainStorm': ('effort', ATK_TGT_SINGLE),
 'BuzzWord': ('speak', ATK_TGT_SINGLE),
 'Calculate': ('phone', ATK_TGT_SINGLE),
 'Canned': ('throw-paper', ATK_TGT_SINGLE),
 'Chomp': ('throw-paper', ATK_TGT_SINGLE),
 'CigarSmoke': ('cigar-smoke', ATK_TGT_SINGLE),
 'ClipOnTie': ('throw-paper', ATK_TGT_SINGLE),
 'Crunch': ('throw-object', ATK_TGT_SINGLE),
 'Demotion': ('magic1', ATK_TGT_SINGLE),
 'DoubleTalk': ('speak', ATK_TGT_SINGLE),
 'Downsize': ('magic2', ATK_TGT_SINGLE),
 'EvictionNotice': ('throw-paper', ATK_TGT_SINGLE),
 'EvilEye': ('glower', ATK_TGT_SINGLE),
 'Filibuster': ('speak', ATK_TGT_SINGLE),
 'FillWithLead': ('pencil-sharpener', ATK_TGT_SINGLE),
 'FingerWag': ('finger-wag', ATK_TGT_SINGLE),
 'Fired': ('magic2', ATK_TGT_SINGLE),
 'FiveOClockShadow': ('glower', ATK_TGT_SINGLE),
 'FloodTheMarket': ('glower', ATK_TGT_SINGLE),
 'FountainPen': ('pen-squirt', ATK_TGT_SINGLE),
 'FreezeAssets': ('glower', ATK_TGT_SINGLE),
 'Gavel': ('gavel', ATK_TGT_SINGLE),
 'GlowerPower': ('glower', ATK_TGT_SINGLE),
 'GuiltTrip': ('magic1', ATK_TGT_GROUP),
 'HalfWindsor': ('throw-paper', ATK_TGT_SINGLE),
 'HangUp': ('phone', ATK_TGT_SINGLE),
 'HeadShrink': ('magic1', ATK_TGT_SINGLE),
 'HotAir': ('speak', ATK_TGT_SINGLE),
 'Jargon': ('speak', ATK_TGT_SINGLE),
 'Legalese': ('speak', ATK_TGT_SINGLE),
 'Liquidate': ('magic1', ATK_TGT_SINGLE),
 'MarketCrash': ('throw-paper', ATK_TGT_SINGLE),
 'MumboJumbo': ('speak', ATK_TGT_SINGLE),
 'ParadigmShift': ('magic2', ATK_TGT_GROUP),
 'PeckingOrder': ('throw-object', ATK_TGT_SINGLE),
 'PickPocket': ('pickpocket', ATK_TGT_SINGLE),
 'PinkSlip': ('throw-paper', ATK_TGT_SINGLE),
 'PlayHardball': ('throw-paper', ATK_TGT_SINGLE),
 'PoundKey': ('phone', ATK_TGT_SINGLE),
 'PowerTie': ('throw-paper', ATK_TGT_SINGLE),
 'PowerTrip': ('magic1', ATK_TGT_GROUP),
 'Quake': ('quick-jump', ATK_TGT_GROUP),
 'RazzleDazzle': ('smile', ATK_TGT_SINGLE),
 'RedTape': ('throw-object', ATK_TGT_SINGLE),
 'ReOrg': ('magic3', ATK_TGT_SINGLE),
 'RestrainingOrder': ('throw-paper', ATK_TGT_SINGLE),
 'Rolodex': ('roll-o-dex', ATK_TGT_SINGLE),
 'RubberStamp': ('rubber-stamp', ATK_TGT_SINGLE),
 'RubOut': ('hold-eraser', ATK_TGT_SINGLE),
 'Sacked': ('throw-paper', ATK_TGT_SINGLE),
 'SandTrap': ('golf-club-swing', ATK_TGT_SINGLE),
 'Schmooze': ('speak', ATK_TGT_SINGLE),
 'Shake': ('stomp', ATK_TGT_GROUP),
 'Shred': ('shredder', ATK_TGT_SINGLE),
 'SongAndDance': ('song-and-dance', ATK_TGT_SINGLE),
 'Spin': ('magic3', ATK_TGT_SINGLE),
 'Synergy': ('magic3', ATK_TGT_GROUP),
 'Tabulate': ('phone', ATK_TGT_SINGLE),
 'TeeOff': ('golf-club-swing', ATK_TGT_SINGLE),
 'ThrowBook': ('throw-object', ATK_TGT_SINGLE),
 'Tremor': ('stomp', ATK_TGT_GROUP),
 'Watercooler': ('watercooler', ATK_TGT_SINGLE),
 'Withdrawal': ('magic1', ATK_TGT_SINGLE),
 'WriteOff': ('hold-pencil', ATK_TGT_SINGLE)}
AUDIT = list(SuitAttacks.keys()).index('Audit')
BITE = list(SuitAttacks.keys()).index('Bite')
BOUNCE_CHECK = list(SuitAttacks.keys()).index('BounceCheck')
BRAIN_STORM = list(SuitAttacks.keys()).index('BrainStorm')
BUZZ_WORD = list(SuitAttacks.keys()).index('BuzzWord')
CALCULATE = list(SuitAttacks.keys()).index('Calculate')
CANNED = list(SuitAttacks.keys()).index('Canned')
CHOMP = list(SuitAttacks.keys()).index('Chomp')
CIGAR_SMOKE = list(SuitAttacks.keys()).index('CigarSmoke')
CLIPON_TIE = list(SuitAttacks.keys()).index('ClipOnTie')
CRUNCH = list(SuitAttacks.keys()).index('Crunch')
DEMOTION = list(SuitAttacks.keys()).index('Demotion')
DOWNSIZE = list(SuitAttacks.keys()).index('Downsize')
DOUBLE_TALK = list(SuitAttacks.keys()).index('DoubleTalk')
EVICTION_NOTICE = list(SuitAttacks.keys()).index('EvictionNotice')
EVIL_EYE = list(SuitAttacks.keys()).index('EvilEye')
FILIBUSTER = list(SuitAttacks.keys()).index('Filibuster')
FILL_WITH_LEAD = list(SuitAttacks.keys()).index('FillWithLead')
FINGER_WAG = list(SuitAttacks.keys()).index('FingerWag')
FIRED = list(SuitAttacks.keys()).index('Fired')
FIVE_O_CLOCK_SHADOW = list(SuitAttacks.keys()).index('FiveOClockShadow')
FLOOD_THE_MARKET = list(SuitAttacks.keys()).index('FloodTheMarket')
FOUNTAIN_PEN = list(SuitAttacks.keys()).index('FountainPen')
FREEZE_ASSETS = list(SuitAttacks.keys()).index('FreezeAssets')
GAVEL = list(SuitAttacks.keys()).index('Gavel')
GLOWER_POWER = list(SuitAttacks.keys()).index('GlowerPower')
GUILT_TRIP = list(SuitAttacks.keys()).index('GuiltTrip')
HALF_WINDSOR = list(SuitAttacks.keys()).index('HalfWindsor')
HANG_UP = list(SuitAttacks.keys()).index('HangUp')
HEAD_SHRINK = list(SuitAttacks.keys()).index('HeadShrink')
HOT_AIR = list(SuitAttacks.keys()).index('HotAir')
JARGON = list(SuitAttacks.keys()).index('Jargon')
LEGALESE = list(SuitAttacks.keys()).index('Legalese')
LIQUIDATE = list(SuitAttacks.keys()).index('Liquidate')
MARKET_CRASH = list(SuitAttacks.keys()).index('MarketCrash')
MUMBO_JUMBO = list(SuitAttacks.keys()).index('MumboJumbo')
PARADIGM_SHIFT = list(SuitAttacks.keys()).index('ParadigmShift')
PECKING_ORDER = list(SuitAttacks.keys()).index('PeckingOrder')
PICK_POCKET = list(SuitAttacks.keys()).index('PickPocket')
PINK_SLIP = list(SuitAttacks.keys()).index('PinkSlip')
PLAY_HARDBALL = list(SuitAttacks.keys()).index('PlayHardball')
POUND_KEY = list(SuitAttacks.keys()).index('PoundKey')
POWER_TIE = list(SuitAttacks.keys()).index('PowerTie')
POWER_TRIP = list(SuitAttacks.keys()).index('PowerTrip')
QUAKE = list(SuitAttacks.keys()).index('Quake')
RAZZLE_DAZZLE = list(SuitAttacks.keys()).index('RazzleDazzle')
RED_TAPE = list(SuitAttacks.keys()).index('RedTape')
RE_ORG = list(SuitAttacks.keys()).index('ReOrg')
RESTRAINING_ORDER = list(SuitAttacks.keys()).index('RestrainingOrder')
ROLODEX = list(SuitAttacks.keys()).index('Rolodex')
RUBBER_STAMP = list(SuitAttacks.keys()).index('RubberStamp')
RUB_OUT = list(SuitAttacks.keys()).index('RubOut')
SACKED = list(SuitAttacks.keys()).index('Sacked')
SANDTRAP = list(SuitAttacks.keys()).index('SandTrap')
SCHMOOZE = list(SuitAttacks.keys()).index('Schmooze')
SHAKE = list(SuitAttacks.keys()).index('Shake')
SHRED = list(SuitAttacks.keys()).index('Shred')
SONG_AND_DANCE = list(SuitAttacks.keys()).index('SongAndDance')
SPIN = list(SuitAttacks.keys()).index('Spin')
SYNERGY = list(SuitAttacks.keys()).index('Synergy')
TABULATE = list(SuitAttacks.keys()).index('Tabulate')
TEE_OFF = list(SuitAttacks.keys()).index('TeeOff')
THROW_BOOK = list(SuitAttacks.keys()).index('ThrowBook')
TREMOR = list(SuitAttacks.keys()).index('Tremor')
WATERCOOLER = list(SuitAttacks.keys()).index('Watercooler')
WITHDRAWAL = list(SuitAttacks.keys()).index('Withdrawal')
WRITE_OFF = list(SuitAttacks.keys()).index('WriteOff')

def getFaceoffTaunt(suitName, doId):
    if suitName in SuitFaceoffTaunts:
        taunts = SuitFaceoffTaunts[suitName]
    else:
        taunts = TTLocalizer.SuitFaceoffDefaultTaunts
    return taunts[doId % len(taunts)]


SuitFaceoffTaunts = OTPLocalizer.SuitFaceoffTaunts

def getAttackTauntIndexFromIndex(suit, attackIndex):
    adict = getSuitAttack(suit.getStyleName(), suit.getLevel(), attackIndex)
    return getAttackTauntIndex(adict['name'])


def getAttackTauntIndex(attackName):
    if attackName in SuitAttackTaunts:
        taunts = SuitAttackTaunts[attackName]
        return random.randint(0, len(taunts) - 1)
    else:
        return 1


def getAttackTaunt(attackName, index = None):
    if attackName in SuitAttackTaunts:
        taunts = SuitAttackTaunts[attackName]
    else:
        taunts = TTLocalizer.SuitAttackDefaultTaunts
    if index != None:
        if index >= len(taunts):
            notify.warning('index exceeds length of taunts list in getAttackTaunt')
            return TTLocalizer.SuitAttackDefaultTaunts[0]
        return taunts[index]
    else:
        return random.choice(taunts)
    return


SuitAttackTaunts = TTLocalizer.SuitAttackTaunts
