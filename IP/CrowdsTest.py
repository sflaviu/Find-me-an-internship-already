from random import randint

class ExperimentCrowdsProtocol:

    # 5 honest,1 corrupt
    def find_result(self):
        members=6
        sender=0
        bad=5
        observed=[]
        for i in range(members-1):
            observed.append(0)
        for numberOfMessages in range(3,7):
            positive = falsePositive = nothing = 0
            for iterations in range(10000):
                for i in range(members-1):
                    observed[i]=0
                for i in range(numberOfMessages):
                    previousClient = sender
                    rand = randint(1,100)
                    while rand > 20:
                        nextClient = randint(0,5)
                        if nextClient==bad and previousClient != bad:
                            observed[previousClient] += 1
                        previousClient = nextClient
                        rand = randint(1,100)
                            
            
                okPositive = 0
                okNothing = 1
                for i in range(members-1):
                    if observed[i] >= 2:
                        okNothing = 0
                        if i==sender:
                            positive += 1
                            okPositive = 1
                
                if okNothing == 1:
                    nothing += 1
                else:
                    if okPositive==0:
                        falsePositive += 1
            sum = positive + falsePositive + nothing
            pbPositive=positive/sum
            pbFalsePositive=falsePositive/sum
        
            print(str(numberOfMessages)+" "+str(pbPositive)+" "+str(pbFalsePositive))
                    
        
test=ExperimentCrowdsProtocol()
test.find_result()
