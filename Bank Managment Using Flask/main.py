import datetime
from twilio.rest import Client
from flask import Flask, render_template,request,session,redirect
import random
import mysql.connector


app = Flask(__name__)
app.secret_key="Bank Management"



@app.route("/")
def homePage():
    return render_template("homepage.html")

@app.route("/addAcc",methods=["GET","POST"])
def addAcc():
    return render_template("addAcc.html")

@app.route("/searchAcc",methods=["GET","POST"])
def searchAcc():
    return render_template("searchAcc.html")

@app.route("/closeAcc",methods=["GET","POST"])
def closeAcc():
    return render_template("closeAcc.html")

@app.route("/showAll",methods=["GET","POST"])
def showAll():
    if("Name" in session):
                mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password="7020101528",
                    database="Bank"
                )
                sql = "select * from account_holder"
                cursor = mydb.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                mydb.commit()
                mydb.close()
                return render_template("showAll.html",result=result)

    else:
        return render_template("admin.html")
    

@app.route("/mainMenu",methods=["GET","POST"])
def mainMenu():
    return render_template("homepage.html")

@app.route("/verify/<int:name>/")
def Verification(name):
    print(name)
    if (name == 0):
        return render_template("admin.html")
    elif (name == 1):
        return render_template("user.html")
    elif (name == 2):
        return render_template("exit.html")

@app.route("/admin",methods=["POST","GET"])
def admin():
    error = None
    uname = request.form["uname"]
    pwd = request.form["pwd"]

    if (uname == "Admin@" and pwd == "Admin@123"):
        session["Name"] = uname
        return redirect("/adminFeature")

    else:
        error = "* Invalid Username and Password"
        return render_template("admin.html", error=error)

@app.route("/adminFeature")
def adminFeature():
    if ("Name" in session):
        return render_template("adminFeature.html") 

    else:
        return render_template("admin.html") 

@app.route("/feature/<int:id>/") 
def feature(id):
    if ("Name" in session):

        if (id == 1):
            return redirect("/addAcc")

        elif(id==2):
            return redirect("/searchAcc")

        elif(id == 3):
            return redirect("/closeAcc")
        
        elif(id== 4):       
            return redirect("/showAll")
            
        
        elif(id == 5):
            return redirect("/logout")

    else:
        return render_template("admin.html")

@app.route("/Addrecord",methods=["POST"])
def Addrecord():
    if ("Name" in session):
        msg = None
        uname = request.form["uname"]
        mob = request.form["no"]
        gen = request.form["gender"]
        type = request.form["type"]
        rand = request.form["accnum"]
        amt = request.form["money"]

        try:
                mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password="7020101528",
                    database="Bank"
                )
                sql = "insert into account_holder (bname,gender,btype,account_Number,amount,mobile) values (%s,%s,%s,%s,%s,%s)"
                val = (uname,gen,type,rand,amt,mob)
                cursor = mydb.cursor()
                cursor.execute(sql,val)
                mydb.commit()
                mydb.close()
                return redirect("/addAcc")
        except:
            return render_template("addAcc.html", msg="***_Account Number Already Exist_***")

    else:
        return render_template("admin.html")
    
@app.route("/searchRecord",methods=["POST"])  
def searchRecord():
    if ("Name" in session):
        uname = request.form["action"]
        print(uname)
        if(uname == "SEARCH BY ID"):
            return render_template("searchID.html")

        elif(uname == "SEARCH BY NAME"):
            return render_template("searchNAME.html")
        
        elif(uname == "SEARCH BY ACCOUNT NUMBER" ):
            return render_template("searchNUM.html")
    
    else:
        return render_template("admin.html")


@app.route("/identify/<int:id>/",methods=["POST"])
def identify(id):
    if(id == 1):
        idd = request.form["ID"]
        mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password="7020101528",
                    database="Bank"
                )
        sql = "select * from account_holder"
        cursor = mydb.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            if(int(i[0])==int(idd)):
                return render_template("searchID1.html",a=i[0],b=i[1],c=i[2],d=i[3],e=i[4],f=i[5],g=i[6])
            
        else:
                return render_template("searchID.html",msg="*No Record Found")

    elif (id == 2):
        idd = request.form["ID"]
        mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password="7020101528",
                    database="Bank"
                )
        sql = "select * from account_holder"
        cursor = mydb.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            print(result)
            if(i[1]== idd):
                return render_template("searchNAME1.html",a=i[0],b=i[1],c=i[2],d=i[3],e=i[4],f=i[5],g=i[6])
                
            
        else:
                return render_template("searchNAME.html",msg="*No Record Found")
    
    elif (id==3):
        idd = request.form["ID"]
        mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password="7020101528",
                    database="Bank"
                )
        sql = "select * from account_holder"
        cursor = mydb.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            
            if(int(i[5])==int(idd)):
                return render_template("searchNUM1.html",a=i[0],b=i[1],c=i[2],d=i[3],e=i[4],f=i[5],g=i[6])
            
        else:
                return render_template("searchNUM.html",msg="*No Record Found")

