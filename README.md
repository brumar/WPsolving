# Constraint modelling on multi-step arithmetical word problem solving   
Still in development.
We aim to model how children fail to solve multi-step word problem solving.   
Our belief is that, in case of impasse, the representation of the problem may change by reinterpretation of certain sentence in the problem.

# Notebook introducing the model

It can be downloaded at [this page](http://nbviewer.ipython.org/github/brumar/WPsolving/blob/master/MultiStep%20Word%20Problems%20investigation.ipynb)


#### (0) IMPORTS
we import all the python files needed


    import lib.operations as operations # basic variables concerning operations
    from lib.schemas import * # related to the mathematical structure of the problem
    from lib.textRepresentations import * # related to the propositions constituting the problem
    
    from lib.subjectRepresentations import * # related to the problem state of a subject (representations and quantities)
    from lib.paths import * # related to the solving process and its storing and analysis
    from lib.dataManager import * # related to the final steps in the process gathering and printing results of simulation

# [1] Create a problem

## 1.1 Declare the mathematical structure of the problem

Two schema describing the first relationships between the quantities are
**created**


    schema1=Schema("PoissonEF","PoissonEI",operations.addition,"PoissonGAIN","change")
    schema2=Schema("ViandeEF","ViandeEI",operations.addition,"ViandeGAIN","change")
    print(schema1.objects)
    print(schema2.objects)

    {'q1': 'PoissonEI', 'q2': 'PoissonGAIN', 'qf': 'PoissonEF'}
    {'q1': 'ViandeEI', 'q2': 'ViandeGAIN', 'qf': 'ViandeEF'}
    

We then create the problem structure and **add** the schemas


    struct=ProblemStructure()
    struct.addSchema(schema1)
    struct.addSchema(schema2)
    struct.schemas




    [<lib.schemas.Schema instance at 0x000000000A4AFF48>,
     <lib.schemas.Schema instance at 0x000000000A4AFD48>]



And we create the schemas in order to create all the correspondances between the
first two schemas


    struct.addBridgingSchemas(schema1,schema2)


    ls=struct.schemas
    for schem in ls:
        print(schem.objects)

    {'q1': 'PoissonEI', 'q2': 'PoissonGAIN', 'qf': 'PoissonEF'}
    {'q1': 'ViandeEI', 'q2': 'ViandeGAIN', 'qf': 'ViandeEF'}
    {'q1': 'PoissonEI', 'q2': 'ViandeEI', 'qf': 'PoissonEIminusViandeEI'}
    {'q1': 'PoissonGAIN', 'q2': 'ViandeGAIN', 'qf': 'PoissonGAINminusViandeGAIN'}
    {'q1': 'PoissonEF', 'q2': 'ViandeEF', 'qf': 'PoissonEFminusViandeEF'}
    {'q1': 'PoissonEIminusViandeEI', 'q2': 'PoissonGAINminusViandeGAIN', 'qf': 'PoissonEFminusViandeEF'}
    

We then update the field corresponding to set of the object in the problem


    print(struct.objectSet)# before
    struct.updateObjectSet() 
    print(struct.objectSet) #after

    set([])
    set(['PoissonEI', 'PoissonEF', 'PoissonEIminusViandeEI', 'PoissonGAINminusViandeGAIN', 'ViandeEF', 'ViandeGAIN', 'ViandeEI', 'PoissonEFminusViandeEF', 'PoissonGAIN'])
    


    print(struct.objectSet)

    set(['PoissonEI', 'PoissonEF', 'PoissonEIminusViandeEI', 'PoissonGAINminusViandeGAIN', 'ViandeEF', 'ViandeGAIN', 'ViandeEI', 'PoissonEFminusViandeEF', 'PoissonGAIN'])
    

## 1.2 Declare the text informations provided in the problem
#### The propositions

We create a text object


    text=Text()

And we add all the propositions, which are


    text.addTextInformation(TextInformation(Representation(Quantity("PoissonGAIN","P1"),'Au supermarché, le kilo de poisson a augmenté de 5 euros cette année')))
    text.addTextInformation(TextInformation(Representation(Quantity("PoissonEF","T1"),'Un kilo de poisson coute maintenant 12 euros.')))
    text.addTextInformation(TextInformation(Representation(Quantity("PoissonEIminusViandeEI","dEI"),'Au début de l\'année, le kilo de viande coutait le même prix que le kilo de poisson.')))
    text.addTextInformation(TextInformation(Representation(Quantity("PoissonGAINminusViandeGAIN","d"),'Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson')))


    for info in text.textInformations:
        q=info.representations[0].quantity
        print(q.object, q.value)

    ('PoissonGAIN', 'P1')
    ('PoissonEF', 'T1')
    ('PoissonEIminusViandeEI', 'dEI')
    ('PoissonGAINminusViandeGAIN', 'd')
    

#### The Goal


    text.setGoal(TextGoal(Goal('ViandeEF','Combien coute le kilo de viande maintenant?')))

#### The alternative representations


    text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEI","P1"),'Au supermarché, le kilo de poisson était de 5 euros'))
    text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEF","P1"),'Au supermarché, le kilo de poisson coute 5 euros'))
    text.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("PoissonEI","T1"),'Un kilo de poisson était de 12 euros.'))
    text.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","dEI"),'Au la fin de l\'année, le kilo de viande coute le même prix que le kilo de poisson.'))
    text.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","dEI"),'Le kilo de viande a augmenté du même prix que le kilo de poisson.'))
    text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","d"),'Le kilo de viande a augmenté de 3 euros'))
    text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","-d"),'Le kilo de viande a diminué de 3 euros'))
    text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","d"),'Le kilo de viande vaut 3 euross de moins que le kilo de poisson'))
    text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeEF","d"),'Le kilo coute 3 euros à la fin'))

