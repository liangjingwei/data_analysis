# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches


def scatter_plot(df, x_col, y_col, cate_col=None, title=None):
    """
    二维散点图
    :Params: df: dataframe contains x_axis, y_axis, category
    :Params: x_col: x_axis, str
    :Params: y_col: y_axis, str
    :Params: cate_col: category variable, str
    :Params: title: title of graph, str
    ----------
    """
    x_str = x_col.capitalize()
    y_str = y_col.capitalize()
    categories = np.unique(df[cate_col])
    colors = [plt.cm.tab10(i/float(len(categories)-1)) 
                for i in range(len(categories))]
    plt.figure(figsize=(10, 8), dpi= 80, facecolor='w', edgecolor='k')
    for i, category in enumerate(categories):
        plt.scatter(x_col, y_col, 
                    data=df.loc[df[cate_col]==category, :], 
                    s=20, cmap=colors[i], label=str(category))

    plt.gca().set(xlabel=x_str, ylabel=y_str)
    plt.xticks(fontsize=12); plt.yticks(fontsize=12)
    title = title if title else "Scatterplot of %s vs %s" % (x_str, y_str)
    plt.title(title, fontsize=22)
    plt.legend(fontsize=12)    
    plt.show()
    
def lmplot(df, x_col, y_col, cate_col=None, title=None):
    """
    线性拟合图
    """
    sns.set_style("white")
    gridobj = sns.lmplot(x=x_col, y=y_col, hue=cate_col, data=df, 
                     height=7, aspect=1.6, robust=True, palette='tab10', 
                     scatter_kws=dict(s=60, linewidths=.7, edgecolors='black'))
    title = title if title else "Scatterplot with line of best fit"
    plt.title(title, fontsize=20)
    plt.show()
    
def strip_plot(df, x_col, y_col, cate_col=None, title=None):
    """
    Strip Plot 抖动图
    通常，多个数据点具有完全相同的 X 和 Y 值。 结果，多个点绘制会重叠并隐藏。 
    为避免这种情况，请将数据点稍微抖动，以便直观地看到它们。
    """
    fig, ax = plt.subplots(figsize=(10, 8), dpi=80)
    sns.stripplot(x=x_col, y=y_col, hue=cate_col, 
                  data=df, jitter=0.25, size=8, ax=ax, linewidth=.5)
    title = title if title else "Use jittered plots to avoid overlapping of points"    
    plt.title(title, fontsize=22)
    plt.show()
    
def count_plot(df, x_col, y_col, title=None):
    """
    避免点重叠问题的另一个选择是增加点的大小，这取决于该点中有多少点。 
    因此，点的大小越大，其周围的点的集中度越高。
    """
    df_counts = df.groupby([x_col, y_col]).size().reset_index(name='counts')
    fig, ax = plt.subplots(figsize=(16,10), dpi= 80)    
    sns.stripplot(df_counts[x_col], df_counts[y_col], 
                  size=df_counts.counts*2, ax=ax)
    title = title if title else 'Counts Plot'
    plt.title(title, fontsize=22)
    plt.show()    
    
def marginal_histogram(df, x_col, y_col, cate_col=None, title=None):
    """边缘直方图
    具有沿 X 和 Y 轴变量的直方图。 这用于可视化 X 和 Y 之间的关系
    以及单独的 X 和 Y 的单变量分布。 这种图经常用于探索性数据分析（EDA）。
    """
    fig = plt.figure(figsize=(10, 8), dpi= 80)
    grid = plt.GridSpec(4, 4, hspace=0.5, wspace=0.2)
    ax_main = fig.add_subplot(grid[:-1, :-1])
    ax_right = fig.add_subplot(grid[:-1, -1], xticklabels=[], yticklabels=[])
    ax_bottom = fig.add_subplot(grid[-1, 0:-1], xticklabels=[], yticklabels=[])
    if cate_col:
        c = df[cate_col].astype('category').cat.codes
    else:
        c = None
    ax_main.scatter(x_col, y_col, c=c,
            alpha=.9, data=df, cmap="tab10", edgecolors='gray', linewidths=.5)
    ax_bottom.hist(df[x_col], 40, histtype='stepfilled', 
                   orientation='vertical', color='deeppink')
    ax_bottom.invert_yaxis()
    ax_right.hist(df[y_col], 40, histtype='stepfilled',
                  orientation='horizontal', color='deeppink')
    title = title if title else 'Scatterplot with Histograms %s vs %s' \
                % (x_col, y_col)
    ax_main.set(title=title, xlabel=x_col, ylabel=y_col)
    ax_main.title.set_fontsize(20)
    for item in ([ax_main.xaxis.label, ax_main.yaxis.label] \
                 + ax_main.get_xticklabels() + ax_main.get_yticklabels()):
        item.set_fontsize(14)
    
    xlabels = ax_main.get_xticks().tolist()
    ax_main.set_xticklabels(xlabels)
    plt.show()

