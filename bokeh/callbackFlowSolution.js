// retrieve current settings
const L     = sliL.value
const wMin  = sliWrat.value*L
const wMax  = wMin+sliLrat.value*L
const Tx    = 3e-3
const Ty    = 3e-3
const h2    = 0
const h1    = h2 + L*1e-3
const Q0    = (h1-h2)/L*Tx*(wMax-wMin)
const q     = sliQnor.value*Q0/L
const shape = rG.active
const por   = 1

// determine coefficients A
const N = 10
const M = 25
var A   = getA(N,M,L,wMin,wMax,shape,Tx,Ty,h1,h2,q)

// get fields of h and psi
const [hField, pField, pMin, pMax] = getFields(L,wMin,wMax,shape,h1,h2,A,Tx,Ty);

// extract contour line sets
var lvlsH = Bokeh.LinAlg.linspace(h2,h1,11)
lvlsH.shift()
lvlsH.pop()

const [XsH,YsH] = getIsolines(hField,lvlsH,L,wMin,wMax,shape)
srcIsoH.data['xs']  = XsH
srcIsoH.data['ys']  = YsH
for (var i = 0; i < lvlsH.length; i++) {
    lvlsH[i] = (lvlsH[i]-h2)/(h1-h2) 
} 
srcIsoH.data['clr'] = lvlsH

var lvlsP = Bokeh.LinAlg.linspace(pMin,pMax,11)
lvlsP.shift()
lvlsP.pop()
const [XsP,YsP] = getIsolines(pField,lvlsP,L,wMin,wMax,shape)
srcIsoP.data['xs'] = XsP
srcIsoP.data['ys'] = YsP

// extract single isoline for exchange zone (he) 
const [heX,heY] = getIsoline(pField,pField[0][0],L,wMin,wMax,shape)
    
if (heX.length==0) {
    srcHE.data['x'] = [0,L]
    srcHE.data['yBot']    = [0,0]
    srcHE.data['yTop']    = [0,0]
} else {
    srcHE.data['x']       = heX
    var heYbot = []
    for (var i = 0; i < heX.length; i++) {
       heYbot.push(0) 
    } 
    srcHE.data['yBot']    = heYbot
    srcHE.data['yTop']    = heY
}

// extract single isoline for hillslope zone (hs)
const pVal = pField[pField.length-1][0]
const [hsX,hsY] = getIsoline(pField,pVal,L,wMin,wMax,shape)

if (hsX.length==0) {
    srcHS.data['x'] = [0,L]
    srcHS.data['yBot']    = [0,0]
    srcHS.data['yTop']    = [0,0]
} else {
    const xMax = Math.max(...hsX)
    if ((xMax < L) && (Math.min(...hsY) < 0.001*wMin))  {
        for (var i = Math.ceil(20*xMax/L); i < 21; i++) {
            hsX.push(L*i/20)
            hsY.push(0)
        } 
    }
    srcHS.data['x']       = hsX
    var hsYtop = []
    for (var i = 0; i < hsX.length; i++) {
       hsYtop.push(fNorth(hsX[i],L,wMin,wMax,shape)) 
    } 
    srcHS.data['yBot']    = hsY
    srcHS.data['yTop']    = hsYtop
}

// determine exchange zone area
var xtemp1      = Array.from(srcHE.data['x'])
var ytemp1      = Array.from(srcHE.data['yBot'])
const xtemp2    = xtemp1.slice()
const ytemp2    = Array.from(srcHE.data['yTop'])
const xPoly     = xtemp1.concat(xtemp2.reverse())
const yPoly     = ytemp1.concat(ytemp2.reverse())
var Aex         = polyarea(xPoly,yPoly)

// define boolean to tell if zone exists
var Qex = getQex(h1,h2,L,wMin,wMax,Tx,Ty,A)
var zoneExists =  (Qex >= 1e-19)

// communicate updates
srcIsoH.change.emit();
srcIsoP.change.emit();
srcHE.change.emit();
srcHS.change.emit();