Let's inspect the different alternative representations pertaining to the fourth
text proposition


    textInfo=text.textInformations[3]
    for representation in textInfo.representations:
        print(representation.quantity.object,representation.quantity.value)

    ('PoissonGAINminusViandeGAIN', 'd')
    ('ViandeGAIN', 'd')
    ('ViandeGAIN', '-d')
    ('PoissonEFminusViandeEF', 'd')
    ('ViandeEF', 'd')
    

## 1.3 final step to construct the problem
A problem is the association of a **structure** and a **text** as defined above


    probleme1=Problem(struct,text)

Set the initial values


    probleme1.setInitialValues({"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})

# [2] Handle solver object

### 2.1 Init its first problem representation


    upD=Updater(probleme1) # create the problem state
    upD.startAsUnderstood() # init the problem state, we start with expert representations

Updater has a central role in the program as it :
- Check if moves are possible
- Apply moves (schemas, reinterpretations) and then update its main attribute
**problemState** which is also an important class

### 2.2 (side note) about the problem state
- The **quantitiesDic** : current object-values association
- **representations** which indicates which representations are currently
selected


    probState=upD.problemState
    print "quantity dic: ", probState.quantitiesDic.dic
    print "\n representations: ",probState.representations

    quantity dic:  {'PoissonEI': [], 'PoissonEF': [12], 'PoissonEIminusViandeEI': [0], 'PoissonGAINminusViandeGAIN': [3], 'ViandeEF': [], 'ViandeGAIN': [], 'ViandeEI': [], 'PoissonEFminusViandeEF': [], 'PoissonGAIN': [5]}
    
     representations:  [0, 0, 0, 0]
    

### 2.3 Define the behavioral constraint of the solvers


    c1=IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0) 

This constraints implies that no negative values can be associated with object
which has 'EI' or 'EF' as substring


    c2=BehavioralConstraint(breakTheOldOne=True)

This constraints implies that if there is an alternative representation is
selected, then the quantity formed by its prevous state is destroyed. In other
terms, only one representation of the the same proposition is active at the same
time.

### 2.4 Create the solvers (final step)


    constraints=[c1,c2]


    solver1=Solver(upD,constraints)

## 2.5 Manually run the solver

### 2.5.1 Apply a schema

- check what are the schemas which can be applied.


    solver1.updater.updateAppliableSchemas()
    l=solver1.updater.appliableSchemaList
    print(l)
    print (l[0].objects)

    [<lib.schemas.Schema instance at 0x000000000A4AFF48>, <lib.schemas.Schema instance at 0x000000000A4AFCC8>, <lib.schemas.Schema instance at 0x000000000A68E148>]
    {'q1': 'PoissonEI', 'q2': 'PoissonGAIN', 'qf': 'PoissonEF'}
    

- apply a schema


    move1=Move(l[0]) # a move is one level more abastract than schema or representation
    stepInformations1=solver1.updater.applyMove(move1,solver1.constraints) # we can then use the function applyMove for schemas or representation

*stepInformations* is an instance of InfoStep (in *subjectRepresentations.py*)
and contains many informations related to the concrete application of the move,
and can be used to inspect precisely a solution path.
Among others :


    print(stepInformations1.formulaFirstPart,stepInformations1.valueToFind,stepInformations1.operands,stepInformations1.unknow)

    (' 12 - 5 ', 7, ['PoissonEF', 'PoissonGAIN'], 'PoissonEI')
    

In this specific case PoissonEI has been found knowing PoissonGAIN and
PoissonEF.
A new quantity is then now available :


    solver1.updater.problemState.quantitiesDic.dic['PoissonEI']




    [7]



### 2.5.2 Apply a representation change

#### informations on representations state and representations change


    solver1.updater.updatePossibleRepresentationChange()
    print len(solver1.updater.possibleRepresentationChangeList), "representations change are possible"
    print solver1.updater.problemState.representations, " is the current representations state"
    
    repChange=solver1.updater.possibleRepresentationChangeList[5]
    print "\nindex of the proposition in the text", repChange.indexTextInformation
    print "index of the alternative representation of this proposition", repChange.indexSelectedRepresentation
    rep=solver1.updater.problem.text.textInformations[repChange.indexTextInformation].representations[repChange.indexSelectedRepresentation]
    print(rep.quantity.object, rep.quantity.value)

    9 representations change are possible
    [0, 0, 0, 0]  is the current representations state
    
    index of the proposition in the text 3
    index of the alternative representation of this proposition 1
    ('ViandeGAIN', 3)
    

#### Apply a representation change works broadly the same way as applying a
Schema :


    move2=Move(repChange)
    stepInformations2=solver1.updater.applyMove(move2,solver1.constraints)
    print solver1.updater.problemState.representations, " is the new representations state"

    [0, 0, 0, 1]  is the new representations state
    

Let's check that this new value is now in the quantitiesDic


    solver1.updater.problemState.quantitiesDic.dic['ViandeGAIN']




    [3]



As we used the constraint *c2=BehavioralConstraint(breakTheOldOne=True)* we can
see that the old representation of this text information is erased.


    oldrep=solver1.updater.problem.text.textInformations[3].representations[0]
    print "before : ",(oldrep.quantity.object, oldrep.quantity.value)
    print "after : ", solver1.updater.problemState.quantitiesDic.dic[oldrep.quantity.object]

    before :  ('PoissonGAINminusViandeGAIN', 3)
    after :  []
    

### 2.5.3 Use steps classes to keep records of the path
Four classes are involved to keep such record :
- StepInfo (explained above)
- Step : has step info as attribute but also
    - An unique id
    - The ids of the step before him (father)
    - The ids of the steps after him (children)
- TreePaths : designed to store the steps, and the paths (as three and as
lines).
- Path : give the essential informations of a path

#### 2.5.3.1 steps

By convention the first step has for father the step with the id=0


    step1=Step(move1,parentId=0, infos=stepInformations1,level=0)
    step2=Step(move2,parentId=step1.sId, infos=stepInformations2, level=1) #we use the id of step1 to create step2

We can check if the problem is solved by the solved attribute


    print "is the problem solved: ",step2.solved

    is the problem solved: 


    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)

    <ipython-input-134-26f944a831e7> in <module>()
    ----> 1 print "is the problem solved: ",step2.solved
    

    AttributeError: Step instance has no attribute 'solved'


