from truecallerpy import search_phonenumber

def search(user_number):
	phone_email=""
	id = "a1i0i--cZbrxwVEFlUzHgOoZao-BD0og4Z5eajg7BSZA2VQycbi-i5jIC6cR0wZz"
	try:
		response = (search_phonenumber(user_number,"IN", id))
		try:
			data = response["data"][0]
			phone_name = data["name"]
			print("Name - ",data["name"])
			data2 = data["phones"][0]
			phone_carrier = data2['carrier']
			print("Carrier - ",data2['carrier'])
			try:
				nothing3 = data["internetAddresses"]
				nothing4 = nothing3[0]
				phone_email = nothing4['id']
				print(phone_email)
			except:
				phone_email = ""
		except:
			phone_name = "Not on Truecaller"
			phone_carrier = "Not on Truecaller"

		final = [phone_name,phone_carrier,phone_email]
		return final
	except Exception as e:
		print(e)
		phone_name = "An error occured"
		phone_carrier = "Check if the no. is correct"
		phone_email = ""
		final = [phone_name,phone_carrier,phone_email]
		return final
