import sqlite3
from getpass import getpass
import time
import random
import datetime
import re

connection = None
cursor = None
uid = None

def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return

def login():
    global connection, cursor, uid
    
    loggedIn = False
    notValid = True
    while loggedIn == False or notValid:
        username = input("Username: ")
        password = getpass("Password: ")    #hides password at time of typing
        userInfo = (username.lower(), password)
        uid = (username.lower(),)
        #injection attacks
        if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
            cursor.execute('SELECT utype FROM users WHERE lower(uid) = ? and pwd = ?;', userInfo)
            utype = cursor.fetchone()
            connection.commit()
            notValid = False
            #user not in db
            if utype == None:
                print('Invalid user. Enter username and password again.')
            else:
                utype = utype[0]
                if utype == 'a':
                    agent_menu()
                    loggedIn = True
                elif utype == 'o':
                    officer_menu()
                    loggedIn = True
                else:
                    non_user()
                    loggedIn = True
        else:
            print("Username or password contains illegal characters")
    return

def non_user():
    global connection, cursor
    #options menu shown for a user who is neither a person nor officer

    print("\n1. Logout\n2. Quit\n")
    notValid = True
    while notValid:
        option = input("Enter the number for the option you want: ")
        try:
            option = int(option)
            if option not in range(1,3):
                print("Invalid option")
            else:
                notValid = False
        except:
            print("Invalid option")

    if int(option) == 1:
        logout()
    elif int(option) == 2:
        print("Exited program")
        quit()
    return

def agent_menu():
    #options menu for agents
    print("\n1. Register a birth\n2. Register a marriage\n3. Renew a vehicle registration\n4. Process a bill of sale\n5. Process a payment\n6. Get a driver abstract\n7. Logout\n8. Quit\n")
    #check if option is integer and within range of options
    notValid = True
    while notValid:
        option = input("Enter the number for the option you want: ")
        try:
            option = int(option)
            if option not in range(1, 9):
                print("Invalid option")
            else:
                notValid = False
        except:
            print("Invalid option")
    if int(option) == 1:
        register_birth()
    elif int(option) == 2:
        register_marriage()
    elif int(option) == 3:
        renew_vehicle()
    elif int(option) == 4:
        process_bill()
    elif int(option) == 5:
        process_payment()
    elif int(option) == 6:
        driver_abstract()        
    elif int(option) == 7:
        logout()
    elif int(option) == 8:
        print("Exited program")
        quit()
    return

def officer_menu():
    #options menu for officers
    print("\n1. Issue a ticket\n2. Find a car owner\n3. Logout\n4. Quit\n")
    notValid = True
    while notValid:
        option = input("Enter the number for the option you want: ")
        try:
            option = int(option)
            if option not in range(1, 5):
                print("Invalid option")
            else:
                notValid = False
        except:
            print("Invalid option")

    if int(option) == 1:
        issue_ticket()
    elif int(option) == 2:
        find_car_owner()
        pass
    elif int(option) == 3:
        logout()
    elif int(option) == 4:
        print("Exited program")
        quit()
    return

