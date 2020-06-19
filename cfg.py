thread=True
receiving=False

serial=0

objfilename="m4.obj"


numberoflines=3
datainterval=250

maxy = 1000
miny = 0

screenwidthdpi=120
screenheightdpi=107


plotnames = ['Acceleration','Altitude    ','Speed       ', 'IDK', 'ok', 'Speed', 'ok', 'ok' ]
pltInterval = 500
datanames = ['Speed','Acceleration','Distance', 'Direction','Health']
speedata = ['Max', 'Current', 'Vertical', 'Ground']
accelerationdara = ['Max', 'Current', 'Vertical', 'Ground']
altitudedata = ['Apogee', 'Current','Vertical', 'Ground']
directiondata = ['Roll', 'Pitch', 'Yaw','Stable']
healthdata = ['Coms','Temp1', 'Temp2','Parachute']

data =[speedata,accelerationdara,altitudedata,directiondata,healthdata]

eventswidth=15
eventsheigh=5
mainlabelheight=1
dataspecificwidth=8

listofevents = ['Ignition', 'Launch', 'Thrust', 'Free flight', 'Apogee', 'Descend','Parachute', 'Descend', 'Landing']