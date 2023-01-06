from cryptography.fernet import Fernet #library used for keys, aka encrypting and decrypting using a generated 32 byte key
with open('FernetKey.txt', 'rb') as f: 
    key = (f.read()) #since the key is stored as in bites, you must read it as bites, hence rb on txt file
encryption_key = Fernet(key) #the key is now stored as a variable that we can call at anytime

                           
def choosepass(chooseacc): #function that lets the user input the password to their account
    guesses = 0 #counter
    while True:
        if guesses == 3: #only 3 total guesses
            print('you ran out of guesses')
            encrypting() #encrypts so the program can decrypt the file on the next run. Also the contents of the of the notepad (text file) is now encrypted to people who open it cannot see other peoples information such as passwords, username, or messages
            exit()  #locks you out, aka exits
        elif input("Enter your password \n : ") == accpassdict[chooseacc]: #checks to see the value of the dictionarry key with the username and compare it to the input, mimicking a login security
            print(f'Welcome {chooseacc} your message is: \n', accmesgdict[chooseacc]) #welcoming message
            chooseoption(chooseacc) #redirects
            return None #exits function immidietly, so it doesn't proceed with other lines of code after the iteration of the function
        else:
            print('wrong password') 
            guesses += 1 #guess counter increases by 1
def chooseoption(chooseacc):
    while True:
            choosecommand = input('Modify your contents : \n type 1 to change pass \n type 2 to change message \n type 3 to exit program \n : ')
            if choosecommand == str(1): #use strings because then we'd have to use int(input()) which would give an error if the user puts in something other than a base 10 number (like for example a letter)   
                changepass(chooseacc)  #redicrects
                break
            elif choosecommand == str(2):
                changemessage(chooseacc) #redirects
                break
            elif choosecommand == str(3): 
                encrypting() #encrypts so the program can decrypt the file on the next run. Also the contents of the of the notepad (text file) is now encrypted to people who open it cannot see other peoples information such as passwords, username, or messages
                exit() #exits 
            else:
                print('not an option') #restart loop
                continue

def changepass(chooseacc): #function that changes the loged-in user's  password
    passchange1 = input(f'your current password is {accpassdict[chooseacc]} \n what would u like to change your password to? \n : ') #asks for input
    if '-' in passchange1: #forbidden character because would create parsing error
        print('you used a - in your password, choose another password')
        changepass(chooseacc) #recursion: calls the same function inside its own function, allows the user to input new passwords if previous ones were not accepted
        return None   #leaves the function immmedietly after completing a second iteration or else it will continute with the next lines afer the iteration
    elif r"\n" in passchange1: #not allowed because would create parsing error in the for loop that reads the lines based of breakpoints(this is one of the break points)
        print('no backslashes permitted, choose another password')
        changepass(chooseacc)
    else:
        pass #because there we no forbidden characters, we pass on to the next line of code

    if passchange1 == input('please confirm your password'): #compares to see if the confirmation is the same as the first input pass
        accpassdict[chooseacc] = passchange1   #changes the password linked with the account name to the new set password in the dictionnary
        print(f'password has been set to {passchange1}') #tells the user that password is set
        chooseoption(chooseacc)  #recalls back to the funciton that allows the user to choose to either exit, change pass or change message
    else:
        print('your confirmation did not line up with your original, pleasae try again') #if the users confirmation password is not the same as the first password input, the function recalls(recursion) then they must redo the account creation
        changepass(chooseacc)

def changemessage(chooseacc): #function that changes the loged-in user's message
    changemessage1 = input(f'your current message is {accmesgdict[chooseacc]}, this new message will override your new one \n enter here \n :')
    if r"\n" in changemessage1: # checks to see if \n is inside the message, its not allowed because one of my functions splits based on new lines, and having these characters would ruin the loop
        print('your message contained a', r"\n", 'please enter a new message') # \ is treated as an escape character, so \n would create a new line in the print statement, but r"\n" treats it as a raw string instead
        changemessage(chooseacc) #recursion, returns to the top of the function
        return None
    else:
        accmesgdict[chooseacc] = changemessage1 #changes the value of the of dictionnary that contains the name as the key and message as the value
        print(f'your message has been set to {accmesgdict[chooseacc]}')
        chooseoption(chooseacc) #redirects

