Point(1) = {0,0,0,1.0};
Point(2) = {10,0,0,1.0};
Point(3) = {10,10,0,1.0};
Point(4) = {12,12,0,1.0};
Point(5) = {8, 10, 0,1.0};
Point(6) = {0,10,0,1.0};

Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,5};
Line(5) = {5,6};
Line(6) = {6,1};

Curve Loop(1) = {1,2,3,4,5,6};
Plane Surface(1) = {1};
Transfinite Surface {1} = {1,2,3,4,5,6};
Recombine Surface {1};
