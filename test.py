def multiply():
	num = input("\nEnter the number \n")
	print("\n")
	for i in range(1,11):
		print (num*i)
	option = raw_input("\nAgain? \n")
 	if option == "yes":
		return multiply()
	else:
		print("\nBye! \n")
multiply()
