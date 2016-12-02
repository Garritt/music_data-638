from sklearn import linear_model
from sklearn import metrics, cross_validation
import pandas as pd

df = pd.DataFrame.from_csv("../../csv/training/dev_set.csv")

# Select only the last 4 attributes
features = list(df.columns[2:5])
targets = df['match'].tolist()

# Logisitic Regression 
log_reg = linear_model.LogisticRegression(C=1)
log_reg.fit(df[features], targets)

cv_pred = cross_validation.cross_val_predict(log_reg, df[features], targets, cv=10)

print("\n\n", metrics.accuracy_score(targets, cv_pred))
print("\n\n", metrics.classification_report(targets, cv_pred))


#Model was learned above, now apply to unknown data.
dTestFrame = pd.DataFrame.from_csv("../../csv/training/eval_set.csv")
#print(dTestFrame)
output = (log_reg.predict(dTestFrame[features]))
#print("output: ",output)
# Check golden labels 
g_labels = []
with open("../../csv/training/eval_set.csv", 'r') as f:
	for line in f:
		g_labels.append(line.split(",")[-1])
for i, val in enumerate(g_labels):
	g_labels[i] = val.replace("\n", "")
g_labels = g_labels[1:]

correct = 0
# Evaluate predictions
total = len(g_labels)
for i, val in enumerate(output):
	pred = int(val)
	true = int(g_labels[i])
	if pred is true:
		correct = correct + 1

print("Correct: " + str(correct))
print("N_accuracy: " + str(correct / total))

cv_pred_eval = cross_validation.cross_val_predict(log_reg, dTestFrame[features], dTestFrame['match'], cv=10)
print("\n\n", metrics.accuracy_score(dTestFrame['match'], cv_pred_eval))
print("\n\n", metrics.classification_report(dTestFrame['match'], cv_pred_eval))







