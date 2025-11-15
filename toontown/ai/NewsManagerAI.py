from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.toonbase import ToontownGlobals

class NewsManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManagerAI')

    def getWeeklyCalendarHolidays(self):
        return []

    def getYearlyCalendarHolidays(self):
        return []

    def getOncelyCalendarHolidays(self):
        return []

    def getRelativelyCalendarHolidays(self):
        return []

    def getMultipleStartHolidays(self):
        return []
    
    def handleAvatarEntered(self, av):
        if self.air.suitInvasionManager.getInvading():
            self.sendUpdateToAvatarId(av.getDoId(), 'setInvasionStatus', [ToontownGlobals.SuitInvasionBulletin,
                                                                          self.air.suitInvasionManager.invadingCog[0],
                                                                          self.air.suitInvasionManager.numSuits,
                                                                          self.air.suitInvasionManager.invadingCog[1]])
    
    def d_setInvasionStatus(self, msgType, cogType, numRemaining, skeleton):
        self.sendUpdate('setInvasionStatus', [msgType, cogType, numRemaining, skeleton])