def register_birth():
    global connection, cursor, uid
    #The agent should be able to register a birth by information about child and parents 
    #The reg date is set totoday's date and the reg place is set to the city of the user. Regno is unique and automatically assigned
    #The address and the phone of the newborn are set to those of the mother
    #If any of the parents is not in the database get info of parents and add them to db (fname and lname required information rest optional)

    print("\nEnter the necessary information to register a birth")
    print("Enter the information about the newborn")
    print("Enter 'QUIT' at anytime to go back to menu")
    child_fname = input("Enter first name: ")
    while child_fname == "":
        print("Information required")
        child_fname = input("Enter first name: ")
    if(child_fname == 'QUIT'):
        agent_menu()
    child_lname = input("Enter last name: ")
    while child_lname == "":
        print("Information required")
        child_lname = input("Enter last name: ")
    if(child_lname == 'QUIT'):
        agent_menu()
    tempchild = (child_fname.upper(), child_lname.upper())
    cursor.execute("SELECT * FROM persons WHERE upper(fname) = ? AND upper(lname) = ?", tempchild)
    tempchildinfo = cursor.fetchone()
    if tempchildinfo == None:
        child_gender = input("Gender (M = Male, F = Female and O = Other): ")
        while child_gender.upper() != 'M' and child_gender.upper() != 'F' and child_gender.upper() != 'O' and child_gender.upper() != 'QUIT':
            print('Invalid input try again')
            child_gender = input("Gender (M = Male, F = Female and O = Other): ")
        if(child_gender == 'QUIT'):
            agent_menu()
        valid = False
        while not valid:
            child_bDate = input("Birth date (yyyy-mm-dd): ")
            if(child_bDate == 'QUIT'):
                valid = True
                agent_menu()
            else:
                try: 
                    child_bDate = datetime.datetime.strptime(child_bDate, "%Y-%m-%d").strftime("%Y-%m-%d")
                    current_date = time.strftime("%Y-%m-%d")
                    if child_bDate > current_date:
                        print("This date is not valid because it is set in the future.")
                    else:
                        valid = True
                except:
                    print("Invalid entry please try again")
        child_bPlace = input("Enter birth place: ")
        while child_bPlace == "":
            print("Information required")
            child_bPlace = input("Enter birth place: ")
        if(child_bPlace == 'QUIT'):
            agent_menu()
        f_fname = input("Enter father's first name: ")
        while f_fname == "":
            print("Information required")
            f_fname = input("Enter father's first name: ")
        if(f_fname == 'QUIT'):
            agent_menu()
        f_lname = input("Enter father's last name: ")
        while f_lname == "":
            print("Information required")
            f_lname = input("Enter father's last name: ")
        if(f_lname == 'QUIT'):
            agent_menu()
        m_fname = input("Enter mother's first name: ")
        while m_fname == "":
            print("Information required")
            m_fname = input("Enter mother's first name: ")
        if(m_fname == 'QUIT'):
            agent_menu()
        m_lname = input("Enter mother's last name: ")
        while m_lname == "":
            print("Information required")
            m_lname = input("Enter mother's last name: ")
        if(m_lname == 'QUIT'):
            agent_menu()
        reg_date = time.strftime("%Y-%m-%d")

        cursor.execute('SELECT u.city FROM users u WHERE lower(uid) = ?;', uid)
        city = cursor.fetchone()
        reg_place = city[0] #needs to be place of user

        #will keep generating a registration number until it is unique
        cursor.execute("SELECT regno FROM births")
        regnos = cursor.fetchall()
        existingNos = []
        for reg in regnos:
            existingNos.append(reg[0])
        regno = random.randint(0, 10000)
        while regno in existingNos:
            regno = random.randint(0, 10000)

        #changing to upper because case insensitive
        fatherInfo = (f_fname.upper(), f_lname.upper())
        motherInfo = (m_fname.upper(), m_lname.upper())

        #will get info if father or mother not in db and insert them into db
        cursor.execute("SELECT * FROM persons WHERE upper(fname) = ? AND upper(lname) = ?", fatherInfo)
        father = cursor.fetchone()
        if father == None:
            print("\n" + " ".join(fatherInfo).title() + " is not registered in the database please enter additional information\n")
            print("Enter 'QUIT' at anytime to go back to menu")
            valid = False
            while not valid:
                f_bDate = input("Birth date (yyyy-mm-dd) (optional): ")
                if(f_bDate == 'QUIT'):
                    valid = True
                    agent_menu()
                else:
                    if f_bDate == "":
                        f_bDate = None
                        valid = True
                    else:
                        try: 
                            f_bDate = datetime.datetime.strptime(f_bDate, "%Y-%m-%d").strftime("%Y-%m-%d")
                            current_date = time.strftime("%Y-%m-%d")
                            if f_bDate > current_date:
                                print("This date is not valid because it is set in the future.")
                            else:
                                valid = True
                        except:
                            print("Invalid entry please try again")
            f_bPlace = input("Enter birth place (optional): ")
            if(f_bPlace == 'QUIT'):
                agent_menu()
            else:
                if f_bPlace == "":
                    f_bPlace = None
            f_address = input ("Enter address (optional): ")
            if(f_address == 'QUIT'):
                agent_menu()
            else:
                if f_address == "":
                    f_address = None
            f_phone = input("Enter phone number (optional): ")
            if(f_phone == 'QUIT'):
                agent_menu()
            else:
                if f_phone == "":
                    f_phone = None
            father = (f_fname, f_lname, f_bDate, f_bPlace, f_address, f_phone)
            cursor.execute("INSERT INTO persons VALUES (?, ?, ?, ?, ?, ?)", father)
            print("\n" + " ".join(fatherInfo).title() + " has successfully been entered in the registry")
            connection.commit()
        
        cursor.execute("SELECT * FROM persons WHERE upper(fname) = ? AND upper(lname) = ?", motherInfo)
        mother = cursor.fetchone()
        if mother == None:
            print("\n" + " ".join(motherInfo).title() + " is not registered in the database please enter additional information")
            print("Enter 'QUIT' at anytime to go back to menu")
            valid = False
            while not valid:
                m_bDate = input("Birth date (yyyy-mm-dd) (optional): ")
                if(m_bDate == 'QUIT'):
                    valid = True
                    agent_menu()
                else:
                    if m_bDate == "":
                        m_bDate = None
                        valid = True
                    else:
                        try: 
                            m_bDate = datetime.datetime.strptime(m_bDate, "%Y-%m-%d").strftime("%Y-%m-%d")
                            current_date = time.strftime("%Y-%m-%d")
                            if m_bDate > current_date:
                                print("This date is not valid because it is set in the future.")
                            else:
                                valid = True
                        except:
                            print("Invalid entry please try again")
            m_bPlace = input("Enter birth place (optional): ")
            if(m_bPlace == 'QUIT'):
                agent_menu()
            else:
                if m_bPlace == "":
                    m_bPlace = None
            m_address = input ("Enter address (optional): ")
            if(m_address == 'QUIT'):
                agent_menu()
            else:
                if m_address == "":
                    m_address = None
            m_phone = input("Enter phone number (optional): ")
            if(m_phone == 'QUIT'):
                agent_menu()
            else:
                if m_phone == "":
                    m_phone = None
            mother = (m_fname, m_lname, m_bDate, m_bPlace, m_address, m_phone)
            cursor.execute("INSERT INTO persons VALUES (?, ?, ?, ?, ?, ?)", mother)
            print("\n" + " ".join(motherInfo).title() + " has successfully been entered in the registry")
            connection.commit()

        #necessary info needed form mother for child
        m_address = mother[4]
        m_phone = mother[5]

        #adding child to person and birth tables
        childInfo = (child_fname, child_lname, child_bDate, child_bPlace, m_address, m_phone)
        birthInfo = (regno, child_fname, child_lname, reg_date, reg_place, child_gender, f_fname, f_lname, m_fname, m_lname)
        cursor.execute("INSERT INTO persons VALUES (?, ?, ?, ?, ?, ?)", childInfo)
        cursor.execute("INSERT INTO births VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", birthInfo)

        childInfo2 = (child_fname, child_lname)
        print("\n" + " ".join(childInfo2).title() + " has successfully been entered in the registry\n")
        connection.commit()
    else:
        print("\n" + " ".join(tempchild).title() + " birth cannot be registered. Person already in database\n")
    connection.commit()
    option_menu('a')
    return

