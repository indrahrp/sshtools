def fn(self):
  print "fn"
  return id(self), self, type(self)
 
def fnb(self):
	print "fnb"
	return id(self)
	
# Traditional Class Definition
class A_Class(object):
  def method_a(self):
    return id(self), self, type(self)
 
instance = A_Class()
 
# Modify the class and add fn as a method
setattr(A_Class, 'method_b', fn)
setattr(A_Class, 'method_a', fn)
 
# Call the traditionally defined method
instance.method_a()
# Call the dynamically added method
instance.method_b()

setattr(A_Class, 'method_a', fnb)
inst2= A_Class()
inst2.method_a()