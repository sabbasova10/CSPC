import os
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, export_text

from sklearn.metrics import (confusion_matrix, accuracy_score,
precision_score, recall_score, f1_score, roc_auc_score, log_loss,
classification_report, ConfusionMatrixDisplay, RocCurveDisplay)

from sklearn.inspection import permutation_importance

os.makedirs("results", exist_ok=True)

# A2
df = pd.read_csv("data/concrete.csv")

print(f"Duplicate rows: {df.duplicated().sum()}")

df = df.drop_duplicates().reset_index(drop=True)

print(f"Empty values: {df.isna().sum()}")
print(f"Duplicate rows: {df.duplicated().sum()}")
print(f"\n{df.describe()}")

X = df[["cement", "slag", "ash", "water", "superplastic",
"coarse_agg", "fine_agg", "age"]]
y = df["strength"]

r_cement, p_cement = pearsonr(X["cement"], y)
r_age, p_age = pearsonr(X["age"], y)
print(f"\nPearson r (cement vs strength): r = {r_cement:.4f}, p = {p_cement:.4e}")
print(f"Pearson r (age vs strength):    r = {r_age:.4f}, p = {p_age:.4e}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))
ax1.scatter(X["cement"], y, alpha=0.5)
ax1.set_xlabel("Cement (kg/m³)")
ax1.set_ylabel("Compressive Strength (MPa)")
ax1.set_title("Strength vs. Cement")

ax2.scatter(X["age"], y, alpha=0.5)
ax2.set_xlabel("Age (days)")
ax2.set_ylabel("Compressive Strength (MPa)")
ax2.set_title("Strength vs. Age")

plt.tight_layout()
plt.show()
fig.savefig("results/corelation.png")

# A3 
X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.2, random_state=42)

print(f"\nTraining set size: X={X_train.shape}, y={y_train.shape}")
print(f"Test set size:     X={X_test.shape}, y={y_test.shape}")

# A4
model = LinearRegression()
model.fit(X_train, y_train)

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

print(f"\nIntercept (beta_0): {model.intercept_:.4f} MPa")
print("Coefficients (beta_1 to beta_8):")
for col, coef in zip(X.columns, model.coef_):
    unit = "MPa / day" if col == "age" else "MPa / (kg/m^3)"
    print(f"  {col:14s}: {coef:+.4f} {unit}")

train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_mae = mean_absolute_error(y_test, y_test_pred)

train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

n_train, p = X_train.shape
train_r2_adj = 1 - (1 - train_r2) * ((n_train - 1) / (n_train - p - 1))

print("\n A4 Performance Metrics ")
print(f"Train RMSE:     {train_rmse:.3f} MPa")
print(f"Test RMSE:      {test_rmse:.3f} MPa")
print(f"Test MAE:       {test_mae:.3f} MPa")
print(f"Train R2:       {train_r2:.3f}")
print(f"Train Adj R2:   {train_r2_adj:.3f}")
print(f"Test R2:        {test_r2:.3f}")

residuals = y_test - y_test_pred

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(X_test["age"], residuals, alpha=0.6, edgecolors="k")
ax.set_xscale("log")
ax.axhline(0, color="red", linestyle="--", linewidth=1.5)
ax.set_xlabel("Age (days, log scale)")
ax.set_ylabel("Residuals (True - Predicted Strength, MPa)")
ax.set_title("Test Residuals vs. Age")

plt.tight_layout()
plt.show()
fig.savefig("results/linear_residuals.png")

# A5
n_train = X_train.shape[0]
degrees = [1, 2, 3, 4]
poly_rows = []
mse_train = []
mse_test = []

for d in degrees:
    poly = make_pipeline(
        PolynomialFeatures(degree=d, include_bias=False),
        StandardScaler(),
        LinearRegression(),
    )
    poly.fit(X_train, y_train)
    p = poly[0].n_output_features_

    y_train_pred = poly.predict(X_train)
    y_test_pred = poly.predict(X_test)

    mse_tr = mean_squared_error(y_train, y_train_pred)
    mse_te = mean_squared_error(y_test, y_test_pred)
    mse_train.append(mse_tr)
    mse_test.append(mse_te)

    train_r2_val = r2_score(y_train, y_train_pred)
    train_r2_adj = 1 - (1 - train_r2_val) * ((n_train - 1) / (n_train - p - 1))

    poly_rows.append({
        "degree": d,
        "p": p,
        "train_RMSE": round(np.sqrt(mse_tr), 3),
        "test_RMSE": round(np.sqrt(mse_te), 3),
        "test_MAE": round(mean_absolute_error(y_test, y_test_pred), 3),
        "train_R2": round(train_r2_val, 3),
        "train_adj_R2": round(train_r2_adj, 3),
        "test_R2": round(r2_score(y_test, y_test_pred), 3),
    })