Updater has no rollback feature for the moment, which means that

#### 2.5.3.2 TreePath

We can now add the step in the TreePaths


    tp=TreePaths(solver1.updater) # or use the treePath instance tied to the solver : tp=solver1.TreePaths
    tp.addStep(step1)
    tp.addStep(step2)

    
    

TreePath allows many things :
- Adding step to a treepaths bind the steps to its children


    id1=step1.childrenIds
    id1




    [UUID('44c1970a-536a-458a-889d-e6418133f57e')]



- TreePaths has a method to generate a tree according the different paths taken


    tp.scanTree()
    print(tp.treeOutput)

     12 - 5 = 7  (PoissonEI)

    	3 interpreted as ViandeGAIN

    		d : interpretation -> ViandeGAIN

    
    

[Note] The last line gives a summary of what happenned. In this specific case we
stopped the solving process without finding the solution. A more complex path
would give such string :
*T1-d : interpretation ->
PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF*
This line is produced by the TreePath method **trackBack** which traceback the
different paths and gives the last line. TrackBack is called in scanTree
whenever a path is ended.


    print(tp.trackBack(step2.sId))

    d : interpretation -> ViandeGAIN
    

trackBack is also usefull to store the different paths in lines which can be
found in the *pathList* attribute of the updater.


    firstPath=tp.pathList[0]
    print(firstPath.formula)
    print(firstPath.objectFormula)
    print(firstPath.interpretationsSummary)
    print(firstPath.valueFound)
    print(firstPath.problemSolved)

    d
    ViandeGAIN
     # d interpreted as ViandeGAIN
    3
    False
    

