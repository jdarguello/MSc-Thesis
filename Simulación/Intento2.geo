//---Dimensiones---
D = 0.2;       //Diámetro interno en m
H = 0.3;       //Altura zona de lodos
A = 0.25;       //Ancho del panel de lamelas
AL = 0.1;      //Ancho de una lamela

Lx = 0.1;    //Ancho de una lamela (depende de la inclinación)
Ly = 0.15;    //Altura de una lamela (depende del ángulo)

mallaMax = 0.01;   //Tamaño máximo de malla
mallaMin = mallaMax;   //Tamño mínimo de malla

espesor = 0.1;    //Espesor de la geometría (tamaño de una partícula)

//---Geometría---
//Puntos
Point(1) = {0,0,0, mallaMax};
Point(2) = {0,-D,0, mallaMax};
Point(3) = {0.5*D,-D,0, mallaMax};
Point(4) = {0.5*D,-D-H, 0, (mallaMin + mallaMax)/2};
Point(5) = {0.5*D+A, -D-H,0, (mallaMin + mallaMax)/2};
Point(6) = {0.5*D+A,0,0, mallaMin};
Point(7) = {0.5*D+A+Lx,Ly,0, mallaMin};
Point(8) = {0.5*D+A+Lx-AL,Ly,0, mallaMin};
Point(9) = {0.5*D+A-AL,0,0, mallaMin};

//Líneas
Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,5};
Line(5) = {5,6};
Line(6) = {6,7};
Line(7) = {7,8};
Line(8) = {8,9};
Line(9) = {9,1};


//Mallado
Line Loop(10) = {1,2,3,4,5,6,7,8,9};
Plane Surface(11) = {10};

//Refinamiento de malla
Transfinite Curve {6, 8} = 100 Using Progression 1;

Recombine Surface {11};


//Extrusión
surfaceVector[] = Extrude {0,0,espesor} {
 Surface{11};
 Layers{1};
 Recombine;
};



//Nombre de las superficies!
Physical Surface("muro-1") = surfaceVector[0];
Physical Volume("fluido") = surfaceVector[1];
Physical Surface("ingreso") = surfaceVector[2];
Physical Surface("salida") = surfaceVector[8];
Physical Surface("muro-2") = surfaceVector[3];
Physical Surface("muro-3") = surfaceVector[4];
Physical Surface("muro-4") = surfaceVector[5];
Physical Surface("muro-5") = surfaceVector[6];
Physical Surface("muro-6") = surfaceVector[7];
Physical Surface("muro-7") = surfaceVector[9];