def register_marriage():
    global connection, cursor, uid
    #The agent should be able to provide the names both partners
    #The system should assign the reg date and place and a unique registration number as discussed in registering a birth partners and add them to db (fname and lname required information rest optional)

    print("\nEnter the necessary information to register a marriage")
    print("Enter 'QUIT' at anytime to go back to menu")
    print("\nEnter information about partner 1")
    p1_fname = input("Enter partner 1 first name: ")
    while p1_fname == "":
        print("Information required")
        p1_fname = input("Enter partner 1 first name: ")
    if(p1_fname == 'QUIT'):
        agent_menu()
    p1_lname = input("Enter partner 1 last name: ")
    while p1_lname == "":
        print("Information required")
        p1_lname = input("Enter partner 1 last name: ")
    if(p1_lname == 'QUIT'):
        agent_menu()
    print("\nEnter information about partner 2")
    p2_fname = input("Enter partner 2 first name: ")
    while p2_fname == "":
        print("Information required")
        p2_fname = input("Enter partner 2 first name: ")
    if(p2_fname == 'QUIT'):
        agent_menu()
    p2_lname = input("Enter partner 2 last name: ")
    while p2_lname == "":
        print("Information required")
        p2_lname = input("Enter partner 2 last name: ")
    if(p2_lname == 'QUIT'):
        agent_menu()

    reg_date = time.strftime("%Y-%m-%d")
    cursor.execute('SELECT u.city FROM users u WHERE lower(uid) = ?;', uid)
    city = cursor.fetchone()
    reg_place = city[0] #needs to be place of user

    #will keep generating a registration number until it is unique
    cursor.execute("SELECT regno FROM marriages")
    regnos = cursor.fetchall()
    regno = random.randint(0, 10000)
    existingNos = []
    for reg in regnos:
        existingNos.append(reg[0])
    while regno in existingNos:
        regno = random.randint(0, 10000)

    p1_info = (p1_fname.upper(), p1_lname.upper())
    p2_info = (p2_fname.upper(), p2_lname.upper())

    #will get info if any partner not in db and insert them into db
    cursor.execute("SELECT * FROM persons WHERE upper(fname) = ? AND upper(lname) = ?", p1_info)
    p1 = cursor.fetchone()
    if p1 == None:
        print(" ".join(p1_info).title() + " is not registered in the database please enter additional information")
        print("Enter 'QUIT' at anytime to go back to menu")
        valid = False
        while not valid:
            p1_bDate = input("Birth date (yyyy-mm-dd) (optional): ")
            if(p1_bDate == 'QUIT'):
                valid = True
                agent_menu()
            else:
                if p1_bDate == "":
                    p1_bDate = None
                    valid = True
                else:
                    try: 
                        p1_bDate = datetime.datetime.strptime(p1_bDate, "%Y-%m-%d").strftime("%Y-%m-%d")
                        current_date = time.strftime("%Y-%m-%d")
                        if p1_bDate > current_date:
                            print("This date is not valid because it is set in the future.")
                        else:
                            valid = True
                    except:
                        print("Invalid entry please try again")
        p1_bPlace = input("Enter birth place (optional): ")
        if(p1_bPlace == 'QUIT'):
            agent_menu()
        else:
            if p1_bPlace == "":
                p1_bPlace = None
        p1_address = input ("Enter address (optional): ")
        if(p1_address == 'QUIT'):
            agent_menu()
        else:
            if p1_address == "":
                p1_address = None
        p1_phone = input("Enter phone number (optional): ")
        if(p1_phone == 'QUIT'):
            agent_menu()
        else:
            if p1_phone == "":
                p1_phone = None
        p1 = (p1_fname, p1_lname, p1_bDate, p1_bPlace, p1_address, p1_phone)
        cursor.execute("INSERT INTO persons VALUES (?, ?, ?, ?, ?, ?)", p1)
        print(" ".join(p1_info).title() + " has successfully been entered in the registry")
        connection.commit()
    
    cursor.execute("SELECT * FROM persons WHERE upper(fname) = ? AND upper(lname) = ?", p2_info)
    p2 = cursor.fetchone()
    if p2 == None:
        print("\n" + " ".join(p2_info).title() + " is not registered in the database please enter additional information")
        print("Enter 'QUIT' at anytime to go back to menu")
        valid = False
        while not valid:
            p2_bDate = input("Birth date (yyyy-mm-dd) (optional): ")
            if(p2_bDate == 'QUIT'):
                valid = True
                agent_menu()
            else:
                if p2_bDate == "":
                    p2_bDate = None
                    valid = True
                else:
                    try: 
                        p2_bDate = datetime.datetime.strptime(p2_bDate, "%Y-%m-%d").strftime("%Y-%m-%d")
                        current_date = time.strftime("%Y-%m-%d")
                        if p2_bDate > current_date:
                            print("This date is not valid because it is set in the future.")
                        else:
                            valid = True
                    except:
                        print("Invalid entry please try again")
        p2_bPlace = input("Enter birth place (optional): ")
        if(p2_bPlace == 'QUIT'):
            agent_menu()
        else:
            if p2_bPlace == "":
                p2_bPlace = None
        p2_address = input ("Enter address (optional): ")
        if(p2_address == 'QUIT'):
            agent_menu()
        else:
            if p2_address == "":
                p2_address = None
        p2_phone = input("Enter phone number (optional): ")
        if(p2_phone == 'QUIT'):
            agent_menu()
        else:
            if p2_phone == "":
                p2_phone = None
        p2 = (p2_fname, p2_lname, p2_bDate, p2_bPlace, p2_address, p2_phone)
        cursor.execute("INSERT INTO persons VALUES (?, ?, ?, ?, ?, ?)", p2)
        print("\n" + " ".join(p2_info).title() + " has successfully been entered in the registry")
        connection.commit()

    marriageInfo = (regno, reg_date, reg_place, p1_fname, p1_lname, p2_fname, p2_lname)
    cursor.execute("INSERT INTO marriages VALUES (?, ?, ?, ?, ?, ?, ?)", marriageInfo)
    print("\n" + " ".join(p1_info).title() + " and " + " ".join(p2_info).title() + " marriage has successfully been entered in the registry\n")
    connection.commit()

    option_menu('a')
    return

