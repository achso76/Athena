
class SystemConfig(object):
    boxDir = ''
    toolRootDir = '../..'

    @classmethod
    def getBoxDir(cls):
        # temporary implementation
        #cls.boxDir = '../../boxes'
        #return cls.boxDir
        return '/Users/hj.bak/AthenaRepo'

    @classmethod
    def getLocalWorkSpaceDir(cls):
        return '/Users/hj.bak/AthenaBoxes'

    @classmethod
    def getToolDir(cls):
        return cls.toolRootDir 

    @classmethod
    def getRepository(cls):
        return '/Users/hj.bak/AthenaRepo'
