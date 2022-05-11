import swisseph as swe
import streamlit as st
import pandas as pd
import datetime
from geopy.geocoders import Nominatim
import random
import string

swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)

zodiac = {0:'Aries', 1:'Taurus', 2:'Gemini', 3:'Cancer', 4:'Leo', 5:'Virgo', 6:'Libra', 7:'Scorpius', 8:'Sagittarius', 9:'Capricorn', 10:'Aquarius', 11:'Pisces'}
nakshatra = {0:'Ashwini', 1:'Bharani', 2:'Krittika', 3:'Rohini', 4:'Mrigshirsha', 5:'Ardra', 6:'Punarvasu', 7:'Pushya', 8:'Ashlesha', 9:'Magha', 10:'Purvaphalguni', 11:'Uttaraphalguni', 12:'Hasta', 13:'Chitra', 14:'Swati', 15:'Vishakha', 16:'Anuradha', 17:'Jyeshtha', 18:'Mula', 19:'Purvashadha', 20:'Uttarashadha', 21:'Shravana', 22:'Dhanishtha', 23:'Shatbhisha', 24:'Poorvabhadrapada', 25:'Uttarabhadrapada', 26:'Revati'}
zodiac_lord = {'Aries':'Mars', 'Taurus':'Venus', 'Gemini':'Mercury', 'Cancer':'Moon', 'Leo':'Sun', 'Virgo':'Mercury', 'Libra':'Venus', 'Scorpius':'Mars', 'Sagittarius':'Jupiter', 'Capricorn':'Saturn', 'Aquarius':'Saturn', 'Pisces':'Jupiter', }
nakshatra_lord = {'Ashwini':'Ketu', 'Bharani':'Venus', 'Krittika':'Sun', 'Rohini':'Moon', 'Mrigshirsha':'Mars', 'Ardra':'Rahu', 'Punarvasu':'Jupiter', 'Pushya':'Saturn', 'Ashlesha':'Mercury', 'Magha':'Ketu', 'Purvaphalguni':'Venus', 'Uttaraphalguni':'Sun', 'Hasta':'Moon', 'Chitra':'Mars', 'Swati':'Rahu', 'Vishakha':'Jupiter', 'Anuradha':'Saturn', 'Jyeshtha':'Mercury', 'Mula':'Ketu', 'Purvashadha':'Venus', 'Uttarashadha':'Sun', 'Shravana':'Moon', 'Dhanishtha':'Mars', 'Shatbhisha':'Rahu', 'Poorvabhadrapada':'Jupiter', 'Uttarabhadrapada':'Saturn', 'Revati':'Mercury', }
sublord = {'Ketu':7, 'Venus':20, 'Sun':6, 'Moon':10, 'Mars':7, 'Rahu':18, 'Jupiter':16, 'Saturn':19, 'Mercury':17}
def local_time_to_jd(year, month, day, hour, minutes, seconds, timezone):
    y, m, d, h, mnt, s = swe.utc_time_zone(year, month, day, hour, minutes, seconds, timezone)
    return swe.utc_to_jd(y, m, d, h, mnt, s, flag = swe.GREG_CAL)[1]
def decdeg2dms(dd):
   is_positive = dd >= 0
   dd = abs(dd)
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return ':'.join([str(int(degrees)),str(int(minutes)),str(int(seconds))])
def rasi(p):
    return zodiac[int(p/30)]
def rasi_lord(p):
    return zodiac_lord[p]
def nakshatra_(p):
    return nakshatra[int(p*27/360)]
def nakshatra_lord_(p):
    return nakshatra_lord[p]
def sub_lord_(p):
    s = nakshatra_(p)
    r = p % (360/27)
    pl_name = list(sublord.keys())
    pl = pl_name.index(nakshatra_lord_(s))
    subs = list(sublord.values())
    a = len(sublord)
    bt = (360/27)/120
    hi = 0.0
    for i in range(a):
        hi = hi + subs[(i+pl)%a] * bt
        if r < hi:
            return pl_name[(i+pl)%a]
