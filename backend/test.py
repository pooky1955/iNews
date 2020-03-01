from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
import numpy as np

model = Sequential()
model.add(Dense(4,activation="sigmoid",input_shape=(2,)))
model.add(Dense(1,activation="sigmoid"))
model.compile(loss="mse",optimizer="sgd")

X = np.array([[0,1],[1,0],[1,1],[0,0]])
Y = np.array([[1],[1],[0],[0]])
model.fit(X,Y,epochs=1000,verbose=0)
print("Finished training")

preds = model.predict(X)
print(f"Preds : {preds}")
print(f"True labels : {Y}")

