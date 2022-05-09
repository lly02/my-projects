import random, sys

def printInput(input):
	if input == 'r':
		return print('ROCK versus...')

	if input == 'p':
		return print('PAPER versus...')

	if input == 's':
		return print('SCISSORS versus...')

	if input == 'q':
		sys.exit()

	print('Please try again')
	return False

def generateInput():
	randomNumber = random.randrange(1,4)

	if randomNumber == 1:
		print('ROCK')
		return 'r'

	if randomNumber == 2:
		print('PAPER')
		return 'p'

	if randomNumber == 3:
		print('SCISSORS')
		return 's'
	

def checkScore(win, score):
	if win == True:
		score[0] += 1
		return score

	if win == False:
		score[1] += 1
		return score

	if win is None:
		score[2] += 1
		return score
				

def checkWin(input, input2):
	if input is None:
		return

	if input == input2:
		return None

	if input == 'r':
		if input2 == 'p':
			return False
		if input2 == 's':
			return True

	if input == 'p':
		if input2 == 's':
			return False
		if input2 == 'r':
			return True
	
	if input == 's':
		if input2 == 'r':
			return False
		if input2 == 'p':
			return True

def printWin(input):
	if input == True:
		return print('You win!')

	if input == False:
		return print('You lose!')

	return print('It is a tie!')
	
def printScore(input):
	print(f'{input[0]} Wins, {input[1]} Losses, {input[2]} Ties')
	
#declare variables
#score = [win, lose, tie]
score = [0,0,0]

print('ROCK, PAPER, SCISSORS')
print('0 Wins, 0 Losses, 0 Ties')

while True:
	print('Enter your move: (r)ock, (p)aper, (s)cissors or (q)uit')

	#Ask for input first
	while True:
		userInput = input()

		inputCheck = printInput(userInput)
		
		if inputCheck != False:
			break


	userInput2 = generateInput()

	win = checkWin(userInput, userInput2)

	printWin(win)

	score = checkScore(win, score)

	printScore(score)