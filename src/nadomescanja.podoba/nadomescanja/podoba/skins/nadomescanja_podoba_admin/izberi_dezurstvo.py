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
datum = form["datum"]
catalog = getToolByName(context, 'portal_catalog')

obj = catalog(portal_type = "dezurstvo", id = datum)

if obj:
  r.RESPONSE.redirect('/nadomescanja/nadomescanja-1/'+ datum)
else:
  dezurstvo_id = context['nadomescanja-1'].invokeFactory(
                type_name='dezurstvo',
                id=datum,
                title=datum                                      
            )
  dezurstvo = context['nadomescanja-1'][dezurstvo_id]
  
  workflow = getToolByName(dezurstvo, 'portal_workflow')
  workflow.doActionFor(dezurstvo, "publish", comment = "published programmatically")
  r.RESPONSE.redirect('/nadomescanja/nadomescanja-1/'+ datum + '/edit')

return printed    
