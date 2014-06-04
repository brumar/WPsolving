import copy
import ast
v={"+":1,"-":-1}


def findAllPossiblesFormulas_stringRepresentation_withOptions(oper,values):
    """
    Custom calls to findAllPossiblesFormulas_stringRepresentation
    corresponding to the kind of formulas we want
    """
    loper1=r1(oper)
    loper2=r2(oper)
    listDefault=[]
    listDefault.append(findAllPossiblesFormulas_stringRepresentation(oper,values))
    list1=[]
    for opers1 in loper1:
        list1.append(findAllPossiblesFormulas_stringRepresentation(opers1,values))
    list2=[]
    for opers2 in loper2:
        list2.append(findAllPossiblesFormulas_stringRepresentation(opers2,values))
    return (listDefault,list1,list2)

#------------------------------------------------------------------------------

def findAllPossiblesFormulas_stringRepresentation(operandLists,values):
    """
    find all the possible formulas
    under the form a+(b-c), a b and c bein given in operandLists
    values are necessary to avoid negative numbers
    """
    possibilities=findAllPossiblesFormulas_listRepresentation(operandLists)
    possibilities_string=turnPossibilitiesIntoStrings(possibilities,values,values.keys(),{},len(operandLists)-1)
    return list(set(possibilities_string))

#------------------------------------------------------------------------------

def findAllPossiblesFormulas_listRepresentation(l,output=[],step=0):
    """
    recurcive function
    find all the possible formula under the composite form ['+','a',['-','b','c']]
    this example means a+|b-c|
    """
    if(step==0):
        output=[]
    if(len(l)==1):
        output.append(l)
    else:
        for operation in ["+","-"]:
            for i,element1 in enumerate(l):
                for element2 in l[i:]:
                    if(element1!=element2): # we avoid formulas such as ['+','b','b']
                        newCompositeElement=[operation,element1,element2]
                        list2=copy.deepcopy(l)
                        list2.remove(element1)
                        list2.remove(element2)
                        list2.append(newCompositeElement)
                        findAllPossiblesFormulas_listRepresentation(list2,output,step+1)#recurcive call
    return output

#------------------------------------------------------------------------------

def turnPossibilitiesIntoStrings(possibilities,values,operandes,formulas,indexToCapture):
    """
    turns ['+','a',['-','b','c']] formulas
    in common forms such as a+(b-c)
    """
    output=[]
    for possibility in possibilities:
        formulas=resolve(possibility,values,operandes,formulas,str(possibility))
        finaleformula=treatFormulas(formulas,"x"+str(indexToCapture))
        output.append(finaleformula)
    return output

#------------------------------------------------------------------------------

def resolve(currentList,values,operandes,formulas,globalList=[],step=0,indexStackHolder=1,verboseFormula=""):
    """
    recurcive function
    transform composite formulas such as ['+','a',['-','b','c']]
    return dictionnaries such as { x2:(b-c), x1 :(a+x2) }
    """
    verboseFormula=str(globalList)
    if (step==0):
        globalList=copy.deepcopy(currentList)
    if not isListFormula(currentList,operandes):
        if(currentList not in v.keys() and currentList not in operandes):
            for sublist in currentList:
                resolve(sublist,values,operandes,formulas,globalList,step+1,indexStackHolder,verboseFormula="")
    else :
        formula,result=getFormulaFromOperation(currentList,values)
        stackHolder="x"+str(indexStackHolder)
        values[stackHolder]=result
        formulas[stackHolder]=formula
        operandes.append(stackHolder)
        verboseFormula=verboseFormula.replace(str(currentList), "'"+stackHolder+"'")
        globalList=ast.literal_eval(verboseFormula)
        g2=copy.deepcopy(globalList)
        resolve( g2,values,operandes,formulas,globalList,0,indexStackHolder+1,verboseFormula)
    return formulas

#------------------------------------------------------------------------------

def getFormulaFromOperation(currentList,values):
    op=currentList[0]
    l1=currentList[1]
    l2=currentList[2]
    val1=values[l1]
    val2=values[l2]
    if(val1<val2):
        val1,val2=val2,val1
        l1,l2=l2,l1
    formula="("+l1+op+l2+")"
    result=val1+val2*v[op]
    return formula,result

#------------------------------------------------------------------------------

def treatFormulas(formulasDic,index):
    """
    transform formulas such as { x2:(b-c), x1 :(a+x2) }
    into common forms such as a+(b-c)
    """
    formulasDic.keys()
    for k1,v1 in formulasDic.iteritems():
        for k2,v2 in formulasDic.iteritems():
            if(k1 in v2):
                formulasDic[k2] = v2.replace(k1,v1)
    output=formulasDic[index]
    return output[1:-1]

#------------------------------------------------------------------------------

def isListFormula(l,operandes):
    """
    test if the list is a formula
    example : ['-','b','c'] is a formula
    """
    return(len(l)==3 and ((l[0] in v.keys() )) and (l[1] in operandes)  and (l[2] in operandes))

#------------------------------------------------------------------------------

def r1(oper):
    """
    generates [a,a,b];[b,b,c];[c,c,b] ...
    [a,b,c] being given
    """
    for o in oper:
        for o2 in oper:
            if(o2!=o):
                yield([o,o2,o2])

def r2(oper):
    """
    generates [a,b,c,c];[a,b,c,a] ....
    [a,b,c] being given
    """
    for o in oper:
        op2=copy.deepcopy(oper)
        op2.append(o)
        yield(op2)

def printMyList(l,defaultindent=1):
    for e in l:
        print ("\t"*defaultindent+e)
    return(len(l))

def printMyDoubleList(l,prefix="set"):
    count=0
    for i,e in enumerate(l):
        print("\t"+prefix+str(i))
        count+=printMyList(e,defaultindent=2)
    return count

if __name__ == "__main__":

    l1,l2,l3=findAllPossiblesFormulas_stringRepresentation_withOptions(["T1","P1","d"],{"P1":7,"T1":16,"d":2})
    print ("solution avec 2 operations, sans reutilisation d'operandes")
    lenght1=printMyList(l1[0])
    print(str(lenght1)+" possibillites")
    print ("solution avec 2 operations, avec reutilisation d'operandes")
    lenght2=printMyDoubleList(l2)
    print(str(lenght2)+" possibillites")
    print ("solution avec 3 operations, avec reutilisation d'operandes")
    lenght3=printMyDoubleList(l3)
    print(str(lenght3)+" possibillites")

    #===============================================================================
    # p=findAllPossiblesFormulas_stringRepresentation(["T1","d","d"],{"P1":7,"T1":16,"d":2,"d2":3})
    # p1=findAllPossiblesFormulas_stringRepresentation(["T1","P1","d","P1"],{"P1":7,"T1":16,"d":2,"d2":3})
    # p2=findAllPossiblesFormulas_stringRepresentation(["T1","P1","d","T1"],{"P1":7,"T1":16,"d":2,"d2":3})
    # p3=findAllPossiblesFormulas_stringRepresentation(["T1","P1","d","d"],{"P1":7,"T1":16,"d":2,"d2":3})
    #===============================================================================
    #print (len(p),len(p1),len(p2),len(p3))