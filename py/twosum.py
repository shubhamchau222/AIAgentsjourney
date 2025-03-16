## two sum (finding the if array having two elements whose sum equal to given number)
# arr= [2, 7, 11, 3] #target 10

def twosum(arr, num):
    #O(N2)
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[i] + arr[j] == num:
                return (arr[i], arr[j])
    return []

def twosumHash(arr, num):
    bucket=dict()
    for i in range(len(arr)):
        diff= num - arr[i]
        if diff in bucket.keys():
            return [arr[i], diff]
        else:
            bucket[arr[i]]= i
    return []

## Another Approch (Two Pointer Approch)

def twoPointer(arr, num):
    """This method needs array to be sorted.."""
    #sort the array
    arr= sorted(arr)
    first=0
    last= -1
    for i in range(len(arr)):
        if arr[i] + arr[last] > num:
            last= last -1
        elif arr[i] + arr[last] < num:
            first = first + 1 
        elif arr[i] + arr[last] == num:
            return [arr[i], arr[last]]
    return []




if __name__ == "__main__":
    arr= [2, 7, 11, 3]
    num=10
    a= twosum(arr, num)
    b= twosumHash(arr,num)
    c= twoPointer(arr,num)
    print("Using Bruite Force Approch", a)
    print("Using Hash Map Approch", b)
    print("Using Two pointer Approch", c)
