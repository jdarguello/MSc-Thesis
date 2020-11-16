Point(1) = {0, 0, 0, 1.0};
Point(2) = {10, 0, 0, 1.0};
Point(3) = {10, 4, 0, 1.0};
Point(4) = {5, 4, 0, 1.0};
Point(5) = {5, 5, 0, 1.0};
Point(6) = {10, 5, 0, 1.0};
Point(7) = {10, 10, 0, 1.0};
Point(8) = {0, 10, 0, 1.0};


Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 5};
Line(5) = {5, 6};
Line(6) = {6, 7};
Line(7) = {7, 8};
Line(8) = {8, 1};

Line Loop(9) = {7, 8, 1, 2, 3, 4, 5, 6};

Plane Surface(10) = {9};
Physical Surface(11) = {10};

/*
Transfinite Line {2}=5;
Transfinite Line {6}=6;
Transfinite Line {8}= 11;
Transfinite Line {7}= 11;
Transfinite Line {1}= 11;
Transfinite Line {3,5} =6;
Transfinite Line {4} = 2;

Transfinite Surface {10}={5,6,7,8,1,2,3,4};
Recombine Surface {10};
*/


Transfinite Line {2}=5;
Transfinite Line {6}=6;
Transfinite Line {8}= (5+6+6*2+2)-5+1;
Transfinite Line {7}= 11;
Transfinite Line {1}= 11;
Transfinite Line {3,5} =6;
Transfinite Line {4} = 2;

//Transfinite Surface {10}={5,6,7,8,1,2,3,4};
Transfinite Surface {10}={1,2,7,8};
Recombine Surface {10};


Mesh.Smoothing = 5; // For a nicer mesh ;-)


surfaceVector[] = Extrude {0,0,espesor} {
 Surface{10};
 Layers{1};
 Recom
};