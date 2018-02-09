class Port(object):
    def __init__(self, box, instName):
        self.dataType = None
        self.box = box
        self.name = instName
        self.connectedTo = None
        self.edge = None

    def connectEdge(self, edge):
        self.edge = edge

    def getEdge(self):
        return self.edge

    def setView(self,viewPort):
        self.view = viewPort

    def getView(self):
        return self.view

    def isConnected(self):
        if self.edge:
        #if self.connectedTo:
            return True
        else:
            return False

    def disconnectPort(self):
        self.edge = None
        #connectedTo = self.connectedTo
        #self.connectedTo = None
        #
        #if connectedTo:
        #    connectedTo.disconnectPort()

class PortIn(Port):
    def __init__(self, box, instName):
        super().__init__(box, instName)
        self.targetType = None # 'code-param' / 'box-port'
        self.targetPort = None
        self.targetClass = None
        self.targetParam = None

    def propagateExecution(self):
        if self.edge:
            self.edge.propagateExecutionToSource()
        #if self.connectedTo:
        #    self.connectedTo.propagateExecution()

    def configFromDesc(self,desc):
        """
        {
            "data":"float",
            "type":"batch",
            "name":"variance",
            "connect":"variance@randomgen"
        }
        """
        # set target class and parameter name
        target_desc = desc['connect']
        self.targetClass = target_desc.split('@')[1]
        self.targetParam = target_desc.split('@')[0]

    def setView(self,viewPort):
        self.view = viewPort

    def passToBox(self,data):
        """
        This method is for PortOut.
        A output port need to transfer data to connected box through input port.
        A output port would call this method to transfer data to a box.
        A box need to get data using getData().
        """
        # Todo : Check the data type.
        self.data = data

    def getData(self):
        """
        A box should call this method to get data transferred from connected boxes.
        """
        return self.data

    def connectPort(self,portOut):
        self.edge = portOut
        #self.connectedTo = portOut

    def getConnection(self):
        return self.edge
        #if self.connectedTo:
        #    return self.connectedTo.getConnection()
        #else:
        #    return None

class PortOut(Port):
    def __init__(self, box, instName):
        super().__init__(box, instName)
        self.data = None

    def setView(self,viewPort):
        self.view = viewPort

    def transferData(self, data):
        if self.edge:
            self.data = data
            self.edge.passToBox(data)
        #if self.connectedTo:
        #    self.data = data   # if it requires caching...  I'm not so sure if it's required or not now. 
        #    self.connectedTo.passToBox(data)

    def propagateExecution(self):
        self.box.run()

    #def connectPort(self,portIn):
    #    self.connectedTo = portIn
    #    portIn.connectPort(self)

    def getConnection(self):
        return self.view.getConnection()

