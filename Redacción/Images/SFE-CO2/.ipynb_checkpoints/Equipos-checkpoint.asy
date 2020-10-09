import settings;
import fontsize;
//settings.tex="pdflatex";
//outformat="pdf";

settings.outformat="pdf";
settings.render=16;
size(16cm, 0);

import graph;

//E1
real a,h, fl; a = 1; h=3; fl=a/3;
draw(box((0,0), (a,h)));
draw((-fl,h/2) -- (0,h/2), arrow=Arrow, L=Label("Alimentacion", position=MidPoint, align=NW));
label("Extractor", (1.6*a,1.1*h/2));
label("E1", (1.2*a, 0.45*h));

//E1 - RV1
draw((a/2,h) -- (a/2,h+fl) -- (a/2+h,h+fl));

//RV1
real vh, va; vh = a/4; va = a/3;
real xr, yr; xr = a/2+h; yr = h+fl-vh/2;
draw((xr,yr) -- (xr,yr+vh) -- (xr+va,yr) -- (xr+va,yr+vh) -- (xr, yr));
label("RV1", (xr+va/2,yr+1.5*vh));

draw((xr+va,yr+vh/2) -- (xr+va+a/2,yr+vh/2));

//---Evaporadores y chillers---

void Eva(real x, real y) {
    real r = 1.5*vh;
    draw(circle((x+r,y), r));
    //M
    draw((x+r/4,y-2*r) -- (x+r/4,y+r/4) -- (x+r,y-r/2) -- (x+2*r-r/4, y+r/4) -- (x+2*r-r/4,y-2*r));
}

//HE2
xr = xr+2.5*va; yr = yr+vh/2;
Eva(xr,yr);
label("Evaporador HE2", (xr+2*(1.5*vh), yr + 2*vh));

xr = xr+2*(1.5*vh);
draw((xr,yr) -- (xr+h/2,yr) -- (xr+h/2,yr - h/2));

//S1
xr = xr+h/2; yr = yr - h/2;
draw((xr - a/2,yr) -- (xr + a/2, yr) -- (xr + a/2, yr-h/2) -- (xr, yr-h/2 - h/8) -- (xr - a/2, yr-h/2) -- cycle);
draw((xr, yr-h/2 - h/8) -- (xr, yr-h/2 - h/8 - fl), arrow=Arrow(), L=Label("Producto", position=EndPoint, align=S));
label("Separador", (xr+1.1*a,yr-h/4));
label("S1",(xr+0.65*a, yr-0.32*h));

xr = xr-a/2; yr = yr-h/4;
draw((xr, yr) -- (xr-a/3, yr) -- (xr-a/3, yr-h/2) -- (xr-2*a/3,yr-h/2));

//C1
xr = xr-2*a/3 - 2*(1.5*vh); yr = yr-h/2;
Eva(xr,yr);
label("C1", (xr+1.5*vh,yr+2*vh));

draw((xr, yr) -- (xr-a/2, yr));

//P1
real r = 1.5*vh;
xr = xr-a/2-r;
draw(circle((xr,yr), r));
draw((xr-r,yr) -- (xr+0.7*r,yr+0.7*r));
draw((xr-r,yr) -- (xr+0.7*r,yr-0.7*r));
label("Bomba P1", (xr,yr+2*vh));

xr = xr-r;
draw((xr,yr) -- (xr-a/2,yr));

//HE1
xr = xr-3.38*r;
Eva(xr,yr);
label("HE1", (xr+r,yr+2*vh));

draw((xr,yr) -- (a/2,yr) -- (a/2,0));