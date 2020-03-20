from functools import reduce

# Removing Zeros & None
def sort_remove_zeros(array):
    temp = []
    clean_array = []
    integer_array = []
    for i in array:
        temp.append(i)
    temp = sorted(temp)

    for value in temp:
        if value != None:
            clean_array.append(value)
    integer_array = [i for i in clean_array if i != 0]
    return integer_array


def partition(array):
    temp = sort_remove_zeros(array)
    negative = []
    positive = []
    i = 0

    #2) Split into sub-arrays based on (+) or (-) integer value list
    for i in range(len(temp)):
        if temp[i] < 0:
            negative.append(temp[i])
            i +=1
        elif temp[i] > 0:
            positive.append(temp[i])
            i +=1
    return negative


def absolute_value(array):
    even = []
    odd = []
    negative = partition(array)
    if len(negative) == 0:
        return None
    else:
        for i in range(len(negative)):
            if len(negative)%2 == 0:
                even.append(abs(negative[i]))
            else:
                odd.append(abs(negative[i]))
        if len(even) == 0:
            odd.pop()
            result = odd
        else:
            result = even
        return result
    

def solution(array):

    ##Special Case Handling
    if len(array) == 1:
        return str(array[0])
    
    if len(set(array)) == 1 and array[0] == 0:
        return str(array[0])
    
    if len(set(array)) == 2:
        comparison = sorted(list(set(array)))
        if comparison[0] < 0 and comparison[1] == 0:
            return str(comparison[1])
    
    input_sub_array = absolute_value(array)

    if input_sub_array == None:
        # this means we know to use temp array from partition, which returns positive
        temp = sort_remove_zeros(array)
        product = reduce((lambda x,y: x*y),temp)
    else: 
        #we combine integer list + unique integer from the list 
        product_array = list(input_sub_array) + list(filter(lambda x:x>0,array))
        product = reduce((lambda x,y: x*y),product_array)
    return str(product)


if __name__ == "__main__":
    #print(solution([2, 0, 2, 2, 0]))
    print(solution([0, 0]))
    print(solution([0, -9999]))
    # print(solution([-2, -2, -2, -2, -2]))
    # print(solution([-2, -3, 4, -5]))
    # print(solution([2,-3,1,0,-5]))
    # print(solution([-2,-2,-2,-2,-2]))
    # print(solution([9,4]))
    print(solution([-10000,0]))
    print(solution([-2, -3, 4, -5,-2, -3, 4, -5,-2, -3, 4, -5,-2, -3, 4, -5,-2, -3, 4, -5,-2, -3, 4, -5,-2, -3, 4, -5,-2, -3, 4, -5,-2, -3, 4, -5,-2, -3, 4, -5,0]))