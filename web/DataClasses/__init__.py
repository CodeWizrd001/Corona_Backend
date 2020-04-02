from ..Utils import *

class User :
    def __init__(self,name="user",mail="a@b.com",password="pass",uid="0") :
        self.uname = name 
        self.umail = mail
        self.upass = hash(password)
        self.uid = uid
    def _dict(self) :
        return {"User":self.uname,"Email":self.umail}
    def __dict(self) :
        return {"User":self.uname,"Email":self.umail,"Passwprd":self.upass,"UserID":self.uid}

class Country :
    '''
    string cName        Country Name
    int tCases          Total Cases
    int nCases          New Cases
    int tDeaths         Total Deaths
    int nDeaths         New Deaths
    int tRec            Total Recovered 
    int aCases          Active Cases
    int sCrit           Serious / Critical
    float tCm           Total Cases/M
    float tDm           Total Deaths/M
    '''

    def __init__(self,C=None) :
        if C is None :
            self.cName = "Nowhere"
            self.tCases = 0
            self.nCases = 0
            self.tDeaths = 0
            self.nDeaths = 0
            self.tRec = 0
            self.aCases = 0
            self.sCrit = 0
            self.tCm = 0.0
            self.tDm = 0.0
        elif type(C) is list :
            self.cName = C[0]
            self.tCases = Numeric(C[1])
            self.nCases = Numeric(C[2])
            self.tDeaths = Numeric(C[3])
            self.nDeaths = Numeric(C[4])
            self.tRec = Numeric(C[5])
            self.aCases = Numeric(C[6])
            self.sCrit = Numeric(C[7])
            self.tCm = float(Numeric(C[8]))
            self.tDm = float(Numeric(C[9]))
        elif type(C) is dict :
            self.cName = C['CountryName']
            self.tCases = Numeric(C['TotalCases'])
            self.nCases = Numeric(C['NewCases'])
            self.tDeaths = Numeric(C['TotalDeaths'])
            self.nDeaths = Numeric(C['NewDeaths'])
            self.tRec = Numeric(C['TotalRecovered'])
            self.aCases = Numeric(C['ActiveCases'])
            self.sCrit = Numeric(C['SeriousCritical'])
            self.tCm = float(Numeric(C['CasesPM']))
            self.tDm = float(Numeric(C['DeathPM']))
    
    def _dict(self) :
        return {
            'CountryName':self.cName,
            'TotalCases':self.tCases,
            'NewCases':self.nCases,
            'TotalDeaths':self.tDeaths,
            'NewDeaths':self.nDeaths,
            'TotalRecovered':self.tRec,
            'ActiveCases':self.aCases,
            'SeriousCritical':self.sCrit,
            'CasesPM':self.tCm,
            'DeathPM':self.tDm
        }