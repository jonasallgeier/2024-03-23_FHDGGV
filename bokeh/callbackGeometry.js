var yNorth = srcNorth.data['y']
var xNorth = srcNorth.data['x']
var TEX = srcTex.data;


const L     = sliL.value
const wMin  = sliWrat.value*L
const wMax  = wMin+sliLrat.value*L
const val = rG.active

var yWt = TEX['yW']
var xWt = TEX['xW']
var yNt = TEX['yN']
var xNt = TEX['xN']
var yEt = TEX['yE']
var xEt = TEX['xE']
var xSt = TEX['xS']

yNt[0] = wMax
xNt[0] = 0.5*L
yWt[0] = 0.5*wMin
yEt[0] = 0.5*wMin
xEt[0] = L
xSt[0] = 0.5*L

for (var i = 0; i < xNorth.length; i++) {
    xNorth[i] = i/(xNorth.length-1)*L
    yNorth[i] = fNorth(xNorth[i],L,wMin,wMax,val)
}

srcLin.data['yW'][1] = wMin
srcLin.data['yE'][1] = wMin
srcLin.data['xE'][0] = L
srcLin.data['xE'][1] = L
srcLin.data['xS'][1] = L

srcLin.change.emit();
srcNorth.change.emit();
srcTex.change.emit();