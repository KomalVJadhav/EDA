import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# improvements : Handle exceptions
class CrossTabAnalysis:
    def __init__(self, data, index_column, column_name):
        """
        Initialize with dataset, index, and column for analysis.
        Usage - Both index_column and column_name have to be categorical features
        
        Parameters:
        - data (DataFrame): The input DataFrame.
        - index_column (str): Name of the index column (e.g., 'Gender').
        - column_name (str): Name of the column (e.g., 'Product').
        """
        self.data = data
        self.index_column = index_column
        self.column_name = column_name
        self.crosstab_df = self._generate_crosstab()

    def _generate_crosstab(self):
        """Generates initial crosstab with marginal counts."""
        return pd.crosstab(index=self.data[self.index_column], columns=self.data[self.column_name], margins=True)

    def calculate_marginal_probabilities(self):
        """Calculates marginal probabilities for index and column."""
        marginal_df = self.crosstab_df.copy()
        # Calculate marginal probability for each column
        marginal_probs = [marginal_df[col]['All'] / marginal_df['All']['All'] for col in marginal_df.columns]
        marginal_df.loc['Marginal_prob_of_' + self.column_name] = [prob * 100 for prob in marginal_probs]

        # Calculate marginal probability for each row in index column
        marginal_df[f'Marginal_prob_of_{self.index_column}'] = (marginal_df['All'] / marginal_df['All']['All']) * 100
        marginal_df[f'Marginal_prob_of_{self.index_column}'][f'Marginal_prob_of_{self.column_name}'] = np.nan
        return marginal_df

    def calculate_conditional_probabilities(self):
        """Calculates conditional probabilities and merges them into crosstab."""
        # P(index | column)
        conditional_df = self.crosstab_df.copy()
        prob_index_given_column = pd.crosstab(index=self.data[self.index_column],
                                              columns=self.data[self.column_name], margins=True, normalize='columns') * 100
        prob_index_given_column = prob_index_given_column[self.data[self.column_name].unique()]
        prob_index_given_column.rename(columns={col: f'prob_{self.index_column}_given_{col}' for col in conditional_df.columns}, inplace=True)

        # Merge with main crosstab
        conditional_df = conditional_df.merge(prob_index_given_column, left_index=True, right_index=True, how='left')

        # P(column | index)
        prob_column_given_index = pd.crosstab(index=self.data[self.index_column],
                                              columns=self.data[self.column_name], margins=True, normalize='index') * 100
        prob_column_given_index = prob_column_given_index.loc[self.data[self.index_column].unique()]
        prob_column_given_index.rename(columns={col: f'prob_{col}_given_{self.index_column}' for col in conditional_df.columns}, inplace=True)

        # Merge with main crosstab
        conditional_df = conditional_df.merge(prob_column_given_index, left_index=True, right_index=True, how='left')
        return conditional_df

    def calculate_joint_probability(self):
        """Calculates joint probability and merges it into crosstab."""
        joint_df = self.crosstab_df.copy()
        joint_prob = pd.crosstab(index=self.data[self.index_column],
                                 columns=self.data[self.column_name], margins=True, normalize=True) * 100
        joint_prob = joint_prob.loc[self.data[self.index_column].unique(), self.data[self.column_name].unique()]
        joint_prob.rename(columns={col: f'joint_prob_{col}_{self.index_column}' for col in joint_prob.columns}, inplace=True)

        # Merge with main crosstab
        joint_df = joint_df.merge(joint_prob, left_index=True, right_index=True, how='left')
        return joint_df


    def get_full_dataframe(self):
        """Returns the complete crosstab DataFrame with all calculations."""
        # Add calculated probabilities as separate DataFrames
        marginal_probs = self.calculate_marginal_probabilities()
        conditional_prob_df = self.calculate_conditional_probabilities()
        conditional_prob_df = conditional_prob_df.drop(columns = conditional_prob_df.columns.intersection(marginal_probs.columns))
        joint_prob = self.calculate_joint_probability()
        joint_prob = joint_prob.drop(columns = joint_prob.columns.intersection(marginal_probs.columns))

        # Combine all parts
        full_df = marginal_probs.merge(conditional_prob_df, left_index=True, right_index=True, how='left')
        full_df = full_df.merge(joint_prob, left_index=True, right_index=True, how='left')
        return full_df


# Usage
#Product_Gender_analysis_obj = CrossTabAnalysis(data, index_column='Gender', column_name='Product')
#Product_Gender_prob_df = Product_Gender_analysis_obj.get_full_dataframe()
#display(Product_Gender_prob_df)
