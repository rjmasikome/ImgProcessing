import matplotlib.pyplot as plt #use for debugging
import csv

def getAverage(taskNum, maskArray):
	averageArray = []
	for mask in maskArray :
		filename = "data"+ str(taskNum) +"/" + str(mask) + ".txt"
		results = list(csv.reader(open(filename), delimiter=";"))
		results = filter(None,results[0])
		results = [float(x) for x in results]
		averageArray.append(sum(results)/len(results))

	return averageArray

def plotGraph():
	maskArray = [3,5,7,9,11,13,15,17,19,21]
	averageArray1 = getAverage(1, maskArray)
	averageArray2 = getAverage(2, maskArray)

	plt.figure("Running Time vs Mask Size")
	plt.subplot(222),plt.xlabel("Time(s)"),plt.ylabel("Mask Size"),plt.plot(maskArray,averageArray1, '-o')
	plt.subplot(223),plt.xlabel("Time(s)"),plt.ylabel("Mask Size"),plt.plot(maskArray,averageArray2, '-o')

	plt.show()

plotGraph()