def planet_house(p, jd, lat, lon):
    houses= swe.houses_ex(jd, lat, lon, hsys = b'P',flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0]
    for i in range(12):
        if houses[i] < houses[(i+1) % 11]:
            if houses[i] < p and p < houses[(i+1) % 11]:
                return i+1
        if houses[i] > houses[(i+1) % 11]:
            if houses[i] < p or p < houses[(i+1) % 11]:
                return i+1
def aspects(p1,p2):
    angle = swe.difdeg2n(p1,p2)
    deviation = 4
    if angle < deviation and p1!=p2 and angle>0:
        return '0'
    elif angle < (30+deviation) and angle > (30-deviation):
        return '30'
    elif angle < (45+deviation) and angle > (45-deviation):
        return '45'
    elif angle < (60+deviation) and angle > (60-deviation):
        return '60'
    elif angle < (90+deviation) and angle > (90-deviation):
        return '90'
    elif angle < (120+deviation) and angle > (120-deviation):
        return '120'
    elif angle < (135+deviation) and angle > (135-deviation):
        return '135'
    elif angle < (150+deviation) and angle > (150-deviation):
        return '150'
    elif angle < (180+deviation) and angle > (180-deviation):
        return '180'
    else:
        return ''
    
def planets(jd, lat, lon):
    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    sun = swe.calc_ut(jd, swe.SUN, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    moon = swe.calc_ut(jd, swe.MOON, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    mercury = swe.calc_ut(jd, swe.MERCURY, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    venus = swe.calc_ut(jd, swe.VENUS, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    mars = swe.calc_ut(jd, swe.MARS, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    jupiter = swe.calc_ut(jd, swe.JUPITER, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    saturn = swe.calc_ut(jd, swe.SATURN, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    rahu = swe.calc_ut(jd, swe.MEAN_NODE, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    ketu = (swe.calc_ut(jd, swe.MEAN_NODE, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0] + 180) % 360
    planets = {'Sun':sun, 'Moon':moon, 'Mercury':mercury, 'Venus':venus, 'Mars':mars, 'Jupiter':jupiter, 'Saturn':saturn, 'Rahu':rahu, 'Ketu':ketu}
    planet_list = []
    for pl in planets:
        p = planets[pl]
        planet_list.append([pl,
                           planet_house(p, jd, lat, lon),
                           rasi(p),
                           decdeg2dms(p%30),
                           rasi_lord(rasi(p)),
                           nakshatra_(p),
                           nakshatra_lord_(nakshatra_(p)),
                           sub_lord_(p)
        ])
    return planet_list

def houses(jd, lat, lon):
    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    houses, ascmc = swe.houses_ex(jd, lat, lon,hsys = b'P',flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)
    i = 0
    house_list = []
    for f in houses:
        i += 1
        house_list.append([str(i),
                          rasi(f),
                          decdeg2dms(f%30),
                          rasi_lord(rasi(f)),  
                          nakshatra_(f),
                          nakshatra_lord_(nakshatra_(f)),
                          sub_lord_(f)
        ])
    return house_list
def aspects_planets2planets(jd):
    sun = swe.calc_ut(jd, swe.SUN, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    moon = swe.calc_ut(jd, swe.MOON, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    mercury = swe.calc_ut(jd, swe.MERCURY, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    venus = swe.calc_ut(jd, swe.VENUS, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    mars = swe.calc_ut(jd, swe.MARS, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    jupiter = swe.calc_ut(jd, swe.JUPITER, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    saturn = swe.calc_ut(jd, swe.SATURN, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    rahu = swe.calc_ut(jd, swe.MEAN_NODE, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    ketu = (swe.calc_ut(jd, swe.MEAN_NODE, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0] + 180) % 360
    planets = {'Sun':sun, 'Moon':moon, 'Mercury':mercury, 'Venus':venus, 'Mars':mars, 'Jupiter':jupiter, 'Saturn':saturn, 'Rahu':rahu, 'Ketu':ketu}
    table = []
    for h in planets:
        ht = []
        for p in planets:
            ht.append(aspects(planets[h],planets[p]))
        table.append(ht)
    return table
def aspects_planets2houses(jd, lat, lon):
    houses, ascmc = swe.houses_ex(jd, lat, lon, hsys = b'P',flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)
    sun = swe.calc_ut(jd, swe.SUN, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    moon = swe.calc_ut(jd, swe.MOON, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    mercury = swe.calc_ut(jd, swe.MERCURY, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    venus = swe.calc_ut(jd, swe.VENUS, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    mars = swe.calc_ut(jd, swe.MARS, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    jupiter = swe.calc_ut(jd, swe.JUPITER, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    saturn = swe.calc_ut(jd, swe.SATURN, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    rahu = swe.calc_ut(jd, swe.MEAN_NODE, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
    ketu = (swe.calc_ut(jd, swe.MEAN_NODE, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0] + 180) % 360
    planets = {'Sun':sun, 'Moon':moon, 'Mercury':mercury, 'Venus':venus, 'Mars':mars, 'Jupiter':jupiter, 'Saturn':saturn, 'Rahu':rahu, 'Ketu':ketu}
    table = []
    for h in houses:
        ht = []
        for p in planets:
            ht.append(aspects(h,planets[p]))
        table.append(ht)
    return table

def time_period(inp, tz):
    t1, t2, lord = inp.split('\n')
    t1 = t1.split('-')
    t2 = t2.split('-')
    t1 = local_time_to_jd(int(t1[0]), int(t1[1]), int(t1[2]), 0, 0, 0, timezone = tz)
    t2 = local_time_to_jd(int(t2[0]), int(t2[1]), int(t2[2]), 0, 0, 0, timezone = tz)
    pl_name = list(sublord.keys())
    subs = list(sublord.values())
    a = len(sublord)
    tp = (t2-t1)/120
    pl=pl_name.index(lord)
    hi = t1
    out = []
    for j in range(a):
        lw = hi
        hi = hi + subs[(j+pl)%a] * tp
        lord1 = pl_name[(j+pl)%a]
        out.append('\n'.join(['-'.join(map(str, swe.revjul(lw)[0:3])),
                    '-'.join(map(str, swe.revjul(hi)[0:3])),
                    lord1]))
    return out

st.set_page_config(
        page_title="Horoscope",
        page_icon="🖖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

d = st.sidebar.date_input("When's your birthday", datetime.date(1995, 9, 27), datetime.date(1901, 1, 1), datetime.date(2100, 1, 1))
year = d.year
month = d.month
date = d.day
lat = float(st.sidebar.text_input('latitude', '21.9320'))
lon = float(st.sidebar.text_input('longitude', '86.7466'))
try:
    address = st.sidebar.text_input('City', 'Baripada')
    letters = string.ascii_lowercase
    a = ''.join(random.choice(letters) for i in range(10))

    geolocator = Nominatim(user_agent=a)
    location = geolocator.geocode(address)

    st.sidebar.caption('Latitude '+str(location.latitude))
    st.sidebar.caption('Longitude '+str(location.longitude))
    lat = location.latitude
    lon = location.longitude
except:
    pass
tz = st.sidebar.slider('time zone', -24.0, 24.0, 5.5, 0.5)
t = st.sidebar.title('When did you come to earth')
#hour = st.sidebar.slider('Hour', 0, 24, 23, 1)
#minutes = st.sidebar.slider('Minutes', 0, 59, 17, 1)
#seconds = st.sidebar.slider('Seconds', 0, 59, 0, 1)'''
hour = int(st.sidebar.text_input('Hour', 23))
minutes = int(st.sidebar.text_input('Minutes',17))
seconds = int(st.sidebar.text_input('Seconds',0))

jd = local_time_to_jd(year, month, date, hour, minutes, seconds, timezone = tz)
df1 = pd.DataFrame(planets(jd, lat, lon), columns = ['PLANETS','HOUSES','RASI','DEGREES', 'RASI LORD', 'NAKSHATRA', 'NAKSHATRA LORD', 'SUB LORD'])
col1, col2 = st.columns(2)

col1.subheader('Bhaba Chart')
hous, asm = swe.houses_ex(jd, lat, lon, hsys = b'P',flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)

h = []
for a in hous:
    h.append(str(int(a/30)+1) +' ' + ' '.join([x[:2] for x in df1[df1['HOUSES'] == hous.index(a)+1]['PLANETS'].values]))

col1.markdown('''<svg height="250" width="250">
  <line x1="0%" y1="0%" x2="100%" y2="100%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="100%" y1="0%" x2="0%" y2="100%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="50%" y1="0%" x2="0%" y2="50%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="0%" y1="50%" x2="50%" y2="100%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="50%" y1="100%" x2="100%" y2="50%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="50%" y1="0%" x2="100%" y2="50%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="0%" y1="0%" x2="0%" y2="100%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="0%" y1="0%" x2="100%" y2="0%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="100%" y1="0%" x2="100%" y2="100%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="0%" y1="100%" x2="100%" y2="100%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <text x="50%" y="25%"  font-size="80%"  text-anchor="middle">''' + h[0] + '''</text>
  <text x="22.5%" y="10%"  font-size="80%"  text-anchor="middle">''' + h[1] +'''</text>
  <text x="10%" y="25%"  font-size="80%"  text-anchor="middle">''' + h[2] + '''</text>
  <text x="25%" y="50%"  font-size="80%"  text-anchor="middle">''' + h[3] + '''</text>
  <text x="10%" y="75%"  font-size="80%"  text-anchor="middle">''' + h[4] + '''</text>
  <text x="25%" y="87.5%"  font-size="80%"  text-anchor="middle">''' + h[5] + '''</text>
  <text x="50%" y="75%"  font-size="80%"  text-anchor="middle">''' + h[6] + '''</text>
  <text x="75%" y="87.5%"  font-size="80%"  text-anchor="middle">''' + h[7] + '''</text>
  <text x="87.5%" y="75%"  font-size="80%"  text-anchor="middle">''' + h[8] + '''</text>
  <text x="75%" y="50%"  font-size="80%"  text-anchor="middle">''' + h[9] + '''</text>
  <text x="87.5%" y="25%"  font-size="80%"  text-anchor="middle">''' + h[10] + '''</text>
  <text x="75%" y="12.5%"  font-size="80%"  text-anchor="middle">''' + h[11] + '''</text>
</svg>''',unsafe_allow_html=True)

col2.subheader('Rasi Chart')
h = []
for a in hous:
    h.append(str(int(a/30)+1) +' ' + ' '.join([x[:2] for x in df1[df1['RASI'] == zodiac[int(a/30)]]['PLANETS'].values]))

col2.markdown('''<svg height="250" width="250">
  <line x1="0%" y1="0%" x2="100%" y2="100%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="100%" y1="0%" x2="0%" y2="100%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="50%" y1="0%" x2="0%" y2="50%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="0%" y1="50%" x2="50%" y2="100%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="50%" y1="100%" x2="100%" y2="50%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="50%" y1="0%" x2="100%" y2="50%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="0%" y1="0%" x2="0%" y2="100%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="0%" y1="0%" x2="100%" y2="0%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="100%" y1="0%" x2="100%" y2="100%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <line x1="0%" y1="100%" x2="100%" y2="100%" style="stroke:rgb(255,0,0);stroke-width:2" />
  <text x="50%" y="25%"  font-size="80%"  text-anchor="middle">''' + h[0] + '''</text>
  <text x="22.5%" y="10%"  font-size="80%"  text-anchor="middle">''' + h[1] +'''</text>
  <text x="10%" y="25%"  font-size="80%"  text-anchor="middle">''' + h[2] + '''</text>
  <text x="25%" y="50%"  font-size="80%"  text-anchor="middle">''' + h[3] + '''</text>
  <text x="10%" y="75%"  font-size="80%"  text-anchor="middle">''' + h[4] + '''</text>
  <text x="25%" y="87.5%"  font-size="80%"  text-anchor="middle">''' + h[5] + '''</text>
  <text x="50%" y="75%"  font-size="80%"  text-anchor="middle">''' + h[6] + '''</text>
  <text x="75%" y="87.5%"  font-size="80%"  text-anchor="middle">''' + h[7] + '''</text>
  <text x="87.5%" y="75%"  font-size="80%"  text-anchor="middle">''' + h[8] + '''</text>
  <text x="75%" y="50%"  font-size="80%"  text-anchor="middle">''' + h[9] + '''</text>
  <text x="87.5%" y="25%"  font-size="80%"  text-anchor="middle">''' + h[10] + '''</text>
  <text x="75%" y="12.5%"  font-size="80%"  text-anchor="middle">''' + h[11] + '''</text>
</svg>''',unsafe_allow_html=True)


st.subheader('Tables')


df2 = pd.DataFrame(houses(jd, lat, lon), columns = ['HOUSES','RASI','DEGREES','RASI LORD', 'NAKSHATRA', 'NAKSHATRA LORD', 'SUB LORD'])

df3 = pd.DataFrame(aspects_planets2houses(jd, lat, lon), columns = ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Rahu','Ketu'], index = range(1,13))

df4 = pd.DataFrame(aspects_planets2planets(jd), columns = ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Rahu','Ketu'], index = ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Rahu','Ketu'])



moon = swe.calc_ut(jd, swe.MOON, flag = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_SIDEREAL)[0][0]
lord = df1[df1["PLANETS"]=='Moon']["NAKSHATRA LORD"].values[0]

t1 = swe.revjul(jd + (sublord[lord])*365.2422*(1-((moon % (360/27))/(360/27))) - (sublord[lord])*365.2422)
t2 = swe.revjul(jd + (sublord[lord])*365.2422*(1-((moon % (360/27))/(360/27))) - (sublord[lord])*365.2422 + 120*365.2422)

#script
#script
def script_table():
    planets = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury' ]
    script_tab = []
    for planet in planets:
        source = planet+' '+str(df1[df1["PLANETS"]==planet]["HOUSES"].values[0])+'/'+','.join(df2[df2['RASI LORD']==planet]["HOUSES"].values)
        if planet == 'Rahu':
            source = planet+' '+str(df1[df1["PLANETS"]==planet]["HOUSES"].values[0])+'/'+','.join(df2[df2['RASI LORD']==df1[df1["PLANETS"]=='Rahu']["RASI LORD"].values[0]]["HOUSES"].values)
        
        if planet == 'Ketu':
            source = planet+' '+str(df1[df1["PLANETS"]==planet]["HOUSES"].values[0])+'/'+','.join(df2[df2['RASI LORD']==df1[df1["PLANETS"]=='Ketu']["RASI LORD"].values[0]]["HOUSES"].values)
        
        star_ = ''
        if planet not in df1['NAKSHATRA LORD'].values:
            star_ = 'no star'
        else:
            star_ = ''
        adtn_h = ''
        if star_ == 'no star':
            adtn_h = ','.join(df2[df2['RASI LORD']==planet]["HOUSES"].values)
        else:
            adtn_h = ''
        planet_nl = df1[df1["PLANETS"]==planet]['NAKSHATRA LORD'].values[0]
        result = planet_nl+' '+str(df1[df1["PLANETS"]==planet_nl]["HOUSES"].values[0])+'/'+','.join(df2[df2['RASI LORD']==planet_nl]["HOUSES"].values)
        if planet_nl == 'Rahu':
            result = planet_nl+' '+str(df1[df1["PLANETS"]==planet_nl]["HOUSES"].values[0])+'/'+','.join(df2[df2['RASI LORD']==df1[df1["PLANETS"]=='Ketu']["RASI LORD"].values[0]]["HOUSES"].values)
        
        if planet_nl == 'Ketu':
            result = planet_nl+' '+str(df1[df1["PLANETS"]==planet_nl]["HOUSES"].values[0])+'/'+','.join(df2[df2['RASI LORD']==df1[df1["PLANETS"]=='Ketu']["RASI LORD"].values[0]]["HOUSES"].values)
        
        planet_sl = df1[df1["PLANETS"]==planet]['SUB LORD'].values[0]
        verifier = planet_sl+' '+str(df1[df1["PLANETS"]==planet_sl]["HOUSES"].values[0])+'/'+','.join(df2[df2['RASI LORD']==planet_sl]["HOUSES"].values)
        if planet_sl == 'Rahu':
            verifier = planet_sl+' '+str(df1[df1["PLANETS"]==planet_sl]["HOUSES"].values[0])+'/'+','.join(df2[df2['RASI LORD']==df1[df1["PLANETS"]=='Rahu']["RASI LORD"].values[0]]["HOUSES"].values)
        
        if planet_sl == 'Ketu':
            verifier = planet_sl+' '+str(df1[df1["PLANETS"]==planet_sl]["HOUSES"].values[0])+'/'+','.join(df2[df2['RASI LORD']==df1[df1["PLANETS"]=='Rahu']["RASI LORD"].values[0]]["HOUSES"].values)
        
        planet_nl_sl = df1[df1["PLANETS"]==planet_nl]['SUB LORD'].values[0]
        result_verifier = planet_nl_sl+' '+str(df1[df1["PLANETS"]==planet_nl_sl]["HOUSES"].values[0])+'/'+','.join(df2[df2['RASI LORD']==planet_nl_sl]["HOUSES"].values)
        if planet_nl_sl == 'Rahu':
            result_verifier = planet_nl_sl+' '+str(df1[df1["PLANETS"]==planet_nl_sl]["HOUSES"].values[0])+'/'+','.join(df2[df2['RASI LORD']==df1[df1["PLANETS"]=='Rahu']["RASI LORD"].values[0]]["HOUSES"].values)
        
        if planet_nl_sl == 'Ketu':
            result_verifier = planet_nl_sl+' '+str(df1[df1["PLANETS"]==planet_nl_sl]["HOUSES"].values[0])+'/'+','.join(df2[df2['RASI LORD']==df1[df1["PLANETS"]=='Ketu']["RASI LORD"].values[0]]["HOUSES"].values)
        
        script_tab.append([planet,
                             source,
                             star_,
                             adtn_h,
                             result,
                             verifier,
                             result_verifier                            
        ])
    return script_tab

expander1 = st.expander("Script Table")
df5 = pd.DataFrame(script_table(), columns = ['Planet','Source','Star_','Additional House','Result','Verifier','result_verifier '])
expander1.dataframe(df5)
expander = st.expander("Reference Tables")
expander.subheader('Houses')
expander.table(df1)
expander.subheader('Planets')
expander.table(df2)
expander.subheader('Aspects Planet to Houses')
expander.table(df3)
expander.subheader('Aspects Planet to Planets')
expander.table(df4)
st.subheader('Timeline')
with st.expander("Maha Dasa lord"):
    mdl = st.selectbox(
        '',
        (time_period('\n'.join(['-'.join(map(str,t1[0:3])),'-'.join(map(str,t2[0:3])),lord]),tz)))
    lord=mdl.split('\n')[2]
    st.table(df1[df1["PLANETS"]==lord])
    st.table(df2[df2["RASI LORD"]==lord])
    st.table(df5[df5["Planet"]==lord])
    st.table(df3[lord].replace('', float('NaN'), regex = True).dropna())
    st.table(df4[lord].replace('', float('NaN'), regex = True).dropna())
with st.expander("Antar Dasa lord"):
    adl = st.selectbox(
        '',
        (time_period(mdl, tz)))
    lord=adl.split('\n')[2]
    st.table(df1[df1["PLANETS"]==lord])
    st.table(df2[df2["RASI LORD"]==lord])
    st.table(df5[df5["Planet"]==lord])
    st.table(df3[lord].replace('', float('NaN'), regex = True).dropna())
    st.table(df4[lord].replace('', float('NaN'), regex = True).dropna())
with st.expander("Pratyantar Dasa lord"):
    pdl = st.selectbox(
        '',
        (time_period(adl, tz)))
    lord=pdl.split('\n')[2]
    st.table(df1[df1["PLANETS"]==lord])
    st.table(df2[df2["RASI LORD"]==lord])
    st.table(df5[df5["Planet"]==lord])
    st.table(df3[lord].replace('', float('NaN'), regex = True).dropna())
    st.table(df4[lord].replace('', float('NaN'), regex = True).dropna())