def renew_vehicle():
    global connection, cursor
    # User should be able to provide an existing registration number and renew the registration

    # select all regno from database
    print("\nEnter the necessary information to renew a vehicle registration")
    cursor.execute('''SELECT regno FROM registrations ; ''')
    connection.commit()
    allRegno = cursor.fetchall()
     
    isValid = False
    # check user input is only a integer and in database
    print("Enter 'QUIT' at anytime to go back to menu")
    while isValid == False:
        regnum = input("Please enter an existing registration number: ")
        while regnum == "":
            print("Information required")
            regnum = input("Please enter an existing registration number: ")
        if(regnum == 'QUIT'):
            agent_menu()
        else:
            try:
                regnum = int(regnum)
                regno = (regnum,)
                if(regno in allRegno):
                    isValid = True
                else:
                    print("Registration number not in database")
            except:
                print("Invalid input")

    # Select the regdate and expiry for that regno
    cursor.execute('''SELECT r.expiry FROM registrations r 
                    WHERE r.regno = ?; ''', regno)
    connection.commit()

    # save all of the info we need
    days = cursor.fetchall()
    expiry = days[0][0]
    current_date = time.strftime("%Y-%m-%d")

    # check if expiry has already expired or expires today 
    if expiry<=current_date:
        # change the date to one year ahead and save it
        cursor.execute('''SELECT DATE('now', '+1 years');''')
        newExpiry = cursor.fetchall()
        newExpiry = newExpiry[0][0]
        
        # save the data we need to update then update expiry to new expiry to that regno
        data = (newExpiry, regnum)
        cursor.execute('UPDATE registrations SET expiry = ? WHERE regno = ?;', data)
        connection.commit()

    # add one year after expiry
    else:
        # add one to the year
        y1,m1,d1 = expiry.split('-')
        y1 = int(y1) + 1
        y1 = str(y1)
        newExpiry = (y1+'-'+m1+'-'+d1)

        print(newExpiry)
        # save the data into a tuple
        data = (newExpiry, regnum)

        # update the new expiry date to one year later
        cursor.execute('UPDATE registrations SET expiry = ? WHERE regno = ?;', data)
        connection.commit()
        
    print("\nVehicle registration is renewed new expiry date is: " + newExpiry + "\n")
    connection.commit()
    option_menu('a')
    return

