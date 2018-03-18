class CodeNode(object):
    def __init__(self):
        self.boxSpec = None
        self.className = None
        self.instanceID = None
        self.dstNode = None
        self.srcNode = []

    def setClassName(self,name):
        self.className = name

    def setBoxSpec(self,spec):
        self.boxSpec = spec

    def addSrcNode(self,node):
        self.srcNode.append(node)
        node.setDstNode(self)

    def setDstNode(self,node):
        self.dstNode = node

    def setInstanceID(self,ID):
        self.instanceID = ID

    def displayGraph(self):
        print('-----------------')
        print('node ref : {}'.format(self))
        print('spec : {}'.format(self.boxSpec))
        print('class : {}'.format(self.className))
        print('ID : {}'.format(self.instanceID))
        print('dst : {}'.format(self.dstNode))
        print('')
        for node in self.srcNode:
            node.displayGraph()