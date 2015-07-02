'''
#need a class for currency variables; ex AvgTck:
calcTck = Vol/Cnt
roundb = "%.2f" %round(calcb, 2)
AvgTck = float(roundb)

from DataQuery import DB_selectAllDataOfMCCCodeType
Vol = 10000 #input from user
Cnt = 1000    #input from user
Cost = 500  #input from user


def AvgTck(Vol, Cnt):
    # global AvgTck
    calcTck = Vol/Cnt
    roundb = "%.2f" %round(calcTck, 2)
    AvgTck = float(roundb)
    return AvgTck

def effRate(cost, vol):
    global effRate
    effRate = float(cost/vol)
    return effRate


mcc_objs = DB_selectAllDataOfMCCCodeType()
category = []
vtotal = []
ctotal = []
rate = []
trans = []

for mcc_ob in mcc_objs:
    category.append(mcc_ob.cagegory)
    vtotal.append(mcc_ob.percentVol)
    ctotal.append(mcc_ob.percentCount)
    rate.append(mcc_ob.rate)
    trans.append(mcc_ob.transactionFee)
        


MCCDict = {'Category': category, 
            '%VTotal': vtotal,
            '%CTotal': ctotal,
            'rate': rate, 
            'tran fee': trans,
            }   

Category = []
VTotal = []
CTotal = []
Rate = []
Trans_fee = []
DistLst = []
VolLst = []
CntLst = []
CostLst = []
MiscCost = []


#fix this later
def calcBcost(Vol, Cnt, assess=0.0011, nabu=0.0195):
    global bcost
    calcb = (Vol*assess) + (Cnt*nabu)
    roundb = "%.2f" %round(calcb, 2)
    bcost = float(roundb)

def calcCost(input):
    
    Calculates the distribution of interchange levels by Volume and Count
    These will eventually be applied to the rate and tran fee to determine cost 
    of the merchant's volume
    
    Vitems = input['%VTotal']
    Citems = input['%CTotal']
    RateFee = input['rate'] # [0.0005, 0.0171]
    TranFee = input['tran fee']
    # n = len(input['Category'])

    for item in Vitems:
        #generate Volume Distribution
        addv = Vol * item
        rounded = "%.2f" %round(addv, 2) #still returning with 1 decimal instead of 2
        clean = float(rounded)
        VolLst.append(clean)
        
    works but will be slightly off in certain scenarios -- come back and correct logic later
    for item in Citems:
        #generate Count Distribution
        addc = Cnt * item
        clean = int(addc)
        CntLst.append(clean)
    
    for item in zip(VolLst,CntLst):
        #append to final Distribution list which can be used against rate and tran fee to 
        #calculate fees
        DistLst.append(item)
    
    x = 0
    for item in DistLst:
        #Calculate Cost list using distributions and MCCDict from DB
        #needs to return Dict that arranges things by categories for future use
        rcost = item[0] * RateFee[x]
        tcost = item[1] * TranFee[x]
        roundr = "%.2f" %round(rcost, 2)
        roundt = "%.2f" %round(tcost, 2)
        CostLst.append(float(roundr))
        CostLst.append(float(roundt))
        x += 1


def compareCost(effRate, rawCost, Vol, Cnt):
    result = 'something messed up' 
    QP=0.0275
    NQP=0.035
    NQT=0.15
    p=0.80
    dp=0.20
      
    flatRCost = ((Vol*p)*QP)+((Vol*dp)*NQP)+((Cnt*dp)*NQT)
    FRcalc = (flatRCost/Vol)
    comp = effRate - rawCost
    compFR = effRate - FRcalc
    effResult = 'your effective rate is ' "{0:.2f}%".format(effRate*100)
    rawResult = 'and the projected raw costs are '"{0:.2f}%".format(IntBrandC*100)
    flatRate = 'the flat rate projection at 2.75%/transaction with 20% downgrade comes to : ' "{0:.2f}%".format(FRcalc*100)
    if comp > 0.025:
        # print 'the effective rate is:', "{0:.2f}%".format(effRate*100),\
        # 'and the projected raw costs are '"{0:.2f}%".format(IntBrandC*100),\
        print effResult, rawResult, ', you are most likely overpaying'
    elif 0.025 > comp > 0.015:
        result =  effResult, flatRate, ' there is most likely better pricing for you out there'
    elif 0.015 > comp > 0.010:
        result = effResult, flatRate, ', there might be better pricing out there'
    elif 0.010 > comp > 0.005:
        result = effResult, flatRate, ', according to our calculations, you have decent pricing'
    elif 0.005 > comp > 0.000:
        result =  effResult, flatRate, ', you have great pricing'
           
    elif compFR > 0.015:
        result = effResult, flatRate, ', you might want to look into no monthly fees and a flat rate scheme'     
    
    return result
        
#program tests
calcBcost(Vol, Cnt)
calcCost(MCCDict)
AvgTck = AvgTck(Vol,Cnt)
effRate = effRate(Cost,Vol)
IntBrandC = (sum(CostLst, bcost)/Vol)
print
compareCost(effRate,IntBrandC,Vol,Cnt)
print

# compareCost(CostLst)
print effRate, IntBrandC, effRate-IntBrandC
print 'the effective rate is:', "{0:.2f}%".format(effRate*100)
print 'the Distribution list looks like: ', DistLst

print 'brand costs: ', bcost
print 'the Cost list looks like: ', CostLst
print
print 'the projected raw cost is $%.2f on %.2f of Volume,' %(sum(CostLst),Vol),\
'thats a '"{0:.2f}%".format(IntBrandC*100),'projected rate on interchange(issuing banks) and brand fees (VISA/MC).'
print
print 'Average Ticket: ', AvgTck
'''