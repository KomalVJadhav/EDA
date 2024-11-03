# Data Visualization Charts Guide

This guide covers various types of data visualization charts, categorized by the number of variables and data types.

## Univariate Data Visualization
Visualizations for exploring the distribution of a single variable.

### Categorical Data
- **Bar Chart**: Represents categories with rectangular bars, where the height represents the count or value.
- **Countplot**: Displays the count of observations in each categorical bin using bars.
- **Pie Chart**: Shows the proportion of each category as a slice of a pie.

### Continuous Data
- **Histogram**: Displays the distribution of data by grouping continuous data into bins.
- **KDE Plot**: Kernel Density Estimate plot shows the probability density of a continuous variable.
- **Box and Whiskers Plot**: Visualizes the spread of the data, showing quartiles and outliers.

## Bivariate Data Visualization
Visualizations for exploring the relationship between two variables.

### Continuous-Continuous
- **Line Plot**: Connects data points in a time series or other sequential data.
- **Scatter Plot**: Displays the relationship between two continuous variables.
- **Joint Plot**: Combines scatter plot with histograms or KDE plots to show individual distributions.

### Categorical-Categorical
- **Dodged Countplot**: Side-by-side countplot to compare categories within groups.
- **Stacked Countplot**: Stacks counts within each category to show total and subgroup distribution.

### Categorical-Continuous
- **Boxplot**: Shows the spread of a continuous variable within categories.
- **Bar Plot**: Displays aggregated values (e.g., mean) of a continuous variable within each category.

### Subplots
- **Subplots**: Arranges multiple plots within a single figure for comparative analysis.

## Trivariate Data Visualization
Visualizations for exploring relationships between three variables.

### Continuous-Continuous-Categorical (CCN)
- **Boxplot**: Uses categories to group continuous data across two continuous dimensions.

### Categorical-Continuous-Continuous (CNN)
- **Scatter Plot**: Uses color, size, or shape to represent a categorical variable alongside two continuous variables.

### Continuous-Continuous-Continuous (NNN)
- **Scatter Plot**: Uses color, size, or shape to represent different dimensions within three continuous variables.

## Multivariate Data Visualization
Visualizations for exploring relationships among multiple variables.

### All Continuous or One Categorical + All other Continuous Variables
- **Pair Plot**: Displays pairwise relationships across multiple continuous variables, often with scatter plots and KDE diagonals.

### All Continuous (Proportion Analysis)
- **Pie Plot**: Shows the proportion of each continuous variable relative to the sum across a set.

### All Continuous (Correlation Analysis)
- **Heatmap**: Displays a correlation matrix for continuous variables, illustrating positive or negative relationships.