@app.route("/modify/<int:id>")
def modification(id):
    if("Name" in session):
        mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password="7020101528",
                    database="Bank"
                )
        sql = "select * from account_holder"
        cursor = mydb.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            print(result)
            if (int(i[0]) ==int(id)):
                return render_template("modify.html",a=i[0],b=i[1],c=i[2],d=i[3],e=i[4],f=i[5],g=i[6])
    
    else:
        return render_template("admin.html")


@app.route("/updateRec/<int:id>", methods=["POST"])
def updateRec(id):
    if("Name" in session):
        uname = request.form["uname"]
        mob = request.form["no"]
        gen = request.form["gender"]
        type = request.form["type"]
        amt = request.form["money"]

        mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password="7020101528",
                    database="Bank"
                )
        sql = "update account_holder set bname=%s, mobile=%s,gender=%s,btype=%s,amount=%s where bid=%s "
        val =(uname,mob,gen,type,amt,id)
        cursor = mydb.cursor()
        cursor.execute(sql,val)
        mydb.commit()
        mydb.close()
        return redirect("/showAll")
    else:
        return render_template("admin.html")

@app.route("/deleteRec",methods=["POST"])
def deleteRec():
    if("Name" in session):
        uname = request.form["uname"]
        mob = request.form["no"]
        type = request.form["type"]
        rand = request.form["accnum"]

        mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password="7020101528",
                    database="Bank"
                )
        sql = "select * from account_holder"
        cursor = mydb.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            if (uname == i[1] and int(mob) == int(i[2]) and type==i[4] and int(rand) == int(i[5])):
                    mydb = mysql.connector.connect(
                                host = "localhost",
                                user = "root",
                                password="7020101528",
                                database="Bank"
                            )
                    sql = " delete from account_holder where account_Number=%s"
                    val=(rand,)
                    cursor = mydb.cursor()
                    cursor.execute(sql,val)       
                    mydb.commit()
                    mydb.close()
                    return render_template("/closeAcc.html",msg = "!!!...Account Deleted Successfully...!!!")
        else:
             return render_template("closeAcc.html",msg="** Details Not Match")

    else:
        return render_template("admin.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("homepage.html")

@app.route("/contentUser/<int:num>",methods=["POST","GET"])
def contentUser(num):
    if(num == 1):
        return render_template("signIn.html")

    elif(num == 2):
        return render_template("signUp.html")
       

    

@app.route("/getOtp",methods=["POST","GET"])
def getOtp():
    
        nm = request.form["uname"]
        accNum = request.form["accnum"]
        mobile = request.form["no"]
        mobb = str(mobile)
        print("mobb",mobb)
        num = request.form["ottp"]
        nump=str(num)
        span = request.form["span"]
        print("otp",span)
        if(mobb.isdigit() and nump.isdigit()==False):
                c =0
                for i in mobb:
                    c +=1
                if(c == 10):
                    try:
                                
                        genotp = random.randint(1000, 9999)

                        account_sid = "AC392788061ea3b7be275e1a4dafec4510"
                        auth_token = "6bf1cd5ba5b21bc969d6f158e642a4dd"

                        client = Client(account_sid, auth_token)

                        msg = client.messages.create(
                            body = f"Hello...!!! Akshay Sending OTP:{genotp}", #net sobt connect pahije
                            from_ ="+18572292965",
                            to = "+91"+mobb
                        )
                        msgs="* OTP send to your mobile Number"
                        print("OTP",genotp)
                        print("OTP",{genotp})
                        #data=genotp
                        
                        return render_template("signUp.html",msgs=msgs,nm=nm, accNum=accNum, mobile=mobile,genotp=genotp)
                    except:
                        msgs="* Please Connect to Internet"
                        return render_template("signUp.html",alert1=msgs,nm=nm, accNum=accNum, mobile=mobile)
                
                else:
                    msgs = "* Enter Valid Mobile Number"
                    return render_template("signUp.html",val=msgs,nm=nm, accNum=accNum, mobile=mobile)


        else:
            alert = "Details Verified Successfull"
            alert1 = "* OOps..!!! Details Not Valid"
            alert2 = "* OTP not match"
            #print(" DATA",span)
            #print(" num",num)
            try:
                if(int(num) == int(span)):
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user = "root",
                        password="7020101528",
                        database = "Bank",
                    )

                    sql = "select * from account_holder"
                    cursor = mydb.cursor()
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for i in result:
                        if (nm == i[1] and int(mobile) == int(i[2]) and  int(accNum) == int(i[5]) ):
                            return render_template("createUser.html",alert=alert,mobile=mobile,accNum=accNum)
                    
                    else:
                        return render_template("SignUp.html",alert1=alert1,nm=nm, accNum=accNum, mobile=mobile)

                else:
                    return render_template("SignUp.html",alert2=alert2,nm=nm, accNum=accNum, mobile=mobile,num=num)
            
            except:
                return render_template("SignUp.html",alert2=alert2,nm=nm, accNum=accNum, mobile=mobile,num=num)


