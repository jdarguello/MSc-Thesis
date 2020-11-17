//---Dimensiones---
D = 0.27;       //Diámetro interno en m
H = 0.2;       //Altura zona de lodos
A = 0.25;       //Ancho del panel de lamelas
AL = 0.025;      //Ancho de una lamela

Lx = 0.11547;    //Ancho de una lamela (depende de la inclinación)
Ly = 0.2;    //Altura de una lamela (depende del ángulo)

mallaMax = 0.02;   //Tamaño máximo de malla
mallaMin = 231;   //Subdivisiones de refinamiento de malla

espesor = 0.001;    //Espesor de la geometría (tamaño de una partícula)

//---Geometría---
//Puntos
Point(1) = {0,0,0, mallaMax};
Point(2) = {0,-D,0, mallaMax};
Point(3) = {0.5*D,-D,0, mallaMax};
Point(4) = {0.5*D,-D-H, 0, mallaMax};
Point(5) = {0.5*D+A, -D-H,0, mallaMax};
Point(6) = {0.5*D+A,0,0, mallaMax};
Point(7) = {0.5*D+A+Lx,Ly,0, mallaMax};
Point(8) = {0.5*D+A+Lx-AL,Ly,0, mallaMax};
Point(9) = {0.5*D+A-AL,0,0, mallaMax};

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
Transfinite Curve {6, 8} = mallaMin Using Progression 1;

Recombine Surface {11};

Physical Surface("back") = {11};



//Extrusión
surfaceVector[] = Extrude {0,0,espesor} {
 Surface{11};
 Layers{1};
 Recombine;
};


/* surfaceVector contains in the following order:
    [0]	- front surface (opposed to source surface)
    [1] - extruded volume
    [2] - bottom surface (belonging to 1st line in "Line Loop (6)")
    [3] - right surface (belonging to 2nd line in "Line Loop (6)")
    [4] - top surface (belonging to 3rd line in "Line Loop (6)")
    [5] - left surface (belonging to 4th line in "Line Loop (6)") */

//Nombre de las superficies!
Physical Surface("front") = surfaceVector[0];
Physical Volume("fluido") = surfaceVector[1];
Physical Surface("ingreso") = surfaceVector[2];
Physical Surface("salida") = surfaceVector[8];
//Physical Surface("muro-2") = surfaceVector[3];
//Physical Surface("muro-3") = surfaceVector[4];
//Physical Surface("muro-4") = surfaceVector[5];
//Physical Surface("muro-5") = surfaceVector[6];
//Physical Surface("muro-6") = surfaceVector[7];
//Physical Surface("muro-7") = surfaceVector[9];
//Physical Surface("muro-8") = surfaceVector[10];
//Physical Surface("muro-9") = surfaceVector[11];
