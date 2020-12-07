//---Dimensiones---
D = DD;       //Diámetro interno en m
L = LLL;      //Largo de la boca
H = HH;       //Altura zona de lodos
A = AA;       //Ancho del panel de lamelas
AL = ALL;      //Ancho de una lamela

Lx = XXX;    //Ancho de una lamela (depende de la inclinación)
Ly = YYY;    //Altura de una lamela (depende del ángulo)

deltax = DELTA;    //Espacio entre lamelas
NL = NUML;        //Número de lamelas

mallaMax = malMax;   //Tamaño máximo de malla
mallaMin = REF;   //Subdivisiones de refinamiento de malla

espesor = ESP;    //Espesor de la geometría (tamaño de una partícula)

//---Geometría---
//Puntos
Point(1) = {0,0,0, mallaMax};
Point(2) = {0,-D,0, mallaMax};
Point(3) = {L,-D,0, mallaMax};
Point(4) = {L,-D-H, 0, mallaMax};
Point(5) = {L+A, -D-H,0, mallaMax};
Point(6) = {L+A,0,0, mallaMax};

//Líneas
Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,5};
Line(5) = {5,6};

ult = 6;    //Último punto conocido
xpos = L+A;
trans[] = {};
transcont = 0;
exits[] = {};
For contador In {0:NL-1}
    trans[transcont] = ult;
    transcont++;
    Point(ult+1) = {xpos+Lx,Ly,0, mallaMax};
    Line(ult) = {ult, ult+1};
    ult++;
    Point(ult+1) = {xpos+Lx-AL,Ly,0, mallaMax};
    Line(ult) = {ult, ult+1};
    exits[contador] = ult;
    ult++;
    trans[transcont] = ult;
    transcont++;
    Point(ult+1) = {xpos-AL,0,0, mallaMax};
    Line(ult) = {ult, ult+1};
    ult++;
    If (NL > 1 && contador < NL-1)
        Point(ult+1) = {xpos-AL-deltax,0,0, mallaMax};
        Line(ult) = {ult, ult+1};
        ult++;
    EndIf
    xpos = xpos-AL-deltax;
EndFor

Line(ult) = {ult, 1};


a[] = {};
For i In {1:ult}
    a[i-1] = i;
EndFor

Line Loop(ult+1) = a[];
Plane Surface(ult+2) = {ult+1};

Transfinite Curve trans[] = mallaMin Using Progression 1;

Recombine Surface {ult+2};

Physical Surface("back") = {ult+2};

surfaceVector[] = Extrude {0,0,espesor} {
 Surface{ult+2};
 Layers{1};
 Recombine;
};

//Nombre de las superficies!
Physical Surface("front") = surfaceVector[0];
Physical Volume("fluid") = surfaceVector[1];
Physical Surface("ingreso") = surfaceVector[2];

salidas[] = {};
For i In {0:NL-1}
    salidas[i] = surfaceVector[exits[i]+1];
EndFor

Physical Surface("salida") = salidas[];
//Physical Surface("salida") = surfaceVector[8];