def process_bill():
    global connection, cursor

    print("\nEnter the necessary information to process a bill of sale")
    # get all vin #s
    cursor.execute('''SELECT lower(vin) FROM vehicles ; ''')
    connection.commit()
    allVin = cursor.fetchall()

    # all the checking
    transferIsValid = False
    print("Enter 'QUIT' at anytime to go back to menu")
    while transferIsValid == False:
        # save vin input
        vinA = str(input("Please enter the vin number of the car: "))
        while vinA == "":
            print("Information required")
            vinA = str(input("Please enter the vin number of the car: "))
        if(vinA == 'QUIT'):
            agent_menu()
        vinB = vinA.lower()
        vin = (vinB,)

        # check if vin is in the vehicles database
        if(vin in allVin):
            # check fname and lname are for the most recent vin
            data = (vinB,vinB)
            cursor.execute('''SELECT lower(r.vin), lower(r.fname), lower(r.lname) 
                                FROM registrations r, vehicles v
                                WHERE lower(r.vin) = ? AND lower(r.vin) = lower(v.vin) AND regdate = (SELECT MAX(regdate)
                                                FROM registrations
                                                WHERE lower(vin) = ?);''', data)
            
            vinNames = cursor.fetchall()
            #checkVin = vinNames[0][0].lower()
            checkFname = vinNames[0][1].lower()
            checkLname = vinNames[0][2].lower()

            # get all people from persons and make it lower case
            cursor.execute('''SELECT lower(fname), lower(lname)
                                FROM persons;''')
            allPeople = cursor.fetchall()

            # get the name of the current owner for the vehicle
            curOwnerFname = input("Please enter the firstname of current owner: ")
            if(curOwnerFname == 'QUIT'):
                agent_menu()
            curOwnerFname = curOwnerFname.lower()
            curOwnerLname = input("Please enter the lastname of current owner: ")
            if(curOwnerLname == 'QUIT'):
                agent_menu()
            curOwnerLname = curOwnerLname.lower()

            # get owners new name and new plate #
            newFname = input("Please enter the new owners first name: ")
            newFname = newFname.lower()
            if(newFname == 'QUIT'):
                agent_menu()
            newLname = input("Please enter the new owners last name: ")
            newLname = newLname.lower()
            if(newLname == 'QUIT'):
                agent_menu()
            newPlate = input("Please enter the new plate number: ")
            if(newPlate == 'QUIT'):
                agent_menu()
            newPersonName = (newFname, newLname)

            # Check if names is equal to the names entered for that vin and if the new owner is in the persons table
            if(curOwnerFname == checkFname and curOwnerLname == checkLname and newPersonName in allPeople):
                transferIsValid = True
            else:
                print("Transfer cannot be made")
        else:
            print("Vin doesn't exist")

    # needed values for dates
    current_date = time.strftime("%Y-%m-%d")
    cursor.execute('''SELECT DATE('now', '+1 years');''')
    newExpiry = cursor.fetchall()
    newExpiry = newExpiry[0][0]

    # get random regno
    newRegno = random_regno()

    # change expiry date to todays date for the previous owner of the vehicle
    data = (current_date, vinB, curOwnerFname, curOwnerLname)
    cursor.execute('UPDATE registrations SET expiry = ? where lower(vin) = ? AND lower(fname) = ? AND lower(lname) = ?;', data)
    connection.commit()

    # new registration under new owners name
    data = (newRegno,current_date,newExpiry,newPlate,vinA,newFname,newLname)
    cursor.execute('INSERT INTO registrations VALUES (?,?,?,?,?,?,?);', data)
    print("\nTransfer was successful\n")
    connection.commit()
    option_menu('a')
    return

def process_payment():
    global connection, cursor

    print("\nEnter the necessary information to process a payment")
    print("Enter 'QUIT' at anytime to go back to menu")
    notExist = True
    notValid = True
    while notValid and notExist:
        tickno = input("Enter a valid ticket number: ")
        if(tickno == 'QUIT'):
            agent_menu()
            notValid = False
        else:
            try:
                tickno = int(tickno)
                if tickno < 0:
                    notValid = False
            except:
                print("Invalid input")
            else:
                info = (tickno, )
                cursor.execute('SELECT tno FROM tickets WHERE tno = ? ;', info)
                valid = cursor.fetchone()  
                if valid == None:
                    print('Ticket number not in database')
                else:
                    notExist = False

    cursor.execute('SELECT tno from payments WHERE tno = ? ;',info)
    check = cursor.fetchone()
    cursor.execute('SELECT t.fine FROM tickets t WHERE tno = ?;', info)
    fine = cursor.fetchone()
    fine = int(fine[0])
    currentdate = time.strftime("%Y-%m-%d")
    if check == None:   
        notValid = True
        while notValid:
            amount = input("Enter amount of payment: ")
            if(amount == 'QUIT'):
                agent_menu()
                notValid = False
            else:
                try:
                    amount = int(amount)
                    if amount > fine:
                        print("Payment is greater than fine")
                    else:
                        notValid = False
                except:
                    print("Invalid input")
        if amount == fine:
            print("Fine of" + str(amount) + " has been fully paid")
        else:
            paymentLeft = fine - amount
            print("\nYou have made an additional payment of " + str(amount) + " towards fine " + str(fine) + ". You have " + str(paymentLeft) + " remaining.\n" )

        #need to make sure the sum is less than total fine due
        payInfo = (tickno,currentdate,amount)
        cursor.execute('INSERT INTO payments VALUES (?,?,?);', payInfo)
    else:
        cursor.execute('SELECT p.pdate FROM payments p WHERE tno = ?;', info)
        paymentDates = cursor.fetchall()
        for date in paymentDates:
            date = datetime.datetime.strptime(date[0], "%Y-%m-%d").strftime("%Y-%m-%d")
            if date == currentdate:
                print("\nCan't make more than one payment on same date\n")
                option_menu('a')
        cursor.execute('SELECT sum(p.amount) FROM payments p WHERE tno = ?;', info)
        sumPayment = cursor.fetchone()
        sumPayment = int(sumPayment[0])
        if sumPayment == fine:
            print('\nTicket has been fully paid\n')
            option_menu('a')
        else:
            notValid = True
            while notValid:
                amount = input("Enter amount of payment: ")
                if(amount == 'QUIT'):
                    agent_menu()
                    notValid = False
                else:
                    try:
                        amount = int(amount)
                        if amount + sumPayment> fine:
                            print("Payment is greater than fine")
                        else:
                            notValid = False
                    except:
                        print("Invalid input")
            if amount + sumPayment == fine:
                print("Fine of " + str(amount) + " has been fully paid")
            else:
                paymentLeft = fine - amount - sumPayment
                print("\nYou have made an additional payment of $" + str(amount) + " a towards fine of $" + str(fine) + ". You have $" + str(paymentLeft) + " remaining.\n" )
            payInfo = (tickno,currentdate,amount)
            cursor.execute('INSERT INTO payments VALUES (?,?,?);', payInfo)
    
    connection.commit()
    option_menu('a')
    return

