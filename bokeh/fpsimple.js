// define and solve system of equations to get coefficients A
function getA(N,M,L,wMin,wMax,shape,Tx,Ty,h1,h2,q) {
  var xSYS    = Bokeh.LinAlg.linspace(0, L, M)
  var ySYS = []

  for (var j = 0; j < M; j++) {
      ySYS[j]    = fNorth(xSYS[j],L,wMin,wMax,shape)
  }
  
  var Umtx    = fUfull([...Array(N+1).keys()],xSYS,ySYS,wMin,wMax,L,Tx,Ty)
  var Fvec    = fFfull(xSYS,ySYS,L,h1,h2,q,Tx)

  var rhs = [];
  for (var j = 0; j < N+1; j++) {
      rhs[j] = 0
      for (var i = 0; i < M; i++) {
          rhs[j] += Fvec[i]*Umtx[j][i]
      }
  }

  var lhs = [];
  for (var i = 0; i < N+1; i++) {
      lhs.push([]);
      for (var k = 0; k < N+1; k++) {
          lhs[i][k] = 0
          
          for (var j = 0; j < M; j++) {
              lhs[i][k] += Umtx[i][j]*Umtx[k][j]
          }
      }
  }
  
  return linSolv(lhs,rhs)
}

// solve a system of equations
function linSolv(A,b) {
  return math.multiply(math.multiply(math.inv(math.multiply(math.transpose(A),A)),math.transpose(A)),b);
}

// retrieve fields of hydraulic head and stream function 
function getFields(L,wMin,wMax,shape,h1,h2,A,Tx,Ty) {
  const dX      = 25*Math.min(wMax,L)
  const xSc     = Bokeh.LinAlg.linspace(0, L, Math.ceil(dX/wMax))
  const ySc     = Bokeh.LinAlg.linspace(0,1, Math.ceil(dX/L))
  var hField = []
  var pField = []
  
  var pMin = Infinity
  var pMax = Number.NEGATIVE_INFINITY

  for (var i = 0; i < ySc.length; i++) {
      hField.push([]);
      pField.push([]);
      for (var j = 0; j < xSc.length; j++) {
          var x = xSc[j]
          var y = ySc[i]*fNorth(xSc[j],L,wMin,wMax,shape)
          
          var [h, p] = getHP(x,y,h1,h2,L,wMin,wMax,Tx,Ty,A)

          hField[i][j] = h
          pField[i][j] = p
          
          pMin = Math.min(pMin,pField[i][j])
          pMax = Math.max(pMax,pField[i][j])
      }
  }

  return [hField,pField,pMin,pMax];
}

// retrieve single values of hydraulic head or stream function at single point (x|y)
function getHP(x,y,h1,h2,L,wMin,wMax,Tx,Ty,A) {
  var h = h1+(h2-h1)*x/L
  var p = A[0]+(h2-h1)*y/L

  for (var k = 1; k < A.length; k++) {
      var c   = k*Math.PI/L
      var kap = Math.sqrt(Tx/Ty)
      var a1  = Math.exp(c*kap*(y-wMax))
      var a2  = Math.exp(c*kap*(-y-wMax))
      
      var lowr = ( 1 + Math.exp(-2*kap*c*wMax) )
      h += A[k]*(a1-a2)/lowr*Math.sin(c*x)
      p += A[k]*(a1+a2)/lowr*Math.cos(c*x)/kap
  }

  p = -p*Tx

  return [h, p]
}

// determine exchange flux
function getQex(h1,h2,L,wMin,wMax,Tx,Ty,A) {
  var x = Bokeh.LinAlg.linspace(0,L,100)
  
  var ps = []
  for (var i = 1; i < x.length; i++) {
    var [h,p] = getHP(x[i],0,h1,h2,L,wMin,wMax,Tx,Ty,A)
    ps.push(p)
  }
  
  const first = Math.min(ps[0],ps[ps.length-1])
  // we need to destructure array to get min of it
  const last =  Math.min(...ps)
  
  return first - last
}