poly_df = pd.DataFrame(poly_rows)
print("\nA5) Polynomial Regression Comparison")
print(poly_df.to_string(index=False))
    
fig, ax = plt.subplots(1,1, figsize=(7, 4.5))
ax.plot(degrees, mse_train, marker="o", color="blue", label="Training MSE")
ax.plot(degrees, mse_test, marker="s", color="red", label="Test MSE")

ax.set_xlabel("Polynomial Degree ")
ax.set_ylabel("MSE (MPa²)")
ax.set_title("Polynomial Regression on Concrete Strength")
ax.set_xticks(degrees)
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
fig.savefig("results/poly_degrees.png")
plt.show()

# A6
y_class = (df["strength"] >= 40).astype(int) # 1 = reaches 40 MPa, 0 = does not
Xc_train, Xc_test, c_train, c_test = train_test_split(
X, y_class, test_size=0.2, random_state=42, stratify=y_class)

print(y_class.value_counts(normalize=True))

K_values = [1, 3, 5, 7, 15, 25, 51, 101]
train_accs = []
test_accs = []

for i in K_values:
    knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=i))
    knn.fit(Xc_train, c_train)
    
    train_accs.append(knn.score(Xc_train, c_train))
    test_accs.append(knn.score(Xc_test, c_test))
    
sweep_df = pd.DataFrame({
    "K": K_values,
    "train_acc": train_accs,
    "test_acc": test_accs,
})
print(sweep_df.to_string(index=False))

fig, ax = plt.subplots(1, 1, figsize=(7, 5))
ax.plot(K_values, train_accs, marker="o", color="blue", label="Training Accuracy")
ax.plot(K_values, test_accs, marker="s", color="red", label="Test Accuracy")
ax.set_xscale("log")
ax.set_xticks(K_values, labels=[str(k) for k in K_values])
ax.set_xlabel("K (number of neighbours, log scale)")
ax.set_ylabel("Accuracy")
ax.set_title("KNN Accuracy vs. K (Concrete Strength >= 40 MPa)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
fig.savefig("results/knn_sweep.png", dpi=150)
plt.show()

best_k = K_values[int(np.argmax(test_accs))]
print(best_k)
best_scaled_acc = max(test_accs)

knn_unscaled = KNeighborsClassifier(n_neighbors=best_k)
knn_unscaled.fit(Xc_train, c_train)
unscaled_acc = knn_unscaled.score(Xc_test, c_test)

print(f"\nChosen K = {best_k}")
print(f"Test accuracy with StandardScaler:    {best_scaled_acc:.4f}")
print(f"Test accuracy without StandardScaler: {unscaled_acc:.4f}")

split_accs = []
for rs in range(5):
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y_class, test_size=0.2, random_state=rs, stratify=y_class
    )
    model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=best_k))
    model.fit(X_tr, y_tr)
    split_accs.append(model.score(X_te, y_te))

spread = max(split_accs) - min(split_accs)
std_acc = np.std(split_accs)
print("\n5-split test accuracies (random_state 0..4):", [round(a, 4) for a in split_accs])
print(f"Mean: {np.mean(split_accs):.4f} | Std: {std_acc:.4f} | Range (max - min): {spread:.4f}")



tree_depth = [1, 2, 3, 4, 5, 6, 8, None]
train_accs = []
test_accs = []
n_leaves = []
actual_depth = []

for i in tree_depth:
    tree = DecisionTreeClassifier(criterion="entropy", max_depth=i,
        min_samples_leaf=1, random_state=0)
    tree.fit(Xc_train, c_train)
    train_accs.append(tree.score(Xc_train, c_train))
    test_accs.append(tree.score(Xc_test, c_test))
    actual_depth.append(tree.get_depth())
    n_leaves.append(tree.get_n_leaves())
    
    
tree_summary = pd.DataFrame({
    "max_depth": [str(d) for d in tree_depth],
    "n_leaves": n_leaves,
    "train_accs": [round(a, 4) for a in train_accs],
    "test_accs": [round(a, 4) for a in test_accs],
    "gap": [round(tr-te, 4) for tr, te in zip(train_accs, test_accs)],
})
print(tree_summary.to_string(index=False))
    
x_pos = range(len(tree_depth))
fig, ax = plt.subplots(1, 1, figsize=(7, 5))
ax.plot(x_pos, train_accs, marker="o", color="blue", label="Training Accuracy")
ax.plot(x_pos, test_accs, marker="s", color="red", label="Test Accuracy")
ax.set_xticks(x_pos, labels=[str(d) for d in tree_depth])
ax.set_xlabel("Max depth")
ax.set_ylabel("Accuracy")
ax.set_title("Tree Accuracy vs. Max depth") 
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
fig.savefig("results/tree_depth.png", dpi=150)
plt.show()

chosen_depth = 4
best_tree = DecisionTreeClassifier(criterion="entropy", max_depth=chosen_depth, 
            min_samples_leaf=1, random_state=0)
