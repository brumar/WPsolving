import operations

class ProblemStructure:
    schemas=[]
    def __init__(self):
        pass
    def addSchema(self,schema):
        self.schemas.append(schema)
    def addBridgingSchemas(self,schema1,schema2,names=[]):#Create all the schemas and objects related to eventual relations between two schemas
                                                         #convention : schema1.objects['qf'] > schema2.objects['qf']
        commonObject=self.detectCommonObject(schema1,schema2)
        if(not commonObject):
            for i,position in enumerate(['q1','q2','qf']):
                self.bridge(schema1,schema2,position,operations.soustractionBridge)
        else :
            theCommonObject=commonObject.pop()# to get the only value of the set
            if(schema1.positions[theCommonObject]==schema2.positions[theCommonObject]):#to bridge two schemas, the commonObject must be at the same position
                posOfTheCommonObject=schema1.positions[theCommonObject]
                l=['q1','q2','qf']
                for i,position in enumerate(l):
                    if position!=posOfTheCommonObject:
                        self.bridge(schema1,schema2,position,operations.soustractionBridge)                 
            else:
                return
    def bridge(self,schema1,schema2,position,operationBridge):
        bridgef=schema1.objects[position]+operationBridge+schema2.objects[position] # create string like T2minusT1
        self.addSchema(Schema(bridgef,schema1.objects[position],operations.soustraction,schema2.objects[position])) # create T1-T2=T1minusT2 schema and to the structure

    def detectCommonObject(self,schema1,schema2):#todo
        return schema1.getSetObjects().intersection(schema2.getSetObjects())
    def updateObjectList(self):
        objectList=[]
        for s,schema in enumerate(self.schemas):
            for o,obj in enumerate(schema.getSetObjects()):
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

