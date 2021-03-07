import settings;
import fontsize;
//settings.tex="pdflatex";
//outformat="pdf";

settings.outformat="pdf";
settings.render=16;
size(16cm, 0);

import graph;
//---Ejes coordenados---
real x,y, flecha;
x = 200; y = x; flecha = x/40;
draw((0,0) -- (0,y+flecha), arrow=Arrow);
draw((0,0) -- (x+flecha,0), arrow=Arrow);

void Valores(real value, real h, real v, bool H = true) {
    real line = x/40;
    if (H) {
        draw((0,h) -- (-line,h), L=Label((string)value, position=EndPoint, align=W));
    } else {
        draw((v,0) -- (v,-line), L=Label((string)value, position=EndPoint, align=S));
    }
}

//Valores verticales
real suma = x;
for (int i=0; i < 5; i = i+1){
    Valores(suma, suma-x,0);
    suma = suma + 50;
}

//Valores horizontales
real valor = 2; suma = 0;
for (int i=0; i < 4; i = i+1){
    Valores(valor, 0,suma, false);
    suma = suma + 66.667;
    valor = valor+1;
}

//labels
real xx = x/10;
label(rotate(90)*"Temperatura $[K]$", (-xx,y/2));
label("Entropia $[kJ/kg K]$", (x/2,-xx/1.1));

//---Domo---
real f(real x) {return -(25/1024)*x^2 + (625/128)*x-(9225/64);}
draw(graph(f, 36,164,operator ..), dashed + rgb(88/255, 42/255, 127/255));

//30 MPa
draw((50,55) -- (105,165), dashdotted, L=rotate(65)*Label("$30 [MPa]$", position=0.76, align=N));
label("P1", (45,55));
draw((55,65) -- (82.5,120), arrow=Arrow, L=rotate(65)*Label("HE1", position=MidPoint, align=N));
draw((82.5,120) .. (100,95) .. (100,90), arrow=Arrow(), L=Label("RV1", position=BeginPoint, align=E));

//6 MPa
draw((120,90) -- (160,165), dashdotted, L=rotate(65)*Label("$6 [MPa]$", position=0.7, align=N));
draw((120,90)-- (126,101), arrow=Arrows, L=rotate(65)*Label("HE2", position=MidPoint, align=S));


draw((120,90) -- (80,90), arrow=Arrows, L=Label("C1", position=EndPoint, align=SE));
draw((80,90) .. (65,70) .. (55,50), arrow=Arrow());
draw((55,50)--(55,65));