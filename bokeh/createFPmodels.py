import numpy as np
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CheckboxButtonGroup, Panel, Tabs, CustomJS, Div, Slider, WheelZoomTool, RadioButtonGroup, FuncTickFormatter
from bokeh.plotting import Figure
from bokeh.embed import components
from colorcet import coolwarm
from bokeh.transform import linear_cmap
import re

for myCase in ["model1","model2","model2x","model5"]:
    print(myCase)
    # set up two figures (flow net and travel time distribution)
    figFN = Figure(tools="pan,reset,save,wheel_zoom",
                match_aspect=True,
                height_policy="fit",
                width_policy="fixed",
                width=1028,
                x_axis_label='x',
                y_axis_label='y')
    figFN.xgrid.grid_line_color = None
    figFN.ygrid.grid_line_color = None

    figFN.yaxis.major_label_text_font_size    = "25px"
    figFN.xaxis.major_label_text_font_size    = "25px"
    figFN.xaxis.axis_label_text_font_size     = "25px"
    figFN.yaxis.axis_label_text_font_size     = "25px"
    figFN.toolbar.logo                        = 'grey' # 'grey'/'normal'/None
    figFN.toolbar.active_scroll               = figFN.select_one(WheelZoomTool)
    figFN.toolbar.active_drag                 = None # disable pan, because it's bad on mobile

    figFN.outline_line_width = 2
    figFN.outline_line_alpha = 1.0
    figFN.outline_line_color = "black"

    # these settings define the sliders (min, max, ini, step)
    bL      = [100, 3000, 1000, 10]
    bX      = [0.0, 0.2, 90/1000, 0.2/100]
    bN      = [0.05, 0.35, 0.21, 0.6/100]
    bQ      = [0.0, 3.0, 0.0, 3/100]
    shapes  = ["cosinusoidal", "bump", "composite"]

    # define initial data set
    iniL        = 1000
    iniWmin     = 210.0
    x           = np.linspace(0,1000,50)
    yTop        = 0.7*300+0.5*(300-0.7*300)*(1-np.cos(2*np.pi*x/1000))
    yBot        = 0*x
    xI1         = np.linspace(0,iniL,11)
    yI1         = np.linspace(0,iniWmin,11)
    xI1         = xI1[1:-1]
    yI1         = yI1[1:-1]

    srcESW      = ColumnDataSource(data=dict(xW=np.array([0,0]), yW=np.array([0,iniWmin]),
                                                xE=np.array([iniL,iniL]), yE=np.array([0,iniWmin]),
                                                xS=np.array([0,iniL]), yS=np.array([0,0])))
    srcNorth    = ColumnDataSource(data=dict(x=x, y=yTop))


    x = np.array([0,41.666666666666664,83.33333333333333,125,166.66666666666666,208.33333333333334,250,291.6666666666667,333.3333333333333,375,416.6666666666667,458.3333333333333,500,541.6666666666666,583.3333333333334,625,666.6666666666666,708.3333333333334,750,791.6666666666666,833.3333333333334,875,916.6666666666666,958.3333333333334,999.9999999999967])
    yTop = np.array([0,0.6623254912820205,2.5911637026069623,5.620606462273126,9.499921466419499,13.924571663409727,18.568169116947065,23.110093706581107,27.256421559885393,30.754241382079183,33.400679012947556,35.04817501234715,35.607317718327884,35.04817501234714,33.400679012947556,30.754241382079183,27.25642155988541,23.110093706581107,18.568169116947008,13.924571663409676,9.499921466419464,5.620606462273072,2.591163702606907,0.6623254912819655,0])  
    yBot = 0*yTop
    srcHE       = ColumnDataSource(data=dict(x=x, yTop=yTop, yBot=yBot))

    srcHS       = ColumnDataSource(data=dict(x=x, yTop=yTop, yBot=yTop))


    xs2 = [[80.78525036402223,83.33333333333333,84.6021090031463,87.90309335573362,90.76484928637113,93.30360267084461,95.62316070034872,97.82205464159712,100.00000000000001,np.NaN],
    [165.4669262740441,166.66666666666666,172.60760657000966,178.67616918402965,183.8739181949402,188.41754694492695,192.49974012057817,196.30122670788452,200.00000000000003,np.NaN],
    [287.2722788375399,291.6666666666667,291.8751414859394,296.07469396805647,300.00000000000006,np.NaN,282.01929396303484,287.2722788375399,np.NaN,275.86537714961014,282.01929396303484,np.NaN,268.52928936481726,275.86537714961014,np.NaN,259.68144202439197,268.52928936481726,np.NaN],
    [370.1229757047856,375,377.24833727354985,383.09089093820853,387.75088230209343,391.54357826840396,394.71940573588046,397.4818297379248,400.00000000000006,np.NaN],
    [500,500,np.NaN,500,500,np.NaN,500,500,np.NaN,500,500,np.NaN,500,500,np.NaN,500,500,np.NaN,499.99999999999983,500,np.NaN],
    [602.5181702620753,600.0000000000001,np.NaN,605.2805942641197,602.5181702620753,np.NaN,608.4564217315962,605.2805942641197,np.NaN,612.2491176979067,608.4564217315962,np.NaN,616.9091090617917,612.2491176979067,np.NaN,622.7516627264501,616.9091090617917,np.NaN,625,622.7516627264501,np.NaN,629.8770242952147,625,np.NaN],
    [703.9253060319438,700.0000000000001,np.NaN,708.1248585140606,703.9253060319438,np.NaN,708.3333333333334,708.1248585140606,np.NaN,712.7277211624602,708.3333333333334,np.NaN,717.9807060369653,712.7277211624602,np.NaN,724.13462285039,717.9807060369653,np.NaN,731.4707106351829,724.13462285039,np.NaN,740.3185579756082,731.4707106351829,np.NaN],
    [803.6987732921156,800.0000000000001,np.NaN,807.5002598794218,803.6987732921156,np.NaN,811.5824530550732,807.5002598794218,np.NaN,816.12608180506,811.5824530550732,np.NaN,821.3238308159706,816.12608180506,np.NaN,827.3923934299905,821.3238308159706,np.NaN,833.3333333333334,827.3923934299905,np.NaN,834.533073725956,833.3333333333334,np.NaN],
    [902.1779453584028,900,np.NaN,904.3768392996514,902.1779453584028,np.NaN,906.6963973291554,904.3768392996514,np.NaN,909.235150713629,906.6963973291554,np.NaN,912.0969066442666,909.235150713629,np.NaN,915.3978909968538,912.0969066442666,np.NaN,916.6666666666666,915.3978909968538,np.NaN,919.2147496359777,916.6666666666666,np.NaN]]
    ys2 = [[215.67363996068494,195.00531522802868,185.32239617608462,154.7791898479947,124.06946138556472,93.22023982776452,62.25162720490362,31.176528192460115,0,np.NaN],
    [232.2068701240851,226.60591594886773,200.54575866384246,168.21565564149822,135.33519362551652,102.008234025683,68.31244665551388,34.30049451875763,0,np.NaN],
    [113.76103843200342,77.89026353180459,76.20108096866579,38.263729804612076,0,np.NaN,150.8527396577781,113.76103843200342,np.NaN,187.34365206305802,150.8527396577781,np.NaN,223.05189078592292,187.34365206305802,np.NaN,257.73567536610926,223.05189078592292,np.NaN],
    [285.82995721697426,258.711787863286,246.22810686620483,205.9968643919638,165.29388269217972,124.2641382572124,83.00236989440978,41.568960675163964,0,np.NaN],
    [42.857142857142854,0,np.NaN,85.71428571428571,42.857142857142854,np.NaN,128.57142857142858,85.71428571428571,np.NaN,171.42857142857142,128.57142857142858,np.NaN,214.28571428571428,171.42857142857142,np.NaN,257.14285714285717,214.28571428571428,np.NaN,300,257.14285714285717,np.NaN],
    [41.568960675163964,0,np.NaN,83.00236989440978,41.568960675163964,np.NaN,124.2641382572124,83.00236989440978,np.NaN,165.29388269217972,124.2641382572124,np.NaN,205.9968643919638,165.29388269217972,np.NaN,246.22810686620485,205.9968643919638,np.NaN,258.7117878632854,246.22810686620485,np.NaN,285.8299572169742,258.7117878632854,np.NaN],
    [38.26372980461207,0,np.NaN,76.20108096866579,38.26372980461207,np.NaN,77.8902635318041,76.20108096866579,np.NaN,113.76103843200342,77.8902635318041,np.NaN,150.85273965777807,113.76103843200342,np.NaN,187.34365206305802,150.85273965777807,np.NaN,223.05189078592292,187.34365206305802,np.NaN,257.7356753661092,223.05189078592292,np.NaN],
    [34.300494518757624,0,np.NaN,68.31244665551388,34.300494518757624,np.NaN,102.00823402568297,68.31244665551388,np.NaN,135.3351936255165,102.00823402568297,np.NaN,168.21565564149816,135.3351936255165,np.NaN,200.54575866384246,168.21565564149816,np.NaN,226.60591594886708,200.54575866384246,np.NaN,232.20687012408507,226.60591594886708,np.NaN],
    [31.17652819246012,0,np.NaN,62.25162720490361,31.17652819246012,np.NaN,93.2202398277645,62.25162720490361,np.NaN,124.06946138556472,93.2202398277645,np.NaN,154.7791898479947,124.06946138556472,np.NaN,185.32239617608462,154.7791898479947,np.NaN,195.0053152280279,185.32239617608462,np.NaN,215.67363996068494,195.0053152280279,np.NaN]]
    srcIsoH     = ColumnDataSource(data=dict(xs=xs2,ys=ys2,clr=[[0.9],[0.8],[0.7],[0.6],[0.5],[0.4],[0.3],[0.2],[0.1]]))

    xs = [[155.36777461853714,166.66666666666666,208.33333333333334,250,291.6666666666667,333.3333333333333,375,416.6666666666667,458.3333333333333,500,541.6666666666666,583.3333333333334,625,666.6666666666666,708.3333333333334,750,791.6666666666666,833.3333333333334,844.6322253814625,np.NaN],
    [0,41.666666666666664,83.33333333333333,125,166.66666666666666,208.33333333333334,245.8004813354393,250,291.6666666666667,333.3333333333333,375,416.6666666666667,458.3333333333333,500,541.6666666666666,583.3333333333334,625,666.6666666666666,708.3333333333334,750,754.19951866456,791.6666666666666,833.3333333333334,875,916.6666666666666,958.3333333333334,1000,np.NaN],
    [0,41.666666666666664,83.33333333333333,125,166.66666666666666,208.33333333333334,250,291.6666666666667,333.3333333333333,375,416.6666666666667,458.3333333333333,500,541.6666666666666,583.3333333333334,625,666.6666666666666,708.3333333333334,750,791.6666666666666,833.3333333333334,875,916.6666666666666,958.3333333333334,1000,np.NaN],
    [0,41.666666666666664,83.33333333333333,125,166.66666666666666,208.33333333333334,250,291.6666666666667,333.3333333333333,375,416.6666666666667,458.3333333333333,500,541.6666666666666,583.3333333333334,625,666.6666666666666,708.3333333333334,750,791.6666666666666,833.3333333333334,875,916.6666666666666,958.3333333333334,1000,np.NaN],
    [0,41.666666666666664,83.33333333333333,125,166.66666666666666,208.33333333333334,250,291.6666666666667,333.3333333333333,375,416.6666666666667,458.3333333333333,500,541.6666666666666,583.3333333333334,625,666.6666666666666,708.3333333333334,750,791.6666666666666,833.3333333333334,875,916.6666666666666,958.3333333333334,1000,np.NaN],
    [0,41.666666666666664,83.33333333333333,125,166.66666666666666,208.33333333333334,250,291.6666666666667,333.3333333333333,375,416.6666666666667,458.3333333333333,500,541.6666666666666,583.3333333333334,625,666.6666666666666,708.3333333333334,750,791.6666666666666,833.3333333333334,875,916.6666666666666,958.3333333333334,1000,np.NaN],
    [0,41.666666666666664,83.33333333333333,125,166.66666666666666,208.33333333333334,250,291.6666666666667,333.3333333333333,375,416.6666666666667,458.3333333333333,500,541.6666666666666,583.3333333333334,625,666.6666666666666,708.3333333333334,750,791.6666666666666,833.3333333333334,875,916.6666666666666,958.3333333333334,1000,np.NaN],
    [0,41.666666666666664,83.33333333333333,125,166.66666666666666,208.33333333333334,250,291.6666666666667,333.3333333333333,375,416.6666666666667,458.3333333333333,500,541.6666666666666,583.3333333333334,625,666.6666666666666,708.3333333333334,750,791.6666666666666,833.3333333333334,875,916.6666666666666,958.3333333333334,1000,np.NaN],
    [0,41.666666666666664,83.33333333333333,125,166.66666666666666,208.33333333333334,250,291.6666666666667,333.3333333333333,375,416.6666666666667,458.3333333333333,500,541.6666666666666,583.3333333333334,625,666.6666666666666,708.3333333333334,750,791.6666666666666,833.3333333333334,875,916.6666666666666,958.3333333333334,1000,np.NaN]]
    ys = [[0, 1.047802891830457, 5.446050029950791, 10.061800618006101, 14.576362617999568, 18.697608474415002, 22.174197107827894, 24.80453001534543, 26.4419832339068, 26.99771463884242, 26.441983233906786, 24.80453001534543, 22.174197107827894, 18.697608474415013, 14.576362617999568, 10.061800618006044, 5.446050029950736, 1.0478028918304285, 0, np.NaN ],
    [17.931837721111126, 18.60246113967142, 20.55552565505092, 23.623182542941553, 27.551682718082738, 32.03272371352507, 36.25896455010497, 36.73676096983185, 41.36800801861022, 45.63028637082452, 49.25146427937324, 52.00675572769775, 53.72876214588339, 54.31436848903418, 53.72876214588338, 52.00675572769776, 49.25146427937324, 45.63028637082455, 41.368008018610226, 36.73676096983179, 36.258964550105006, 32.03272371352502, 27.551682718082684, 23.6231825429415, 20.555525655050864, 18.602461139671362, 17.931837721111073, np.NaN ],
    [43.92907966880011, 44.61451618018794, 46.61592616114389, 49.77516323261593, 53.84884802260344, 58.533731128665565, 63.494571769677314, 68.39053783970017, 72.89786672032439, 76.72825961562684, 79.64333489751428, 81.46545394073287, 82.08514906369841, 81.46545394073284, 79.6433348975143, 76.72825961562684, 72.8978667203244, 68.3905378397002, 63.49457176967726, 58.53373112866553, 53.84884802260341, 49.775163232615874, 46.615926161143854, 44.614516180187884, 43.92907966880006, np.NaN ],
    [69.41199329068971, 70.13605793914545, 72.25397923039102, 75.60821106369376, 79.95281394434974, 84.97551459334856, 90.32370300912525, 95.63098346405572, 100.54179448272396, 104.73323677148495, 107.9339444589955, 109.93926949219578, 110.62208310620527, 109.93926949219578, 107.9339444589955, 104.73323677148493, 100.54179448272397, 95.63098346405573, 90.32370300912521, 84.97551459334854, 79.95281394434971, 75.6082110636937, 72.25397923039098, 70.13605793914539, 69.41199329068965, np.NaN ],
    [94.38432684069663, 95.17027206543771, 97.4717128426347, 101.1238854759321, 105.86669814173784, 111.36555512765476, 117.23786372481467, 123.08157440130144, 128.50238246247204, 133.1387374276316, 136.68468882022484, 138.90863635087513, 139.6663028756243, 138.90863635087513, 136.68468882022484, 133.1387374276316, 128.50238246247207, 123.08157440130144, 117.23786372481462, 111.36555512765473, 105.86669814173783, 101.12388547593206, 97.47171284263466, 95.17027206543763, 94.38432684069656, np.NaN ],
    [118.8090719854388, 119.68170780769869, 122.23849697627745, 126.29994890833198, 131.58049236700862, 137.71013621373228, 144.26390143390398, 150.7937633450456, 156.8583215483853, 162.0505030371184, 166.02451999257286, 168.51827139183038, 169.36812479576332, 168.51827139183038, 166.02451999257286, 162.05050303711838, 156.85832154838528, 150.7937633450456, 144.26390143390395, 137.71013621373228, 131.58049236700862, 126.29994890833197, 122.23849697627739, 119.6817078076986, 118.80907198543876, np.NaN ],
    [142.53308227421567, 143.5220892320157, 146.4226078245527, 151.03735983686548, 157.04766947570562, 164.03529224669734, 171.51705277457532, 178.98276806062793, 185.92686097442038, 191.87840387123669, 196.43634559329763, 199.29819069481655, 200.2740524206944, 199.29819069481655, 196.43634559329766, 191.87840387123666, 185.92686097442032, 178.98276806062793, 171.51705277457526, 164.0352922466973, 157.04766947570562, 151.0373598368654, 146.4226078245527, 143.52208923201562, 142.53308227421567, np.NaN ],
    [165.64937137207167, 166.78513515535533, 170.11853159799713, 175.42757865628133, 182.3473260789021, 190.39350462748772, 199.00856709688415, 207.60972941774165, 215.61710855123548, 222.48152656261522, 227.73695921164676, 231.03902373957285, 232.1666404196936, 231.0390237395729, 227.7369592116468, 222.4815265626152, 215.6171085512354, 207.60972941774165, 199.00856709688406, 190.39350462748772, 182.34732607890209, 175.42757865628127, 170.1185315979971, 166.78513515535528, 165.64937137207167, np.NaN ],
    [188.14311278201384, 189.45751263240646, 193.31839313175038, 199.4741659189431, 207.50108828329388, 216.82923427643058, 226.8100759898489, 236.7818312769704, 246.07932283246873, 254.0482333693505, 260.1420989834069, 263.97980221251595, 265.29649640776177, 263.97980221251606, 260.1420989834069, 254.04823336935047, 246.0793228324687, 236.7818312769703, 226.81007598984885, 216.82923427643058, 207.50108828329388, 199.4741659189431, 193.31839313175038, 189.4575126324064, 188.14311278201382, np.NaN]];

    srcIsoP     = ColumnDataSource(data=dict(xs=xs,ys=ys))
    mapper      = linear_cmap(field_name='clr', palette=coolwarm ,low=0,high=1)

    visFF = myCase != "model1"

    hIsoP   = figFN.multi_line(xs='xs',ys='ys', line_color='rgba(230,232,237, 1.0)',  line_width=5, source=srcIsoP,line_alpha=0.7,visible=visFF)
    hHS     = figFN.varea(x='x', y1='yTop',y2='yBot', source=srcHS, fill_alpha=0.4,fill_color=(201,174,105),visible=visFF)
    hHE     = figFN.varea(x='x', y1='yTop',y2='yBot', source=srcHE, fill_alpha=0.4,fill_color=(105,186,201),visible=visFF)
    hIsoH   = figFN.multi_line(xs='xs',ys='ys', line_color=mapper,  line_width=5, source=srcIsoH,line_alpha=1.0,visible=visFF)
    hW      = figFN.line(x='xW', y='yW', source=srcESW, line_width=5, color='rgba(192,2,6,1.0)', line_cap="round",visible=True)
    hE      = figFN.line(x='xE', y='yE', source=srcESW, line_width=5, color='rgba(32, 81, 219, 1.0)', line_cap="round",visible=True)
    hS      = figFN.line(x='xS', y='yS', source=srcESW, line_width=5, color='rgba(105,186,201,1.0)', line_cap="round",visible=True)
    hN      = figFN.line(x='x', y='y', source=srcNorth, line_width=5, color='rgba(201,174,105,1.0)', line_cap="round",visible=True)

    srcTex      = ColumnDataSource(data=dict(xW=[0], yW=[0.5*210], txtW=["h₁"],
                                                xE=[1000], yE=[0.5*210], txtE=["h₂"],
                                                xS=[500], yS=[0],txtS=["h₁ + (h₂-h₁) · x/L"],
                                                xN=[500], yN=[300],txtN=["q"]))

    
    visText = (myCase == "model1")
    hTw = figFN.text(x='xW',y='yW', source=srcTex, text='txtW',text_baseline="middle", text_align="left",text_font_size="25px",x_offset=12,visible=visText)
    hTe = figFN.text(x='xE',y='yE', source=srcTex, text='txtE',text_baseline="middle", text_align="right",text_font_size="25px",x_offset=-12,visible=visText)
    hTs = figFN.text(x='xS',y='yS', source=srcTex,text='txtS',text_baseline="bottom", text_align="center",text_font_size="25px",y_offset=-8,visible=visText)
    hTn = figFN.text(x='xN',y='yN', source=srcTex,text='txtN',text_baseline="top", text_align="center",text_font_size="25px",y_offset=15,visible=visText)

    # define sliders for input
    sliL            = Slider(start=bL[0], end=bL[1], value=bL[2], step=bL[3],
                        format=FuncTickFormatter(code="""return 'scale'"""),height=65,height_policy="fixed")
    sliLrat         = Slider(start=bX[0], end=bX[1], value=bX[2], step=bX[3],
                        format=FuncTickFormatter(code="""return 'widening'"""),height=65,height_policy="fixed")
    sliWrat         = Slider(start=bN[0], end=bN[1], value=bN[2], step=bN[3],
                        format=FuncTickFormatter(code="""return 'base width'"""),height=65,height_policy="fixed")
    sliQnor         = Slider(start=bQ[0], end=bQ[1], value=bQ[2], step=bQ[3],
                        format=FuncTickFormatter(code="""return 'influx'"""),height=65,height_policy="fixed")

    for sli in [sliL, sliLrat, sliWrat, sliQnor] :
        sli.bar_color   = '#63a6cc'

    #  define radio button group for shape selection
    radioGroup  = RadioButtonGroup(labels=shapes, active=0,margin=(10,3,10,3),height=50,height_policy="fixed")

    # define two check box button groups for visibility toggles
    toggles = CheckboxButtonGroup(labels=["west","south","east","north"], active=[0,1,2,3],margin=(10,3,10,3),height=50,height_policy="fixed")
    toggles.js_on_click(CustomJS(args=dict(hIsoP=hIsoP,hIsoH=hIsoH,hE=hE,hW=hW,hS=hS,hN=hN),code="""
        var act         = this.active
        hW.visible      = act.includes(0)
        hS.visible      = act.includes(1)
        hE.visible      = act.includes(2)
        hN.visible      = act.includes(3)
    """))

    toggles2 = CheckboxButtonGroup(labels=["heads","stream","zone south", "zone north"], active=[0,1,2,3],margin=(10,3,10,3),height=50,height_policy="fixed")
    toggles2.js_on_click(CustomJS(args=dict(hHE=hHE,hHS=hHS,hIsoP=hIsoP,hIsoH=hIsoH),code="""
        var act         = this.active
        hIsoH.visible   = act.includes(0)
        hIsoP.visible   = act.includes(1)
        hHE.visible     = act.includes(2)
        hHS.visible     = act.includes(3)
    """))


    # first callback; adapts changes to geometry
    with open('callbackGeometry.js','r') as file:
        cbCode = file.read()
    callbackG = CustomJS(args=dict( srcNorth=srcNorth,
                                    srcLin=srcESW,
                                    sliL=sliL,
                                    sliLrat=sliLrat,
                                    sliWrat=sliWrat,
                                    srcTex=srcTex,
                                    rG=radioGroup     ), code=cbCode)

    #  second callback; updates the flow field and results
    with open('callbackFlowSolution.js','r') as file:
        cbCode = file.read()
    callbackF = CustomJS(args=dict( sliQnor=sliQnor,
                                    sliL=sliL,
                                    sliLrat=sliLrat,
                                    sliWrat=sliWrat,
                                    srcIsoH=srcIsoH,
                                    srcHE=srcHE,
                                    srcHS=srcHS,
                                    srcIsoP=srcIsoP,
                                    rG=radioGroup     ), code=cbCode)

    # attach geometry callback to geometry properties
    for sli in [sliL,sliLrat,sliWrat] :
        sli.js_on_change('value',callbackG)
    radioGroup.js_on_click(callbackG)

    # attach flow field callback to all properties
    for sli in [sliL,sliLrat,sliWrat,sliQnor] :
        sli.js_on_change('value',callbackF)
    radioGroup.js_on_click(callbackF)

    if myCase == "model5":
        layout = column(sliL,
                    sliWrat,
                    sliLrat,
                    sliQnor,
                    radioGroup,width_policy="fixed", height_policy="min",width=411)
    else:
        layout = column(sliL,
                    sliWrat,
                    sliLrat,
                    radioGroup,width_policy="fixed", height_policy="min",width=411)

    # print the script to file
    script, (div1, div2) = components((layout,figFN))
    print(div1)
    print(div2)
    result = re.search('id="(.*)" data', div1)
    script = script.replace(result.group(1), myCase+"left")
    result = re.search('id="(.*)" data', div2)
    script = script.replace(result.group(1), myCase+"right")

    f = open("./"+myCase+".js", "w")
    script = "\n".join(script.split("\n")[1:-2])
    f.write(script)
    f.close()