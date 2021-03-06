import tkinter
import os
from tkinter import ttk
from tkinter.ttk import Progressbar
import xlwt

USERPATH = ''

class softwareestimate ():
    def __init__ ( self ):
        self.effort = -1


def initbackend ():
    path = os.getcwd ()

    if not os.path.exists ( path + '/data' ):
        os.makedirs ( path + '/data' )

    path = path + '/data'

    if not os.path.isfile ( path + '/users.txt' ):
        file = open ( path + '/users.txt' , 'w' )
        file.close ()
    
    global USERPATH
    USERPATH = path + '/users.txt'

    global estimation
    estimation = softwareestimate ()

def createuser ( username , password ):
    if username == '' or password == '':
        return -2
    global USERPATH
    file = open ( USERPATH , 'r+' )
    ret = 0
    while 1:
        nowuser = file.readline ()
        nowuser = nowuser[:-1]
        if nowuser == '':
            break
        # print ( nowuser )
        # print ( username )
        if nowuser == username:
            ret = -1
            break
        nowpassword = file.readline ()
    if ret == 0:
        file.write ( username + '\n' )
        file.write ( password + '\n' )

    file.close ()
    return ret

def login ( username , password ):
    if username == '' or password == '':
        return -2
    global USERPATH
    file = open ( USERPATH , 'r+' )
    ret = -1
    while 1:
        nowuser = file.readline ()
        nowuser = nowuser[:-1]
        if nowuser == '':
            break
        nowpassword = file.readline ()
        nowpassword = nowpassword[:-1]
        if nowuser == username:
            if password == nowpassword:
                ret = 0
                break
            else:
                break
            break

    file.close ()
    return ret


