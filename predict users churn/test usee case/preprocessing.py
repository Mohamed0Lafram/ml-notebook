from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA



class Preprocessing(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.pca1 = PCA(n_components=1)
        self.pca2 = PCA(n_components=1)
        self.scaler = StandardScaler()

    def fit(self, X, y=None):
        #X = X.copy()
        # Merge two columns
        X['total_navigations_fav1_fav2'] = X['total_navigations_fav1'] + X['total_navigations_fav2']

        # Feature engineering - PCA 1
        X1 = X[['drives', 'sessions']].values
        X_pca1 = self.pca1.fit_transform(X1)
        X['drives_sessions'] = X_pca1

        # PCA 2
        X2 = X[['driving_days', 'activity_days']].values
        X_pca2 = self.pca2.fit_transform(X2)
        X['driving_activity_days'] = X_pca2


        # Drop old columns (ignore errors if columns don't exist)
        cols_to_drop = ['ID', 'driving_days', 'activity_days', 'drives', 'sessions',
                         'total_navigations_fav1', 'total_navigations_fav2']
        X = X.drop(columns=cols_to_drop, errors='ignore')

        # Standardize numeric columns (except 'label' and 'device')
        numeric_cols = [col for col in X.columns if col not in ['label', 'device']]
        self.scaler.fit(X[numeric_cols])
        return self

    def transform(self, X):
        x_transform = X.copy()

        # Merge two columns
        x_transform['total_navigations_fav1_fav2'] = x_transform['total_navigations_fav1'] + x_transform['total_navigations_fav2']

        # Feature engineering - PCA 1
        X1 = x_transform[['drives', 'sessions']].values
        X_pca1 = self.pca1.transform(X1)
        x_transform['drives_sessions'] = X_pca1

        # PCA 2
        X2 = x_transform[['driving_days', 'activity_days']].values
        X_pca2 = self.pca2.transform(X2)
        x_transform['driving_activity_days'] = X_pca2


        # Drop old columns (ignore errors if columns don't exist)
        cols_to_drop = ['ID', 'driving_days', 'activity_days', 'drives', 'sessions',
                         'total_navigations_fav1', 'total_navigations_fav2']
        x_transform = x_transform.drop(columns=cols_to_drop, errors='ignore')

        # Standardize numeric columns (except 'label' and 'device')
        numeric_cols = [col for col in x_transform.columns if col not in ['label', 'device']]
        x_transform[numeric_cols] = self.scaler.transform(x_transform[numeric_cols])

        return x_transform