def driver_abstract():
    global connection, cursor
    
    print("\nEnter the necessary information to get a driver abstract")
    print("Enter 'QUIT' at anytime to go back to menu")
    firstname = input("Enter first name: ")
    while firstname == "":
        print("Invalid input")
        firstname = input("Enter first name: ")
    if firstname == 'QUIT':
        agent_menu()
    lastname = input("Enter last name: ")
    while lastname == "":
        print("Invalid input")
        lastname = input("Enter last name: ")
    if lastname == 'QUIT':
        agent_menu()
    fullname = (firstname.upper(),lastname.upper())
    notValid = True
    while notValid:
        cursor.execute('SELECT * FROM persons p WHERE upper(fname) = ? AND upper(lname) = ?;', fullname)
        person = cursor.fetchone()
        if person == None:
            print('Person not in database')
            firstname = input("Enter first name: ")
            while firstname == "":
                print("Invalid input")
                firstname = input("Enter first name: ")
            if firstname == 'QUIT':
                notValid = False
                agent_menu()
            lastname = input("Enter last name: ")
            while lastname == "":
                print("Invalid input")
                lastname = input("Enter last name: ")
            if lastname == 'QUIT':
                notValid = False
                agent_menu()
            fullname = (firstname.upper(),lastname.upper())
        else:
            notValid = False

    #Find total tickets for a person
    cursor.execute('''SELECT COUNT(t.tno) FROM tickets t,registrations r WHERE t.regno = r.regno AND upper(r.fname) = ? AND upper(r.lname) = ?''',fullname)
    total_tickets = cursor.fetchone()
    total_tickets = total_tickets[0]

    #Get all the ticket info for the person
    #ADD v.make, v.model From vehicles v where r.vin = v.vin if all tickets have vehicles associated, confused because of post on forum
    cursor.execute('''SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model FROM vehicles v, tickets t,registrations r WHERE lower(v.vin) = lower(r.vin) AND t.regno = r.regno AND upper(r.fname) = ? AND upper(r.lname) = ? ORDER BY t.vdate DESC''',fullname)
    alltickets = cursor.fetchall()
    
    #This gets the total number of demerit notices for the person entered 
    cursor.execute('''SELECT Count(*) FROM demeritNotices d WHERE upper(d.fname) = ? AND upper(d.lname) = ?;''',fullname)
    total_notices = cursor.fetchone()
    total_notices = total_notices[0]
    
    #Finds total demerit points for a person
    cursor.execute('''SELECT sum(d.points) FROM demeritNotices d WHERE upper(d.fname) = ? AND upper(d.lname) = ?''',fullname)
    total_demeritpoints = cursor.fetchone()
    total_demeritpoints = total_demeritpoints[0]
    
    #Calculate date 2 years ago
    cursor.execute('''SELECT date('now','-2 year') ''')
    past_date = cursor.fetchone()
    past_date = past_date[0]
    d_info = (past_date,firstname.upper(),lastname.upper())

    #Find Tickets Spanning Back 2 years. (new)
    cursor.execute('''SELECT COUNT(t.tno) FROM tickets t, registrations r WHERE t.vdate >= ? AND t.regno = r.regno AND upper(r.fname) = ? AND upper(r.lname) = ?''',d_info)
    recent_tickets = cursor.fetchone()
    recent_tickets = recent_tickets[0]

    #Find Demerit Notices Spanning Back 2 years. (new)
    cursor.execute('''SELECT Count(*) FROM demeritNotices d WHERE d.ddate >= ? AND upper(d.fname) = ? AND upper(d.lname) = ?;''',d_info)
    recent_dnotices = cursor.fetchone()
    recent_dnotices = recent_dnotices[0]

    #Find Demerit Points Spanning Back 2 years.
    cursor.execute('''SELECT sum(d.points) FROM demeritNotices d WHERE d.ddate >= ? AND upper(d.fname) = ? AND upper(d.lname) = ?''',d_info)
    recent_demeritpoints = cursor.fetchone()
    recent_demeritpoints = recent_demeritpoints[0]
      
    print("\nTotal Tickets: " + str(total_tickets) + " --Tickets within last two years: " + str(recent_tickets) + " -- Total Demerit Notices: " + str(total_notices) + " -- Demerit Notices within last two years: " + str(recent_dnotices) + " -- Total Demerit Points: " + str(total_demeritpoints) + " -- Demerit Points Within Last 2 Years: " + str(recent_demeritpoints) + "\n")

    connection.commit()

    decision = input('Would you like to view the tickets (y/n): ')
    while decision.upper() != 'Y' and decision.upper() != 'N':
        print('Invalid option')
        decision = input('Would you like to view the tickets (y/n): ')
    if decision.upper() == 'Y':
        numTickets = len(alltickets)
        if numTickets == 0:
            print("\nThere are no tickets to view\n")
        elif numTickets <= 5:
            print("\nThese are all the tickets\n")
            for x in range(numTickets):
                ticketnumb = alltickets[x][0]
                ticketdate = alltickets[x][4]
                ticketvio = alltickets[x][3]
                ticketfine = alltickets[x][2]
                ticketreg = alltickets[x][1]
                vehiclemake = alltickets[x][5]
                vehiclemodel = alltickets[x][6]
                print("Ticket Number: " + str(ticketnumb) + " -- Violation Date: " + str(ticketdate) + " -- Violation: " +str(ticketvio) + " -- Fine: " + str(ticketfine) + " -- Registration Number: " + str(ticketreg) + "  -- Vehicle Make: " + str(vehiclemake) + " -- Vehicle Model: " + str(vehiclemodel))
        else:
            for x in range(0, 5):
                ticketnumb = alltickets[x][0]
                ticketdate = alltickets[x][4]
                ticketvio = alltickets[x][3]
                ticketfine = alltickets[x][2]
                ticketreg = alltickets[x][1]
                vehiclemake = alltickets[x][5]
                vehiclemodel = alltickets[x][6]
                print("Ticket Number: " + str(ticketnumb) + " -- Violation Date: " + str(ticketdate) + " -- Violation: " +str(ticketvio) + " -- Fine: " + str(ticketfine) + " -- Registration Number: " + str(ticketreg) + "  -- Vehicle Make: " + str(vehiclemake) + " -- Vehicle Model: " + str(vehiclemodel))
            decision = input("Would you like to see the remaining tickets? (y/n): ")
            while decision.upper() != 'Y' and decision.upper() != 'N':
                print('Invalid option')
                decision = input("Would you like to view more tickets (y/n): ")
            if decision.upper() == 'Y':
                print("Next set of tickets this person has: ")
                tracker = 5
                group = (numTickets // 5) - 1
                notfin = False
                while notfin == False:
                    if group <= 0:
                        endpoint = numTickets
                    else:
                        endpoint = tracker + 5
                    for x in range(tracker, endpoint):
                        ticketnumb = alltickets[x][0]
                        ticketdate = alltickets[x][4]
                        ticketvio = alltickets[x][3]
                        ticketfine = alltickets[x][2]
                        ticketreg = alltickets[x][1]
                        vehiclemake = alltickets[x][5]
                        vehiclemodel = alltickets[x][6]
                        print("Ticket Number: " + str(ticketnumb) + " -- Violation Date: " + str(ticketdate) + " -- Violation: " +str(ticketvio) + " -- Fine: " + str(ticketfine) + " -- Registration Number: " + str(ticketreg) + "  -- Vehicle Make: " + str(vehiclemake) + " -- Vehicle Model: " + str(vehiclemodel))
                    group -= 1
                    tracker += 5
                    if endpoint == numTickets:
                        print("\nThese are all the tickets\n")
                        notfin = True
                    else:
                        decision = input("Would you like to see the remaining tickets? (y/n): ")
                        while decision.upper() != 'Y' and decision.upper() != 'N':
                            print('Invalid option')
                            decision = input("Would you like to view more tickets (y/n): ")
                        if decision.upper() == 'Y':
                            print("Next set of tickets this person has: ")
                        else:
                            notfin = True
    connection.commit()
    option_menu('a')
    return
    
def issue_ticket():
    global connection, cursor
    
    print("\nEnter the necessary information to issue a ticket")
    print("Enter 'QUIT' at anytime to go back to menu")
    notValid = True
    #keeps checking if input is an integer
    while notValid:
        regno = input("Registration number: ")
        if regno == 'QUIT':
            notValid = False
            officer_menu()
        else:
            try:
                regno = int(regno)
                notValid = False
            except:
                print("Invalid input")
    cursor.execute('SELECT regno FROM registrations')
    allreg = cursor.fetchall()
    found = False
    #checks if registration exists
    for reg in allreg:
        if reg[0] == regno:
            found = True
    if found == False:
        print("Registration does not exist")
    else:
        regnoinfo = (regno,)
        cursor.execute('''SELECT r.fname, r.lname, v.make, v.model, v.year, v.color FROM registrations r, vehicles v 
                        WHERE r.regno = ?
                        AND lower(r.vin) = lower(v.vin);''', regnoinfo)
        info = cursor.fetchone()
        #printing on who the registration is under
        print("Name: " + str(info[0]).title() + " " + str(info[1]).title() + " Make: " + info[2].title() + " Model: " + info[3].title() + " Year: " + str(info[4]))
        cursor.execute("SELECT tno FROM tickets")
        ticknos = cursor.fetchall()
        existingNos = []
        #generates a random integer that is unique
        for tic in ticknos:
            existingNos.append(tic[0])
        tno = random.randint(0, 10000)
        while tno in existingNos:
            tno = random.randint(0, 10000)
        #keeps asking for valid date format if not left blank
        valid = False
        while not valid:
            vdate = input("Date of violation (yyyy-mm-dd) (if left empty violation will be set to today's date): ")
            if vdate == 'QUIT':
                valid = True
                officer_menu()
            else:
                if vdate == "":
                    vdate = time.strftime("%Y-%m-%d")
                    valid = True
                else:
                    try: 
                        vdate = datetime.datetime.strptime(vdate, "%Y-%m-%d").strftime("%Y-%m-%d")
                        valid = True
                    except:
                        print("Invalid entry please try again")
        violation = input("Violation type: ")
        while violation == '':
            print("Invalid input")
            violation = input("Violation type: ")
        if violation == 'QUIT':
            officer_menu()
        notValid = True
        while notValid:
            fine = input("Violation fine: $")
            if fine == 'QUIT':
                notValid = False
                officer_menu()
            else:
                try:
                    fine = int(fine)
                    notValid = False
                except:
                    print("Invalid input")
        ticketInfo = (tno, regno, fine, violation, vdate)
        cursor.execute('INSERT into tickets VALUES (?, ?, ?, ?, ?);', ticketInfo)
        print("\nTicket has been issued\n")
    connection.commit()
    option_menu('o')
    return

def find_car_owner():
    global connection, cursor
    
    print("\nEnter at least one of the following information about the car")
    print("Enter 'QUIT' at anytime to go back to menu")
    make = input("Enter the make of car: ")
    if make == 'QUIT':
        officer_menu()
    else:
        if make == '':
            make = '%'
    model = input("Enter the model of the car: ")
    if model == 'QUIT':
        officer_menu()
    else:
        if model == '':
            model = '%'
    valid = False
    while not valid:
        year = input("Enter year of car (yyyy): ")
        if year == 'QUIT':
            officer_menu()
            valid = True
        else:
            if year == '':
                year = '%'
                valid = True
            else:
                try: 
                    datetime.datetime.strptime(year, "%Y").strftime("%Y")
                    valid = True
                except:
                    print("Invalid entry please try again")
    color = input("Enter color: ")
    if color == 'QUIT':
        officer_menu()
    else:
        if color == '':
            color = '%'
    plate = input("Enter plate: ")
    if plate == 'QUIT':
        officer_menu()
    else:
        if plate == '':
            plate = '%'
    carInfo = (make.lower(), model.lower(), year, color.lower(), plate.lower())
    carInfo2 = (make.lower(), model.lower(), year, color.lower())
    compare = ('%', '%', '%', '%', '%')
    if carInfo == compare:
        print("Did not enter at least one of the information")
    else:
        cursor.execute('''
                    SELECT lower(r.vin) as avin, v.make, v.model, v.year, v.color, r.plate, max_date, r.expiry, r.fname, r.lname
                    FROM registrations r left outer join vehicles v on lower(r.vin) = lower(v.vin)
                    INNER JOIN
                    (SELECT lower(r.vin) as vin, MAX(r.regdate) as max_date
                    FROM registrations r left outer join vehicles v on lower(r.vin) = lower(v.vin)
                    GROUP BY lower(v.vin))a
                    on a.vin = avin AND a.max_date = r.regdate
                    AND lower(v.make) LIKE ? 
                    AND lower(v.model) LIKE ? 
                    AND v.year LIKE ? 
                    AND lower(v.color) LIKE ? 
                    AND lower(r.plate) LIKE ?; ''', carInfo)

        withreg = cursor.fetchall()
        cursor.execute('''
                        SELECT lower(v.vin), v.make, v.model, v.year, v.color
                        FROM vehicles v
                        WHERE lower(v.make) LIKE ? 
                        AND lower(v.model) LIKE ? 
                        AND v.year LIKE ? 
                        AND lower(v.color) LIKE ?; ''', carInfo2)
        withoutreg = cursor.fetchall()
        allregs = []
        for reg1 in withoutreg:
            for reg2 in withreg:
                if reg1[0].lower() == reg2[0].lower():
                    regs = []
                    for x in range(1, len(reg2)):
                        regs.append(str(reg2[x]))
                    allregs.append(regs)
                else:
                    regs = []
                    for x in range(1, len(reg1)):
                        regs.append(str(reg1[x]))
                    allregs.append(regs)
        if allregs == []:
            print("\nNo matches found in the database\n")
        else:
            numofcars = len(allregs)
            if numofcars < 4:
                print("\n")
                for reg in allregs:
                    if len(reg) < 9:
                        print(' | '.join(reg) + " | NO OWNER")
                    else:
                        print(' | '.join(reg))
                print("\n")
            else:
                count = 1
                for reg in allregs:
                    print(str(count) + '. ' + " | ".join(reg[:5]))
                    count += 1
                notvalid = True
                while notvalid: 
                    option = input("Choose the option you want to show more information about the car or 'QUIT' to exit: ")
                    if option == 'QUIT':
                        officer_menu()
                        notvalid = False
                    else:
                        try:
                            option = int(option)
                            if option in range(numofcars):
                                notvalid = False
                        except:
                            print("Invalid input")
                
                choice = allregs[int(option) - 1]
                if len(choice) < 9:
                    print("\n" + ' | '.join(choice) + " | NO OWNER" + "\n")
                else:
                    print("\n" + ' | '.join(choice) + "\n")
    connection.commit()
    option_menu('o')
    return

def random_regno():
    global connection, cursor

    cursor.execute('''SELECT regno FROM registrations ; ''')
    connection.commit()
    allRegnum = cursor.fetchall()
    allRegno = [int(x) for x, in allRegnum]
    randRegno = random.randint(0,10000)

    return random_regno() if randRegno in allRegno else randRegno

def option_menu(user):
    print("1. Go back to main menu\n2. Logout\n3. Quit\n")
    #keeps asking for valid option
    notValid = True
    while notValid:
        option = input("Enter the number for the option you want: ")
        try:
            option = int(option)
            if option not in range(1, 4):
                print("Invalid option")
            else:
                notValid = False
        except:
            print("Invalid option")
    if int(option) == 1:
        if user == 'a':
            agent_menu()
        else:      
            officer_menu()
    elif int(option) == 2:
        logout()      
    elif int(option) == 3:
        print("Exited program")
        quit()
    return

def logout():
    #will logout user by calling login page again
    print("User Logged Out")
    login()

    return

def main():
    global connection, cursor

    notValid = True
    while notValid:
        path = input("Enter database filename as filename.db filename being the name of your file: ")
        temp = path.split('.')
        if len(temp) != 2:
            print("Invalid filename")
        else:
            if temp[1] == 'db':
                notValid = False
            else:
                print("Incorrect extension")
    path = "./" + path
    connect(path)
    login()

    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()