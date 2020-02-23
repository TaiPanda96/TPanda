
from random import randint
#MergeSort(arr[], l,  r)
#If r > l
    # 1. Find the middle point to divide the array into two halves:  
           #  middle m = (l+r)/2
    # 2. Call mergeSort for first half:   
            # Call mergeSort(arr, l, m)
    # 3. Call mergeSort for second half:
            # Call mergeSort(arr, m+1, r)
    # 4. Merge the two halves sorted in step 2 and 3:
            # Call merge(arr, l, m, r)

# arr = [9,11,222,354,33,12,67,89,0,6,32,4,77]
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2 
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0 

        while i < len(L) and j < len(R):
            if L[i]< R[j]:
                arr[k] = L[i]
                i+=1
            else:
                arr[k] = R[j]
                j+=1
            k +=1 
    
     # Checking if any element was left 
        while i < len(L): 
            arr[k] = L[i] 
            i+=1
            k+=1
          
        while j < len(R): 
            arr[k] = R[j] 
            j+=1
            k+=1

def print_result(arr):
    for i in range(len(arr)):
        print(arr[i],end=" ")
    print()

if __name__ == "__main__":
    arr = [9,11,222,354,33,12,67,89,0,6,32,4,77]
    print("Given Array",end="\n")
    print_result(arr)
    merge_sort(arr)
    print("Sorted Array is:",end="\n")
    print_result(arr)
