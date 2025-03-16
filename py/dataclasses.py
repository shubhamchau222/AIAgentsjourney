# creating a employee class
class employee:
	
	# init method or constructor
	def __init__(self, name, emp_id, age, city):
		
		# Instance Variable
		self.name = name
		self.emp_id = emp_id
		self.age = age
		self.city = city
	
	# magic function to return class object
	def __repr__(self):
		return ("employee (name={}, emp_id={}, age={}, city={} )"
				.format(self.name, self.emp_id, self.age, self.city))
	
	# magic function to return boolean
	def __eq__(self, check):
		return ((self.name, self.emp_id, self.age, self.city) ==
				((check.name, check.emp_id, check.age, check.city)))


# initialization the object
emp1 = employee("Satyam", "ksatyam858", 21, 'Patna')
emp2 = employee("Anurag", "au23", 28, 'Delhi')
emp3 = employee("Satyam", "ksatyam858", 21, 'Patna')

print("employee object are :")
print(emp1)
print(emp2)
print(emp3)

# printing new line
print()

# referring two object to check equality
print("Data in emp1 and emp2 are same? ", emp1 == emp2)
print("Data in emp1 and emp3 are same? ", emp1 == emp3)
