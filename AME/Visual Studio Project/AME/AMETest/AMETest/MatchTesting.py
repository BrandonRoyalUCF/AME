from Matcher import *

#ideal confidence matrix test
test1 = [] 
test1.append([1, 2, 3, 4, 5])
test1.append([2, 1, 3, 4, 5])
test1.append([2, 3, 1, 4, 5])
test1.append([2, 3, 4, 1, 5])
test1.append([2, 3, 4, 5, 1])
results1 = [0, 1, 2, 3, 4]

#two have same top match test
test2 = [] 
test2.append([10, 20, 30, 40, 50])
test2.append([11, 13, 30, 40, 50])
test2.append([20, 30, 10, 40, 50])
test2.append([20, 30, 40, 10, 50])
test2.append([20, 30, 40, 50, 10])
results2 = [0, 1, 2, 3, 4]

#someone absent test
test3 = [] 
test3.append([10, 20, 30, 40, 50, 55])
test3.append([11, 13, 30, 40, 50, 60])
test3.append([20, 30, 10, 40, 50, 65])
test3.append([20, 30, 40, 10, 50, 70])
test3.append([20, 30, 40, 50, 10, 74])
results3 = [0, 1, 2, 3, 4]


matcher = Matcher(1, 1)
results = matcher.matchStudents(test3)
print()
print("Results:")
print(results)
print("Expected Results:")
print(results3)