@app.route("/submitData",methods=["POST"])
def submitData():
        user = request.form["user"]
        pwd = request.form["pwd"]
        acc = request.form["acc1"]
        mbb = request.form["mb1"]
        
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="7020101528",
            database = "Bank",
        )
        sql ="select * from account_holder"
        cursor=mydb.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            try:
                if(int(acc) == int(i[5]) and int(mbb)== int(i[2])):
                    sql = "update account_holder set login_id=%s,password=%s where account_Number=%s"
                    val=(user,pwd,int(acc))
                    cursor.execute(sql,val)
                    '''sql = "update account_holder set password=%s where account_Number=%s"
                    val=(pwd,int(acc))
                    cursor.execute(sql,val)'''
                    mydb.commit()
                    mydb.close()
                    return render_template("signIn.html")


            except:
                    msg="* User-Name Already Exist"
                    return render_template("createUser.html",msg=msg)


@app.route("/entryData",methods=["POST"])
def entryData():
    name ="* Account Holder: "
    userId = request.form["user"]
    passw = request.form["pwd"]
    time=datetime.datetime.now()
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "7020101528",
        database = "Bank",
    )
    sql = "select * from account_holder"
    cursor = mydb.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        if (userId == i[7] and passw == i[8]):
            session["userId"] = userId
            return render_template("userFeature.html",user=userId,password=passw,result=i[6],map=i[1],name=name,time=time)
        
    else:
        msg = "* Invalid Username and Password"
        return render_template("signIn.html", msg = msg)

@app.route("/userFeature",methods=["POST"])
def userFeature():
    if("userId" in session):
        userId = request.form["users"]
        passw = request.form["pass"]
        name = request.form["balance"]
        bal = "** Your Balance Is: "
        print("ID",userId)
        print("name",name)
        time=datetime.datetime.now()
        
        mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "7020101528",
                database = "Bank",
            )
        if(name == "BALANCE ENQUIRY"):
            sql = "select * from account_holder"
            #val = (userId,)
            cursor = mydb.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            #print("result",result)
            
            for i in result:
                name=" Account Holder:"
                if(userId == i[7] and passw == i[8]  ):
                    return render_template("userFeature1.html",bal=bal, result=i[6],map=i[1],name=name,user1=userId,password=passw,time=time)
            else:
                msg="* UserId and Password not Matches"
                return render_template("userFeature1.html",msg=msg)
                
        elif(name == "WITHDRAW AMOUNT"):
            return render_template("userFeature2.html",user2=userId,password=passw,time=time)
        
        elif(name== "DEPOSIT AMOUNT"):
            return render_template("userFeature3.html",user2=userId,password=passw,time=time)

        elif(name== "TRANSFER AMOUNT"):
            return render_template("userFeature4.html",user2=userId,password=passw,time=time)
        
    else:
        return render_template("signIn.html")


@app.route("/withDraw", methods=["POST"])
def withDraw():
    if("userId" in session):
        amt=request.form["val"]
        pw = request.form["ps"]
        mainPass=request.form["pass"]
        userId = request.form["users"]
        mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "7020101528",
                database = "Bank",
        )
        if(mainPass == pw):
            try:
                sql = "select amount from account_holder where login_id=%s"
                val = (userId,)
                cursor = mydb.cursor()
                cursor.execute(sql,val)
                result = cursor.fetchone()
                if(int(amt)>0):
                    if(result[0]>=int(amt)):
                        balance= (result[0] - int(amt))
                        sql = "update account_holder set amount=%s where login_id=%s"
                        val = (balance,userId)
                        cursor = mydb.cursor()
                        cursor.execute(sql,val)
                        mydb.commit()
                        msg= "!!..WithDrawal Successful"
                        return render_template("userFeature2.html",msgs=msg,user2=userId,password=mainPass)

                    else:
                        msg="* Insufficient Amount"
                        return render_template("userFeature2.html",msg=msg,user2=userId,password=mainPass)

                else:
                    msg="* Not Valid Amount"
                    return render_template("userFeature2.html",msg=msg,user2=userId,password=mainPass)
        
            except:
                msg="* Invalid Credentials"
                return render_template("userFeature2.html",msg=msg,user2=userId,password=mainPass)
        
        else:
            msg="* Invalid Password"
            return render_template("userFeature2.html",msg=msg,user2=userId,password=mainPass)
    else:
        return render_template("signIn.html")

