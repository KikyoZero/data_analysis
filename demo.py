import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
#from fpdf import FPDF
#from matplotlib.ticker import MaxNLocator
st.set_page_config(layout="wide")
# 解决streamlit不能显示中文的问题
mpl.font_manager.fontManager.addfont('font/simsun.ttc') 
mpl.font_manager.fontManager.addfont('font/times.ttf') 
sns.set_theme(context='notebook', style='ticks', palette='deep', font_scale=1, color_codes=True, rc=None )            
sns.set_style({'font.sans-serif':['simsun','times']}) # 适配中英文            
#plt.rcParams['xtick.direction'] = 'in' # 刻度朝内            
#plt.rcParams['ytick.direction'] = 'in'            
plt.rcParams['font.sans-serif'] = 'simsun' # 解决中文显示            
plt.rcParams['axes.unicode_minus'] = False # 解决符号无法显示
# 读取Excel文件并返回DataFrame对象
def read_excel(file_path):
    df = pd.read_excel(file_path)
    return df
# 主函数
def main():
    st.title('443科研论文图表绘制')
    # 创建两列布局
    col1, col2, col3= st.columns([1, 1, 2])
    with col1:
        st.header('文件上传及数据分析板块')
        st.subheader('注意事项')
        st.write('分组类型为Group列，X轴数据为X列，Y轴数据为Y列')
        st.write('建议按照示例表格放置数据。绘制图形的时候注意相关参数的选择，如散点图要选择点的形状不然会报错')
        if st.button('查看示例表格'):
            st.image('demo.jpg')
        st.subheader('读取Excel文件')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # 上传Excel文件
        file = st.file_uploader('上传Excel文件', type=['xlsx', 'xls'])
        if file is not None:
            # 读取Excel文件并删除空白列
            df = read_excel(file)
            df.dropna(axis=1, how='all', inplace=True)
                # 显示数据表格
        else:
            # 创建示例数据
            categories = ['A', 'B']
            repeats = [1, 1, 1, 2, 2, 2, 3, 3, 3]
            values = [10, 20]
            # 构建DataFrame
            data = {'Group': [], 'X': [], 'Y': []}
            for category in categories:
                for repeat in repeats:
                    data['Group'].append(category)
                    data['X'].append(repeat)
                    data['Y'].append(values[categories.index(category)])
            df = pd.DataFrame(data)
        st.subheader('数据表格')
        if st.button('查看表格数据'):
            st.dataframe(df)
        st.subheader('分组描述统计')
        #if st.button('分组描述统计'):
        st.dataframe(pd.DataFrame(df.groupby('Group').describe().round(2).T))                
        #st.subheader('结果展示')            
        st.subheader('多因素方差分析')
        def perform_anova(data):
                    # 创建一个线性模型
                model = ols(anovaformula, data=data).fit()
                        # 执行方差分析
                anova_table = sm.stats.anova_lm(model)
                        # 将结果转换为DataFrame
                anova_result = pd.DataFrame(anova_table)
                return anova_result
                #if st.button('方差分析结果'):
        anovaformula = st.text_input('请填写方差分析公式：','Y ~ Group * X')
        st.write('公式为：数值 ~ 分组1 * 分组2 * 分组n')
        anova_result = perform_anova(df)
            # 显示方差分析结果
        st.dataframe(anova_result)
    with col2:
            st.header('绘图参数版块')
            groupname = st.text_input('请输入分组：', 'Group')
            xname = st.text_input('请输入X列名：','X')
            yname = st.text_input('请输入Y列名：', 'Y')
            st.subheader('作图细节调整')
            plottitle = st.text_input('请输入标题：')
            xlabname = st.text_input('请输入X标题：','X')
            ylabname = st.text_input('请输入Y标题：','Y')
            xmins = st.number_input('X最小值：')
            xmaxs = st.number_input('X最大值：')
            ymins = st.number_input('Y最小值：',value= df[yname].min())
            ymaxs = st.number_input('Y最大值：',value= df[yname].max())
            # 获取用户输入的图像尺寸
            width = st.number_input('请输入图像宽度：', value=8.0, min_value=1.0, max_value=20.0, step=0.1)
            height = st.number_input('请输入图像高度：', value=6.0, min_value=1.0, max_value=20.0, step=0.1)
            # 定义颜色选项列表
            #coloroptions = ['NULL','Accent','Paired']   
            ecolor = st.text_input('请输入颜色类别：','Pastel1')
            st.write('色彩选项：Accent、Blues、BrBG、BuGn、BuPu、CMRmap、Dark2、GnBu、Greys、OrRd、Paired、Pastel1、Pastel2、PiYG等')
            # 定义散点形状选项列表
            spoptions = ['.','o','v','^','<','>','s','p','*','h','H','D','d','P','X']  
            shapepoint = st.multiselect('请选择散点形状：', spoptions)
            if st.button('查看形状列表'):
                st.image('param/makers.jpg', caption='Makers')
            # 定义线条类型选项列表
            ltyoptions = ['solid', 'dashed', 'dotted','dashdot','loosely dotted','densely dotted','dashdotted','dashdotdotted']
            lty = st.multiselect('请选择线条类型：', ltyoptions)
            if st.button('查看线条列表'):
                st.image('param/linetype.jpg', caption='Linetypes')

    with col3:
            st.header('绘图版块')
            st.subheader('关于')
            button_clicked = st.button('查看详情')
            if button_clicked:
                # 检查按钮点击状态
                if st.session_state.show_content:
                    # 如果按钮已点击并且内容已显示，隐藏内容
                    st.session_state.show_content = False
                else:
                    # 如果按钮已点击并且内容未显示，显示内容
                    st.session_state.show_content = True
            else:
                # 如果按钮未点击，初始状态为隐藏内容
                st.session_state.show_content = False
            if st.session_state.show_content:
                    st.subheader('作者详情')
                    st.write('作者：朱铁忠')
                    st.write('微信公众号：吐西瓜皮怎么吃西瓜')
                    st.write('源码和示例文档：https://github.com/KikyoZero/data_analysis')
                    st.subheader('版本更新历史如下')
                    st.write('2023年5月30日完成初版发表')
                    st.write('2023年5月31日添加箱型图绘制、保存')
                    st.write('2023年6月01日添加双因素方差分析')
                    st.write('2023年6月02日添加中文宋体支持、自定义列名、热图和相关性图')
                    st.write('2023年6月03日改双因素方差分析为多因素方差分析，添加图形保存格式选择')
                    st.write('2023年6月04日修改误差棒粗细')
            barlwd = st.number_input('边框：', value = 1.0, step= 0.1)
            errsize = st.number_input('误差棒宽度：', value = 0.1, step= 0.01)
            errlwd = st.number_input('误差棒粗度：', value = 1.0, step= 0.1)
            #绘制热图
            def heatmap_chart(df):
                fig, ax = plt.subplots(figsize=(width, height))
                sns.heatmap(df, center = 0.5,  cmap= ecolor)
                plt.xlabel(xlabname)
                plt.ylabel(ylabname)
                plt.title(plottitle)
                fig = plt.gcf()
                return fig
            # 绘制相关性图
            def pairplot_chart(df):
                # 创建图形对象，并设置尺寸
                fig, ax = plt.subplots(figsize=(width, height))
                sns.pairplot(df, hue=groupname,
                            palette = sns.color_palette(ecolor), 
                            markers = shapepoint
                            )
                plt.xlabel(xlabname)
                plt.ylabel(ylabname)
                plt.title(plottitle)
                plt.grid(False)
                # 去除图例背景
                plt.legend(loc='upper right', frameon=False)
                fig = plt.gcf()
                return fig
            # 绘制散点图
            def plot_scatter_chart(df):
                # 创建图形对象，并设置尺寸
                fig, ax = plt.subplots(figsize=(width, height))
                sns.scatterplot(x=df[xname],y=df[yname], hue=df[groupname], 
                                style=df[groupname], 
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
                sns.barplot(x=df[xname],y=df[yname], hue=df[groupname], 
                            errorbar ='sd', capsize =errsize,
                            errwidth= errlwd,
                            errcolor ='black',edgecolor ='black',
                            palette = sns.color_palette(ecolor), 
                            lw= barlwd, width =0.5)
                plt.title(plottitle)
                plt.xlabel(xlabname)
                plt.ylabel(ylabname)
                #plt.xlim([xmins-1, xmaxs])
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
                sns.pointplot(x=df[xname],y=df[yname], hue=df[groupname], 
                            palette = sns.color_palette(ecolor), 
                            capsize = errsize, errwidth = errlwd,markers = shapepoint, 
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
                sns.boxplot(x=df[xname],y=df[yname], hue=df[groupname], 
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
            # 定义选项列表
            options = ['NULL','散点图', '柱状图', '点线图', '箱型图', '热图' , '相关性图']
            # 显示列表选择框
            selected_option = st.selectbox('请选择一个选项：', options)
            # 显示用户选择的选项
            st.write('您选择的选项是：', selected_option)
            # 绘图
            st.subheader('选择图表形式')
            if selected_option == '散点图':
                fig = plot_scatter_chart(df)
            elif selected_option == '柱状图':
                fig = plot_bar_chart(df)
            elif selected_option == '点线图':
                fig = plot_pointline_chart(df)
            elif selected_option == '箱型图':
                fig = plot_boxplot_chart(df)
            elif selected_option == '热图':
                fig = heatmap_chart(df)
            elif selected_option == '相关性图':
                st.write('目前仍有缺陷，运行较慢，记得添加形状参数')
                fig = pairplot_chart(df)
            else:
                st.write('请选择正确的图片类型')
            st.pyplot(fig)
            figuertype = ['jpg', 'pdf', 'png', 'tif', 'tiff', 'eps', 'jpeg',  'pgf', 'ps', 'raw', 'rgba', 'svg', 'svgz', 'webp']
            selected_figuertype = st.selectbox('请选择保存的图片类型：', figuertype)
            st.write('保存的图表格式为：', selected_figuertype)
            output_path = "Figure"  # 指定保存的图像文件路径和名称
            plt.savefig(output_path, dpi=600, format = selected_figuertype,bbox_inches='tight')
            download_button(output_path)
        # 显示图像文件下载链接
        #st.subheader('保存生成的图像文件')
            #st.markdown(f'<a href="{output_path}" download>点击这里下载</a>', unsafe_allow_html=True)
        #else:
            #st.write('点击保存')
def download_button(output_path):
    # 创建下载按钮
    with open(output_path, 'rb') as file:
        contents = file.read()
        st.download_button('保存结果', data=contents, file_name='Figure')

# 运行主函数
if __name__ == '__main__':
    main()