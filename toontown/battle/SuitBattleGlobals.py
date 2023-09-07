from .BattleBase import *
import random
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
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


SuitAttributes = {'f': {'name': TTLocalizer.SuitFlunky,
       'singularname': TTLocalizer.SuitFlunkyS,
       'pluralname': TTLocalizer.SuitFlunkyP,
       'level': 0,
       'attacks': (('PoundKey', 2, 75, 30, 1, 1, 5, 0), 
                     ('Shred', 3, 50, 30, 1, 1, 5, 0), 
                     ('ClipOnTie', 1, 75, 60, 0.5, 1, 5, 0))},

 'p': {'name': TTLocalizer.SuitPencilPusher,
       'singularname': TTLocalizer.SuitPencilPusherS,
       'pluralname': TTLocalizer.SuitPencilPusherP,
       'level': 1,
       'attacks': (('FountainPen', 2, 75, 20, 1.75, 5, 0),
                   ('RubOut', 4, 75, 20, 2, 5, 0),
                   ('FingerWag', 1, 75, 35, 0.75, 5, 0),
                   ('WriteOff', 4, 75, 5, 2, 5, 0),
                   ('FillWithLead', 3, 75, 20, 1, 5, 0))},
                   
 'ym': {'name': TTLocalizer.SuitYesman,
        'singularname': TTLocalizer.SuitYesmanS,
        'pluralname': TTLocalizer.SuitYesmanP,
        'level': 2,
        'attacks': (('RubberStamp', 2, 50, 35, 0.5, 5, 0),
                    ('RazzleDazzle', 1, 50, 25, 0, 5, 0),
                    ('Synergy', 4, 50, 5, 1, 5, 0),
                    ('TeeOff', 3, 50, 35, 0.5, 5, 0))},

 'mm': {'name': TTLocalizer.SuitMicromanager,
        'singularname': TTLocalizer.SuitMicromanagerS,
        'pluralname': TTLocalizer.SuitMicromanagerP,
        'level': 3,
        'attacks': (('Demotion', 6, 50, 30, 3, 5, 0),
                    ('FingerWag', 4, 50, 10, 2, 5, 0),
                    ('FountainPen', 3, 50, 15, 1.75, 5, 0),
                    ('BrainStorm', 4, 5, 25, 2.75, 5, 0),
                    ('BuzzWord', 4, 50, 20, 2.75, 5, 0))},

 'ds': {'name': TTLocalizer.SuitDownsizer,
        'singularname': TTLocalizer.SuitDownsizerS,
        'pluralname': TTLocalizer.SuitDownsizerP,
        'level': 4,
        'attacks': (('Canned', 5, 60, 25, 1.75, 5, 0),
                    ('Downsize', 8, 50, 35, 1.75, 5, 0),
                    ('PinkSlip', 4, 60, 25, 1, 5, 0),
                    ('Sacked', 5, 50, 15, 1, 5, 0))},

 'hh': {'name': TTLocalizer.SuitHeadHunter,
        'singularname': TTLocalizer.SuitHeadHunterS,
        'pluralname': TTLocalizer.SuitHeadHunterP,
        'level': 5,
        'attacks': (('FountainPen', 5, 60, 15, 1.75, 5, 0),
                    ('GlowerPower', 7, 50, 20, 1.5, 5, 0),
                    ('HalfWindsor', 8, 60, 20, 2, 5, 0),
                    ('HeadShrink', 10, 65, 35, 2.75, 5, 0),
                    ('Rolodex', 6, 60, 10, 1, 5, 0))},

 'cr': {'name': TTLocalizer.SuitCorporateRaider,
        'singularname': TTLocalizer.SuitCorporateRaiderS,
        'pluralname': TTLocalizer.SuitCorporateRaiderP,
        'level': 6,
        'attacks': (('Canned', 6, 60, 20, 1, 5, 0),
                    ('EvilEye', 12, 60, 35, 3, 5, 0),
                    ('PlayHardball', 7, 60, 30, 2.25, 5, 0),
                    ('PowerTie', 10, 65, 15, 2, 5, 0))},

 'tbc': {'name': TTLocalizer.SuitTheBigCheese,
         'singularname': TTLocalizer.SuitTheBigCheeseS,
         'pluralname': TTLocalizer.SuitTheBigCheeseP,
         'level': 7,
         'attacks': (('CigarSmoke', 10, 55, 20, 2.5, 5, 0),
                     ('FloodTheMarket', 14, 70, 10, 2, 5, 0),
                     ('SongAndDance', 14, 60, 20, 1.5, 5, 0),
                     ('TeeOff', 8, 55, 50, 3, 5, 0))},


                     

 'cc': {'name': TTLocalizer.SuitColdCaller,
        'singularname': TTLocalizer.SuitColdCallerS,
        'pluralname': TTLocalizer.SuitColdCallerP,
        'level': 0,
        'attacks': (('FreezeAssets', 1, 90, 5, 0, 5, 0),
                    ('PoundKey', 2, 75, 25, 0.75, 5, 0),
                    ('DoubleTalk', 2, 50, 25, 1.5, 5, 0),
                    ('HotAir', 3, 50, 45, 1.75, 5, 0))},

 'tm': {'name': TTLocalizer.SuitTelemarketer,
        'singularname': TTLocalizer.SuitTelemarketerS,
        'pluralname': TTLocalizer.SuitTelemarketerP,
        'level': 1,
        'attacks': (('ClipOnTie', 2, 75, 15, 0.5, 5, 0),
                    ('PickPocket', 1, 75, 15, 0, 5, 0),
                    ('Rolodex', 4, 50, 30, 2, 5, 0),
                    ('DoubleTalk', 4, 75, 40, 2, 5, 0))},

 'nd': {'name': TTLocalizer.SuitNameDropper,
        'singularname': TTLocalizer.SuitNameDropperS,
        'pluralname': TTLocalizer.SuitNameDropperP,
        'level': 2,
        'attacks': (('RazzleDazzle', 4, 75, 30, 2, 5, 0),
                    ('Rolodex', 5, 95, 40, 2.25, 5, 0),
                    ('Synergy', 3, 50, 15, 2.25, 5, 0),
                    ('PickPocket', 2, 95, 15, 2, 5, 0))},

 'gh': {'name': TTLocalizer.SuitGladHander,
        'singularname': TTLocalizer.SuitGladHanderS,
        'pluralname': TTLocalizer.SuitGladHanderP,
        'level': 3,
        'attacks': (('RubberStamp', 4, 90, 40, 0.75, 5, 0),
                    ('FountainPen', 3, 70, 40, 0.5, 5, 0),
                    ('Filibuster', 4, 30, 10, 2.75, 5, 0),
                    ('Schmooze', 5, 55, 10, 3.75, 5, 0))},

 'ms': {'name': TTLocalizer.SuitMoverShaker,
        'singularname': TTLocalizer.SuitMoverShakerS,
        'pluralname': TTLocalizer.SuitMoverShakerP,
        'level': 4,
        'attacks': (('BrainStorm', 5, 60, 15, 1.75, 5, 0),
                    ('HalfWindsor', 6, 50, 20, 2.5, 5, 0),
                    ('Quake', 9, 60, 20, 3, 5, 0),
                    ('Shake', 6, 70, 25, 2, 5, 0),
                    ('Tremor', 5, 50, 20, 1, 5, 0))},

 'tf': {'name': TTLocalizer.SuitTwoFace,
        'singularname': TTLocalizer.SuitTwoFaceS,
        'pluralname': TTLocalizer.SuitTwoFaceP,
        'level': 5,
        'attacks': (('EvilEye', 10, 60, 30, 2, 5, 0),
                    ('HangUp', 7, 50, 15, 1.5, 5, 0),
                    ('RazzleDazzle', 8, 60, 30, 2, 5, 0),
                    ('RedTape', 6, 60, 25, 1, 5, 0))},

 'm': {'name': TTLocalizer.SuitTheMingler,
       'singularname': TTLocalizer.SuitTheMinglerS,
       'pluralname': TTLocalizer.SuitTheMinglerP,
       'level': 6,
       'attacks': (('BuzzWord', 10, 60, 20, 1, 5, 0),
                   ('ParadigmShift', 12, 60, 25, 3, 5, 0),
                   ('PowerTrip', 10, 60, 15, 2, 5, 0),
                   ('Schmooze', 7, 55, 30, 2.25, 5, 0),
                   ('TeeOff', 8, 70, 10, 1, 5, 0))},

 'mh': {'name': TTLocalizer.SuitMrHollywood,
        'singularname': TTLocalizer.SuitMrHollywoodS,
        'pluralname': TTLocalizer.SuitMrHollywoodP,
        'level': 7,
        'attacks': (('PowerTrip', 10, 55, 50, 2.5, 5, 0), 
                    ('RazzleDazzle', 8, 70, 50, 3, 5, 0))},




 'sc': {'name': TTLocalizer.SuitShortChange,
        'singularname': TTLocalizer.SuitShortChangeS,
        'pluralname': TTLocalizer.SuitShortChangeP,
        'level': 0,
        'attacks': (('Watercooler', 2, 50, 20, 1, 5, 0),
                    ('BounceCheck', 3, 75, 15, 2, 5, 0),
                    ('ClipOnTie', 1, 50, 25, 0.5, 5, 0),
                    ('PickPocket', 2, 95, 40, 1, 5, 0))},

 'pp': {'name': TTLocalizer.SuitPennyPincher,
        'singularname': TTLocalizer.SuitPennyPincherS,
        'pluralname': TTLocalizer.SuitPennyPincherP,
        'level': 1,
        'attacks': (('BounceCheck', 4, 75, 45, 2, 5, 0), 
                    ('FreezeAssets', 2, 75, 20, 1.75, 5, 0), 
                    ('FingerWag', 1, 50, 35, 1.25, 5, 0))},

 'tw': {'name': TTLocalizer.SuitTightwad,
        'singularname': TTLocalizer.SuitTightwadS,
        'pluralname': TTLocalizer.SuitTightwadP,
        'level': 2,
        'attacks': (('Fired', 3, 75, 75, 0.75, 5, 0),
                    ('GlowerPower', 3, 95, 10, 2.25, 5, 0),
                    ('FingerWag', 3, 75, 5, 0.5, 5, 0),
                    ('FreezeAssets', 3, 75, 5, 2.25, 5, 0),
                    ('BounceCheck', 5, 75, 5, 3.25, 5, 0))},

 'bc': {'name': TTLocalizer.SuitBeanCounter,
        'singularname': TTLocalizer.SuitBeanCounterS,
        'pluralname': TTLocalizer.SuitBeanCounterP,
        'level': 3,
        'attacks': (('Audit', 4, 95, 20, 2.75, 5, 0),
                    ('Calculate', 4, 75, 25, 2.75, 5, 0),
                    ('Tabulate', 4, 75, 25, 2.75, 5, 0),
                    ('WriteOff', 4, 95, 30, 2.75, 5, 0))},

 'nc': {'name': TTLocalizer.SuitNumberCruncher,
        'singularname': TTLocalizer.SuitNumberCruncherS,
        'pluralname': TTLocalizer.SuitNumberCruncherP,
        'level': 4,
        'attacks': (('Audit', 5, 60, 15, 1.75, 5, 0),
                    ('Calculate', 6, 50, 30, 1.75, 5, 0),
                    ('Crunch', 8, 60, 35, 1.75, 5, 0),
                    ('Tabulate', 5, 50, 20, 1, 5, 0))},
                    
 'mb': {'name': TTLocalizer.SuitMoneyBags,
        'singularname': TTLocalizer.SuitMoneyBagsS,
        'pluralname': TTLocalizer.SuitMoneyBagsP,
        'level': 5,
        'attacks': (('Liquidate', 10, 60, 30, 2, 5, 0), 
                      ('MarketCrash', 8, 60, 45, 2, 5, 0), 
                      ('PowerTie', 6, 60, 25, 1, 5, 0))},

 'ls': {'name': TTLocalizer.SuitLoanShark,
        'singularname': TTLocalizer.SuitLoanSharkS,
        'pluralname': TTLocalizer.SuitLoanSharkP,
        'level': 6,
        'attacks': (('Bite', 10, 60, 30, 1.5, 5, 0),
                    ('Chomp', 12, 60, 35, 3, 5, 0),
                    ('PlayHardball', 9, 55, 20, 1.5, 5, 0),
                    ('WriteOff', 6, 70, 15, 2, 5, 0))},

 'rb': {'name': TTLocalizer.SuitRobberBaron,
        'singularname': TTLocalizer.SuitRobberBaronS,
        'pluralname': TTLocalizer.SuitRobberBaronP,
        'level': 7,
        'attacks': (('PowerTrip', 11, 60, 50, 2.5, 5, 0), 
                      ('TeeOff', 10, 60, 50, 2, 5, 0))},




 'bf': {'name': TTLocalizer.SuitBottomFeeder,
        'singularname': TTLocalizer.SuitBottomFeederS,
        'pluralname': TTLocalizer.SuitBottomFeederP,
        'level': 0,
        'attacks': (('RubberStamp', 2, 75, 20, 1, 5, 0),
                    ('Shred', 2, 50, 20, 2, 5, 0),
                    ('Watercooler', 3, 95, 10, 1, 5, 0),
                    ('PickPocket', 1, 25, 50, 0.5, 5, 0))},

 'b': {'name': TTLocalizer.SuitBloodsucker,
       'singularname': TTLocalizer.SuitBloodsuckerS,
       'pluralname': TTLocalizer.SuitBloodsuckerP,
       'level': 1,
       'attacks': (('EvictionNotice', 1, 75, 20, 0.75, 5, 0),
                   ('RedTape', 2, 75, 20, 1.75, 5, 0),
                   ('Withdrawal', 6, 95, 10, 2, 5, 0),
                   ('Liquidate', 2, 50, 50, 1.75, 5, 0))},

 'dt': {'name': TTLocalizer.SuitDoubleTalker,
        'singularname': TTLocalizer.SuitDoubleTalkerS,
        'pluralname': TTLocalizer.SuitDoubleTalkerP,
        'level': 2,
        'attacks': (('RubberStamp', 1, 50, 5, 0, 5, 0),
                    ('BounceCheck', 1, 50, 5, 0, 5, 0),
                    ('BuzzWord', 1, 50, 20, 1.25, 5, 0),
                    ('DoubleTalk', 6, 50, 25, 3, 5, 0),
                    ('Jargon', 3, 50, 25, 2.25, 5, 0),
                    ('MumboJumbo', 3, 50, 20, 2.25, 5, 0))},

 'ac': {'name': TTLocalizer.SuitAmbulanceChaser,
        'singularname': TTLocalizer.SuitAmbulanceChaserS,
        'pluralname': TTLocalizer.SuitAmbulanceChaserP,
        'level': 3,
        'attacks': (('Shake', 4, 75, 15, 2.75, 5, 0),
                    ('RedTape', 6, 75, 30, 3.25, 5, 0),
                    ('Rolodex', 3, 75, 20, 1, 5, 0),
                    ('HangUp', 2, 75, 35, 1, 5, 0))},

 'bs': {'name': TTLocalizer.SuitBackStabber,
        'singularname': TTLocalizer.SuitBackStabberS,
        'pluralname': TTLocalizer.SuitBackStabberP,
        'level': 4,
        'attacks': (('GuiltTrip', 8, 60, 40, 2.5, 5, 0), 
                    ('RestrainingOrder', 6, 50, 25, 1.75, 5, 0), 
                    ('FingerWag', 5, 50, 35, 1, 5, 0))},

 'sd': {'name': TTLocalizer.SuitSpinDoctor,
        'singularname': TTLocalizer.SuitSpinDoctorS,
        'pluralname': TTLocalizer.SuitSpinDoctorP,
        'level': 5,
        'attacks': (('ParadigmShift', 9, 60, 30, 2, 5, 0),
                    ('Quake', 8, 60, 20, 2, 5, 0),
                    ('Spin', 10, 70, 35, 2.5, 5, 0),
                    ('WriteOff', 6, 60, 15, 1, 5, 0))},

 'le': {'name': TTLocalizer.SuitLegalEagle,
        'singularname': TTLocalizer.SuitLegalEagleS,
        'pluralname': TTLocalizer.SuitLegalEagleP,
        'level': 6,
        'attacks': (('EvilEye', 10, 60, 20, 1.5, 5, 0),
                    ('Jargon', 7, 60, 15, 2, 5, 0),
                    ('Legalese', 11, 55, 35, 2.5, 5, 0),
                    ('PeckingOrder', 12, 70, 30, 2.5, 5, 0))},

 'bw': {'name': TTLocalizer.SuitBigWig,
        'singularname': TTLocalizer.SuitBigWigS,
        'pluralname': TTLocalizer.SuitBigWigP,
        'level': 7,
        'attacks': (('PowerTrip', 10, 75, 50, 1.5, 5, 0), 
                    ('ThrowBook', 13, 80, 50, 2, 5, 0))}} 
                    

                    

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