// get a set of isolines
function getIsolines(field,lvls,L,wMin,wMax,shape) {
  const options = {polygons: false, linearRing: false, noFrame: true}
  var isos = MarchingSquaresJS.isoLines(field, lvls, options);
  
  // iterate over contour levels
  var Xs = []
  var Ys = []
  
  var sclX    = field[0].length-1
  var sclY    = field.length-1

  for (var i = 0; i < isos.length; i++) {
      var theLin = isos[i]
      // add line to output
      Xs.push([]);
      Ys.push([]);
      
      // iterate over segments
      for (var j = 0; j < theLin.length; j++) {
          var theSeg = theLin[j]
          // iterate over points
          for (var k = 0; k < theSeg.length; k++) {
              var xVal = theSeg[k][0]*L/sclX
              Xs[i].push(xVal)
              Ys[i].push(theSeg[k][1]*fNorth(xVal,L,wMin,wMax,shape)/sclY)    
          }
          Xs[i].push(NaN)
          Ys[i].push(NaN)
      }
  }

  return [Xs,Ys];
}

// get a single isoline
function getIsoline(field,lvl,L,wMin,wMax,shape) {
  const options = {polygons: false, linearRing: false, noFrame: true}
  var iso = MarchingSquaresJS.isoLines(field, lvl, options);
  
  // iterate over contour levels
  var Xs = []
  var Ys = []
  
  var sclX    = field[0].length-1
  var sclY    = field.length-1

  for (var j = 0; j < iso.length; j++) {
    // iterate over points
    for (var k = 0; k < iso[j].length; k++) {
      var xVal = iso[j][k][0]*L/sclX
      var yVal = iso[j][k][1]*fNorth(xVal,L,wMin,wMax,shape)/sclY
      Xs.push(xVal)
      Ys.push(yVal)    
    }
  }

  return [Xs,Ys];
}

// define northern boundary shape
function fNorth(x,L,wMin,wMax,val) {
  var y = []
  var xL = x/L
  if (val==1) {
        y = wMin+(wMax-wMin)*Math.exp(1-1/(1-(2*xL-1)**2+1e-9))
    } else if (val==0) {
        y = wMin+0.5*(wMax-wMin)*(1-Math.cos(2*Math.PI*xL))
    } else if (val==2) {
      if (xL >= 1/40 && xL <= 15/40) {
        y = wMin+(wMax-wMin)*0.5*(   (1-Math.cos(Math.PI/(14/40)*(xL-1/40))) )
      } else if (xL >= 25/40 && xL <= 39/40) {
        y = wMin+(wMax-wMin)*0.5*(   (1+Math.cos(Math.PI/(14/40)*(xL-25/40))) )
      } else if (xL >= 15/40 && xL < 25/40) {
        y = wMax
      } else {
        y = wMin
      }
    }

  return y
}

// get U-values of system of equations
function fU(n,x,y,wMin,wMax,L,Tx,Ty) {
  var c = n.map(temp => temp * Math.PI/L)
  
  const kap = 1
  var v = [];

  for (var j = 0; j < n.length; j++) {
    v.push([]);
    for (var i = 0; i < x.length; i++) {
      var b1 = c[j]*kap*(y[i]-wMax)
      var b2 = c[j]*kap*(-y[i]-wMax)
      var b3 = c[j]*x[i]
      v[j][i] = Math.exp(b1)+Math.exp(b2)
      v[j][i] = v[j][i]/(1+Math.exp(-2*kap*c[j]*wMax))
      v[j][i] = v[j][i]*Math.cos(b3)
    }
  }
  return v
}

function fF(x,y,L) {
  var F = x.slice()
  for (var i = 0; i < x.length; i++) {
    F[i] = -1/L*y[i]
  }
  return F
}

// determine the advective velocity at a location (x,y)
function velocity(x,y,A,Tx,Ty,L,wMax,h1,h2,por) {
  
  const kap = Math.sqrt(Tx/Ty)

  // evaluate qx
  var qx = (h2-h1)/L
  for (var j = 1; j < A.length; j++) {
    var c = j*Math.PI/L
    qx +=  A[j] * Math.cos(c*x) * Math.sinh(c*kap*y)*c / Math.cosh(c*kap*wMax)
  }
  qx = -Tx*qx

  // evaluate qy
  var qy = 0
  for (var j = 1; j < A.length; j++) {
    var c = j*Math.PI/L
    qy +=  A[j] * Math.sin(c*x) * Math.cosh(c*kap*y)*c *kap/ Math.cosh(c*kap*wMax)
  }
  qy = -Ty*qy


  // get v
  var v = Math.hypot(qx,qy)
  return v/por
}

// determine the area of a polygon
function polyarea(x,y) {
  var Area = 0.5* ( x[0]-x[x.length-1] )* ( y[0]+y[y.length-1] )

  for (i = 1; i < x.length; i++ ) {
    Area = Area + 0.5* ( x[i]-x[i-1] )* ( y[i]+y[i-1] )
  }

  Area = Math.abs(Area)

  return Area
}