def marginal_boxplot(df, x_col, y_col, cate_col=None, title=None):
    """边缘箱图
    与边缘直方图具有相似的用途。 然而，箱线图有助于精确定位 X 和 Y 
    的中位数、第25和第75百分位数。
    """
    fig = plt.figure(figsize=(10, 8), dpi= 80)
    grid = plt.GridSpec(4, 4, hspace=0.5, wspace=0.2)
    ax_main = fig.add_subplot(grid[:-1, :-1])
    ax_right = fig.add_subplot(grid[:-1, -1], xticklabels=[], yticklabels=[])
    ax_bottom = fig.add_subplot(grid[-1, 0:-1], xticklabels=[], yticklabels=[])
    if cate_col:
        c = df[cate_col].astype('category').cat.codes
    else:
        c = None
    ax_main.scatter(x_col, y_col, c=c, alpha=.9, data=df, 
                    cmap="Set1", edgecolors='black', linewidths=.5)
    sns.boxplot(df[x_col], ax=ax_right, orient="v")
    sns.boxplot(df[y_col], ax=ax_bottom, orient="h")
    ax_bottom.set(xlabel='')
    ax_right.set(ylabel='')
    title = title if title else 'Scatterplot with Histograms %s vs %s' \
                % (x_col, y_col)
    ax_main.set(title=title, xlabel='displ', ylabel='hwy')
    ax_main.title.set_fontsize(20)
    for item in ([ax_main.xaxis.label, ax_main.yaxis.label] \
                 + ax_main.get_xticklabels() + ax_main.get_yticklabels()):
        item.set_fontsize(14)
    plt.show()    
      
def corr_plot(df, x_variables, title=None):
    """相关系数热力图"""
    plt.figure(figsize=(10,8), dpi= 80)
    sns.heatmap(df.corr(), xticklabels=df[x_variables].corr().columns, 
            yticklabels=df.corr().columns, cmap='RdYlGn', center=0, annot=True)
    title = title if title else 'Correlogram of Variables'
    plt.title(title, fontsize=22)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.show()
    
def pairplot(df, x_variables, cate_cols=None, title=None):
    """矩阵图
    """
    plt.figure(figsize=(10,8), dpi= 80)
    sns.pairplot(df, kind="scatter", hue=cate_cols, 
                 plot_kws=dict(s=80, edgecolor="white", linewidth=2.5))
    title = title if title else 'Pair Plot'
    plt.title(title, fontsize=22)
    plt.show()

def diverging_bar_plot(df, x_col, y_col, title=None):
    """发散型条形图
    """
    x_str_z = x_col + '_z'
    df[x_str_z] = (df[x_col] - df[x_col].mean()) / df[x_col].std()
    df['colors'] = np.where(df[x_str_z] < 0, 'green', 'red')
    df.sort_values(x_str_z, inplace=True)
    df.reset_index(inplace=True)
    plt.figure(figsize=(14,10), dpi= 80)
    plt.hlines(y=df.index, xmin=0, xmax=df[x_str_z], 
               color=df['colors'], alpha=0.4, linewidth=5)
    plt.gca().set(ylabel='$Model$', xlabel=x_col)
    plt.yticks(df.index, df[y_col], fontsize=12)
    title = title if title else 'Diverging Bars of %s' % y_col
    plt.title(title, fontdict={'size':20})
    plt.grid(linestyle='--', alpha=0.5)
    plt.show()

