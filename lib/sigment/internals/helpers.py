def flatten(X):
    if X.ndim == 2:
        return X.reshape(-1) if any(i == 1 for i in X.shape) else X
    else:
        return X

def choice(random_state, p):
    return random_state.uniform(size=1).item() < p