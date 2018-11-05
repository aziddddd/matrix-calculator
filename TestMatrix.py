from MatrixOperator import MyMatrix
from MatrixOperator import MatrixError

def matval(matrix):
	print('==================Matrix {}=================='.format(matrix))
	row = int(input('Number of Row : '))
	col = int(input('Number of Column : '))
	matmaker = MyMatrix(row, col, False)
	mat = []
	for i in range(row):
		colist = []
		print('\n--------------------')
		print('Element of row : {}'.format(i+1))
		for j in range(col):
			ele = float(input())
			colist.append(ele)
		mat.append(colist)
	matmaker.rows = mat

	return matmaker

def main():
	print('\nMatrix Operation : [addition] [subtraction] [multiplication] [inverse]\n')
	type = (input( "Enter matrix operation type: "))

	if (type == 'addition'):
			mat1, mat2 = matval(1), matval(2)
			result = mat1 + mat2

	elif (type == 'subtraction'):
			mat1, mat2 = matval(1), matval(2)
			result = mat1 - mat2

	elif (type == 'multiplication'):
			mat1, mat2 = matval(1), matval(2)
			result = mat1 * mat2

	elif  (type == 'inverse'):
			mat = matval(1)
			result = mat.getInverse()

	else:
			print('No known matrix operation specified : ', type)
			quit()

	print('\n~~~~~~~~~~~~~~~~{}~~~~~~~~~~~~~~~~'.format(type))
	print(result)

main()