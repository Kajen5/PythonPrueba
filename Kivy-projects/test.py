'''from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp

layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
# Make sure the height is such that there is something to scroll.
layout.bind(minimum_height=layout.setter('height'))
for i in range(100):
    btn = Button(text=str(i), size_hint_y=None, height=40)
    layout.add_widget(btn)
root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
root.add_widget(layout)

runTouchApp(root)'''



#These "asserts" using only for self-checking and not necessary for auto-testing
"""meses=[31,28,31,30,31,30,31,31,30,31,30,31]

def days_diff(dat1,dat2):
	days=0
	date1=[]
	date2=[]
	if dat1[2]>dat2[2]:
		date1=dat1
		date2=dat2
	else:
		date1=dat2
		date2=dat1
	days=abs(date1[2]-date2[2])
	for i in range(abs(date1[1]-date2[1])):
		mes=date2[1]+i
		if mes>12:
			mes-=12
		days+=meses[mes]
		if ((i==1)&(date1[0]%4==0)):
			days+=1
	days+=abs(date1[0]-date2[0])*365	
	days+=abs((date1[0]-date2[0])/4)
	print(days)
	return days"""


def clock_angle(time):
    
    hour = time.split(":")
    angle = ((int(hour[0])%12)/12)*360-((-int(hour[1]))+60*5.5)+360
    return abs(angle)%360


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    print (clock_angle("02:30"))# == 105, "02:30"
    print( clock_angle("13:42")) #== 159, "13:42"
    print (clock_angle("01:42")) #== 159, "01:42"
    print (clock_angle("01:43")) #== 153.5, "01:43"
    print (clock_angle("00:00")) #== 0, "Zero"
    print (clock_angle("12:01")) #== 5.5, "Little later"
    print (clock_angle("18:00")) #== 180, "Opposite"

    print("Now that you're finished, hit the 'Check' button to review your code and earn sweet rewards!")
