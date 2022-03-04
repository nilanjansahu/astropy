import swisseph as swe
import streamlit as st
import pandas as pd
import datetime
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
    angle = abs(swe.difdeg2n(p1,p2))
    deviation = 4
    if angle < deviation and p1!=p2:
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
    planets = {'sun':sun, 'moon':moon, 'mercury':mercury, 'venus':venus, 'mars':mars, 'jupiter':jupiter, 'saturn':saturn, 'rahu':rahu, 'ketu':ketu}
    planet_list = []
    for pl in planets:
        p = planets[pl]
        planet_list.append([pl,
                           planet_house(p, jd, lat, lon),
                           rasi(p), 
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
    planets = {'sun':sun, 'moon':moon, 'mercury':mercury, 'venus':venus, 'mars':mars, 'jupiter':jupiter, 'saturn':saturn, 'rahu':rahu, 'ketu':ketu}
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
    planets = {'sun':sun, 'moon':moon, 'mercury':mercury, 'venus':venus, 'mars':mars, 'jupiter':jupiter, 'saturn':saturn, 'rahu':rahu, 'ketu':ketu}
    table = []
    for h in houses:
        ht = []
        for p in planets:
            ht.append(aspects(h,planets[p]))
        table.append(ht)
    return table

def time_period(t1,t2, lord):
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
        out.append([lw, hi, lord1])
    return out

st.set_page_config(
        page_title="Horoscope",
        page_icon="🖖",
        
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


tz = st.sidebar.slider('time zone', -24.0, 24.0, 5.5, 0.5)
t = st.sidebar.title('When did you come to earth')
hour = st.sidebar.slider('Hour', 0, 24, 23, 1)
minutes = st.sidebar.slider('Minutes', 0, 59, 17, 1)
seconds = st.sidebar.slider('Seconds', 0, 59, 0, 1)

jd = local_time_to_jd(year, month, date, hour, minutes, seconds, timezone = tz)

df1 = pd.DataFrame(planets(jd, lat, lon), columns = ['PLANETS','HOUSES','RASI', 'RASI LORD', 'NAKSHATRA', 'NAKSHATRA LORD', 'SUB LORD'])
st.dataframe(df1)
df2 = pd.DataFrame(houses(jd, lat, lon), columns = ['HOUSES','RASI','RASI LORD', 'NAKSHATRA', 'NAKSHATRA LORD', 'SUB LORD'])
st.dataframe(df2)
df3 = pd.DataFrame(aspects_planets2houses(jd, lat, lon), columns = ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Rahu','Ketu'], index = range(1,13))
st.dataframe(df3)
df4 = pd.DataFrame(aspects_planets2planets(jd), columns = ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Rahu','Ketu'], index = ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Rahu','Ketu'])
st.dataframe(df4)
t2 = 2098
t1 = 1978
lord = 'Rahu'

mdl = st.selectbox(
     'Maha Dasa Lord',
     (time_period(t1, t2, lord)))

adl = st.selectbox(
     'Antar Dasa Lord',
     (time_period(mdl[0], mdl[1], mdl[2])))

pdl = st.selectbox(
     'Pratyantar Dasa Lord',
     (time_period(adl[0], adl[1], adl[2])))
