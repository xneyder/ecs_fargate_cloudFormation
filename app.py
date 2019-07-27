#Simple flask hello world app
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class SimpleClass(Resource):
	"""
		Simple class returns the hello world in a dict
	"""
	def get(self):
		return {'Hola': 'Daniel !!!'}

api.add_resource(SimpleClass, '/')

#entry point
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port='80')