best_tree.fit(Xc_train, c_train)
y_pred = best_tree.predict(Xc_test)

print(f"\nTop two levels of tree (max_depth={chosen_depth}):")
print(export_text(best_tree, feature_names=list(X.columns), max_depth=2))


best_knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=best_k))
best_knn.fit(Xc_train, c_train)

# A7
models = [
    (f"KNN (K={best_k})", best_knn),
    (f"Decision Tree (max_depth={chosen_depth})", best_tree),]

metrics_rows = []
for name, clf in models:
    y_pred = clf.predict(Xc_test)
    tn, fp, fn, tp = confusion_matrix(c_test, y_pred).ravel()
    metrics_rows.append({
        "model": name,
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "TN": tn,
        "accuracy": round(accuracy_score(c_test, y_pred), 4),
        "precision": round(precision_score(c_test, y_pred), 4),
        "recall": round(recall_score(c_test, y_pred), 4),
        "f1": round(f1_score(c_test, y_pred), 4),
    })
    
metrics_df = pd.DataFrame(metrics_rows)
print(metrics_df.to_string(index=False))

metrics_df.to_csv("results/A_metrics.csv", index=False)


proba = best_knn.predict_proba(Xc_test)[:, 1]
thresholds = [0.3, 0.5, 0.7, 0.9]

thresh_rows = []
for t in thresholds:
    y_pred_t = (proba >= t).astype(int)
    tn, fp, fn, tp = confusion_matrix(c_test, y_pred_t).ravel()
    thresh_rows.append({
        "threshold": t,
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "TN": tn,
        "precision": round(precision_score(c_test, y_pred_t, zero_division=0), 4),
        "recall": round(recall_score(c_test, y_pred_t), 4),
    })

thresh_df = pd.DataFrame(thresh_rows)
print(f"\nThreshold change for KNN (K={best_k})")
print(thresh_df.to_string(index=False))

# A8
lin_raw = LinearRegression()
lin_raw.fit(X_train, y_train)

lin_std = make_pipeline(StandardScaler(), LinearRegression())
lin_std.fit(X_train, y_train)

tree_imp = best_tree.feature_importances_

perm_knn = permutation_importance(best_knn, Xc_test, c_test,scoring="f1", n_repeats=20, random_state=0)
perm_tree = permutation_importance(best_tree,  Xc_test, c_test,scoring="f1", n_repeats=20, random_state=0)
    
imp_df = pd.DataFrame({
    "feature": X.columns,
    "raw_coef": np.round(lin_raw.coef_, 4),
    "std_coef": np.round(lin_std[-1].coef_, 4),
    "tree_imp": np.round(tree_imp, 4),
    "perm_knn_f1": np.round(perm_knn.importances_mean, 4),
    "perm_knn_std": np.round(perm_knn.importances_std, 4),
    "perm_tree_f1": np.round(perm_tree.importances_mean, 4),
    "perm_tree_std": np.round(perm_tree.importances_std, 4),
})

print("\nA8) Feature Importance Comparison")
print(imp_df.to_string(index=False))

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

axes[0].barh(imp_df["feature"], imp_df["std_coef"], color="steelblue")
axes[0].axvline(0, color="black", linewidth=0.8)
axes[0].set_xlabel("MPa per 1 SD")
axes[0].set_title("Standardised Linear Coef")

axes[1].barh(imp_df["feature"], imp_df["tree_imp"], color="seagreen")
axes[1].set_xlabel("Normalised Entropy Gain")
axes[1].set_title("Decision Tree Importance")

axes[2].barh(imp_df["feature"], imp_df["perm_knn_f1"], color="coral")
axes[2].set_xlabel("Mean F1")
axes[2].set_title("KNN Permutation Importance")

for ax in axes:
    ax.grid(True, axis="x", linestyle="--", alpha=0.5)

plt.tight_layout()
fig.savefig("results/feature_importance.png", dpi=150)
plt.show()

# Bonus

X_b1 = X.copy()
X_b1["age"] = np.log(X_b1["age"])

X_b2 = X_b1.copy()
X_b2["water"] = X_b2["water"] / (X_b2["cement"] + X_b2["slag"] + X_b2["ash"])

bonus_rows = []
for name, X_feat in [("Linear + log(age)", X_b1), ("Linear + log(age) + w/b", X_b2)]:
    Xb_tr, Xb_te, yb_tr, yb_te = train_test_split(
        X_feat, y, test_size=0.2, random_state=42
    )
    reg = LinearRegression().fit(Xb_tr, yb_tr)
    bonus_rows.append({
        "model": name,
        "p": reg.n_features_in_,
        "test_R2": round(r2_score(yb_te, reg.predict(Xb_te)), 3)
    })

print("\nBonus) Physics-Informed Features")
print(pd.DataFrame(bonus_rows).to_string(index=False))