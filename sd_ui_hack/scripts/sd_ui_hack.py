import os
import gradio as gr  
import json
import glob
import re
import site  
import fileinput

import modules.scripts as scripts
from modules import script_callbacks
from modules.ui_components import ResizeHandleRow

def keep_yushe(u_id,lis):#预设保存
    global shuju,data_id
    map_=shuju['原始预设'].copy()
    shu=0;lis_=lis[:-2]
    for i in map_.keys():
        if i=='base':
            map_[i]=lis[-2]
            continue
        if i=='default':
            map_[i]=lis[-1]
            continue
        for j in map_[i].keys():
            map_[i][j]=lis_[shu]
            shu+=1
    with open(f'{data_id}\\{u_id}.json', 'w') as f:  
        json.dump(map_, f)
    return map_
def data_th(seek):#应用设定
    global colors_id,base_id,default_id,index_2,index_3
    with open(colors_id, "r") as f:
        data = f.read()
    for x in seek.keys():
        if x=='base':
            data_th_23(base_id,index_2,seek[x])
            continue
        if x=='default':
            data_th_23(default_id,index_3,seek[x])
            continue
        data_x=re.search(f'{x} = Color\\(\n    name="{x}",\n(.*?)\n\\)', data, re.S).group(1)
        for i in seek[x].keys():
            data_x=re.sub(f'c{i}="(.*?)",',f'c{i}="{seek[x][i]}",',data_x, re.S)
        data=re.sub(re.search(f'{x} = Color\\(\n    name="{x}",\n(.*?)\n\\)', data, re.S).group(1),data_x,data, re.S)
    with open(colors_id, "w") as j:
        j.write(data)
def data_th_23(u_id,index,seek):#应用设定2-3
    with open(u_id, "r") as f:
        data = f.read()
    data_1=re.search(index[0], data, re.S).group(1)
    data_x=re.sub(f'{index[1]}"(.*?)"',f'{index[1]}"{seek}"',data_1, re.S)
    for line in fileinput.input(u_id, inplace=True):  
        print(line.replace(data_1, data_x), end='')
def yushe(data):#获取预设
    global shuju
    lis=[];base='';default=''
    for i in shuju[data].keys():
        if i=='base':
            base=shuju[data][i]
            continue
        if i=='default':
            default=shuju[data][i]
            continue
        for x in shuju[data][i].values():
            lis.append(x)
    lis.append(base)
    lis.append(default)
    return lis[:]
def yushe_lis():#获取预设列表
    lis=[]
    for i in shuju.keys():
        lis.append(i)
    return lis
def yushe_user(*lis):#自定义预设保存
    if lis[0]=='':
        return'请输入名字再试!!!!!'
    else:
        keep_yushe(lis[0],lis[1:])
        return '自定义预设已保存'

def keep(*lis):#go
    seek=keep_yushe('当前预设',lis)
    data_th(seek)
    return '设置成功'

#文件地址
colors_id=f"{site.getsitepackages()[1]}\\gradio\\themes\\utils\\colors.py"
base_id=f'{site.getsitepackages()[1]}\\gradio\\themes\\base.py'
default_id=f'{site.getsitepackages()[1]}\\gradio\\themes\\default.py'
data_id=f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\data'#数据存放位置

index_2=['self.background_fill_primary = background_fill_primary or getattr\\(\n(.*?)\n        \\)','self, "background_primary", ']#文件2，正则索引
index_3=['input_border_width="1px",\n(.*?),\n','input_background_fill=']#文件3，正则索引
shuju={}
for file in glob.glob(f'{data_id}\\*.json'):#获取全部预设文件
    with open(file, 'r') as f:  
        loaded_data = json.load(f)  
        shuju[file.split('\\')[-1].split('.')[0]]=loaded_data
ch_yushe=yushe('当前预设')

def on_ui_tabs():
    with gr.Blocks() as demo:
        with gr.Tab("界面颜色设置") as clean_up_tab, ResizeHandleRow(equal_height=False):
            with gr.Row():
                txt_1_1 = gr.ColorPicker(value=ch_yushe[0],label='生成键框上半截色')
                txt_1_3 = gr.ColorPicker(value=ch_yushe[1],label='生成键框下半截色')
                txt_1_2 = gr.ColorPicker(value=ch_yushe[2],label='生成键边框色')
                txt_1_6 = gr.ColorPicker(value=ch_yushe[3],label='生成键字体色')
            with gr.Row():
                txt_3= gr.ColorPicker(value=ch_yushe[16],label='输入框色')
                txt_2_0 = gr.ColorPicker(value=ch_yushe[4],label='鼠标点击输入框后外框高亮色')
                txt_2_3= gr.ColorPicker(value=ch_yushe[5],label='鼠标点击输入框后外框的内框高亮色(颜色不深不明显)')
                txt_2_6= gr.ColorPicker(value=ch_yushe[6],label='勾选框色')
                txt_3_3= gr.ColorPicker(value=ch_yushe[10],label='勾选框边框色')
            with gr.Row():
                txt_3_0= gr.ColorPicker(value=ch_yushe[7],label='图片展示框内外边填充色')
                txt_3_1 = gr.ColorPicker(value=ch_yushe[8],label='全部按键框上半截颜色')
                txt_3_2= gr.ColorPicker(value=ch_yushe[9],label='全部按键框下半截颜色+边框色')
            with gr.Row():
                txt_3_4= gr.ColorPicker(value=ch_yushe[11],label='字体色1')
                txt_3_5= gr.ColorPicker(value=ch_yushe[12],label='字体色2')
                txt_3_7= gr.ColorPicker(value=ch_yushe[13],label='字体色3')
                txt_3_8= gr.ColorPicker(value=ch_yushe[14],label='字体色4+鼠标放置高亮色')
            with gr.Row():
                txt_2= gr.ColorPicker(value=ch_yushe[15],label='主体背景填充色')
                error=gr.Textbox(value='',label='信息')
            with gr.Row():
                drop=gr.Dropdown(choices=shuju.keys(),label='预设选择',value=None)
                btn= gr.Button("确认使用设定")
            with gr.Accordion("自定义预设", open=False):
                with gr.Row():
                    name=gr.Textbox(label='请输入预设名字')
                    btn_=gr.Button("把当前设定添加到预设(记得为预设命名)")
            data_1=[txt_1_1,txt_1_3,txt_1_2,txt_1_6,
                    txt_2_0,txt_2_3,txt_2_6,
                    txt_3_0,txt_3_1,txt_3_2,txt_3_3,txt_3_4,txt_3_5,txt_3_7,txt_3_8,
                    txt_2,txt_3
                    ]
            drop.change(fn=yushe, inputs=drop, outputs=data_1)
            btn.click(keep, inputs=data_1, outputs=error)
            btn_.click(yushe_user, inputs=[name]+data_1, outputs=error)

# demo.launch()
        
        return (demo, "界面颜色设置",'112'),


script_callbacks.on_ui_tabs(on_ui_tabs)