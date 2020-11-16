SetFactory("OpenCASCADE");
Mesh.Algorithm = 8;
//---Dimensiones---
D = 0.2;       //Diámetro interno en m
H = 0.3;       //Altura zona de lodos
A = 0.25;       //Ancho del panel de lamelas
AL = 0.1;      //Ancho de una lamela

Lx = 0.1;    //Ancho de una lamela (depende de la inclinación)
Ly = 0.15;    //Altura de una lamela (depende del ángulo)

mallaMax = 0.01;   //Tamaño máximo de malla

inSubx = 5;        //Subdivisiones de malla en la entrada H
inSuby = 10;        //Subdivisiones de malla en la entrada V

intSubx = 5;       //Subdivisiones de malla en el cuerpo H.
intSuby = 10;       //Subdivisiones de malla en el cuerpo V.

lodosSubx = 5;     //Subdivisiones de malla en zona de lodos H 
lodosSuby = 10;     //Subdivisiones de malla en zona de lodos V

minSub = 400;      //Subdivisones de malla en salida

espesor = 0.1;    //Espesor de la geometría (tamaño de una partícula)

//---Superficies---
s0 = news;
Rectangle(s0) = {0,0,0, 0.5*D,-D};   //Entrada
Transfinite Surface {s0};

s1 = news;
Rectangle(s1) = {0.5*D,0,0,A, -D - H};
Transfinite Surface {s1};

bo1[] = BooleanUnion{Surface {s0}; Delete;} {Surface {s1}; Delete;};

/*
Transfinite Surface {bo1};
Recombine Surface {bo1};

ex1[] = Extrude{0,0,1}{
 Surface{bo1};
 Recombine;
};
*/


