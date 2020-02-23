# Binary Search
# example array
# x = 2
# x = 45 
array = [0,1121,9,5,88,11,42,10,55,1,9,71,43,57]

def quick_sort(array):
    j = len(array)
    if j > 1:
        L = []
        R = [] 
        pivot = array.pop()
        for i in array:
            if i < pivot:
                L.append(i)
            else:
                R.append(i)
        return quick_sort(L) + [pivot] + quick_sort(R)
    else:
        return array 

def binary_search(array, x):
    n = len(array)
    L = 0
    R = n-1 
    while L <= R:
        middle = L + ((R-L)//2)
        if array[middle] == x:
            return array[middle]
        # Move the Left Index to the Right by + 1 position in the array 
        elif array[middle] < x:
            L = middle + 1  
        else:
        # Move the Right Index to the Left by - 1 position in the array
            R = middle - 1
    return False 
  

print('Unsorted Array', '\n', array)
z = quick_sort(array)
print('Sorted Array', '\n', z)
print('Binary Search Result','\n', binary_search(z,1121))