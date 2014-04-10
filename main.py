import operations

class ProblemStructure:
    schemas=[]
    objects=[]
    def __init__(self):
        pass
    def addSchema(self,schema):
        self.schemas.append(schema)
    def addBridgingSchema(self,schema1,schema2,names=[]):#Create all the schemas and objects related to eventual relations between two schemas
                                                         #convention : schema1.qf > schema2.qf
        commonObject=detectCommonObject(schema1,schema2)
        if(commonObject=="none"):  
            bridgef=schema1.qf+operations.soustractionBridge+schema2.qf # create string like T2minusT1
            bridge1=schema1.q1+operations.soustractionBridge+schema2.q1
            bridge2=schema1.q2+operations.soustractionBridge+schema2.q2
            self.addSchema(Schema(bridgef,schema1.qf,operations.soustraction,schema2.qf)) # create T1-T2=T1minusT2 schema and to the structure
            self.addSchema(Schema(bridge1,schema1.q1,operations.soustraction,schema2.q1)) # P1-P2=P1minusP2
            self.addSchema(Schema(bridge2,schema1.q2,operations.soustraction,schema2.q2))
            self.addSchema(Schema(bridge2,schema1.q2,operations.soustraction,schema2.q2))#
        else :
            #todo
    def detectCommonObject(schema1,schema2):#todo
        return "none"
          
##
##class SuperSchema(self,schema1,schema2,names=[]):
##    def  __init__(self,schema1,schema2,names=[]):
##        self.schema1=schema1
##        self.schema2=schema2
##    
    

class Schema: #a simple schema is a schema binding 3 values (e.g. a+b=c)
    def  __init__(self,qf,q1,operation,q2,name=""):#convention : q1 must be bigger than q2
        self.name=name
        self.qf=qf
        self.q1=q1
        self.operation=operation
        self.q2=q2
#    def solve()
    
schema1=Schema("T1","p1",operations.addition,"p2","partie-tout (1)")
schema2=Schema("T2","p3",operations.addition,"p2","partie-tout (2)")
struc=ProblemStructure()
struc.addSchema(schema1)
struc.addSchema(schema2)
struc.addBridgingSchema(schema1,schema2)
#print(struc.schemas.pop().q1)
