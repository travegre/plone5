# -*- encoding: utf-8 -*-
## Script (Python) "oddaj_narocilo"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Add multiple items with multiple quantities to cart

from Products.CMFCore.utils import getToolByName

r = container.REQUEST
session = r.SESSION
form = r.form
catalog = getToolByName(context, 'portal_catalog')
oseba = False
od = ''
do = ''
try:
	izvoz1 = form["izvoz-1-izbira"]
	if izvoz1 == 'oddo':
		od = form["od"]
		do = form["do"]	
		if not (od and do):
			return r.RESPONSE.redirect('/nadomescanja')
except:
	izvoz1 = False
try:
	izvoz2 = form["izvoz-2-oseba"]
	oseba = form["izvoz-2-oseba"]
	izbira = form["izvoz-2-izbira"]
	if izbira == '':
		return r.RESPONSE.redirect('/nadomescanja')
	if izbira == 'oddo':
		od = form["od"]
		do = form["do"]	
		if not (od and do):
			return r.RESPONSE.redirect('/nadomescanja')
except:
	izvoz2 = False
	oseba = False



if izvoz1:
	mode = izvoz1
elif izvoz2:
	mode = izbira
else:
	return r.RESPONSE.redirect('/nadomescanja')

today = DateTime()
year = today.year()
month = today.month()
if month == 12:
	next_month_year = year + 1
	next_month = 1
else:
	next_month_year = year
	next_month = month + 1
if month == 1:
	prev_month_year = year - 1
	prev_month = 12
else:
	prev_month_year = year
	prev_month = month - 1

if mode == 'teden':
	first_day = today - today.dow() - 7
	last_day = today + (7 - today.dow()) - 7
elif mode == 'tedenplus2':
	first_day = today - today.dow()
	last_day = first_day + 14
elif mode == 'tekoci':
	first_day = DateTime('%s-%s-%s' % (year, month, '1'))
	last_day = DateTime('%s-%s-%s' % (next_month_year, next_month, '1')) - 1
elif mode == 'pretekli':
	first_day = DateTime('%s-%s-%s' % (prev_month_year, prev_month, '1'))
	last_day = DateTime('%s-%s-%s' % (year, month, '1')) - 1
elif mode == 'oddo':	
	if not (od and do):
		return r.RESPONSE.redirect('/nadomescanja')
	od_parts = od.split('.')
	do_parts = do.split('.')
	if len(od_parts) != 3 or len(do_parts) != 3:
		return r.RESPONSE.redirect('/nadomescanja')
	if not all(part.isdigit() for part in od_parts + do_parts):
		return r.RESPONSE.redirect('/nadomescanja')
	try:
		first_day = DateTime(od_parts[2] + '-' + od_parts[1] + '-' + od_parts[0])
		last_day = DateTime(do_parts[2] + '-' + do_parts[1] + '-' + do_parts[0])
	except:
		return r.RESPONSE.redirect('/nadomescanja')



dezurstvo_results = catalog(portal_type = "dezurstvo")
if not dezurstvo_results:
	return r.RESPONSE.redirect('/nadomescanja')
dezurstvo_obj = dezurstvo_results[0].getObject()
print(dezurstvo_obj.excel_export(first_day, last_day, oseba))

return printed
