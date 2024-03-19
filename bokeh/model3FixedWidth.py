from bokeh.layouts import column, row
from bokeh.models import Slider, ColumnDataSource, CustomJS, WheelZoomTool, CheckboxButtonGroup
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN
import pandas as pd
from bokeh.embed import file_html,components
import re
from bokeh.transform import linear_cmap
import colorcet as cc
import numpy as np

# define output file
output_file('trafo.html',title='dataset')

# read data sets
dfScatter   = pd.read_csv(r'./dataTrafo.csv')
dfScatter["x"] = dfScatter.L
dfScatter["y"] = dfScatter.wMax-dfScatter.wMin
dfScatter["alph"] = 0* dfScatter.wMax+0.8
srcSc       = ColumnDataSource(dfScatter)

sli        = Slider(start=0, end=1, value=0, step=0.01, tooltips=True, bar_color='rgba(60, 60, 60, 0.6)', margin=(25,10,10,10),title=None,height=20,width=500,height_policy="fixed", align="center")

fig1 = figure(  tools="pan,reset,save,wheel_zoom",
                x_axis_label='L',
                y_axis_label='Δw', width=1028)
fig1.yaxis.major_label_text_font_size    = "25px"
fig1.xaxis.major_label_text_font_size    = "25px"
fig1.xaxis.axis_label_text_font_size     = "25px"
fig1.yaxis.axis_label_text_font_size     = "25px"
fig1.toolbar.logo                        = 'grey' # 'grey'/'normal'/None
fig1.toolbar.active_scroll               = fig1.select_one(WheelZoomTool)
fig1.toolbar.active_drag                 = None # disable pan, because it's bad on mobile

mapper      = linear_cmap(field_name='Qex', palette=cc.CET_L12,low=np.min(dfScatter.Qex),high=np.max(dfScatter.Qex))

hDot = fig1.circle(x='x', y='y', source=srcSc, color=mapper, size=15, fill_alpha='alph',line_alpha=0)
fig1.yaxis.major_label_text_font_size    = "25px"
fig1.xaxis.major_label_text_font_size    = "25px"
fig1.xaxis.axis_label_text_font_size     = "20px"
fig1.yaxis.axis_label_text_font_size     = "20px"

x = np.linspace(0,1.0,40)
y = np.NaN*1/np.cosh(6.242*x)

srcLin = ColumnDataSource(data=dict(x=x,y=y))

sli.js_on_change('value', CustomJS(args=dict(sli=sli,srcSc=srcSc,axisX=fig1.xaxis[0],axisY=fig1.yaxis[0]),
    code="""
    var DAT = srcSc.data;
    var val = sli.value;

    if (val==0) {
        axisX.axis_label = "L";
        axisY.axis_label = "Δw";
    } else if (val == 1) {
        axisX.axis_label = "wMean/L";
        axisY.axis_label = "Qex · L / (Δw Δh Tx)";
    } else {
        axisX.axis_label = "Atot^" + val.toFixed(2) + " · L^" + (1-3*val).toFixed(2)
        axisY.axis_label = "(Qex · L)^" + val.toFixed(2) + " / (Δw^" + (2*val-1).toFixed(2) + " Δh Tx)"
    }
    
    var x = DAT['x'];
    var y = DAT['y'];
    var Atot = DAT['Atot'];
    var Qex = DAT['Qex'];
    var L = DAT['L'];
    var wMin = DAT['wMin'];
    var wMax = DAT['wMax'];

    for (var i = 0; i < x.length; i++) {
        x[i] = Math.pow(Atot[i],val)*Math.pow(L[i],1-3*val)
        y[i] = Math.pow(Qex[i],val)*Math.pow(L[i],val)*Math.pow(wMax[i]-wMin[i],1-2*val)
    }

    srcSc.change.emit();
    """))


layout    = column(fig1,sli,height_policy="fixed",height=700,width_policy="fixed",width=1028)


script, div1 = components(layout)
# print(script)
print(div1)

result = re.search('id="(.*)" data', div1)
script = script.replace(result.group(1), "model3")

f = open("./model3.js", "w")
script = "\n".join(script.split("\n")[1:-2])
f.write(script)
f.close()

# env = Environment(loader=FileSystemLoader(searchpath='./'))
# templ = env.get_template("template.html")

# html = file_html(layout,CDN,"geometry",template=templ)

# f = open("myTest.html", "w")
# f.write(html)
# f.close()
