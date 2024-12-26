from scipy.stats import zscore
import numpy as np
import pandas as pd

class OutlierHandler:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def remove_outliers_iqr(self, columns):
        """Remove rows with outliers based on IQR method for specified columns."""
        for col in columns:
            Q1 = self.dataframe[col].quantile(0.25)
            Q3 = self.dataframe[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            self.dataframe = self.dataframe[(self.dataframe[col] >= lower_bound) & (self.dataframe[col] <= upper_bound)]
        return self.dataframe

    def remove_outliers_percentile(self, columns, lower_percentile=0.05, upper_percentile=0.95):
        """Remove rows with outliers outside specified percentiles for given columns."""
        for col in columns:
            lower_bound = self.dataframe[col].quantile(lower_percentile)
            upper_bound = self.dataframe[col].quantile(upper_percentile)
            self.dataframe = self.dataframe[(self.dataframe[col] >= lower_bound) & (self.dataframe[col] <= upper_bound)]
        return self.dataframe

    def clip_outliers(self, columns, method="iqr", lower_percentile=0.05, upper_percentile=0.95):
        """Clip outliers for specified columns based on IQR or percentile method."""
        for col in columns:
            if method == "iqr":
                Q1 = self.dataframe[col].quantile(0.25)
                Q3 = self.dataframe[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
            elif method == "percentile":
                lower_bound = self.dataframe[col].quantile(lower_percentile)
                upper_bound = self.dataframe[col].quantile(upper_percentile)
            self.dataframe[col] = self.dataframe[col].clip(lower=lower_bound, upper=upper_bound)
        return self.dataframe

    def log_transform(self, columns):
        """Apply log transformation to specified columns."""
        for col in columns:
            self.dataframe[col] = np.log1p(self.dataframe[col])  # log(1 + x) to handle zero values
        return self.dataframe

    def winsorize_outliers(self, columns, limits=(0.05, 0.05)):
        """Apply winsorization to specified columns with given limits."""
        from scipy.stats.mstats import winsorize
        for col in columns:
            self.dataframe[col] = winsorize(self.dataframe[col], limits=limits)
        return self.dataframe

    def flag_outliers(self, columns, method="iqr", lower_percentile=0.05, upper_percentile=0.95):
        """Flag outliers in specified columns using IQR or percentile method."""
        for col in columns:
            if method == "iqr":
                Q1 = self.dataframe[col].quantile(0.25)
                Q3 = self.dataframe[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
            elif method == "percentile":
                lower_bound = self.dataframe[col].quantile(lower_percentile)
                upper_bound = self.dataframe[col].quantile(upper_percentile)
            self.dataframe[f"{col}_outlier_flag"] = ~self.dataframe[col].between(lower_bound, upper_bound)
        return self.dataframe

    def remove_outliers_zscore(self, columns, threshold=3):
        """Remove rows with outliers based on Z-score method for specified columns."""
        for col in columns:
            self.dataframe = self.dataframe[(zscore(self.dataframe[col].dropna()) < threshold).reindex(self.dataframe.index, fill_value=False)]
        return self.dataframe

    def clip_outliers_zscore(self, columns, threshold=3):
        """Clip outliers based on Z-score method for specified columns."""
        for col in columns:
            z_scores = zscore(self.dataframe[col].dropna())
            outlier_mask = (z_scores.abs() >= threshold)
            col_median = self.dataframe[col].median()
            self.dataframe[col] = np.where(outlier_mask, col_median, self.dataframe[col])
        return self.dataframe

#Removing the outliers by clipping the data outside of the iqr range
# OutlierHandler_obj = OutlierHandler(data)

# outlier_treated_data = OutlierHandler_obj.clip_outliers(num_features, method="iqr")
# outlier_treated_data.head(2)
