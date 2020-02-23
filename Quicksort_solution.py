from random import randint

def array_generator(size=15,max=30):
    return [randint(0,max)for _ in range(size)]

def quick_sort_b(array):
    length = len(array)
    if length <= 1:
        return array 
    else:
        pivot = array.pop()
    
    smaller = []
    larger = [] 
    for item in array:
        if item < pivot:
            smaller.append(item)
        else:
            larger.append(item)
    return quick_sort_b(smaller) + [pivot] + quick_sort_b(larger)

if __name__ == "__main__":
    test_array = array_generator(size=15,max=30)
    print('Unsorted','\n',test_array)
    test2_array = quick_sort_b(test_array)
    print('Sorted','\n',test2_array)

