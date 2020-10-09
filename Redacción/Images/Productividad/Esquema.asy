import settings;
import fontsize;
//settings.tex="pdflatex";
//outformat="pdf";

settings.outformat="pdf";
settings.render=16;
size(25cm, 0);

import graph;
//Destilador
real a, h;
a = 2;
h = a/2;
draw(box(0, (a,a)));
label("Destilador", (a/2,a/2));
draw((a,a){(a+h,a+h)} .. {right}((a+pi)/2,a+h));
draw(((a+pi)/2,a+h) -- ((a+pi)/2+h/8,a+h+h/8));
draw((0,a){(0,a+h)} .. {right}((a+pi)/2+h/8,a+h+h/8));
draw((a/2,0) -- (a/2,-a/2), arrow=Arrow, L=Label("Aceite esencial", position=EndPoint, align=S, rgb(245/255, 92/255, 92/255)));

//Dest - Secador
real fl = a/2;
draw((a,a/2) -- (a+fl, a/2), arrow=Arrow, L=Label("$m_v$", position=MidPoint, align=N));

//Secador
real x = 2*a+fl+h;
draw(box((a+fl, 0), (x,a)));
label("Secador", ((x-(a+fl))/2 + (a+fl),a/2));

//Molienda
draw((x, a/2) -- (x+fl, a/2), arrow=Arrow);
x = x+3*fl/2;
//Primer círculo
draw((x,0){left} .. (x-0.4,a/5) .. (x,a));
draw((x,0){right} .. (x+0.4,a/5) .. (x,a));

draw((x,0) -- (x+3*a/2,0));
draw((x,a) -- (x+3*a/2,a));
label("Molienda", (x+(3*a/2)/2,a/2));
draw((x+(x-3*a/2)/3,a+fl) -- (x+(x-3*a/2)/3, a), arrow=Arrow, L=Label("Agente Dispersante", position=BeginPoint, align=N));
x = x+3*a/2;
draw((x,0){right} .. (x+0.4,a/5) .. (x,a));

//Decantación
real y, H, xf;
x = x+0.48;
draw(((x,a/2) -- (x+3*fl,a/2)), arrow=Arrow, L=Label("Elucion - Filtrado", position=MidPoint, align=N));

x = x+fl+2;
y = -1;
H = 3;
xf = 2*a/5;
draw((x+xf,2*y) -- (x+xf,3*y/2) -- (x,y) -- (x,y+H));
//xf = x+a/2;
draw((x,y+H) .. (x+a/4,y+H+H/20) .. (x+a/2,y+H).. (x+3*a/4,y+H-H/20) .. (x+a, y+H));
draw((x+a/2,y+H) .. (x+3*a/4,y+H+H/20) .. (x+a,y+H));
draw((x+a,y+H) -- (x+a,y) -- (x+a-xf,3*y/2) -- (x+a-xf,2*y));
draw(box((x+a-xf,2*y + y/2+a/10),(x+xf,3*y)));
//Decantación - llave
draw((x+xf/2,2*y + y/2 + a/10) -- (x,2*y + y/2) -- (x,2*y+a/10) -- (x+xf/2,2*y) -- (x+a-xf/2,2*y) -- (x+a, 2*y+a/10) -- (x+a,2*y + y/2) -- (x+a-xf/2,2*y + y/2+a/10) -- (x+xf/2,2*y + y/2 + a/10));

draw((x+a/2,y+H+fl) -- (x+a/2,y+H), arrow=Arrow, L=Label("Solvente", position=BeginPoint, align=N));
draw((x+a,a/2) -- (x+a+fl,a/2), arrow=Arrow, L=Label("MV + AD", position=EndPoint, align=E));

label(".", (x+a+3*fl, a/2));

//Evaporación al vacío
draw((x+a/2,3*y) -- (x+a/2,3*y-fl), arrow=Arrow);
y = 3*y-fl;
draw(box((x-a/4,y),(x+5*a/4,y-a)));
label("Evaporador al vacio", (x+0.5*a,y-a/2));

draw((x+0.5*a,y-a) -- (x+0.5*a, y-a-fl) -- (x+2.5*a, y-a-fl) -- (x+2.5*a, y+2.5*fl+2*a) -- (x+0.5*a, y+2.5*fl+2*a), arrow=Arrow );

draw((x-a/4, y-a/2) -- (x-a/4-2.5*fl, y-a/2), L=Label("Extracto Humedo", position=MidPoint, align=N, rgb(245/255, 92/255, 92/255)));

//Función de líneas discontinuas
void Disc(real xi, real xf, real yi, real yf, bool message=false, real num=10) {
   real suma_ant = 0;
   real suma, signox, signoy, size;
   if (xi != xf){
       signoy = 0;
       if (xi < xf) {
           size = (xf-xi)/num;
           signox = 1;
       } else {
           signox=-1;
           size = (xi-xf)/num;
       }
   } else {
       signox = 0;
       if (yi < yf) {
           signoy = 1;
           size = (yf-yi)/num;
       } else {
           signoy = -1;
           size = (yi-yf)/num;
       }
   }
   if (message){
       label("Experimentacion", ((xf+xi)/2-a,yi), align=N);
   }
   for (int i=0; i<=num; i=i+1) {
       if (signox != 0) {
           suma = suma_ant + signox*size;
           draw((xi+suma_ant,yi) -- (xi+suma, yi));
           suma_ant = suma + signox*size;
       } else {
           suma = suma_ant + signoy*size;
           draw((xi,yi+suma_ant) -- (xi, yi+suma));
           suma_ant = suma + signoy*size;
       }
   }
}

//Experimentación
x = x-a/4-2.5*fl;
y = y-a/2;

Disc(x,x-2*a,y-a,y-a);
Disc(x, x-2*a, y+a, y+a, true);
Disc(x,x,y-a,y-a/10);
Disc(x-4.2*a, x-4.2*a, y-a, y-a/10);

draw((x,y) -- (x-fl,y), arrow=Arrow);
x = x-fl;
draw(box((x,y-a/2), (x-1.2*a,y+a/2)));
label("Rotaevaporador", (x-1.2*a/2, y));
draw((x-1.2*a/2, y-a/2) -- (x-1.2*a/2, y-a/2-fl/2) -- (x+a +3*fl, y-a/2-fl/2), arrow=Arrow);

x = x-1.2*a;
draw((x,y) -- (x-fl,y), arrow=Arrow);
x = x-fl;
draw(box((x, y-a/2),(x-1.2*a, y+a/2)));
label("Liofilizador", (x-0.6*a, y));
draw((x-1.2*a, y) -- (x-1.2*a-2*fl, y), arrow=Arrow, L=Label("Extracto seco", position=EndPoint, align=W));
y = y-a/2;
x = x-0.6*a;
draw((x,y) -- (x,y-0.5*fl) .. (x+0.2*fl,y-0.75*fl) .. (x,y-1*fl) .. (x-0.2*fl,y-1.25*fl) .. (x,y-1.5*fl) .. (x+0.2*fl,y-1.75*fl) .. (x,y-2*fl) .. (x-0.2*fl,y-2.25*fl).. (x, y-2.5*fl) -- (x, y-3*fl), arrow=Arrow, L=Label("Solvente", position=EndPoint, align=S));
