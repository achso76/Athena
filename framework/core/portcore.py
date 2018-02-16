""" Port module consists of 3 classes.

.. uml::

    @startuml

    'style options 
    skinparam monochrome true
    skinparam circledCharacterRadius 0
    skinparam circledCharacterFontSize 0
    skinparam classAttributeIconSize 0
    hide empty members

    Port <|-- PortIn
    Port <|-- PortOut

    Port : edgeIn
    Port : edgeOut
    Port : connectEdge(edge)
    Port : getEdge()
    Port : setView(view)
    Port : getView()
    Port : isConnected()
    Port : disconnectPort()
    PortOut : transferData(data)
    PortOut : propagateExecution()
    PortOut : getConnection()
    PortIn : targetType
    PortIn : targetPort
    PortIn : targetClass
    PortIn : targetParam
    PortIn : propagateExecution()
    PortIn : configFromDesc(desc)
    PortIn : passToBox(data)
    PortIn : getData()
    PortIn : connectPort(portOut)
    PortIn : getConnection()

    @enduml

"""

class Port(object):
    """ Common port interface
    """
    def __init__(self, box, instName):
        self.dataType = None
        self.box = box
        self.name = instName
        self.connectedTo = None
        self.edge = None
    
    def isBoxOpened(self):
        """ Check if the box is opened or not

        Returns:
            boolean

            True -- The box is opened on the screen.
            False -- The box is closed.
        """
        return self.box.isOpened()

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
            return True
        else:
            return False

    def disconnectPort(self):
        self.edge = None

    def createEdge(self):
        self.box.createEdge(self)
        return self.edge

class PortIn(Port):
    """ PortIn class 
    """
    def __init__(self, box, instName):
        """ Initialise in-port.
        
        Args:
            box: box object that has this port as an element
            instName : instance name of this port
        """
        super().__init__(box, instName)
        self.targetType = None # 'code-param' / 'box-port'
        self.targetPort = None
        self.targetClass = None
        self.targetParam = None
            
    def setEdge(self,edge):
        """ degree of all the edges is 2. 1 for incoming and 1 for outgoing.

        .. uml::

            @startuml

            PortIn <- BoxCore : connectEdge(edge)
            activate PortIn
            PortIn -> PortIn : isBoxOpened()
            activate PortIn
            PortIn -> BoxCore : isOpened()
            activate BoxCore
            deactivate BoxCore
            deactivate PortIn
            alt opend case
                PortIn -> PortIn : setEdgeIn(edge)
                activate PortIn
                deactivate PortIn
            else closed case
                PortIn -> PortIn : setEdgeOut(edge)
                activate PortIn
                deactivate PortIn
            end
            deactivate PortIn

            @enduml
        """
        pass

    def propagateExecution(self):
        if self.edge:
            self.edge.propagateExecutionToSource()

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

    def getConnection(self):
        return self.edge
        
class PortOut(Port):
    def __init__(self, box, instName):
        super().__init__(box, instName)
        self.data = None

    def transferData(self, data):
        if self.edge:
            self.data = data
            self.edge.passToBox(data)
        
    def propagateExecution(self):
        self.box.run()

    def getConnection(self):
        return self.view.getConnection()

