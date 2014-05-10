import operations

class ProblemStructure:#fields : schemas,objectSet
    def __init__(self):
        self.objectSet=set()
        self.schemas=[]
    def addSchema(self,schema):
        self.schemas.append(schema)
    def addBridgingSchemas(self,schema1,schema2,names=[]):#Create all the schemas and objects related to eventual relations between two schemas
                                                        # important convention : schema1.objects['qf'] > schema2.objects['qf']
                                                        #4 schemas max is created 3 binding the q1,q2,qf together, and 1 binding the two schemas
        commonObject=self.detectCommonObject(schema1,schema2)
        if(not commonObject):
            for position in ['q1','q2','qf']:
                self.bridge(schema1,schema2,position,operations.soustractionBridge)
            self.lastbridge(schema1,schema2,operations.soustractionBridge)
        else :
            theCommonObject=commonObject.pop()# to get the only value of the set
            if(schema1.positions[theCommonObject]==schema2.positions[theCommonObject]):#to bridge two schemas with a common object, the commonObject must be at the same position
                posOfTheCommonObject=schema1.positions[theCommonObject]
            else :
                posOfTheCommonObject=-1 # else we ignore that schemas share a common element
            l=['q1','q2','qf']
            for position in l:
                if position!=posOfTheCommonObject:
                    self.bridge(schema1,schema2,position,operations.soustractionBridge)
            self.lastbridge(schema1,schema2,operations.soustractionBridge)

    def bridge(self,schema1,schema2,position,operationBridge):
        bridge=schema1.objects[position]+operationBridge+schema2.objects[position] # create string like T2minusT1
        self.addSchema(Schema(bridge,schema1.objects[position],operations.soustraction,schema2.objects[position])) # create T1-T2=T1minusT2 schema and to the structure

    def lastbridge(self,schema1,schema2,operationBridge):
        bridge1=schema1.objects['q1']+operationBridge+schema2.objects['q1'] # create string like T2minusT1
        bridge2=schema1.objects['q2']+operationBridge+schema2.objects['q2']
        bridgef=schema1.objects['qf']+operationBridge+schema2.objects['qf']
        self.addSchema(Schema(bridgef , bridge1 , schema1.operation*schema2.operation , bridge2))#schema1.operation*schema2.operation works because operation.addition=1 and operation.soustraction=-1

    def detectCommonObject(self,schema1,schema2):
        return schema1.getSetObjects().intersection(schema2.getSetObjects())

    def updateObjectSet(self):
        objectList=[]
        for schema in self.schemas:
            for obj in schema.getSetObjects():
                objectList.append(obj)
        self.objectSet=set(objectList)


class Schema: #a simple schema is a schema binding 3 values (e.g. a+b=c)
    def  __init__(self,qf,q1,operation,q2,name=""):#convention : q1 must be bigger than q2
        self.name=name
        self.operation=operation
        self.objects = {'qf': qf, 'q1': q1,  'q2': q2}
        self.positions = {qf: 'qf', q1: 'q1',  q2: 'q2'}#usefull to get the position (e.g T1 is the qf of this schema)
    def getSetObjects(self):
        return set([self.objects['q1'],self.objects['q2'],self.objects['qf']])

