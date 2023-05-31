import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
#from matplotlib.ticker import MaxNLocator
sns.set_theme(context='notebook', style='ticks', palette='deep', font_scale=1, color_codes=True, rc=None )            
sns.set_style({'font.sans-serif':['simsun','serif']}) # 适配中英文            
#plt.rcParams['xtick.direction'] = 'in' # 刻度朝内            
#plt.rcParams['ytick.direction'] = 'in'            
plt.rcParams['font.sans-serif'] = 'simsun' # 解决中文显示            
plt.rcParams['axes.unicode_minus'] = False # 解决符号无法显示
st.set_page_config(layout="wide")

# 读取Excel文件并返回DataFrame对象
def read_excel(file_path):
    df = pd.read_excel(file_path)
    return df
#ecolor = ['red','blue', 'orange', 'green']  
#shapepoint = ['o', 's', 'D', '^']
#lty = ['solid', 'dashed', 'solid', 'dashed']
    

# 主函数
def main():
    st.title('Excel文件图形绘制')
    # 创建两列布局
    col1, col2 = st.columns([1, 2])
    with col1:
        st.header('作者信息')
        if st.button('联系方式'):
            st.write('QQ:1131525309')
            st.write('目前这还是一个不成熟的项目，在继续改进中')
        else:
            st.write('KikyoZero')
        st.subheader('读取Excel文件')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # 上传Excel文件
        file = st.file_uploader('上传Excel文件', type=['xlsx', 'xls'])
        if file is not None:
            # 读取Excel文件
                df = read_excel(file)
       # 定义X轴标题
        st.subheader('作图细节调整')
        #st.write('可后期输入调整')
        plottitle = st.text_input('请输入标题：')
        xlabname = st.text_input('请输入X标题：')
        ylabname = st.text_input('请输入Y标题：')
        #xsteprange = df['X'].min()
        #ysteprange = df['X'].min()
        xmins = st.number_input('X最小值：',value= df['X'].min())
        xmaxs = st.number_input('X最大值：',value= df['X'].max())
        ymins = st.number_input('Y最小值：',value= df['Y'].min())
        ymaxs = st.number_input('Y最大值：',value= df['Y'].max())
        #st.subheader('坐标标题设置')
        # 获取用户输入的图像尺寸
        width = st.number_input('请输入图像宽度：', value=8.0, min_value=1.0, max_value=20.0, step=0.1)
        height = st.number_input('请输入图像高度：', value=6.0, min_value=1.0, max_value=20.0, step=0.1)
        # 定义颜色选项列表
        #coloroptions = ['NULL','Accent','Paired']   
        ecolor = st.text_input('请输入颜色类别：','Pastel1')
        st.write('色彩包：Accent、Blues、BrBG、BuGn、BuPu、CMRmap、Dark2、GnBu、Greys、OrRd、Paired、Pastel1、Pastel2、PiYG等')
        #ecolor = st.multiselect('请选择颜色分类：', coloroptions)
        # 定义散点形状选项列表
        spoptions = ['.','o','v','^','<','>','8','s','p','*','h','H','D','d','P','X']  
        shapepoint = st.multiselect('请选择散点形状：', spoptions)
        if st.button('查看形状列表'):
            st.image('param/makers.jpg', caption='Makers')
        # 定义线条类型选项列表
        ltyoptions = ['solid', 'dashed', 'dotted','dashdot','loosely dotted','densely dotted','dashdotted','dashdotdotted']
        lty = st.multiselect('请选择线条类型：', ltyoptions)
        if st.button('查看线条列表'):
            st.image('param/linetype.jpg', caption='Linetypes')
    with col2:
            # 绘制散点图
            def plot_scatter_chart(df):
                # 创建图形对象，并设置尺寸
                fig, ax = plt.subplots(figsize=(width, height))
                sns.scatterplot(x=df['X'],y=df['Y'], hue=df['Group'], 
                                style=df['Group'],
                            palette = sns.color_palette(ecolor), 
                            markers = shapepoint, sizes = 10)
                plt.xlabel(xlabname)
                plt.ylabel(ylabname)
                plt.title(plottitle)
                plt.xlim([xmins-1, xmaxs])
                plt.ylim([ymins, ymaxs])
                plt.grid(False)
                # 去除图例背景
                plt.legend(loc='upper left', frameon=False)
                # 设置刻度数量
                #plt.locator_params(axis='both', nbins=5)
                # 保存图形为图像文件
                fig = plt.gcf()
                return fig
            # 柱状图 
            def plot_bar_chart(df):
                # 创建图形对象，并设置尺寸
                fig, ax = plt.subplots(figsize=(width, height))
                sns.barplot(x=df['X'],y=df['Y'], hue=df['Group'], 
                            errorbar ='sd', capsize =0.1, 
                            errcolor ='black',edgecolor ='black',
                            palette = sns.color_palette(ecolor), 
                            lw=1, width =0.5)
                plt.title(plottitle)
                plt.xlabel(xlabname)
                plt.ylabel(ylabname)
                plt.xlim([xmins-1, xmaxs])
                plt.ylim([ymins, ymaxs])
                plt.grid(False)
                plt.legend(loc='upper left', frameon=False)
                #plt.locator_params(axis='both', nbins=5)
                fig = plt.gcf()
                return fig
            # 绘制点线图
            def plot_pointline_chart(df):
                # 创建图形对象，并设置尺寸
                fig, ax = plt.subplots(figsize=(width, height))
                sns.pointplot(x=df['X'],y=df['Y'], hue=df['Group'], 
                            palette = sns.color_palette(ecolor), 
                            capsize = 0.2, markers = shapepoint, 
                            linestyles = lty)
                plt.title(plottitle)
                plt.xlabel(xlabname)
                plt.ylabel(ylabname)
                plt.xlim([xmins-1, xmaxs])
                plt.ylim([ymins, ymaxs])
                plt.grid(False)
                plt.legend(loc='upper left', frameon=False)
                #plt.locator_params(axis='both', nbins=5)
                fig = plt.gcf()
                return fig
            # 绘制箱型图
            def plot_boxplot_chart(df):
                # 创建图形对象，并设置尺寸
                fig, ax = plt.subplots(figsize=(width, height))
                sns.boxplot(x=df['X'],y=df['Y'], hue=df['Group'], 
                            palette = sns.color_palette(ecolor))
                plt.title(plottitle)
                plt.xlabel(xlabname)
                plt.ylabel(ylabname)
                #plt.xlim([xmins-1, xmaxs])
                #plt.ylim([ymins, ymaxs])
                plt.grid(False)
                plt.legend(loc='upper left', frameon=False)
                #plt.locator_params(axis='both', nbins=5)
                fig = plt.gcf()
                return fig
            if file is not None:
            # 读取Excel文件
                df = read_excel(file)
                # 显示数据表格
                st.subheader('数据表格')
                if st.button('表格数据'):
                    st.dataframe(df)
                # 均值
                st.subheader('分组描述统计')
                if st.button('分组描述统计'):
                    st.dataframe(pd.DataFrame(df.groupby('Group').describe().round(2)))
                
            st.header('结果展示')
            # 定义选项列表
            options = ['NULL','散点图', '柱状图', '点线图', '箱型图']
            # 显示列表选择框
            selected_option = st.selectbox('请选择一个选项：', options)
            # 显示用户选择的选项
            st.write('您选择的选项是：', selected_option)
            # 绘图
            st.subheader('选择图表形式')
            if selected_option == '散点图':
                fig = plot_scatter_chart(df)
                st.pyplot(fig)
                if st.button('保存'):
                    output_path = "散点图.pdf"  # 指定保存的图像文件路径和名称
                    fig.savefig(output_path, dpi=600, bbox_inches='tight')
                    st.write('已保存')
            elif selected_option == '柱状图':
                fig = plot_bar_chart(df)
                st.pyplot(fig)
                if st.button('保存'):
                    output_path = "柱状图.pdf"  # 指定保存的图像文件路径和名称
                    fig.savefig(output_path, dpi=600, bbox_inches='tight')
                    st.write('已保存')
            elif selected_option == '点线图':
                fig = plot_pointline_chart(df)
                st.pyplot(fig)   
                if st.button('保存'):
                    output_path = "点线图.pdf"  # 指定保存的图像文件路径和名称
                    fig.savefig(output_path, dpi=600, bbox_inches='tight')
                    st.write('已保存')
            elif selected_option == '箱型图':
                fig = plot_boxplot_chart(df)
                st.pyplot(fig)   
                if st.button('保存'):
                    output_path = "箱型图.pdf"  # 指定保存的图像文件路径和名称
                    fig.savefig(output_path, dpi=600, bbox_inches='tight')
                    #st.write('已保存')
                    st.markdown(f'<a href="{output_path}" download>点击这里下载</a>', unsafe_allow_html=True)
            else:
                st.write('请选择正确的作图类型')
        # 显示图像文件下载链接
        #st.subheader('保存生成的图像文件')
            #st.markdown(f'<a href="{output_path}" download>点击这里下载</a>', unsafe_allow_html=True)
        #else:
            #st.write('点击保存')
        

# 运行主函数
if __name__ == '__main__':
    main()