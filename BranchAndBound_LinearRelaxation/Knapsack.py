from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

import sys
sys.setrecursionlimit(1100)


def greedy(cost_density_list_sorted, takenList, capacity):

    value_best = 0
    weight = 0

    i = 0
    for density , item in cost_density_list_sorted:

        if weight + item.weight <= capacity:
            value_best += item.value
            weight += item.weight
            takenList[item.index] = 1

        i += 1

    return (takenList, value_best)


def CalculateBestPossible(cost_density_list_sorted, BestPossibleList, capacity):

    value_best = 0
    weight = 0

    i = 0
    for density , item in cost_density_list_sorted:


        if BestPossibleList[i]:

            if weight + item.weight <= capacity:
                value_best += item.value
                weight += item.weight
            else:
                Remaining_capacity = capacity - weight
                allowed_weight = Remaining_capacity
                fract_cost = (allowed_weight / item.weight) * item.value
                value_best += fract_cost

                break

        i += 1

    return value_best



def BranchAndBound(items , takenList, cost_density_list_sorted, BestPossibleList ,BestPossible, depth, currentValue, currentWeight, capacity, BestSoFar=[0]):

    BestPossible = CalculateBestPossible(cost_density_list_sorted, BestPossibleList, capacity)

    #print(BestPossible , BestSoFar[0], BestPossibleList)

    if BestPossible < BestSoFar[0]:
        #print('Prunned')
        return (takenList, currentValue)

    if depth == len(items):
        #print('BestPoss, CurrentVal = ', BestPossible, currentValue )

        if BestSoFar[0] < currentValue:
            BestSoFar[0] = currentValue
            #print('New Best - ', BestSoFar[0])

        return (takenList, currentValue)

    else:

        if currentWeight + items[depth].weight <= capacity:

            # Include
            new_TakenList = takenList[:]
            new_TakenList[ items[depth].index ] = 1
            new_currentValue = currentValue + items[depth].value
            new_depth = depth + 1
            new_currentWeight = currentWeight + items[depth].weight
            new_BestPossibleList = BestPossibleList[:]
            
            Out1 = BranchAndBound(items, new_TakenList, cost_density_list_sorted, new_BestPossibleList, BestPossible, new_depth, new_currentValue, new_currentWeight, capacity, BestSoFar)


            #Do not include
            new_TakenList = takenList[:]
            new_currentValue = currentValue
            new_depth = depth + 1
            new_currentWeight = currentWeight 
            new_BestPossibleList = BestPossibleList[:]
            new_BestPossibleList[ items[depth].index ] = 0

            Out2 = BranchAndBound(items, new_TakenList, cost_density_list_sorted, new_BestPossibleList, BestPossible, new_depth, new_currentValue, new_currentWeight, capacity, BestSoFar)

            if Out1[1] > Out2[1]:
                return Out1[:]
            else:
                return Out2[:]
        
        else:

            new_TakenList = takenList[:]
            new_currentValue = currentValue
            new_depth = depth + 1
            new_currentWeight = currentWeight 
            new_BestPossibleList = BestPossibleList[:]
            new_BestPossibleList[ items[depth].index ] = 0

            Out2 = BranchAndBound(items, new_TakenList, cost_density_list_sorted, new_BestPossibleList, BestPossible, new_depth, new_currentValue, new_currentWeight, capacity, BestSoFar)

            return Out2[:]


if __name__ == '__main__':


    file_location = "KnapSack_InputFile"


    problem = open(file_location, 'r')
    input_data = problem.read()

    problem.close()


    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    cost_density_list_sorted = [ (item.value / item.weight , item) for item in items ]
    cost_density_list_sorted.sort(key=lambda x : x[0])
    cost_density_list_sorted.reverse()

    #print(cost_density_list)

    value_best = CalculateBestPossible(cost_density_list_sorted, [1]*len(items), capacity)


    #print('Best Possible value = ', value_best, capacity)


    taken = [0]*len(items)

    Ans = []

    if len(items) < 30:
        print('Executing Branch And Bound with linear relaxation')
        Ans = BranchAndBound(items, taken, cost_density_list_sorted, [1]*len(items), value_best, 0, 0, 0, capacity, BestSoFar=[0])
    else:
        print('Executing Greedy')
        Ans = greedy(cost_density_list_sorted, taken, capacity)

    taken = Ans[0]
    value = Ans[1]
    
    print('Taken Array : ', taken)
    print('Value : ', value)