class Risk:


    def __init__(self, rated_current = 6.5, max_score = 11):
        self.rated_current =  rated_current
        self.max_score = max_score

    def current_scorer(self, xal):
    
        score = xal/self.rated_current

        if score <= 0.80:
            return 0 #normal reading
        elif score <=1:
            return 2 #warning
        else:
            return 3 #critical reading


    def voltage_scorer(self, xa):
        #the inverter itself regulates the voltage, and for this inverter 240V is the max
        if xa < 180 or xa > 240:
            return 2 # critical zone
        elif 220 <= xa <= 240:
            return 0 # safe zone
        elif 180 < xa >= 180:   
            return 1 # warning zone

    def temperature_scorer(self, xa):
        if xa < 40:
            return 0
        elif xa <= 45:
            return 1
        else:
            return 2

    def powerfactor_scorer(self,xa):
        if xa >= .90:
            return 0
        elif xa >= .79:
            return 1
        else:
            return 2 #either not functioning well or overfunctioning

    def frequency_scorer(self,xa):
        if 49.5 <= xa <= 50.5:
            return 0
        else:
            return 1


    def humidity_scorer(self,xa):
        if xa < 70:
            return 0
        else:
            return 1


    def risk_grouper(self,total):
        risk_score = total/self.max_score
        if risk_score == 0:
            return "Healthy"
        elif risk_score  <= 0.25:
            return "Low Risk"
        elif risk_score <= 0.55:
            return "Caution(Moderate Risk)"
        else:
            return "Critical"

    def risk_scorer(self, voltage,current, frequency,powerfactor,temperature,humidity):
        scores ={
            'voltage' : self.voltage_scorer(voltage),
            'current' : self.current_scorer(current),
            'frequency' : self.frequency_scorer(frequency),
            'powerfactor' : self.powerfactor_scorer(powerfactor),
            'temperature' : self.temperature_scorer(temperature),
            'humidity' : self.humidity_scorer(humidity)
        }

        total = sum(scores.values())
        risk_severity = self.risk_grouper(total)
        return {
            "risk_severity" : risk_severity}