// retrieve a travel time distribution
function getTTD(pField,L,wMin,wMax,h1,h2,Tx,Ty,A,shape,por) {
  var [,p1] = getHP(0,0,h1,h2,L,wMin,wMax,Tx,Ty,A)
  var [,p2] = getHP(L,0,h1,h2,L,wMin,wMax,Tx,Ty,A)

  // get lower limit value
  const psiH = Math.min(p1,p2);

  // get upper limit value
  var psiL = Infinity
  const res = 120
  for (i = 0; i < res+1; i++ ) {
    var [,pT] = getHP(i/res*L,0,h1,h2,L,wMin,wMax,Tx,Ty,A)
    psiL = Math.min(psiL,pT)
  }
  
  const k = 49
  var lvls = Bokeh.LinAlg.linspace(psiL,psiH,k+1)
  lvls.shift()

  var [Xs,Ys] = getIsolines(pField,lvls,L,wMin,wMax,shape)

  var t = [0]
  var f = [0]

  const sum = (arr=[]) => arr.reduce((total, val) => total + val);
  // iterate over all lines
  for (var j = 0; j < Xs.length; j++) {
    var xT = Xs[j]
    var yT = Ys[j]
    var dt = 0

    // iterate over all segments
    for (var i = 1; i < xT.length-1; i++) {
      // evaluate v at i
      var v1 = velocity(xT[i],yT[i],A,Tx,Ty,L,wMax,h1,h2,por)
      // evaluate v at i-1
      var v2 = velocity(xT[i-1],yT[i-1],A,Tx,Ty,L,wMax,h1,h2,por)
      
      var ds = Math.hypot( xT[i]-xT[i-1], yT[i]-yT[i-1]  )
      var vM = 0.5*v1+0.5*v2
      dt += ds/vM
    }
    t.push(dt);
    f.push(lvls[j]-psiL);
  }

  for (var j = 0; j < f.length; j++) {
    f[j] = f[j]/f[f.length-1]  
  }

  return [t,f];
} 

// get U-values of system of equations
function fUfull(n,x,y,wMin,wMax,L,Tx,Ty) {
  var c = n.map(temp => temp * Math.PI/L)
  
  const kap = Math.sqrt(Tx/Ty)
  var v = [];

  for (var j = 0; j < n.length; j++) {
    v.push([]);
    for (var i = 0; i < x.length; i++) {
      var b1 = c[j]*kap*(y[i]-wMax)
      var b2 = c[j]*kap*(-y[i]-wMax)
      var b3 = c[j]*x[i]
      v[j][i] = Math.exp(b1)+Math.exp(b2)
      v[j][i] = v[j][i]/(1+Math.exp(-2*kap*c[j]*wMax))
      v[j][i] = v[j][i]*Math.cos(b3)/kap
    }
  }
  return v
}

// get F values of system of equations
function fFfull(x,y,L,h1,h2,q,Tx) {
  var F = x.slice()
  for (var i = 0; i < x.length; i++) {
    F[i] = -q*x[i]/Tx+(h1-h2)/L*y[i]
  }
  return F
}

// determine the advective velocity at a location (x,y)
function velocityfull(x,y,A,Tx,Ty,L,wMax,h1,h2,por) {
  
  const kap = Math.sqrt(Tx/Ty)

  // evaluate qx
  var qx = (h2-h1)/L
  for (var j = 1; j < A.length; j++) {
    var c = j*Math.PI/L
    qx +=  A[j] * Math.cos(c*x) * Math.sinh(c*kap*y)*c / Math.cosh(c*kap*wMax)
  }
  qx = -Tx*qx

  // evaluate qy
  var qy = 0
  for (var j = 1; j < A.length; j++) {
    var c = j*Math.PI/L
    qy +=  A[j] * Math.sin(c*x) * Math.cosh(c*kap*y)*c *kap/ Math.cosh(c*kap*wMax)
  }
  qy = -Ty*qy


  // get v
  var v = Math.hypot(qx,qy)
  return v/por
}

// determine the area of a polygon
function polyareafull(x,y) {
  var Area = 0.5* ( x[0]-x[x.length-1] )* ( y[0]+y[y.length-1] )

  for (i = 1; i < x.length; i++ ) {
    Area = Area + 0.5* ( x[i]-x[i-1] )* ( y[i]+y[i-1] )
  }

  Area = Math.abs(Area)

  return Area
}
