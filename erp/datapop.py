import openpyxl
from main.models import slot
wb = openpyxl.load_workbook('media/tt.xlsx')
sheetlist = wb.get_sheet_names()
c=-1
course1 = ''
name1 = ''
teacher1 = ''
day1 = ''
hour1 = 0
stype1 = ''
room1 = 0
sec1 = 0

flag = 0
def dayhour(a,b):
	daydict = {'M':'0','T':'1','W':'2','Th':'3','F':'4','S':'5'}
	l1 = a.split()
	d1 = h1 =''
	d1 = ''.join(daydict[abc] for abc in l1)
	h1 = int(''.join(str(b).split()))
	return d1, h1	
for sh in sheetlist:
	sheet = wb.get_sheet_by_name(sh)
	for l in range(2,1200):
		c=c+1
		print(c)
		if sheet['H'+str(l)].value == None:
			break

		if str(sheet['A'+str(l)].value).split()[0]=="COM":
			pass
		elif str(sheet['K'+str(l)].value)!='None' and int(str(sheet['K'+str(l)].value).split()[0])>9:
			pass
		elif str(sheet['B'+str(l)].value) != 'None':
			s = slot(totalseats=5,availableseats=5)
			s.course = course1 = sheet['B'+str(l)].value
			s.name = name1 = sheet['C'+str(l)].value
			s.teacher = teacher1 = sheet['H'+str(l)].value
			s.sec = sec1 = int(sheet['G'+str(l)].value)
			flag = 0
			if sheet['I'+str(l)].value == None:
				s.stype = stype1 = 'PROJECT'
				s.room = room1 = 0
				s.day = day1 = ''
				s.hour = hour1 = 0
			else:
				s.stype = stype1 = ''
				s.room = room1 = int(sheet['I'+str(l)].value)
				s.day, s.hour = day1, hour1 = dayhour(sheet['J'+str(l)].value, sheet['K'+str(l)].value)
			s.save()
		elif sheet['C'+str(l)].value!=None and sheet['B'+str(l)].value==None:
			s = slot()
			s.totalseats = 5
			s.availableseats = 5			
			s.course = course1
			s.name = name1
			s.teacher = teacher1 = sheet['H'+str(l)].value
			s.stype = stype1 = sheet['C'+str(l)].value
			s.day, s.hour = day1, hour1 = dayhour(sheet['J'+str(l)].value, sheet['K'+str(l)].value)
			s.room = room1 = int(sheet['I'+str(l)].value)
			if sheet['G'+str(l)].value==None:
				s.sec = sec1 = 1
			else:
				s.sec = sec1 = sheet['G'+str(l)].value
			s.save()
		elif sheet['C'+str(l)].value==None and sheet['G'+str(l)].value==None:
			s = slot.objects.get(course=course1,name=name1,sec=sec1,stype=stype1)
			s.teacher = s.teacher + '/ ' + sheet['H'+str(l)].value
			s.save()
		elif sheet['C'+str(l)].value==None and sheet['G'+str(l)].value!=None:
			s = slot()
			s.totalseats = 5
			s.availableseats = 5			
			s.course = course1
			s.name = name1
			s.teacher = teacher1 = sheet['H'+str(l)].value
			s.stype = stype1
			s.day, s.hour = day1, hour1 = dayhour(sheet['J'+str(l)].value, sheet['K'+str(l)].value)
			s.room = room1 = int(sheet['I'+str(l)].value)
			s.sec = sec1 = sheet['G'+str(l)].value
			s.save()