def createaccount(): #function that creates an account
    accname = input('create username \n : ') #input
    if accname in accmesgdict.keys(): #check to see if the the username is taken, kind of like using a .find() function
        print('already taken') #who would win in a 1v1 panna meg competition, me or u at 15?
        createaccount() #recursion, calls back to its own function
        return None #exits the function right after
    elif ',' in accname: #cannot contain a comma because my program reads the username until a .split(',') so a comma would ruin the username 
        print('you cannot use a , inside your username. Try another username')
        createaccount() #redirect
        return None #exits function
    else:
        pass #passes
    accpass = input('choose a password \n :  ')
    if '-' in accpass: #used because the program reads the contents of the lines in the file using break points, so a - would interefer with the readings
        print('you used a - in your password, choose another password')
        createaccount() #recursion: calls the same function inside its own function, allows the user to input new passwords if previous ones were not accepted
        return None   
    else:
        pass

    if accpass == input('please confirm your password \n : '): #checks to see if the confirmation password is the same as the first password given
        accpassdict.update({accname:accpass}) #adds to the dictionnary the username as the key and the password as the value
    else:
        print('your confirmation did not line up with your original, pleasae try again')
        createaccount() #redirects to another function
        return None #exits the function, or else it will start the function, then proceed the final 3 lines twice in a row
    accmesgdict.update({accname:input('what message do you want to store \n : ')}) #adds to the dictionnary the username as they key and message as the value
    chooseacc = accname #allows the next function to be called since it requires 1 positional argument: chooseacc
    chooseoption(chooseacc) 
    
    
def encrypting(): #function that encrypts the file and rewrites all the new content from dictionnary
    with open('EncryptedData.txt', 'w') as f: #open the file as write module
        for info in accpassdict.keys(): #loops for every account in the file, as in the amount of times is the amount of total accounts
            f.write(f'{info},{accpassdict[info]}-{accmesgdict[info]}\n') #writes/formats the strings from the dictionaries  as (username,password-message *new line*)so the next time the program runs, the for loops at the beggining can read the content
    
    with open('EncryptedData.txt', 'r') as f:
        messages = (f.read()) #stores the entire file as a variable
        encoded = messages.encode()  #converts the contents of file into bytes because the encryption function can only be used on byte values
        encrypted = encryption_key.encrypt(encoded) #using the key from the very beggining, we encrypt the content so viewers who find the file will see some random a random 32 byte string created by the key
    
    with open('EncryptedData.txt', 'wb') as f: #mode: write in 
        f.write(encrypted) #the encrypted message is stored in bytes so that the program can decrypt the message for the next run

        

accpassdict = {} #set dictionaries which will be used to store information in later code - this one stores username:password
accmesgdict = {}  #                                                                      - this one stores username:message
with open('EncryptedData.txt', 'rb') as f: #opens the file in read bytes because the decrypt function must read bytes and the program wrote the encrypted message in bytes the previous time it ran
    encrypted_message = encryption_key.decrypt(f.read()) #uses the key generated at beggining to decrypt the file, but now stores the regular messages in bytes instead of strings
    original_messsage = encrypted_message.decode() #turns the byte into strings so the next for loop can read the contents
    for acc1 in original_messsage.split('\n'):  #tokenizes each line of the file as a string because a new line is stored as \n in python
        user = acc1[:acc1.find(',')] #beggining till the , is the username
        pass1 = acc1[acc1.find(',')+1:acc1.find('-')]  #from after the , till - is pass
        secret1 = acc1[acc1.find('-')+1:]  # everything after the - is the message
        accpassdict.update({user:pass1}) #stores string of users as a key and pass1 as the value in a dictionnary
        accmesgdict.update({user:secret1}) #stores string of user as a key and secret message as the value in a dictionnary



    print("Welcome to the world's safest online password storage \n over the course of history, Litvin Security had a total of 0 succesful data breaches against its immaculate security system")
    while True: #a while loop that keeps repeating until broken
        welcoming = input(' type A to create an account \n type B to login to an existing account \n : ') #takes the input of the user
        if welcoming == 'A': #depending on the input, redirects to another function that allows user to create an account
            createaccount()
            break
        elif welcoming == 'B':  
            break #exits the while loop depending on the user input, will now go to the next while loop
        else:
            print('that is not an option') #if none of the options were choosen, the while loop will start again
        
        
    accguess = 0 #sets a counter so the user only has 3 tries
    while True:  
        chooseacc = input('Login username \n :  ') #takes user input
        if chooseacc in accmesgdict.keys(): #kind of like using a .find() function except on a list
            choosepass(chooseacc) #if the user chooses an available account, the program is redirected to a function that checks the password
            break
        elif accguess == 2:                   # only 3 guesses total 
            print('u sure ur actually a family member?, prove your worthiness by answering the security question') #time to test the user if hes truly a real family member
            if input('how old was grandma when she passed away? \n : ') == str(88): #takes user input and if the asnwer is correct, it will give user 3 more tries
                accguess = 0 #reset counter
                continue  #go back to the beggining of the loop
            else:
                encrypting() #must encrypt the data or else the program will not be able to decrypt when it runs next time
                exit() #exists the program
        else:                 
            print("That is not an account") #goes back to the loop right after telling user they did not input an exisiting account
            accguess += 1 #the counter number gets 1 added to what it was before

      
