def basic_eda(data):
  print('Head of data')
  display(data.head())
  print('*************************************************************************************')
  print('Shape of data')
  print(data.shape)
  print('*************************************************************************************')
  print('Unique values in data')
  data.drop_duplicates(inplace = True)
  display(data.nunique())
  print('*************************************************************************************')
  print('Non-Null count and datatypes of columns in data')
  data.info()
  print('*************************************************************************************')
  print('Description of numerical data')
  display(data.describe())
  print('*************************************************************************************')



# Improvements: Add subplots functionality,
#               Option to select top/bottom n or given list of categories for categorical features analysis,
#               Can add run_all feature that runs all the functions and gives all the graphs
#               Exception handling
class Plotter:
    def __init__(self, data):
        """
        Initializes the Plotter object.
        Parameters:
        - data (DataFrame): pandas DataFrame containing the data for plotting.
        """
        self.data = data
#data[data.source_name.isin(data['source_name'].value_counts(ascending = False).reset_index()['source_name'][:10])]
    def countplot(self, column, title=None, color= None, fontsize = None, bar_label = False, top_n = None):
        """
        Creates a count plot for a specified column.
        Usage - Univariate categorical analysis
        If so many categories, recommended to filter for top few categories data only
        Parameters:
        - column (str): Name of the column to plot.
        - title (str): Title for the plot.
        """
        try:
          plt.figure(figsize=(10, 6))
          if top_n:
            print('Total unique values: ', self.data[column].nunique())
            top_n_category_df = self.data[self.data[column].isin(self.data[column].value_counts(ascending = False).reset_index()[column][:top_n])]
          else:
            top_n_category_df = self.data
          ax=sns.countplot(data=top_n_category_df, x=column, order=top_n_category_df[column].value_counts().index, color=color if color else 'cornflowerblue')
          if bar_label:
            ax.bar_label(ax.containers[0])
          plt.title(title if title else f'Count Plot of {column}')
          plt.xlabel(column)
          plt.ylabel('Count')
          plt.xticks(rotation = 90, fontsize = fontsize)
          plt.show()
        except Exception as e:
          print(e)

    def pieplot(self, column, title=None, startangle = 90, top_n = None):
        """
        Creates a pie plot for a specified column.
        Usage - Univariate categorical analysis
        If so many categories, recommended to filter for top few categories data only
        Parameters:
        - column (str): Name of the column to plot.
        - title (str): Title for the plot.
        """
        try:
          if top_n:
            print('Total unique values: ', self.data[column].nunique())
            top_categories = self.data[column].value_counts(ascending=False).index[:top_n]
            top_n_category_df = self.data.copy()
            top_n_category_df[column] = top_n_category_df[column].apply(lambda x: x if x in top_categories else "Other")
          else:
            top_n_category_df = self.data
          plt.figure(figsize=(10, 6))
          top_n_category_df[column].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle = startangle, shadow = False, wedgeprops={'edgecolor': 'black', 'linewidth':0.5})
          plt.title(title if title else f'Pie Plot of {column}')
          plt.ylabel('')
          plt.show()
        except Exception as e:
          print(e)

    def histogram(self, column, bins=30, use_bins = False, title=None, kde = False):
        """
        Creates a histogram for a specified column.
        Usage - Univariate numerical analysis
        Parameters:
        - column (str): Name of the column to plot.
        - bins (int): Number of bins for the histogram.
        - use_bins (Bool): if bins are to be used(use for numerical data, recommended not to use for number categorical data like year)
        - color (str): Color of the histogram bars.
        - title (str): Title for the plot.
        - kde (Bool) : Whether to include a kernel density estimate (KDE) plot.
        """
        try:
          plt.figure(figsize=(10, 6))
          if use_bins:
            sns.histplot(self.data[column], bins=bins, kde=kde)
          else:
            sns.histplot(self.data[column],  kde=kde)
          plt.title(title if title else f'Histogram of {column}')
          plt.xlabel(column)
          plt.ylabel('Frequency')
          plt.show()
        except Exception as e:
          print(e)

    def kdeplot(self, column, title=None):
        """
        Creates a kernel density plot for a specified column.
        Usage - Univariate numerical analysis
        Parameters:
        - column (str): Name of the column to plot.
        - title (str): Title for the plot.
        """
        try:
          plt.figure(figsize=(10, 6))
          sns.kdeplot(self.data[column], fill=True)
          plt.title(title if title else f'Kernel Density Plot of {column}')
          plt.xlabel(column)
          plt.ylabel('Density')
          plt.show()
        except Exception as e:
          print(e)

    def boxplot(self, column, title=None):
        """
        Creates a box plot for a specified column.
        Usage - Univariate numerical analysis
        Parameters:
        - column (str): Name of the column to plot.
        - title (str): Title for the plot.
        """
        try:
          plt.figure(figsize=(8, 6))
          sns.boxplot(y = self.data[column])
          plt.title(title if title else f'Boxplot of {column}')
          plt.ylabel(column)
          plt.show()
        except Exception as e:
          print(e)

    def lineplot(self, x_column, y_column, title=None, color = None, xlimit=None,ylimit=None):
        """
        Creates a line plot between two specified columns.
        Usage - Bivariate numerical-numerical analysis(One numerical column like 'year')
        Parameters:
        - x_column (str): Name of the column for the x-axis.
        - y_column (str): Name of the column for the y-axis.
        - title (str): Title for the plot.
        - xlimit (dict): Dictionary with 'left' and 'right' keys for x-axis limits.
        - ylimit (dict): Dictionary with 'left' and 'right' keys for y-axis limits.
        - color (str): Color of the line plot.
        """
        try:
          plt.figure(figsize=(10, 6))
          sns.lineplot(data=self.data, x=x_column, y=y_column, color = color)
          if xlimit:
            plt.xlim(left = xlimit['left'], right = xlimit['right'])
          if ylimit:
            plt.ylim(left = ylimit['left'], right = ylimit['right'])
          plt.title(title if title else f'Line Plot of {x_column} vs {y_column}')
          plt.xlabel(x_column)
          plt.ylabel(y_column)
          plt.show()
        except Exception as e:
          print(e)

    def scatterplot(self, x_column, y_column,  title=None):
        """
        Creates a scatter plot between two specified columns.
        Usage - Bivariate numerical-numerical analysis
        Parameters:
        - x_column (str): Name of the column for the x-axis.
        - y_column (str): Name of the column for the y-axis.
        - title (str): Title for the plot.
        """
        try:
          plt.figure(figsize=(10, 6))
          sns.scatterplot(data=self.data, x=x_column, y=y_column)
          plt.title(title if title else f'Scatterplot of {x_column} vs {y_column}')
          plt.xlabel(x_column)
          plt.ylabel(y_column)
          plt.show()
        except Exception as e:
          print(e)

    def dodgedcountplot(self, x_column, hue,  title=None, top_n = None):
        """
        Creates a dodged countplotplot between two specified columns.
        Usage - Bivariate categorical-categorical analysis
        If so many categories, recommended to filter for top few categories data only
        Parameters:
        - x_column (str): Name of the column for the x-axis.
        - hue (str): Column name to be used for color coding.
        - title (str): Title for the plot.
        """
        try:
          if top_n:
            print(f'Total unique values for {x_column} is {self.data[x_column].nunique()} and {hue} is {self.data[hue].nunique()}')
            top_n_category_df = self.data[(self.data[x_column].isin(self.data[x_column].value_counts(ascending = False).reset_index()[x_column][:top_n])) & (self.data[hue].isin(self.data[hue].value_counts(ascending = False).reset_index()[hue][:top_n]))]
          else:
            top_n_category_df = self.data
          plt.figure(figsize=(10, 6))
          sns.countplot(data=top_n_category_df, x=x_column, hue=hue)
          plt.title(title if title else f'barplot distribution of {hue} for {x_column}')
          plt.ylabel('Count')
          plt.show()
        except Exception as e:
          print(e)

    def stackedcountplot(self, x_column, hue,  title=None, top_n = None):
        """
        Creates a stacked countplot between two specified columns.
        Usage - Bivariate categorical-categorical analysis
        If so many categories, recommended to filter for top few categories data only
        Parameters:
        - x_column (str): Name of the column for the x-axis.
        - hue (str): Column name to be used for color coding.
        - title (str): Title for the plot.
        """
        try:
          if top_n:
            print(f'Total unique values for {x_column} is {self.data[x_column].nunique()} and {hue} is {self.data[hue].nunique()}')
            top_n_category_df = self.data[(self.data[x_column].isin(self.data[x_column].value_counts(ascending = False).reset_index()[x_column][:top_n])) & (self.data[hue].isin(self.data[hue].value_counts(ascending = False).reset_index()[hue][:top_n]))]
          else:
            top_n_category_df = self.data
          plt.figure(figsize=(10, 6))
          data = pd.crosstab(index=top_n_category_df[x_column], columns=top_n_category_df[hue])
          data.plot(kind='bar', stacked=True, figsize=(10, 6))
          plt.title(title if title else f'barplot distribution of {hue} for {x_column}')
          plt.xticks(rotation=90)
          plt.legend()
          plt.show()
        except Exception as e:
          print(e)

    def bivariateboxplot(self, categorical_column, numerical_column, title=None, rotate_xaxis_ticks = False, top_n = None):
        """
        Creates a boxplot between two specified columns.
        Usage - Bivariate categorical-numerical
        If so many categories, recommended to filter for top few categories data only
        Parameters:
        - categorical_column (str): Name of the column for the x-axis.
        - numerical_column (str): Name of the column for the y-axis.
        - title (str): Title for the plot.
        - rotate_xaxis_ticks (bool): Whether to rotate x-axis ticks for better readability.
        """
        try:
          if top_n:
            print(f'Total unique values for {categorical_column} is {self.data[categorical_column].nunique()}')
            top_n_category_df = self.data[self.data[categorical_column].isin(self.data[categorical_column].value_counts(ascending = False).reset_index()[categorical_column][:top_n])]
          else:
            top_n_category_df = self.data
          sns.boxplot(data=top_n_category_df, x=categorical_column, y=numerical_column)
          plt.title(title if title else f'Boxplot of {numerical_column} for {categorical_column}')
          if rotate_xaxis_ticks:
            plt.xticks(rotation=90)
          plt.xlabel(categorical_column)
          plt.ylabel(numerical_column)
          plt.show()
        except Exception as e:
          print(e)

    def bivariatebarplot(self, categorical_column, numerical_column, title=None, rotate_xaxis_ticks = False, top_n = None):
        """
        Creates a boxplot between two specified columns.
        Usage - Bivariate categorical-numerical
        If so many categories, recommended to filter for top few categories data only
        Parameters:
        - categorical_column (str): Name of the column for the x-axis.
        - numerical_column (str): Name of the column for the y-axis.
        - title (str): Title for the plot.
        """
        try:
          if top_n:
            print(f'Total unique values for {categorical_column} is {self.data[categorical_column].nunique()}')
            top_n_category_df = self.data[self.data[categorical_column].isin(self.data[categorical_column].value_counts(ascending = False).reset_index()[categorical_column][:top_n])]
          else:
            top_n_category_df = self.data
          sns.barplot(data=top_n_category_df, x=categorical_column, y=numerical_column, estimator=np.mean)
          plt.title(title if title else f'Barplot of {numerical_column} for {categorical_column}')
          if rotate_xaxis_ticks:
            plt.xticks(rotation=90)
          plt.xlabel(categorical_column)
          plt.ylabel(numerical_column)
          plt.show()
        except Exception as e:
          print(e)

    def jointplot(self, x_column, y_column, title=None):
        """
        Creates a joint plot between two specified columns.
        Usage - Bivariate numerical-numerical analysis
        Parameters:
        - x_column (str): Name of the column for the x-axis.
        - y_column (str): Name of the column for the y-axis.
        - title (str): Title for the plot.
        """
        try:
          sns.jointplot(data=self.data, x=x_column, y=y_column, kind='reg')
          plt.title(title if title else f'Joint Plot of {x_column} vs {y_column}')
          plt.xlabel(x_column)
          plt.ylabel(y_column)
          plt.show()
        except Exception as e:
          print(e)

    def trivariatescatterplot_CNN(self, numerical_column1, numerical_column2, categorical_column, title=None, top_n = None):
        """
        Creates a scatter plot between two specified columns.
        Usage - Trivariate CNN analysis
        Parameters:
        - numerical_column1 (str): Name of the column for the x-axis.
        - numerical_column2 (str): Name of the column for the y-axis.
        - categorical_column (str): Column name to be used for color coding.
        - title (str): Title for the plot.
        """
        try:
          if top_n:
            print(f'Total unique values for {categorical_column} is {self.data[categorical_column].nunique()}')
            top_n_category_df = self.data[self.data[categorical_column].isin(self.data[categorical_column].value_counts(ascending = False).reset_index()[categorical_column][:top_n])]
          else:
            top_n_category_df = self.data
          plt.figure(figsize=(10, 6))
          sns.scatterplot(data=top_n_category_df, x=numerical_column1, y=numerical_column2, hue=categorical_column)
          plt.title(title if title else f'Scatter plot of {numerical_column1} vs {numerical_column2} for {categorical_column}')
          plt.xlabel(numerical_column1)
          plt.ylabel(numerical_column2)
          plt.show()
        except Exception as e:
          print(e)

    def trivariateboxplot(self, categorical_column1, categorical_column2, numerical_column, title=None, rotate_xaxis_ticks = False, top_n = None):
        """
        Creates a boxplot between two specified columns.
        Usage - Trivariate CCN analysis
        If so many categories, recommended to filter for top few categories data only
        Parameters:
        - categorical_column1 (str): Name of the column for the x-axis.
        - categorical_column2 (str): Name of the column for the x-axis.
        - numerical_column (str): Name of the column for the y-axis.
        - title (str): Title for the plot.
        - rotate_xaxis_ticks (bool): Whether to rotate x-axis ticks for better readability.
        """
        try:
          if top_n:
            print(f'Total unique values for {categorical_column1} is {self.data[categorical_column1].nunique()} and {categorical_column2} is {self.data[categorical_column2].nunique()}')
            top_n_category_df = self.data[(self.data[categorical_column1].isin(self.data[categorical_column1].value_counts(ascending = False).reset_index()[categorical_column1][:top_n])) & (self.data[categorical_column2].isin(self.data[categorical_column2].value_counts(ascending = False).reset_index()[categorical_column2][:top_n]))]
          else:
            top_n_category_df = self.data
          plt.figure(figsize=(12,8))
          sns.boxplot(x=categorical_column1,y=numerical_column,hue=categorical_column2,data=top_n_category_df)
          plt.title(title if title else f'Boxplot of {numerical_column} for {categorical_column1} and {categorical_column2}')
          if rotate_xaxis_ticks:
            plt.xticks(rotation=90)
          plt.xlabel(categorical_column1)
          plt.ylabel(numerical_column)
          plt.show()
        except Exception as e:
          print(e)

    #improvements : add sizes range functionality
    def trivariatescatterplot_NNN(self, x_column, y_column, size, title=None):
        """
        Creates a scatter plot between two specified columns.
        Usage - Trivariate NNN analysis
        Parameters:
        - x_column (str): Name of the column for the x-axis.
        - y_column (str): Name of the column for the y-axis.
        - size (str): Column name to be used for size coding.(rank like column)
        - title (str): Title for the plot.
        """
        try:
          plt.figure(figsize=(10, 6))
          sns.scatterplot(x=x_column, y=y_column, size=size, data=self.data)
          plt.title(title if title else f'Scatterplot of {x_column} vs {y_column} for {size}')
          plt.xlabel(x_column)
          plt.ylabel(y_column)
          plt.show()
        except Exception as e:
          print(e)

    def trivariatejointplot(self, numerical_column1, numerical_column2, categorical_column, title=None, top_n = None):
        """
        Creates a joint plot between two specified columns.
        Usage - trivariate CNN analysis
        Parameters:
        - numerical_column1 (str): Name of the column for the x-axis.
        - numerical_column2 (str): Name of the column for the y-axis.
        - categorical_column (str): Column name to be used for color coding.
        - title (str): Title for the plot.
        """
        try:
          if top_n:
            print(f'Total unique values for {categorical_column} is {self.data[categorical_column].nunique()}')
            top_n_category_df = self.data[self.data[categorical_column].isin(self.data[categorical_column].value_counts(ascending = False).reset_index()[categorical_column][:top_n])]
          else:
            top_n_category_df = self.data
          sns.jointplot(x=numerical_column1, y=numerical_column2, data=top_n_category_df, hue=categorical_column)
          # plt.title(title if title else f'Joint Plot of {numerical_column1} vs {numerical_column2} for {categorical_column}')
          plt.show()
        except Exception as e:
          print(e)

    def pairplot(self, columns=None, vars = None,hue=None, top_n = None):
        """
        Creates pair plot for multiple columns.
        Usage : Multivariate numerical analysis(one category column can be added optionally using 'hue' argument)
        Parameters:
        - columns (list): List of column names to include in the pair plot(optional).
        - vars (list): dictionary of lists for x and y column names to include in the pair plot(optional).
        - hue (str): Column name to be used for color coding.
        """
        try:
          if top_n:
            top_n_category_df = self.data[self.data[hue].isin(self.data[hue].value_counts(ascending = False).reset_index()[hue][:top_n])]
          else:
            top_n_category_df = self.data
          if vars:
            sns.pairplot(top_n_category_df, x_vars=vars['x'], y_vars=vars['y'], hue=hue)
          else:
            sns.pairplot(top_n_category_df if columns is None else top_n_category_df[columns], hue=hue)
          plt.show()
        except Exception as e:
          print(e)

    def heatmap(self, columns=None, title="Correlation Heatmap"):
        """
        Creates a heatmap for correlation between specified columns.
        Usage - Multivariate numerical analysis(correlation analysis)
        Parameters:
        - columns (list): List of column names to include in the heatmap(optional. If None, all numerical cols are selected)
        - title (str): Title for the heatmap.
        """
        try:
          plt.figure(figsize=(10, 8))
          corr = self.data.select_dtypes(include=[float,int]).corr() if columns is None else self.data[columns].corr()
          sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
          plt.title(title)
          plt.show()
        except Exception as e:
          print(e)

    def multivariatepieplot(self, columns, title=None, explode = None):
        """
        Creates a pie plot for a specified column.
        Usage - Multivariate numerical analysis(to check proportion for given column sums)
        Parameters:
        - columns (list): List of names of the columns to plot.
        - title (str): Title for the plot.
        - explode (list): List of explode values for each slice of pie chart.
        """
        try:
          plt.figure(figsize=(10, 6))
          data = self.data[columns].T.sum(axis='columns')
          plt.pie(x=data, labels=data.index,startangle=90,explode = explode,shadow=True,autopct = '%.2f%%')
          columns_list = ", ".join(columns)  # Join all column names with a comma and space
          plt.title(title if title else f'Pie Plot of share of {columns_list}')
          plt.show()
        except Exception as e:
          print(e)



class quick_eda_obj:
  def __init__(self, data):
    self.data = data
    self.plotter_obj = Plotter(data)

  def univariate_analysis(self, cat_col_list=[], num_col_list=[], top_n = None):
    """
    Performs univariate analysis on categorical and numerical columns.
    """
    if cat_col_list:
      for col in cat_col_list:
        self.plotter_obj.countplot(column = col, bar_label = True, top_n = top_n)
        self.plotter_obj.pieplot(column = col, startangle = 90, top_n = top_n)

    if num_col_list:
      for col in num_col_list:
        self.plotter_obj.histogram(column = col, bins=30, use_bins = False, kde = False)
        self.plotter_obj.kdeplot(column = col)
        self.plotter_obj.boxplot(column = col)
