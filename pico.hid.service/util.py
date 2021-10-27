import os
from numpy import log as ln

fibonacci = lambda n:pow(2<<n,n+1,(4<<2*n)-(2<<n)-1)%(2<<n)


# Function to find the `k` closest elements to `target` in a sorted integer array `nums`
def findKClosestElements(nums, k, target):
 
    left = 0
    right = len(nums) - 1
 
    while right - left >= k:
        if abs(nums[left] - target) > abs(nums[right] - target):
            left = left + 1
        else:
            right = right - 1
 
    return nums[left:left + k]

def calculateNextReconnectInterval(counter: int, currentInterval: float) -> float:
    return max(currentInterval + ln(counter), currentInterval)

def resolvePath(pathRaw: str) -> str:
    variable = pathRaw.split('<',1)[-1].split('>',1)[0]
    if variable != pathRaw:
        expandedVar = os.getenv(variable)
        if expandedVar is not None:
            return pathRaw.replace(f"<{variable}>", expandedVar)
    return pathRaw