from sklearn.model_selection import cross_val_score
from pandas import DataFrame
import numpy
import os
import subprocess
from sklearn import tree
from sklearn import metrics, cross_validation


#Dev set to set up tree.
df = DataFrame.from_csv("../../csv/training/dev_set.csv")


#Sets the columns of the vectors we use for ML. Does not include ID column.
#id,atable_id,btable_id,sim_title,sim_artist,dif_year,match
#ID is ignored because DataFram.from_csv defaults to having the first column as the ID column. 
#atable_id, btable_id ignored in the following line. Match ignored in the following line because the 2:5 is inclusive:exclusive
features = list(df.columns[2:5])

#Build the tree. min_samples_split takes 20 vectors per sample. Seed for random num gen is 99
dt = tree.DecisionTreeClassifier(min_samples_split=20, random_state=99)

#Per vector, learn from the features | the match value of that vector.
t = dt.fit(df[features], df['match'])
# Cross validation metrics in 10 folds 
#cv_pred = cross_validation.cross_val_predict(t, df[features], df['match'], cv=10)
score = cross_validation.cross_val_score(t, df[features], df['match'], cv=10)
print("\n\nTRAIN cvs: ",numpy.mean(score))
#print("\n\n", metrics.accuracy_score(df['match'], cv_pred))
#print( metrics.classification_report(df['match'], cv_pred))
tree.export_graphviz(dt,out_file='../../csv/training/tree.dot',feature_names=features)


################### EVAL ###########################
#Model was learned above, now apply to unknown data.
dTestFrame = DataFrame.from_csv("../../csv/training/eval_set.csv")
#print(dTestFrame)
output = (t.predict(dTestFrame[features]))

#print("output: ",output)
# # Check golden labels 
# g_labels = []
# true_lines = []
# with open("../../csv/training/eval_set.csv", 'r') as f:
# 	for line in f:
# 		true_lines.append(line)
# 		g_labels.append(line.split(",")[-1])
# for i, val in enumerate(g_labels):
# 	g_labels[i] = val.replace("\n", "")
# g_labels_n = g_labels[1:]

# correct = 0
# # Evaluate predictions
# total = len(g_labels_n)
# for i, val in enumerate(output):
# 	pred = int(val)
# 	true = int(g_labels_n[i])
# 	#print(pred, " ", true)
# 	if pred is true:
# 		correct = correct + 1
# 	else:
# 		pass
# 		#print(pred," ", true)
# 		#print(true_lines[i])
# print("Correct: " + str(correct))
# print("N_accuracy: " + str(correct / total))

cv_eval = cross_validation.cross_val_score(t, dTestFrame[features], dTestFrame['match'], cv=10)
print("\nEVAL: cvs: ",numpy.mean(score),"\n\n")
#print("\n\n", metrics.accuracy_score(dTestFrame['match'], cv_pred_eval))
#print("\n\n", metrics.classification_report(dTestFrame['match'], cv_pred_eval))


