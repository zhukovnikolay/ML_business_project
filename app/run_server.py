import dill
import pandas as pd
import os
# import cloudpickle
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime


dill._dill._reverse_typemap['ClassType'] = type
# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)
	print(model)

modelpath = "/Users/nikolayzhukov/PycharmProjects/ML_business_project/app/models/model.dill"
#modelpath = "/app/app/models/model.dill"
load_model(modelpath)


@app.route("/", methods=["GET"])
def general():
	return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST"""


@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")
	# ensure an image was properly uploaded to our endpoint

	def if_in_req(request, field_name):
		if request[field_name]:
			return request[field_name]
		else:
			return 0

	if flask.request.method == "POST":
		request_json = flask.request.get_json()
		print(request_json)
		usd = if_in_req(request_json, 'USD course')
		com_long = if_in_req(request_json, 'Commitments Long-Term')
		com_short = if_in_req(request_json, 'Commitments Short-Term')
		earn = if_in_req(request_json, 'Earnings per share')
		ebitda = if_in_req(request_json, 'EBITDA')
		cb_rate = if_in_req(request_json, 'CB rate')
		frs_rate = if_in_req(request_json, 'FRS rate')
		nickel = if_in_req(request_json, 'Nickel close price, USD')
		copper = if_in_req(request_json, 'Copper close price, USD')
		palladium = if_in_req(request_json, 'Palladium close price, USD')
		platinum = if_in_req(request_json, 'Platinum close price, USD')
		mmvb = if_in_req(request_json, 'MMVB close')

		logger.info(f'{dt} Date: usd={usd}, com_long={com_long}, com_short={com_short}, earn={earn},'
					f'ebitda={ebitda}, cb_rate={cb_rate}, frs={frs_rate}, nickel={nickel}, copper={copper},'
					f'palladium={palladium}, platinum={platinum}, mmvb={mmvb}')
		try:
			preds = model.predict(pd.DataFrame({'USD course': [usd],
												'Commitments Long-Term': [com_long],
												'Commitments Short-Term': [com_short],
												'Earnings per share': [earn],
												'EBITDA': [ebitda],
												'CB rate': [cb_rate],
												'FRS rate': [frs_rate],
												'Nickel close price, USD': [nickel],
												'Copper close price, USD': [copper],
												'Palladium close price, USD': [palladium],
												'Platinum close price, USD': [platinum],
												'MMVB close': [mmvb]}))[0]
		except AttributeError as e:
			logger.warning(f'{dt} Exception: {str(e)}')
			data['predictions'] = str(e)
			data['success'] = False
			return flask.jsonify(data)

		data["predictions"] = preds
		# indicate that the request was a success
		data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server


if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
			"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 8180))
	app.run(host='0.0.0.0', debug=True, port=port)
