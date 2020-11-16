gridSize = 0.01;

Point(1) = {0,0,0, gridSize};
Point(2) = {0,-0.27,0, gridSize};
Point(3) = {0.27/2,-0.27,0, gridSize};
Point(4) = {0.27/2, 0,0, gridSize};
Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

Line Loop(5) = {1,2,3,4};
Plane Surface(6) = {5};
Transfinite Surface {6};
Recombine Surface {6};