## 2.6 Automatic use of solver to generate a solution space

### 2.6.1 Simple example : only solve

#### 2.6.1.1 solver.SOLVER instruction

We create a new solver from start


    upD.startAsUnderstood()
    autoSolver=Solver(upD,constraints)

Now, we give the pattern of actions the solver has to explore


    l=[autoSolver.SOLVER]
    autoSolver.generalSequentialSolver(listOfActions=l)

This is the simplest example, the instruction solver.SOLVER means that schemas
will be applied until the solution is found. At each step, the research tree has
as many branches as schemas which can be applied.

#### 2.6.1.2 inspect the solution space

We can now check what gives treeOutput and pathList with the solver process


    autoSolver.TreePaths.scanTree()
    print(autoSolver.TreePaths.treeOutput)

     12 - 5 = 7  (PoissonEI)

    	 7 - 0 = 7  (ViandeEI)

    		 5 - 3 = 2  (ViandeGAIN)

    			 7 + 2 = 9  (ViandeEF)

    				(T1-P1)+(P1-d) : interpretation -> ((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF

    			 3 + 0 = 3  (PoissonEFminusViandeEF)

    				 7 + 2 = 9  (ViandeEF)

    					(T1-P1)+(P1-d) : interpretation -> ((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF

    				 12 - 3 = 9  (ViandeEF)

    					T1-d : interpretation -> PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF

    		 3 + 0 = 3  (PoissonEFminusViandeEF)

    			 5 - 3 = 2  (ViandeGAIN)

    				 7 + 2 = 9  (ViandeEF)

    					(T1-P1)+(P1-d) : interpretation -> ((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF

    				 12 - 3 = 9  (ViandeEF)

    					T1-d : interpretation -> PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF

    			 12 - 3 = 9  (ViandeEF)

    				T1-d : interpretation -> PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF

    	 5 - 3 = 2  (ViandeGAIN)

    		 7 - 0 = 7  (ViandeEI)

    			 7 + 2 = 9  (ViandeEF)

    				(T1-P1)+(P1-d) : interpretation -> ((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF

    			 3 + 0 = 3  (PoissonEFminusViandeEF)

    				 7 + 2 = 9  (ViandeEF)

    					(T1-P1)+(P1-d) : interpretation -> ((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF

    				 12 - 3 = 9  (ViandeEF)

    					T1-d : interpretation -> PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF

    		 3 + 0 = 3  (PoissonEFminusViandeEF)

    			 7 - 0 = 7  (ViandeEI)

    				 7 + 2 = 9  (ViandeEF)

    					(T1-P1)+(P1-d) : interpretation -> ((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF

    				 12 - 3 = 9  (ViandeEF)

    					T1-d : interpretation -> PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF

    			 12 - 3 = 9  (ViandeEF)

    				T1-d : interpretation -> PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF

    	 3 + 0 = 3  (PoissonEFminusViandeEF)

    		 7 - 0 = 7  (ViandeEI)

    			 5 - 3 = 2  (ViandeGAIN)

    				 7 + 2 = 9  (ViandeEF)

    					(T1-P1)+(P1-d) : interpretation -> ((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF

    				 12 - 3 = 9  (ViandeEF)

    					T1-d : interpretation -> PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF

    			 12 - 3 = 9  (ViandeEF)

    				T1-d : interpretation -> PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF

    		 5 - 3 = 2  (ViandeGAIN)

    			 7 - 0 = 7  (ViandeEI)

    				 7 + 2 = 9  (ViandeEF)

    					(T1-P1)+(P1-d) : interpretation -> ((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF

    				 12 - 3 = 9  (ViandeEF)

    					T1-d : interpretation -> PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF

    			 12 - 3 = 9  (ViandeEF)

    				T1-d : interpretation -> PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF

    		 12 - 3 = 9  (ViandeEF)

    			T1-d : interpretation -> PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF

     5 - 3 = 2  (ViandeGAIN)

    	 12 - 5 = 7  (PoissonEI)

    		 7 - 0 = 7  (ViandeEI)

    			 7 + 2 = 9  (ViandeEF)

    				(T1-P1)+(P1-d) : interpretation -> ((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF

    			 3 + 0 = 3  (PoissonEFminusViandeEF)

    				 7 + 2 = 9  (ViandeEF)

    					(T1-P1)+(P1-d) : interpretation -> ((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF

    				 12 - 3 = 9  (ViandeEF)

    					T1-d : interpretation -> PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF

    		 3 + 0 = 3  (PoissonEFminusViandeEF)

    			 7 - 0 = 7  (ViandeEI)

    				 7 + 2 = 9  (ViandeEF)

    					(T1-P1)+(P1-d) : interpretation -> ((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF
	ETC....

    print(str(autoSolver.TreePaths.pathsCount)+" different paths have been discovered" )

    41 different paths have been discovered
    

Let's inspect the first path recorded in the treePaths


    aPath=autoSolver.TreePaths.pathList[0]
    print(aPath.formula)
    print(aPath.objectFormula)
    print(aPath.interpretationsSummary)
    print(aPath.valueFound)
    print(aPath.problemSolved)

    (T1-P1)+(P1-d)
    ((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF
    
    9
    True
    

### 2.6.2 Other intructions

solver.SCHEMAS and solver.INTERP are two other instructions.
For example if the list of actions is [solver.SCHEM,solver.INTERP,solver.SOLVE],
then the automatic solver will start with applying a schema, then applying a
interpretation change, and finally will finish by a solving process as seen
above.
This list of instruction will find all the paths which has this kind of pattern.


    upD.startAsUnderstood()
    autoSolver2=Solver(upD,constraints)
    autoSolver2.generalSequentialSolver(listOfActions=[autoSolver2.SCHEMA,autoSolver2.INTERP,autoSolver2.SOLVER])

Let's inspect a path


    autoSolver2.TreePaths.scanTree()
    aPath=autoSolver2.TreePaths.pathList[43]
    print(aPath.formula)
    print(aPath.objectFormula)
    print(aPath.interpretationsSummary)
    print(aPath.valueFound)
    print(aPath.problemSolved)

    P1-d
    PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF
     # P1 interpreted as PoissonEF
    2
    True
    

# [3] Handle the simulated datas

SimulatedDatas is a class used to store different treepath and eventually reduce
some redondancies between the different paths.


    simulatedDatas=SimulatedDatas()
    simulatedDatas.addDataSet(solver1.TreePaths.pathList,"pbm1","Manual Solver")
    simulatedDatas.addDataSet(autoSolver.TreePaths.pathList,"pbm1","Expert Solver")
    simulatedDatas.addDataSet(autoSolver2.TreePaths.pathList,"pbm1","Another Solver")

simulatedDatas can print its datas in a CSV via **simulatedDatas.printCSV()** or
in the console using **simulatedDatas.printLines()**


    simulatedDatas.printLines()

    ('pbm1', 'Expert Solver', ['T1-d', True, 'PoissonEF-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF', ''])
    ('pbm1', 'Expert Solver', ['(T1-P1)+(P1-d)', True, '((PoissonEF-PoissonGAIN)-PoissonEIminusViandeEI)+(PoissonGAIN-PoissonGAINminusViandeGAIN)=ViandeEF', ''])
    ('pbm1', 'Another Solver', ['(T1+P1)-d', True, '((PoissonEF-PoissonGAIN)+PoissonGAIN)-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF', ' # T1 interpreted as PoissonEI'])
    ('pbm1', 'Another Solver', ['(T1+P1)-d', True, '(PoissonEI+PoissonGAIN)-(PoissonGAINminusViandeGAIN+PoissonEIminusViandeEI)=ViandeEF', ' # T1 interpreted as PoissonEI'])
    ('pbm1', 'Another Solver', ['P1', False, 'PoissonGAIN-PoissonGAINminusViandeGAIN=ViandeGAIN', ' # dEI interpreted as PoissonGAINminusViandeGAIN'])
	etc....