@app.route("/Deposit", methods=["POST"])
def Deposit():
    if("userId" in session):
        amt=request.form["val"]
        pw = request.form["ps"]
        mainPass=request.form["pass"]
        userId = request.form["users"]
        mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "7020101528",
                database = "Bank",
        )
        if(mainPass == pw):
            try:
                sql = "select amount from account_holder where login_id=%s"
                val = (userId,)
                cursor = mydb.cursor()
                cursor.execute(sql,val)
                result = cursor.fetchone()
                if(int(amt)>0):
                    
                        balance= (result[0] + int(amt))
                        sql = "update account_holder set amount=%s where login_id=%s"
                        val = (balance,userId)
                        cursor = mydb.cursor()
                        cursor.execute(sql,val)
                        mydb.commit()
                        msg= "!!..Deposit Successful"
                        return render_template("userFeature3.html",msgs=msg,user2=userId,password=mainPass)          

                else:
                    msg="* Not Valid Amount"
                    return render_template("userFeature3.html",msg=msg,user2=userId,password=mainPass)
        
            except:
                msg="* Invalid Credentials"
                return render_template("userFeature3.html",msg=msg,user2=userId,password=mainPass)

        else:
            msg="* Invalid Password"
            return render_template("userFeature3.html",msg=msg,user2=userId,password=mainPass)

    else:
        return render_template("signIn.html")

@app.route("/TransAmt", methods=["POST"])
def TransAmt():
    if("userId" in session):
        benef=request.form["val"]
        pw=request.form["ps"]
        mainPass=request.form["pass"]
        amt=request.form["trans"]
        userId = request.form["users"]
        mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "7020101528",
                database = "Bank",
        )
        if(mainPass ==pw):
            try:
                sql = "select account_Number from account_holder where account_Number=%s"
                val = (int(benef),)
                cursor = mydb.cursor()
                cursor.execute(sql,val)
                result = cursor.fetchone()
                if(int(benef)==result[0]):
                    if(int(amt)>0):
                        sql = "select amount from account_holder where login_id=%s"
                        val = (userId,)
                        cursor = mydb.cursor()
                        cursor.execute(sql,val)
                        result = cursor.fetchone()
                        if(result[0]>=int(amt)):
                            balance= (result[0] - int(amt))
                            sql = "update account_holder set amount=%s where login_id=%s"
                            val = (balance,userId)
                            cursor = mydb.cursor()
                            cursor.execute(sql,val)
                            sql = "select amount from account_holder where account_Number=%s"
                            val=(int(benef),)
                            cursor = mydb.cursor()
                            cursor.execute(sql,val)
                            result = cursor.fetchone()
                            balance= (result[0] + int(amt))
                    
                            sql = "update account_holder set amount=%s where account_Number=%s"
                            val = (balance,int(benef))
                            cursor = mydb.cursor()
                            cursor.execute(sql,val)                   
                            mydb.commit()
                            msg= "!!..Transfer Successful"
                            return render_template("userFeature4.html",msgs=msg,user2=userId,password=mainPass)  

                        else:
                                
                            msg="* Insufficient Amount"
                            return render_template("userFeature4.html",msg=msg,user2=userId,password=mainPass)


                else:
                    msg="* Beneficiary Account Not Valid"
                    return render_template("userFeature4.html",msg=msg,user2=userId,password=mainPass)
        
            except:
                msg="* Beneficiary Account Not Valid"
                return render_template("userFeature4.html",msg=msg,user2=userId,password=mainPass)
        else:
            msg="* Invalid Password"
            return render_template("userFeature4.html",msg=msg,user2=userId,password=mainPass)

    else:
        return render_template("signIn.html")

@app.route("/userLogout")
def userLogout():
    session.clear()
    return render_template("homepage.html")


if(__name__=="__main__"):
    app.run(debug=True)
