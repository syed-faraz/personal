def multiply():
	num = input("\nEnter the number to generate multiplication table \n")
	print("\n")
	for i in range(1,11):
		print (num*i)
	option = raw_input("\nMultiply Again? yes/no \n")
 	if option == "yes":
		return multiply()
	else:
		print("\nBye! \n")
multiply()