def ordered_bar_chart(df, x_col, cate_col, title=None):
    """
    有序柱形图
    """
    df = df[[x_col, cate_col]].groupby(cate_col).agg({x_col: 'mean'})
    df.sort_values(x_col, inplace=True)
    df.reset_index(inplace=True)
    fig, ax = plt.subplots(figsize=(16,10), facecolor='white', dpi= 80)
    ax.vlines(x=df.index, ymin=0, ymax=df[x_col], 
              color='firebrick', alpha=0.7, linewidth=20)
    for i, cty in enumerate(df[x_col]):
        ax.text(i, cty+0.1, round(cty, 1), horizontalalignment='center')
    title = title if title else "Bar chart"
    ax.set_title(title, fontdict={'size':22})
    ax.set(ylabel=cate_col, ylim=(0, df[x_col].max() + 0.8))
    plt.xticks(df.index, df[cate_col], rotation=60, 
               horizontalalignment='right', fontsize=12)
    p1 = patches.Rectangle((.57, -0.005), width=.33, height=.13, 
            alpha=.1, facecolor='green', transform=fig.transFigure)
    p2 = patches.Rectangle((.124, -0.005), width=.446, height=.13, 
                    alpha=.1, facecolor='red', transform=fig.transFigure)
    fig.add_artist(p1)
    fig.add_artist(p2)
    plt.show()

def lollipop_chart(df, x_col, cate_col, title=None):  
    """
    棒棒糖图，类似柱形图
    """
    df = df[[x_col, cate_col]].groupby(cate_col).agg({x_col: 'mean'})
    df.sort_values(x_col, inplace=True)
    df.reset_index(inplace=True)
    df.rename(columns={x_col: 'x_col'}, inplace=True)
    fig, ax = plt.subplots(figsize=(12,8), dpi= 80)
    ax.vlines(x=df.index, ymin=0, ymax=df['x_col'], 
              color='firebrick', alpha=0.7, linewidth=2)
    ax.scatter(x=df.index, y=df['x_col'], s=75, color='firebrick', alpha=0.7)
    title = title if title else "Lollipop Chart"
    ax.set_title(title, fontdict={'size':22})
    ax.set_ylabel(x_col)
    ax.set_xticks(df.index)
    ax.set_xticklabels(df[cate_col], rotation=60, 
                       fontdict={'horizontalalignment': 'right', 'size':12})
    ax.set_ylim(0, 30)
    for row in df.itertuples():
        ax.text(row.Index, row.x_col+.5, s=round(row.x_col, 2), 
    horizontalalignment= 'center', verticalalignment='bottom', fontsize=14)
    plt.show()

def density_plot(df, x_col, cate_col, title=None):
    """
    密度函数曲线
    """
    plt.figure(figsize=(10,8), dpi= 80)
    categories = df[cate_col].unique()
    for i, category in enumerate(categories):
        data = df[df[cate_col] == category]
        sns.kdeplot(data[x_col], shade=True, label="{}={}".format(cate_col, category), alpha=.7)
    title = title if title else "Density Plot"
    plt.title(title, fontsize=22)
    plt.legend()
    plt.show()   

def density_histogram_plot(df, x_col, cate_col, title=None):
    """
    密度函数-直方图
    """
    plt.figure(figsize=(10,8), dpi= 80)
    categories = df[cate_col].unique()
    for i, category in enumerate(categories):
        data = df[df[cate_col] == category]
        sns.distplot(data[x_col], label=category, hist_kws={'alpha':.7}, kde_kws={'linewidth':3})
    title = title if title else "Density Historgram Plot "   
    plt.title(title, fontsize=22)
    plt.legend()
    plt.show()

def population_pyramid(df, x_col, y_col, cate_col, title=None):
    """
    金字塔: example cate_col: Gender
    """
    plt.figure(figsize=(10,8), dpi=80)
    order_of_bars = df[y_col].unique()[::-1]
    colors = [plt.cm.Spectral(i/float(len(df[cate_col].unique())-1)) for i in range(len(df[cate_col].unique()))]
    
    for c, group in zip(colors, df[cate_col].unique()):
        sns.barplot(x=x_col, y=y_col, data=df.loc[df[cate_col]==group, :], order=order_of_bars, color=c, label=group)
    
    # Decorations    
    plt.xlabel("${}$".format(x_col))
    plt.ylabel(y_col)
    plt.yticks(fontsize=12)
    title = title if title else "Population Pyramid "
    plt.title(title, fontsize=22)
    plt.legend()
    plt.show()
    
def pie_chart(df, cate_col, title=None):
    """
    饼状图
    """
    df = df.groupby(cate_col).size()
    df.plot(kind='pie', subplots=True, figsize=(8, 8))
    title = title if title else "Pie Chart"
    plt.title("Pie Chart of Vehicle Class - Bad")
    plt.ylabel("")
    plt.show()