class mywindow ():
    
    def setstage ( self , stageid ):
        # print ( stageid )
        if ( stageid not in range ( self.stagenumber ) ):
            return
        self.stage[self.nowstage].grid_forget ()
        self.stage[self.nowstage].grid_propagate(0)
        self.stage[stageid].grid ( row = 0 , column = 0 )
        self.nowstage = stageid

    def closewindow ( self , window1 , window2 ):
        window2.destroy ()
        window1.destroy ()

    def createuser ( self , windowsignup , username , password ):
        res = createuser ( username , password )
        if res == 0:
            windowsuccess = tkinter.Toplevel ( windowsignup )
            windowsuccess.title ( '????????????' )

            text = tkinter.Label ( windowsuccess , text = '????????????' )
            button = tkinter.Button ( windowsuccess , text = '??????' , command = lambda:self.closewindow(windowsignup,windowsuccess) )
            
            text.grid ( row = 0 , column = 0 )
            button.grid ( row = 1 , column = 0 )
        else:
            windowfail = tkinter.Toplevel ( windowsignup )
            windowfail.title ( '????????????' )

            if res == -1:
                error = '?????????????????????'
            elif res == -2:
                error = '??????????????????????????????'
            else:
                error = '????????????'
            
            text = tkinter.Label ( windowfail , text = error )
            button = tkinter.Button ( windowfail , text = '??????' , command = windowfail.destroy )
            
            text.grid ( row = 0 , column = 0 )
            button.grid ( row = 1 , column = 0 )



    def signup ( self ):
        windowsignup = tkinter.Toplevel ( self.mainwindow )

        windowsignup.title ( '????????????' )

        textuser = tkinter.Label ( windowsignup , text = '?????????' )
        textpassword = tkinter.Label ( windowsignup , text = '??????' )

        entryuser = tkinter.Entry ( windowsignup )
        entrypassword = tkinter.Entry ( windowsignup , show='*')

        textuser.grid ( row = 0, column = 0 )
        entryuser.grid ( row = 0 , column = 1 )
        textpassword.grid ( row = 1 , column = 0 )
        entrypassword.grid ( row = 1 , column = 1 )

        buttonconfirm = tkinter.Button ( windowsignup , text = '??????' , command = lambda:self.createuser(windowsignup,entryuser.get(),entrypassword.get()) )
        buttoncancel = tkinter.Button ( windowsignup , text = '??????' , command = lambda:windowsignup.destroy() )

        buttoncancel.grid ( row = 2 , column = 0 )
        buttonconfirm.grid ( row = 2 , column = 1 )

    def signin ( self , stageid , username , password ):
        ret = login ( username , password )
        if ret == 0:
            self.setstage ( self.nowstage + 1 )
        elif ret == -2:
            pass
        else:
            windowfail = tkinter.Toplevel ( self.stage[stageid] )
            windowfail.title ( '????????????' )

            text = tkinter.Label ( windowfail , text = '????????????????????????' )
            button = tkinter.Button ( windowfail , text = '??????' , command = windowfail.destroy )
            
            text.grid ( row = 0 , column = 0 )
            button.grid ( row = 1 , column = 0 )
    
    def initlogin ( self ):
        stageid = 0

        textuser = tkinter.Label ( self.stage[stageid] , text = 'Username       ' )
        textpassword = tkinter.Label ( self.stage[stageid] , text = 'Password       ' )

        entryuser = tkinter.Entry ( self.stage[stageid] )
        entrypassword = tkinter.Entry ( self.stage[stageid] , show = '*' )

        self.pbar[stageid].grid ( row = 0, column = 0, columnspan = 4 )
        textuser.grid ( row = 1 , column = 1 )
        entryuser.grid ( row = 1 , column = 2 )
        textpassword.grid ( row = 2 , column = 1 )
        entrypassword.grid ( row = 2 , column = 2 )

        self.stagebut[stageid][0].config ( text = 'Regsiter' , command = self.signup )
        self.stagebut[stageid][1].config ( text = 'Login' , command = lambda:self.signin(stageid,entryuser.get(),entrypassword.get()) )
        self.stagebut[stageid][0].grid ( row = 4 ,  column = 1 )
        self.stagebut[stageid][1].grid ( row = 4 ,  column = 2 )

    def commitcodeline ( self , window , codeline ):
        if codeline == '':
            return

        windowshow = tkinter.Toplevel ( window )

        textcodeline = tkinter.Label ( windowshow , text = '???????????????' + codeline )
        textcodeline.grid ( row = 0 , column = 0 )

        buttonok = tkinter.Button ( windowshow , text = '??????' , command = lambda:self.closewindow(window,windowshow) )
        buttonok.grid ( row = 100 , column = 0 )

        global estimation
        estimation.codeline = codeline


    def codeline ( self ):
        window = tkinter.Toplevel ( self.mainwindow )

        textcodeline = tkinter.Label ( window , text = '????????????' )
        
        entrycodeline = tkinter.Entry ( window )

        textcodeline.grid ( row = 1 , column = 0 )
        entrycodeline.grid ( row = 1 , column = 1 )

        buttonok = tkinter.Button ( window , text = '??????' , command = lambda:self.commitcodeline(window,entrycodeline.get()) )
        buttoncancel = tkinter.Button ( window , text = '??????' , command = window.destroy )
        buttoncancel.grid ( row = 100 , column = 0 )
        buttonok.grid ( row = 100 , column = 1 )

    def commitfunctionpoint ( self , window , UFP , VAF ):
        if UFP == '' or VAF == '':
            return

        windowshow = tkinter.Toplevel ( window )

        textFP = tkinter.Label ( windowshow , text = '????????????' + str(int(UFP) * int(VAF)) )
        textFP.grid ( row = 0 , column = 0 )

        buttonok = tkinter.Button ( windowshow , text = '??????' , command = lambda:self.closewindow(window,windowshow) )
        buttonok.grid ( row = 100 , column = 0 )

        global estimation
        estimation.UFP = UFP
        estimation.VAF= VAF
        estimation.FP = str(int(UFP) * int(VAF))


    def functionpoint ( self ):
        window = tkinter.Toplevel ( self.mainwindow )

        textUFP = tkinter.Label ( window , text = '??????????????????' )
        textVAF = tkinter.Label ( window , text = '????????????' )
        
        entryUFP = tkinter.Entry ( window )
        entryVAF = tkinter.Entry ( window )

        textUFP.grid ( row = 1 , column = 0 )
        entryUFP.grid ( row = 1 , column = 1 )
        textVAF.grid ( row = 2 , column = 0 )
        entryVAF.grid ( row = 2 , column = 1 )

        buttonok = tkinter.Button ( window , text = '??????' , command = lambda:self.commitfunctionpoint(window,entryUFP.get(),entryVAF.get()) )
        buttoncancel = tkinter.Button ( window , text = '??????' , command = window.destroy )
        buttoncancel.grid ( row = 100 , column = 0 )
        buttonok.grid ( row = 100 , column = 1 )

    def commitobjectpoint ( self , window , UOP , R ):
        if UOP == '' or R == '':
            return 

        windowshow = tkinter.Toplevel ( window )

        res = int(UOP) * (100-int(R)) / 100.0
        res = int (res)
        textOP = tkinter.Label ( windowshow , text = '????????????' + str(res) )
        textOP.grid ( row = 0 , column = 0 )

        buttonok = tkinter.Button ( windowshow , text = '??????' , command = lambda:self.closewindow(window,windowshow) )
        buttonok.grid ( row = 100 , column = 0 )

        global estimation
        estimation.UOP = UOP
        estimation.R = R
        estimation.OP = str(res)

    def objectpoint ( self ):
        window = tkinter.Toplevel ( self.mainwindow )

        textUOP = tkinter.Label ( window , text = '???????????????' )
        textR = tkinter.Label ( window , text = '???????????????' )
        
        entryUOP = tkinter.Entry ( window )
        entryR = tkinter.Entry ( window )

        textUOP.grid ( row = 1 , column = 0 )
        entryUOP.grid ( row = 1 , column = 1 )
        textR.grid ( row = 2 , column = 0 )
        entryR.grid ( row = 2 , column = 1 )

        buttonok = tkinter.Button ( window , text = '??????' , command = lambda:self.commitobjectpoint(window,entryUOP.get(),entryR.get()) )
        buttoncancel = tkinter.Button ( window , text = '??????' , command = window.destroy )
        buttoncancel.grid ( row = 100 , column = 0 )
        buttonok.grid ( row = 100 , column = 1 )

    def commitusecasepoint ( self , window , UUCP , TCF , ECF , PF ):
        if UUCP == '' or TCF == '' or ECF == '' or PF == '':
            return

        windowshow = tkinter.Toplevel ( window )

        UCP = int(UUCP) * float(TCF) * float(ECF)
        Effort = UCP * float(PF)
        textUCP = tkinter.Label ( windowshow , text = '????????????' + str(int(UCP)) )
        textEffort = tkinter.Label ( windowshow , text = '????????????' + str(int(Effort)) )
        textUCP.grid ( row = 0 , column = 0 )
        textEffort.grid ( row = 1 , column = 0 )

        buttonok = tkinter.Button ( windowshow , text = '??????' , command = lambda:self.closewindow(window,windowshow) )
        buttonok.grid ( row = 100 , column = 0 )

        global estimation
        estimation.UUCP = UUCP
        estimation.TCF = TCF
        estimation.ECF = ECF
        estimation.PF = PF
        estimation.UCP = str(int(int(UUCP) * float(TCF) * float(ECF)))
        estimation.Effort = str(int(UCP * float(PF)))

    def usecasepoint ( self ):
        window = tkinter.Toplevel ( self.mainwindow )

        textUUCP = tkinter.Label ( window , text = '??????????????????' )
        textTCF = tkinter.Label ( window , text = '?????????????????????' )
        textECF = tkinter.Label ( window , text = '?????????????????????' )
        textPF = tkinter.Label ( window , text = '???????????????' )
        
        entryUUCP = tkinter.Entry ( window )
        entryTCF = tkinter.Entry ( window )
        entryECF = tkinter.Entry ( window )
        entryPF = tkinter.Entry ( window )

        textUUCP.grid ( row = 1 , column = 0 )
        entryUUCP.grid ( row = 1 , column = 1 )
        textTCF.grid ( row = 2 , column = 0 )
        entryTCF.grid ( row = 2 , column = 1 )
        textECF.grid ( row = 3 , column = 0 )
        entryECF.grid ( row = 3 , column = 1 )
        textPF.grid ( row = 4 , column = 0 )
        entryPF.grid ( row = 4 , column = 1 )

        buttonok = tkinter.Button ( window , text = '??????' , command = lambda:self.commitusecasepoint(window,entryUUCP.get(),entryTCF.get(),entryECF.get(),entryPF.get()) )
        buttoncancel = tkinter.Button ( window , text = '??????' , command = window.destroy )
        buttoncancel.grid ( row = 100 , column = 0 )
        buttonok.grid ( row = 100 , column = 1 )

    def initscale ( self ):
        stageid = 1

        buttoncode = tkinter.Button ( self.stage[stageid] , text = '???????????????' , command = self.codeline )
        buttonfunction = tkinter.Button ( self.stage[stageid] , text = '???????????????' , command = self.functionpoint )
        buttonobject = tkinter.Button ( self.stage[stageid] , text = '???????????????' , command = self.objectpoint )
        buttonusecase = tkinter.Button ( self.stage[stageid] , text = '???????????????' , command = self.usecasepoint )
        
        buttoncode.grid ( row = 1 , column = 0 )
        buttonfunction.grid ( row = 1 , column = 1 )
        buttonobject.grid ( row = 1 , column = 2 )
        buttonusecase.grid ( row = 1 , column = 3 )
        
        self.pbar[stageid].grid ( row = 0, column = 0, columnspan = 5 )
        self.stagebut[stageid][0].grid ( row = 4 ,  column = 1 )
        self.stagebut[stageid][1].grid ( row = 4 ,  column = 2 )
        
    def commitcocomo ( self , window , KDSI , a , b , F ):
        if KDSI == '' or a == '' or b == '' or F == '':
            return

        windowshow = tkinter.Toplevel ( window )

        Effort = float(a) * int(KDSI) ** float(b) * float ( F )
        textEffort = tkinter.Label ( windowshow , text = '????????????' + str(Effort) )
        textEffort.grid ( row = 0 , column = 0 )

        buttonok = tkinter.Button ( windowshow , text = '??????' , command = lambda:self.closewindow(window,windowshow) )
        buttonok.grid ( row = 100 , column = 0 )

        global estimation
        estimation.effort = Effort
        estimation.method = 'COCOMO 81'

    def cocomo ( self ):
        window = tkinter.Toplevel ( self.mainwindow )

        textKDSI = tkinter.Label ( window , text = '??????????????????' )
        texta = tkinter.Label ( window , text = '?????? a' )
        textb = tkinter.Label ( window , text = '?????? b' )
        textF = tkinter.Label ( window , text = '????????????' )
        
        entryKDSI = tkinter.Entry ( window )
        entrya = tkinter.Entry ( window )
        entryb = tkinter.Entry ( window )
        entryF = tkinter.Entry ( window )

        textKDSI.grid ( row = 1 , column = 0 )
        entryKDSI.grid ( row = 1 , column = 1 )
        texta.grid ( row = 2 , column = 0 )
        entrya.grid ( row = 2 , column = 1 )
        textb.grid ( row = 3 , column = 0 )
        entryb.grid ( row = 3 , column = 1 )
        textF.grid ( row = 4 , column = 0 )
        entryF.grid ( row = 4 , column = 1 )

        buttonok = tkinter.Button ( window , text = '??????' , command = lambda:self.commitcocomo(window,entryKDSI.get(),entrya.get(),entryb.get(),entryF.get()) )
        buttoncancel = tkinter.Button ( window , text = '??????' , command = window.destroy )
        buttoncancel.grid ( row = 100 , column = 0 )
        buttonok.grid ( row = 100 , column = 1 )

    def commitanalog ( self , window , entry ):
        for i in range ( 1 , 5 ):
            for j in range ( 6 ):
                if entry[i][j].get () == '' and not ( i == 1 and j == 5 ):
                    return

        parameter = []

        for i in range ( 1 , 5 ):
            now = []
            for j in range ( 6 ):
                now.append ( entry[i][j].get () )
            parameter.append ( now )

        dis = [ 0.0 for i in range ( 4 ) ]
        print ( parameter )
        for i in range ( 1 , 4 ):
            for j in range ( 1 , 3 ):
                if parameter[0][j] != parameter[i][j]:
                    dis[i] += 1
        for j in range ( 3 , 5 ):
            mn = 999999999
            mx = -1
            for i in range ( 4 ):
                mn = min ( mn , int(parameter[i][j]) )
                mx = max ( mx , int(parameter[i][j]) )
            for i in range ( 1 , 4 ):
                dis[i] += ( (int(parameter[0][j])-int(parameter[i][j])) / (mx-mn) ) ** 2

        mn = 999999999
        mi = 0
        for i in range ( 1 , 4 ):
            if dis[i] < mn:
                mn = dis[i]
                mi = i
        
        windowshow = tkinter.Toplevel ( window )
        
        textsimilar = tkinter.Label ( windowshow , text = '????????????????????????' + parameter[mi][0] )
        textEffort = tkinter.Label ( windowshow , text = '?????????????????????' + parameter[mi][5] )
        textsimilar.grid ( row = 0 , column = 0 )
        textEffort.grid ( row = 1 , column = 0 )

        buttonok = tkinter.Button ( windowshow , text = '??????' , command = lambda:self.closewindow(window,windowshow) )
        buttonok.grid ( row = 100 , column = 0 )

        global estimation
        estimation.effort = float (parameter[mi][5])
        estimation.method = '?????????'


    def analog ( self ):
        window = tkinter.Toplevel ( self.mainwindow )
        
        colsize = 6
        colname = ['?????????','????????????','????????????','????????????','????????????','?????????']
        entry = [ [ 0 for i in range (colsize)] for j in range ( 5 ) ]

        for i in range ( 5 ):
            for j in range ( colsize ):
                entry[i][j] = tkinter.Entry ( window )
                entry[i][j].grid ( row = i , column = j )
                if i == 0 or ( i == 1 and j == colsize - 1 ):
                    if i == 0 :
                        entry[i][j].insert ( 0 , colname[j] )
                    entry[i][j].config ( state = 'disable' )
        
        buttonok = tkinter.Button ( window , text = '??????' , command = lambda:self.commitanalog(window,entry) )
        buttoncancel = tkinter.Button ( window , text = '??????' , command = window.destroy )
        buttoncancel.grid ( row = 100 , column = 0 )
        buttonok.grid ( row = 100 , column = 1 )

    def initwork ( self ):
        stageid = 2

        buttoncocomo = tkinter.Button ( self.stage[stageid] , text = 'COCOMO 81' , command = self.cocomo )
        buttonanalog = tkinter.Button ( self.stage[stageid] , text = '?????????' , command = self.analog )
        
        buttoncocomo.grid ( row = 1 , column = 1 )
        buttonanalog.grid ( row = 1 , column = 2 )
        
        self.pbar[stageid].grid ( row = 0, column = 0, columnspan = 4 )
        self.stagebut[stageid][0].grid ( row = 4 ,  column = 1 )
        self.stagebut[stageid][1].grid ( row = 4 ,  column = 2 )

    def commitcost ( self , window , CF ):
        if CF == '':
            return

        windowshow = tkinter.Toplevel ( window )

        global estimation

        cost = float(CF) * estimation.effort
        textEffort = tkinter.Label ( windowshow , text = '???????????????' + str(cost) )
        textEffort.grid ( row = 0 , column = 0 )

        buttonok = tkinter.Button ( windowshow , text = '??????' , command = lambda:self.closewindow(window,windowshow) )
        buttonok.grid ( row = 100 , column = 0 )

        estimation.CF = CF
        estimation.cost = cost


    def cost ( self ):
        global estimation
        if estimation.effort == -1:
            window = tkinter.Toplevel ( self.mainwindow )

            texterror = tkinter.Label ( window , text = '???????????????????????????' )
            texterror.grid ( row = 0 , column = 0 )
            buttonok = tkinter.Button ( window , text = '??????' , command = window.destroy )
            buttonok.grid ( row = 100 , column = 0 )

            return

        window = tkinter.Toplevel ( self.mainwindow )
        
        textCF = tkinter.Label ( window , text = '????????????' )
        entryCF = tkinter.Entry ( window )

        textCF.grid ( row = 0 , column = 0 )
        entryCF.grid ( row = 0 , column = 1 )
        
        buttonok = tkinter.Button ( window , text = '??????' , command = lambda:self.commitcost(window,entryCF.get()) )
        buttoncancel = tkinter.Button ( window , text = '??????' , command = window.destroy )
        buttoncancel.grid ( row = 100 , column = 0 )
        buttonok.grid ( row = 100 , column = 1 )

    def initcost ( self ):
        stageid = 3

        buttoncost = tkinter.Button ( self.stage[stageid] , text = '????????????' , command = self.cost )
        
        self.pbar[stageid].grid ( row = 0, column = 0, columnspan = 5 )
        self.stagebut[stageid][0].grid ( row = 3 ,  column = 1 )
        self.stagebut[stageid][1].grid ( row = 3 ,  column = 3 )
        buttoncost.grid ( row = 1 , column = 2 )

    def export ( self ):
        book = xlwt.Workbook ()
        sheet = book.add_sheet ( 'report' )

        sheet.write ( 0 , 0 , '????????????' )
        
        global estimation
        row = 3
        col = 0
        flag = 0

        if hasattr ( estimation , 'codeline' ) or hasattr ( estimation , 'FP' ) or hasattr ( estimation , 'UP' ) or hasattr ( estimation , 'UCP' ):
            sheet.write ( 2 , 0 , '????????????' )

        if hasattr ( estimation , 'codeline' ):
            sheet.write ( row , col , '???????????????' )
            sheet.write ( row + 1 , col , '???????????????' )
            sheet.write ( row + 1 , col + 1 , estimation.codeline )
            col += 3
            flag = 1
        
        if hasattr ( estimation , 'FP' ):
            sheet.write ( row , col , '???????????????' )
            sheet.write ( row + 1 , col , '?????????????????????' )
            sheet.write ( row + 1 , col + 1 , estimation.UFP )
            sheet.write ( row + 2 , col , '???????????????' )
            sheet.write ( row + 2 , col + 1 , estimation.VAF )
            sheet.write ( row + 3 , col , '????????????' )
            sheet.write ( row + 3 , col + 1 , estimation.FP )
            col += 3
            flag = 1
            
        if hasattr ( estimation , 'OP' ):
            sheet.write ( row , col , '???????????????' )
            sheet.write ( row + 1 , col , '??????????????????' )
            sheet.write ( row + 1 , col + 1 , estimation.UOP )
            sheet.write ( row + 2 , col , '??????????????????' )
            sheet.write ( row + 2 , col + 1 , estimation.R )
            sheet.write ( row + 3 , col , '????????????' )
            sheet.write ( row + 3 , col + 1 , estimation.OP )
            col += 3
            flag = 1

        if hasattr ( estimation , 'UCP' ):
            sheet.write ( row , col , '???????????????' )
            sheet.write ( row + 1 , col , '?????????????????????' )
            sheet.write ( row + 1 , col + 1 , estimation.UUCP )
            sheet.write ( row + 2 , col , '????????????????????????' )
            sheet.write ( row + 2 , col + 1 , estimation.TCF )
            sheet.write ( row + 3 , col , '????????????????????????' )
            sheet.write ( row + 3 , col + 1 , estimation.ECF )
            sheet.write ( row + 4 , col , '??????????????????' )
            sheet.write ( row + 4 , col + 1 , estimation.PF )
            sheet.write ( row + 5 , col , '????????????' )
            sheet.write ( row + 5 , col + 1 , estimation.UCP )
            sheet.write ( row + 6 , col , '????????????' )
            sheet.write ( row + 6 , col + 1 , estimation.Effort )
            col += 3
            flag = 1

        if flag == 1:
            row += 8

        if hasattr ( estimation , 'method' ):
            sheet.write ( row , 0 , '???????????????' )
            sheet.write ( row + 1 , 0 , '??????' + estimation.method + '????????????' )
            sheet.write ( row + 2 , 0 , '????????????' )
            sheet.write ( row + 2 , 1 , estimation.effort )
            row += 4

        if hasattr ( estimation , 'cost' ):
            sheet.write ( row , 0 , '????????????' )
            sheet.write ( row + 1 , 0 , '???????????????' )
            sheet.write ( row + 1 , 1 , estimation.CF )
            sheet.write ( row + 2 , 0 , '???????????????' )
            sheet.write ( row + 2 , 1 , estimation.cost )

        book.save ( 'report.xls' )

    def initexport ( self ):
        stageid = 4

        buttoncost = tkinter.Button ( self.stage[stageid] , text = '????????????' , command = self.export )
        self.pbar[stageid].grid ( row = 0, column = 0, columnspan = 3 )
        
        buttoncost.grid ( row = 1 , column = 1 )


    def __init__ (self):
        self.mainwindow = tkinter.Tk()
        self.mainwindow.title ( 'FudanSCETool' )
        ws = self.mainwindow.winfo_screenwidth()
        hs = self.mainwindow.winfo_screenheight()
        w = 375
        h = 150
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.mainwindow.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.stagenumber = 5

        self.stage = [ 0 for i in range (self.stagenumber) ]
        self.stagebut = [ 0 for i in range (self.stagenumber) ]
        self.pbar = [ 0 for i in range (self.stagenumber) ]
        self.nowstage = 0
        self.padding = tkinter.Label ( self.mainwindow , text = ' ' )
        
        for i in range ( self.stagenumber ):
            s = ttk.Style()
            s.configure('TLabelframe.Label', foreground='blue')
            self.stage[i] = ttk.LabelFrame ( self.mainwindow, text = 'Stage ' + str(i), width=w-10,height=h-10,)
            self.stage[i].grid_propagate(0)
            # self.stage[i].grid_columnconfigure(1, minsize=2, weight = 1)
            # self.stage[i].grid_columnconfigure(2, minsize=200, weight = 1)
            # self.stage[i].grid_columnconfigure(3, minsize=200, weight = 1)
            # self.stage[i].grid_columnconfigure(4, minsize=200, weight = 1)
            # self.stage[i].grid_rowconfigure(1, minsize=5, weight = 1)
            # self.stage[i].grid_rowconfigure(2, minsize=5, weight = 1)
            # self.stage[i].grid_rowconfigure(3, minsize=5, weight = 1)
            self.stagebut[i] = [tkinter.Button(self.stage[i],command = lambda:self.setstage(self.nowstage-1) ),
                                tkinter.Button(self.stage[i],command = lambda:self.setstage(self.nowstage+1) )]
            self.stagebut[i][0].config ( text = 'Back' )
            self.stagebut[i][1].config ( text = 'Next' )
            
            self.pbar[i] = Progressbar(self.stage[i], length=w, style='black.Horizontal.TProgressbar')
            self.pbar[i]['value'] = 100 * (i + 1) / self.stagenumber
            
        self.stage[self.nowstage].grid ( row = 0 , column = 0 )

        self.initlogin ()
        self.initscale ()
        self.initwork ()
        self.initcost ()
        self.initexport ()

if __name__ == '__main__' :
    initbackend ()

    mw = mywindow ()

    mw.mainwindow.mainloop ()