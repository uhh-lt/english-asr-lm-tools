import TTSTextNormalization.classification
import pickle

xgb_model_path = "TTSTextNormalization/models/xgb_sub5750_5c_4w_5f_v18_model.dat"
model = pickle.load(open(xgb_model_path, "rb"))

normalizer = TTSTextNormalization.classification.Test()

df = normalizer.predict(model, ["On", "22th November 1999", "the" ,"fastest", "swimmer", "was", "25 km/h", ".", "It", "was", "22:59",".", "CO2", "is", "bad", "!", "22th", "November", "1999"])
result = normalizer.convert(df)

result_str = ' '.join(result["cust_after"])

print(result_str)
